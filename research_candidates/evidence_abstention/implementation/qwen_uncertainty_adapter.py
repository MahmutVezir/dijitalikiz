from dataclasses import dataclass
import hashlib
import json
import math
import re
from typing import Any, Mapping, Sequence

from uncertainty_policy import (
    DecisionPolicy,
    DecisionRequest,
    DecisionResult,
    EmpiricalConfidenceCalibrator,
    decide,
)
from semantic_evidence_auditor import parse_semantic_audit


@dataclass(frozen=True)
class GenerationSample:
    text: str
    token_entropies: tuple[float, ...]
    seed: int
    prompt_sha256: str

    @property
    def mean_entropy(self) -> float:
        if not self.token_entropies:
            raise ValueError("sample has no generated-token scores")
        if any(not math.isfinite(value) or not 0.0 <= value <= 1.0 for value in self.token_entropies):
            raise ValueError("token entropies must be finite values in [0, 1]")
        return sum(self.token_entropies) / len(self.token_entropies)

    @property
    def output_sha256(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class StructuredAnswer:
    decision: str
    root_cause: str
    evidence_refs: tuple[str, ...]
    rationale: str
    alternative_hypotheses: tuple[str, ...]
    missing_evidence: tuple[str, ...]


@dataclass(frozen=True)
class EvidenceAudit:
    packet_validation_status: str | None
    available_evidence_ids: frozenset[str]
    supported_claim_coverage: float | None
    self_check_conflict: bool | None
    explicit_contradiction: bool | None


def evidence_audit_with_semantic_report(
    structural_audit: EvidenceAudit,
    raw_report: str,
) -> EvidenceAudit:
    if structural_audit.packet_validation_status != "valid":
        return structural_audit

    try:
        assessment = parse_semantic_audit(raw_report, structural_audit.available_evidence_ids)
    except ValueError:
        return EvidenceAudit(
            structural_audit.packet_validation_status,
            structural_audit.available_evidence_ids,
            None,
            None,
            None,
        )

    return EvidenceAudit(
        structural_audit.packet_validation_status,
        structural_audit.available_evidence_ids,
        assessment.supported_claim_coverage,
        assessment.self_check_conflict,
        assessment.explicit_contradiction,
    )


def evidence_audit_from_structural_report(report: Any) -> EvidenceAudit:
    """Bridge structural packet checks without fabricating semantic judgments."""
    status = getattr(report, "status", None)
    errors = getattr(report, "errors", None)
    if not isinstance(status, str) or status not in {"valid", "invalid"}:
        return EvidenceAudit(None, frozenset(), None, None, None)
    if status == "invalid" or not isinstance(errors, (tuple, list)) or errors:
        return EvidenceAudit("invalid", frozenset(), None, None, None)

    raw_ids = getattr(report, "available_evidence_ids", None)
    if not isinstance(raw_ids, (tuple, list, set, frozenset)):
        return EvidenceAudit("invalid", frozenset(), None, None, None)
    evidence_ids = tuple(raw_ids)
    if any(
        not isinstance(item, str)
        or re.fullmatch(r"[A-Z][A-Z0-9_-]{0,63}", item) is None
        for item in evidence_ids
    ) or len(evidence_ids) != len(set(evidence_ids)):
        return EvidenceAudit("invalid", frozenset(), None, None, None)

    return EvidenceAudit("valid", frozenset(evidence_ids), None, None, None)


def parse_structured_answer(raw: str) -> StructuredAnswer:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("model output is not a single JSON object") from exc

    required = {
        "decision",
        "root_cause",
        "evidence_refs",
        "rationale",
        "alternative_hypotheses",
        "missing_evidence",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("model output does not match the frozen output schema")
    if value["decision"] not in {"diagnose", "abstain"}:
        raise ValueError("decision must be diagnose or abstain")
    if not isinstance(value["root_cause"], str) or not isinstance(value["rationale"], str):
        raise ValueError("root_cause and rationale must be strings")
    refs = value["evidence_refs"]
    if not isinstance(refs, list) or len(refs) > 8:
        raise ValueError("evidence_refs must be a list with at most eight items")
    if any(not isinstance(ref, str) or re.fullmatch(r"[A-Z][A-Z0-9_-]*", ref) is None for ref in refs):
        raise ValueError("evidence_refs contains an invalid identifier")
    if len(refs) != len(set(refs)):
        raise ValueError("evidence_refs must contain unique identifiers")
    for key in ("alternative_hypotheses", "missing_evidence"):
        if not isinstance(value[key], list) or len(value[key]) > 8 or any(not isinstance(item, str) for item in value[key]):
            raise ValueError(key + " must be a list of at most eight strings")
    if value["decision"] == "diagnose" and not value["root_cause"].strip():
        raise ValueError("diagnose requires a non-empty root_cause")
    if value["decision"] == "abstain" and value["root_cause"] != "":
        raise ValueError("abstain requires an empty root_cause")

    return StructuredAnswer(
        decision=value["decision"],
        root_cause=value["root_cause"],
        evidence_refs=tuple(refs),
        rationale=value["rationale"],
        alternative_hypotheses=tuple(value["alternative_hypotheses"]),
        missing_evidence=tuple(value["missing_evidence"]),
    )


def assess_candidates(
    samples: Sequence[GenerationSample],
    audit: EvidenceAudit,
    calibrator: EmpiricalConfidenceCalibrator,
    policy: DecisionPolicy,
) -> DecisionResult:
    if len(samples) < 2:
        return DecisionResult("abstain", None, None, ("uncertainty_samples_insufficient",))
    if any(re.fullmatch(r"[0-9a-f]{64}", sample.prompt_sha256) is None for sample in samples):
        return DecisionResult("abstain", None, None, ("invalid_candidate_prompt_hash",))
    if len({sample.prompt_sha256 for sample in samples}) != 1:
        return DecisionResult("abstain", None, None, ("candidate_prompt_hash_mismatch",))
    if len({sample.seed for sample in samples}) != len(samples):
        return DecisionResult("abstain", None, None, ("candidate_seeds_not_unique",))

    try:
        parsed = [parse_structured_answer(sample.text) for sample in samples]
        entropy = sum(sample.mean_entropy for sample in samples) / len(samples)
    except ValueError:
        return DecisionResult("abstain", None, None, ("invalid_candidate_output",))
    except (TypeError, OverflowError):
        return DecisionResult("abstain", None, None, ("invalid_uncertainty_signal",))

    selected = parsed[0]
    candidate_answers = tuple(
        item.root_cause if item.decision == "diagnose" else "ABSTAIN: " + item.rationale
        for item in parsed
    )
    request = DecisionRequest(
        packet_validation_status=audit.packet_validation_status,
        answer=selected.root_cause if selected.decision == "diagnose" else "",
        available_evidence_ids=audit.available_evidence_ids,
        cited_evidence_ids=selected.evidence_refs,
        supported_claim_coverage=audit.supported_claim_coverage,
        normalized_token_entropy=entropy,
        candidate_answers=candidate_answers,
        self_check_conflict=audit.self_check_conflict,
        explicit_contradiction=audit.explicit_contradiction,
        model_requested_abstention=selected.decision == "abstain",
    )
    return decide(request, calibrator, policy)


def _normalized_entropy_from_tensor(torch: Any, scores: Any) -> float:
    values = scores.detach().float()
    if values.ndim != 1 or values.numel() < 2:
        raise ValueError("each generation score must be a one-dimensional vocabulary vector")
    if bool(torch.isnan(values).any()) or bool(torch.isposinf(values).any()) or not bool(torch.isfinite(values).any()):
        raise ValueError("generation scores contain an invalid distribution")

    probabilities = torch.softmax(values, dim=-1)
    terms = torch.where(
        probabilities > 0,
        -probabilities * torch.log(probabilities.clamp_min(torch.finfo(probabilities.dtype).tiny)),
        torch.zeros_like(probabilities),
    )
    entropy = terms.sum() / math.log(probabilities.numel())
    result = float(entropy.item())
    if not math.isfinite(result) or not 0.0 <= result <= 1.0:
        raise ValueError("normalized entropy is outside [0, 1]")
    return result


def generate_candidates(
    tokenizer: Any,
    model: Any,
    messages: Sequence[Mapping[str, str]],
    candidate_count: int,
    base_seed: int,
    max_new_tokens: int = 240,
    temperature: float = 0.7,
    top_p: float = 1.0,
) -> tuple[GenerationSample, ...]:
    if candidate_count < 2:
        raise ValueError("candidate_count must be at least two")
    if max_new_tokens < 1:
        raise ValueError("max_new_tokens must be positive")
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("temperature must be finite and positive")
    if not math.isfinite(top_p) or not 0.0 < top_p <= 1.0:
        raise ValueError("top_p must be within (0, 1]")
    if not messages:
        raise ValueError("messages must not be empty")

    try:
        import torch
    except ImportError as exc:
        raise RuntimeError("PyTorch is required for Qwen generation") from exc

    prompt_digest = hashlib.sha256(
        json.dumps(list(messages), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    encoded = tokenizer.apply_chat_template(
        list(messages),
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True,
    )
    if not isinstance(encoded, Mapping) or "input_ids" not in encoded:
        raise ValueError("chat template must return input_ids and attention_mask")
    input_ids = encoded["input_ids"].to(model.device)
    attention_mask = encoded.get("attention_mask")
    if attention_mask is None:
        attention_mask = torch.ones_like(input_ids)
    else:
        attention_mask = attention_mask.to(model.device)
    if input_ids.ndim != 2 or input_ids.shape[0] != 1:
        raise ValueError("each candidate requires an independent single-prompt session")
    if attention_mask.shape != input_ids.shape:
        raise ValueError("attention_mask shape must match input_ids")

    device = getattr(model, "device", torch.device("cpu"))
    devices = []
    if getattr(device, "type", str(device).split(":")[0]) == "cuda":
        device_index = getattr(device, "index", None)
        devices = [torch.cuda.current_device() if device_index is None else device_index]

    samples = []
    for index in range(candidate_count):
        seed = base_seed + index
        with torch.random.fork_rng(devices=devices):
            torch.manual_seed(seed)
            if devices:
                torch.cuda.manual_seed_all(seed)
            output = model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=top_p,
                top_k=0,
                repetition_penalty=1.0,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                output_scores=True,
                return_dict_in_generate=True,
            )

        generated_ids = output.sequences[0, input_ids.shape[-1]:]
        scores = output.scores
        if generated_ids.numel() == 0 or not scores or len(scores) != generated_ids.numel():
            raise RuntimeError("generation did not return aligned token IDs and score vectors")
        token_entropies = tuple(_normalized_entropy_from_tensor(torch, step[0]) for step in scores)
        text = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
        if not text:
            raise RuntimeError("model generated an empty response")
        samples.append(GenerationSample(text, token_entropies, seed, prompt_digest))

    return tuple(samples)
