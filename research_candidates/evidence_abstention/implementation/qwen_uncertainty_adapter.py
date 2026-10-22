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
    operational_evidence_status: str | None
    available_evidence_ids: frozenset[str]
    supported_claim_coverage: float | None
    self_check_conflict: bool | None
    explicit_contradiction: bool | None


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
    if not isinstance(refs, list) or len(refs) > 8 or len(refs) != len(set(refs)):
        raise ValueError("evidence_refs must be a unique list with at most eight items")
    if any(not isinstance(ref, str) or re.fullmatch(r"[A-Z][A-Z0-9_-]*", ref) is None for ref in refs):
        raise ValueError("evidence_refs contains an invalid identifier")
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
        operational_evidence_status=audit.operational_evidence_status,
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
    input_ids = tokenizer.apply_chat_template(
        list(messages),
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to(model.device)
    if input_ids.ndim != 2 or input_ids.shape[0] != 1:
        raise ValueError("each candidate requires an independent single-prompt session")

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
