import hashlib
import json
import os
import re
from pathlib import Path
from typing import Mapping


HEX64 = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"
EXPECTED_MODEL_REVISION = "aa8e72537993ba99e69dfaafa59ed015b17504d1"
REQUIRED_ARTIFACTS = (
    "case_registry",
    "output_schema",
    "prompt_template",
    "analysis_plan",
    "runtime_lock",
    "calibration_data",
    "evidence_audit_protocol",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def evaluate_gate(root: Path, manifest_path: Path, env: Mapping[str, str] | None = None) -> dict:
    root = root.resolve()
    manifest_path = manifest_path if manifest_path.is_absolute() else root / manifest_path
    environment = os.environ if env is None else env
    blockers = []

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "ready": False,
            "mode": "read_only_no_model_execution",
            "blockers": ["Manifest missing or invalid: " + str(exc)],
            "model_inference_performed": False,
        }

    checks = (
        (manifest.get("inference_allowed") is True, "Manifest does not explicitly authorize inference."),
        (manifest.get("dataset_validation_gate") == "CLOSED", "Dataset validation gate is not CLOSED."),
        (manifest.get("preregistration_status") == "registered" and bool(manifest.get("preregistration_uri")), "A verifiable preregistration record is missing."),
        (manifest.get("reviewer_protocol_frozen") is True, "Independent reviewer and adjudication protocol is not frozen."),
        (manifest.get("calibration_complete") is True, "Independent confidence calibration is not complete."),
    )
    blockers.extend(message for passed, message in checks if not passed)

    model = manifest.get("model")
    if not isinstance(model, dict):
        blockers.append("Immutable model configuration is missing.")
    else:
        if model.get("id") != EXPECTED_MODEL_ID or model.get("revision") != EXPECTED_MODEL_REVISION:
            blockers.append("Model ID/revision differs from the reviewed immutable checkpoint.")
        if model.get("tokenizer_id") != EXPECTED_MODEL_ID or model.get("tokenizer_revision") != EXPECTED_MODEL_REVISION:
            blockers.append("Tokenizer ID/revision differs from the reviewed immutable checkpoint.")
        if model.get("runtime_verification") != "passed":
            blockers.append("Exact model/tokenizer/runtime preflight has not passed.")

    case_ids = manifest.get("case_ids")
    if not isinstance(case_ids, list) or len(case_ids) != len(set(case_ids)):
        blockers.append("Case IDs are missing, malformed, or duplicated.")
        case_ids = []

    try:
        registry_path = root / manifest.get("case_registry_path", "")
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        accepted = [
            row for row in registry.get("records", [])
            if isinstance(row, dict) and row.get("accepted_for_confirmatory") is True
        ]
        accepted_ids = [row.get("case_id") for row in accepted]
        if case_ids != accepted_ids:
            blockers.append("Manifest case IDs do not match the ordered accepted case registry.")
        if len(accepted) < int(manifest.get("minimum_confirmatory_cases", 60)):
            blockers.append("Accepted independent case count is below the required minimum.")
        project_count = len({row.get("upstream_project") for row in accepted if row.get("upstream_project")})
        if project_count < int(manifest.get("minimum_upstream_projects", 8)):
            blockers.append("Upstream project count is below the required minimum.")
        for row in accepted:
            required_true = (
                "evidence_levels_reviewed",
                "test_pair_verified",
                "license_reviewed",
                "leakage_reviewed",
                "prior_exposure_clearance",
            )
            for key in required_true:
                if row.get(key) is not True:
                    blockers.append(str(row.get("case_id", "unknown")) + ": scientific gate not passed: " + key)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        blockers.append("Case registry missing or invalid: " + str(exc))
        project_count = 0

    frozen = manifest.get("frozen_artifacts")
    if not isinstance(frozen, dict):
        frozen = {}
        blockers.append("Frozen artifact manifest is missing.")
    for name in REQUIRED_ARTIFACTS:
        entry = frozen.get(name)
        if not isinstance(entry, dict):
            blockers.append("Frozen artifact entry missing: " + name)
            continue
        expected = entry.get("sha256")
        relative_path = entry.get("path")
        if not isinstance(expected, str) or not HEX64.fullmatch(expected) or not isinstance(relative_path, str) or not relative_path:
            blockers.append("Frozen artifact path or SHA-256 missing/invalid: " + name)
            continue
        target = root / relative_path
        if not target.is_file():
            blockers.append("Frozen artifact file missing: " + name)
        elif sha256_file(target) != expected:
            blockers.append("Frozen artifact SHA-256 mismatch: " + name)

    if environment.get("EVIDENCE_UNCERTAINTY_INFERENCE_APPROVED") != "YES":
        blockers.append("Separate explicit inference authorization is missing.")

    return {
        "ready": not blockers,
        "mode": "read_only_no_model_execution",
        "blockers": blockers,
        "case_count": len(case_ids),
        "upstream_project_count": project_count,
        "model_inference_performed": False,
    }


def load_authorized_qwen(root: Path, manifest_path: Path):
    report = evaluate_gate(root, manifest_path)
    if not report["ready"]:
        raise RuntimeError("Inference blocked: " + "; ".join(report["blockers"]))

    resolved_manifest = manifest_path if manifest_path.is_absolute() else root / manifest_path
    manifest = json.loads(resolved_manifest.read_text(encoding="utf-8"))
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("Pinned PyTorch and Transformers runtime is required") from exc

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU is required by the frozen runtime policy.")

    model_config = manifest["model"]
    tokenizer = AutoTokenizer.from_pretrained(
        model_config["tokenizer_id"],
        revision=model_config["tokenizer_revision"],
        trust_remote_code=False,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_config["id"],
        revision=model_config["revision"],
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=False,
    )
    model.eval()
    return tokenizer, model
