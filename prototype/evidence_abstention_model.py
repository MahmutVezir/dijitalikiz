"""Qwen adapter for the evidence-abstention project; not the confirmatory runner."""
import hashlib
import json
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"
MODEL_REVISION = "aa8e72537993ba99e69dfaafa59ed015b17504d1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "research_candidates" / "evidence_abstention" / "OUTPUT_SCHEMA.json"
MAX_INPUT_CHARS = 16000
MAX_NEW_TOKENS = 512
REQUIRED = {
    "decision", "root_cause", "evidence_refs", "rationale",
    "alternative_hypotheses", "missing_evidence",
}
POLICY_INSTRUCTIONS = {
    "P0": (
        "Choose and state one single most likely root cause. Do not abstain. "
        "If the evidence is incomplete, still give the most likely diagnosis and "
        "identify which supplied evidence led you to it."
    ),
    "P1": (
        "Give a root-cause diagnosis only when the evidence packet sufficiently "
        "supports and distinguishes it from plausible alternatives. If the packet "
        "is insufficient or contradictory, abstain rather than guess, and list the "
        "specific additional evidence needed to distinguish the alternatives."
    ),
}
SYSTEM_PROMPT = (
    "You are analyzing a software defect using the evidence packet supplied in the user message.\n"
    "Base factual claims only on information in that packet. Do not use external tools, web search, "
    "retrieval, or code execution. Do not claim to have run tests. Distinguish a plausible hypothesis "
    "from a cause supported by the packet. Return exactly one valid JSON object matching the provided "
    "output schema, without Markdown fences or text outside the JSON."
)


@dataclass(frozen=True)
class EvidencePacket:
    code: str
    traceback: str
    context: str = ""

    def validate(self) -> None:
        for name, value in (("code", self.code), ("traceback", self.traceback), ("context", self.context)):
            if not isinstance(value, str):
                raise TypeError(name + " metin olmalıdır.")
            if len(value) > MAX_INPUT_CHARS:
                raise ValueError(name + " en fazla 16000 karakter olabilir.")
        if not self.code.strip():
            raise ValueError("Araştırma protokolüyle uyum için code alanı boş olamaz.")
        if not self.traceback.strip():
            raise ValueError("Araştırma protokolüyle uyum için traceback alanı boş olamaz.")

    def items(self) -> list[dict[str, str]]:
        fields = (
            ("CODE_1", "source_code", self.code),
            ("TRACE_1", "error_trace", self.traceback),
            ("CONTEXT_1", "environment_context", self.context),
        )
        return [
            {"id": key, "kind": kind, "content": value.strip()}
            for key, kind, value in fields
            if value.strip()
        ]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_output_schema() -> dict:
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("Kanonik OUTPUT_SCHEMA.json okunamadı: " + str(exc)) from exc
    if not isinstance(schema, dict) or set(schema.get("required", [])) != REQUIRED:
        raise RuntimeError("Kanonik çıktı şeması beklenen alanlarla eşleşmiyor.")
    return schema


def render_evidence_packet(packet: EvidencePacket) -> str:
    packet.validate()
    sections = [
        "[CODE_1]\n" + packet.code,
        "[TRACE_1]\n" + packet.traceback,
    ]
    if packet.context.strip():
        sections.append("[CONTEXT_1]\n" + packet.context)
    return "\n\n".join(sections)


def build_messages(packet: EvidencePacket, policy: str) -> list[dict[str, str]]:
    """Mirror the frozen Stage 3 prompt contract; never include the hidden E1/E2/E3 label."""
    if policy not in POLICY_INSTRUCTIONS:
        raise ValueError("policy yalnızca P0 veya P1 olabilir.")
    schema = load_output_schema()
    evidence_packet = render_evidence_packet(packet)
    user_prompt = (
        "Task: Assess the likely root cause of the reported software defect.\n\n"
        "Policy instruction:\n"
        + POLICY_INSTRUCTIONS[policy]
        + "\n\nEvidence packet:\n"
        + evidence_packet
        + "\n\nUse evidence item IDs when referring to packet evidence. Do not cite information "
        "that is not present in the packet. If abstaining, leave root_cause as an empty string and "
        "list the specific evidence that would distinguish the plausible causes. Return only the JSON "
        "object defined by the schema.\n\nJSON schema:\n"
        + json.dumps(schema, ensure_ascii=False)
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def validate_output(raw: str, packet: EvidencePacket, policy: str) -> dict:
    """Check syntax and evidence IDs without rewriting the model's observed decision."""
    if policy not in POLICY_INSTRUCTIONS:
        raise ValueError("policy yalnızca P0 veya P1 olabilir.")
    load_output_schema()
    try:
        answer = json.loads(raw)
        if not isinstance(answer, dict) or set(answer) != REQUIRED:
            raise ValueError("Çıktı kanonik JSON alanlarıyla tam eşleşmiyor.")
        if answer["decision"] not in {"diagnose", "abstain"}:
            raise ValueError("decision diagnose veya abstain olmalıdır.")
        if not isinstance(answer["root_cause"], str) or not isinstance(answer["rationale"], str):
            raise ValueError("root_cause ve rationale metin olmalıdır.")
        for key in ("evidence_refs", "alternative_hypotheses", "missing_evidence"):
            values = answer[key]
            if not isinstance(values, list) or len(values) > 8 or any(not isinstance(value, str) for value in values):
                raise ValueError(key + " en fazla sekiz öğeli metin listesi olmalıdır.")
        if answer["decision"] == "diagnose" and not answer["root_cause"].strip():
            raise ValueError("Teşhis kararı boş kök neden içeremez.")
        if answer["decision"] == "abstain" and answer["root_cause"] != "":
            raise ValueError("Kaçınma kararında root_cause boş olmalıdır.")
        if len(answer["evidence_refs"]) != len(set(answer["evidence_refs"])):
            raise ValueError("Tekrarlı kanıt ID'si bulunuyor.")
        import re
        if any(not re.fullmatch(r"[A-Z][A-Z0-9_-]*", value) for value in answer["evidence_refs"]):
            raise ValueError("Kanıt ID biçimi kanonik şemaya uymuyor.")
    except (json.JSONDecodeError, TypeError, ValueError, KeyError) as exc:
        return {
            "status": "invalid_model_output", "policy": policy, "decision": "invalid_output",
            "root_cause": "", "evidence_refs": [], "rationale": "Model çıktısı doğrulanamadı.",
            "alternative_hypotheses": [], "missing_evidence": ["Geçerli kanonik JSON yanıtı gerekli."],
            "validation_error": str(exc), "semantic_support": "not_assessed",
        }

    packet.validate()
    allowed = {item["id"] for item in packet.items()}
    invalid = sorted(set(answer["evidence_refs"]) - allowed)
    missing_citation = answer["decision"] == "diagnose" and not answer["evidence_refs"]
    if invalid or missing_citation:
        reason = ("Paket dışı kanıt ID'si: " + ", ".join(invalid)) if invalid else "Teşhis kanıt referansı içermiyor."
        status = "invalid_evidence_references"
    else:
        reason = None
        status = "policy_noncompliance" if policy == "P0" and answer["decision"] == "abstain" else "ok"
    return {
        "status": status, "policy": policy, **answer,
        "validation_error": reason or ("P0 istediği halde model kaçındı." if status == "policy_noncompliance" else None),
        "semantic_support": "not_assessed",
    }


class QwenEvidenceAbstentionModel:
    """Lazy local inference wrapper for exploratory engineering demonstrations."""

    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.device = None
        self.runtime_info = {}

    def load(self) -> None:
        if self.model is not None:
            return
        try:
            import torch
            import transformers
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError(
                "Bu ortamda torch ve transformers kurulu olmalıdır; otomatik paket kurulumu yapılmaz."
            ) from exc
        if not torch.cuda.is_available() and os.getenv("EVIDENCE_ALLOW_CPU", "0") != "1":
            raise RuntimeError("GPU bulunamadı. Kaggle Settings > Accelerator > GPU seç; CPU varsayılan olarak kapalı.")
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_ID, revision=MODEL_REVISION, trust_remote_code=False
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, revision=MODEL_REVISION, torch_dtype=dtype, device_map="auto",
            low_cpu_mem_usage=True, trust_remote_code=False
        )
        self.model.eval()
        self.device = next(self.model.parameters()).device
        model_commit = getattr(self.model.config, "_commit_hash", None)
        tokenizer_commit = (
            getattr(self.tokenizer, "_commit_hash", None)
            or getattr(self.tokenizer, "init_kwargs", {}).get("_commit_hash")
        )
        if model_commit and model_commit != MODEL_REVISION:
            raise RuntimeError("Yüklenen model commit'i sabit revision ile eşleşmiyor.")
        if tokenizer_commit and tokenizer_commit != MODEL_REVISION:
            raise RuntimeError("Yüklenen tokenizer commit'i sabit revision ile eşleşmiyor.")
        self.runtime_info = {
            "python_version": os.sys.version.split()[0],
            "torch_version": torch.__version__,
            "transformers_version": transformers.__version__,
            "device": str(self.device),
            "cuda_available": bool(torch.cuda.is_available()),
            "model_commit_observed": model_commit,
            "tokenizer_commit_observed": tokenizer_commit,
            "revision_passed_to_loader": MODEL_REVISION,
        }

    def analyze(self, packet: EvidencePacket, policy: str = "P1") -> dict:
        messages = build_messages(packet, policy)
        self.load()
        import torch
        prompt_text = json.dumps(messages, ensure_ascii=False)
        rendered_packet = render_evidence_packet(packet)
        tokens = self.tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
        ).to(self.device)
        with torch.inference_mode():
            output = self.model.generate(
                tokens, max_new_tokens=MAX_NEW_TOKENS, do_sample=False, num_beams=1,
                pad_token_id=self.tokenizer.eos_token_id, eos_token_id=self.tokenizer.eos_token_id
            )
        raw = self.tokenizer.decode(output[0, tokens.shape[-1]:], skip_special_tokens=True)
        report = validate_output(raw, packet, policy)
        report.update({
            "model_id": MODEL_ID,
            "model_revision": MODEL_REVISION,
            "raw_model_output": raw,
            "evidence_ids_available": [item["id"] for item in packet.items()],
            "prompt_sha256": sha256_text(prompt_text),
            "evidence_packet_sha256": sha256_text(rendered_packet),
            "raw_output_sha256": sha256_text(raw),
            "runtime": self.runtime_info,
            "research_status": "exploratory_engineering_demo_not_confirmatory_result",
        })
        return report


@lru_cache(maxsize=1)
def get_model() -> QwenEvidenceAbstentionModel:
    return QwenEvidenceAbstentionModel()
