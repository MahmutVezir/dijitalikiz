"""Qwen evidence-abstention prototype; separate from the confirmatory experiment."""
import json
import os
from dataclasses import dataclass
from functools import lru_cache

MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"
MODEL_REVISION = "aa8e72537993ba99e69dfaafa59ed015b17504d1"
REQUIRED = {"decision", "root_cause", "evidence_refs", "rationale", "alternative_hypotheses", "missing_evidence"}
POLICIES = {
    "P0": "Give the most likely root-cause diagnosis; do not abstain. Cite supplied evidence.",
    "P1": (
        "Diagnose only if evidence distinguishes the cause from plausible alternatives. Otherwise abstain, "
        "leave root_cause empty, and list what evidence is missing. Never guess just to answer."
    ),
}

@dataclass(frozen=True)
class EvidencePacket:
    code: str
    traceback: str
    context: str = ""

    def validate(self):
        if not self.code.strip() and not self.traceback.strip():
            raise ValueError("En azından kod veya hata/traceback girilmelidir.")
        for name, value in (("code", self.code), ("traceback", self.traceback), ("context", self.context)):
            if not isinstance(value, str):
                raise TypeError(name + " metin olmalıdır.")
            if len(value) > 16000:
                raise ValueError(name + " en fazla 16000 karakter olabilir.")

    def items(self):
        fields = (("CODE_1", "source_code", self.code), ("TRACE_1", "error_trace", self.traceback), ("CONTEXT_1", "environment_context", self.context))
        return [{"id": key, "kind": kind, "content": value.strip()} for key, kind, value in fields if value.strip()]

def build_messages(packet, policy):
    packet.validate()
    if policy not in POLICIES:
        raise ValueError("policy yalnızca P0 veya P1 olabilir.")
    items = packet.items()
    payload = {
        "task": "Yazılım hatasının kök nedenini yalnızca bu kanıt paketine dayanarak değerlendir.",
        "policy": POLICIES[policy],
        "evidence_items": items,
        "allowed_evidence_ids": [item["id"] for item in items],
        "required_json_keys": sorted(REQUIRED),
    }
    system = (
        "You are a careful software-defect analyst. Use only supplied evidence; do not claim to run tests. "
        "Distinguish hypotheses from supported conclusions. Cite evidence IDs exactly. Return one JSON object only."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}]

def validate_output(raw, packet, policy):
    try:
        text = raw.strip()
        fence = chr(96) * 3
        if text.startswith(fence) and text.endswith(fence):
            text = "\n".join(text.splitlines()[1:-1]).strip()
        answer = json.loads(text)
        if not isinstance(answer, dict) or set(answer) != REQUIRED:
            raise ValueError("Gerekli JSON alanlarıyla eşleşmiyor.")
        if answer["decision"] not in {"diagnose", "abstain"}:
            raise ValueError("decision diagnose veya abstain olmalıdır.")
        if not isinstance(answer["root_cause"], str) or not isinstance(answer["rationale"], str):
            raise ValueError("root_cause ve rationale metin olmalıdır.")
        for key in ("evidence_refs", "alternative_hypotheses", "missing_evidence"):
            if not isinstance(answer[key], list) or any(not isinstance(v, str) for v in answer[key]):
                raise ValueError(key + " metin listesi olmalıdır.")
        if answer["decision"] == "diagnose" and not answer["root_cause"].strip():
            raise ValueError("Boş kök neden teşhis olarak kabul edilmez.")
        if answer["decision"] == "abstain" and answer["root_cause"] != "":
            raise ValueError("Kaçınmada root_cause boş olmalıdır.")
        if len(answer["evidence_refs"]) != len(set(answer["evidence_refs"])):
            raise ValueError("Tekrarlı kanıt ID'si bulunuyor.")
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        return {"status": "invalid_model_output", "policy": policy, "decision": "invalid_output",
                "root_cause": "", "evidence_refs": [], "rationale": "Model çıktısı doğrulanamadı.",
                "alternative_hypotheses": [], "missing_evidence": ["Geçerli JSON yanıtı gerekli."],
                "validation_error": str(exc), "semantic_support": "not_assessed"}
    allowed = {item["id"] for item in packet.items()}
    invalid = sorted(set(answer["evidence_refs"]) - allowed)
    missing_citation = answer["decision"] == "diagnose" and not answer["evidence_refs"]
    if invalid or missing_citation:
        reason = ("Paket dışı kanıt ID'si: " + ", ".join(invalid)) if invalid else "Teşhis kanıt referansı içermiyor."
        if policy == "P1" and answer["decision"] == "diagnose":
            return {"status": "guarded_abstention", "policy": policy, "decision": "abstain",
                    "root_cause": "", "evidence_refs": [], "rationale": "Kanıt bağlantısı doğrulanamadı; teşhis yayımlanmadı.",
                    "alternative_hypotheses": answer["alternative_hypotheses"],
                    "missing_evidence": list(answer["missing_evidence"]) + [reason],
                    "validation_error": reason, "semantic_support": "not_assessed"}
        return {"status": "invalid_evidence_references", "policy": policy, **answer,
                "validation_error": reason, "semantic_support": "not_assessed"}
    status = "policy_noncompliance" if policy == "P0" and answer["decision"] == "abstain" else "ok"
    return {"status": status, "policy": policy, **answer,
            "validation_error": "P0 istediği halde model kaçındı." if status != "ok" else None,
            "semantic_support": "not_assessed"}

class QwenEvidenceAbstentionModel:
    """Lazy local inference wrapper. Use a GPU for the pinned 3B checkpoint."""

    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.device = None

    def load(self):
        if self.model is not None:
            return
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("Bu ortamda torch ve transformers kurulu olmalıdır; otomatik paket kurulumu yapılmaz.") from exc
        if not torch.cuda.is_available() and os.getenv("EVIDENCE_ALLOW_CPU", "0") != "1":
            raise RuntimeError("GPU bulunamadı. Kaggle Settings > Accelerator > GPU seç; CPU varsayılan olarak kapalı.")
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION, trust_remote_code=False)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, revision=MODEL_REVISION, torch_dtype=dtype, device_map="auto",
            low_cpu_mem_usage=True, trust_remote_code=False
        )
        self.model.eval()
        self.device = next(self.model.parameters()).device

    def analyze(self, packet, policy="P1"):
        messages = build_messages(packet, policy)
        self.load()
        import torch
        tokens = self.tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt").to(self.device)
        with torch.inference_mode():
            output = self.model.generate(tokens, max_new_tokens=512, do_sample=False, num_beams=1,
                                         pad_token_id=self.tokenizer.eos_token_id, eos_token_id=self.tokenizer.eos_token_id)
        raw = self.tokenizer.decode(output[0, tokens.shape[-1]:], skip_special_tokens=True).strip()
        report = validate_output(raw, packet, policy)
        report.update({"model_id": MODEL_ID, "model_revision": MODEL_REVISION, "raw_model_output": raw,
                       "evidence_ids_available": [item["id"] for item in packet.items()],
                       "research_status": "engineering_demo_not_confirmatory_result"})
        return report

@lru_cache(maxsize=1)
def get_model():
    return QwenEvidenceAbstentionModel()
