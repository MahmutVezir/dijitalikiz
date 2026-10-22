import argparse
import hashlib
import json
import os
import re
import sys
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
EVIDENCE_LEVELS = ("E1_sufficient", "E2_partial", "E3_insufficient")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _reviewer_panel(record: dict, field: str, label: str, case_id: str, blockers: list[str]) -> set[str]:
    reviewer_ids = record.get(field)
    if not isinstance(reviewer_ids, list) or len(reviewer_ids) < 2:
        blockers.append(f"{case_id}: at least two {label} reviewer IDs are required in {field}.")
        return set()
    if any(not isinstance(value, str) or not value.strip() for value in reviewer_ids):
        blockers.append(f"{case_id}: {field} must contain non-empty pseudonymous strings.")
        return set()
    if len(set(reviewer_ids)) != len(reviewer_ids):
        blockers.append(f"{case_id}: duplicate IDs in {field}.")
    return set(reviewer_ids)


def _validate_accepted_case(row: dict, blockers: list[str]) -> None:
    case_id = row.get("case_id")
    if not isinstance(case_id, str) or not case_id.strip():
        blockers.append("Accepted registry record has no non-empty case_id.")
        case_id = "unknown"

    required_text = (
        "upstream_project",
        "source_repository",
        "license_reference",
        "buggy_commit",
        "fixed_commit",
        "test_command",
        "runtime_fingerprint",
        "root_cause_reference",
        "metadata_python_version",
        "runtime_python_version",
        "buggy_test_log_uri",
        "fixed_test_log_uri",
    )
    for field in required_text:
        value = row.get(field)
        if not isinstance(value, str) or not value.strip():
            blockers.append(f"{case_id}: required non-empty field missing: {field}.")

    if row.get("buggy_commit") and row.get("buggy_commit") == row.get("fixed_commit"):
        blockers.append(f"{case_id}: buggy and fixed commits must differ.")
    if row.get("metadata_python_version") != row.get("runtime_python_version"):
        blockers.append(f"{case_id}: runtime Python does not match dataset metadata.")
    if row.get("buggy_test_outcome") != "target_failure_reproduced":
        blockers.append(f"{case_id}: buggy target failure was not reproduced; environment/setup failures do not qualify.")
    if row.get("fixed_test_outcome") != "target_test_passed":
        blockers.append(f"{case_id}: fixed target test did not pass.")

    required_true = (
        "license_reviewed",
        "leakage_reviewed",
        "prior_exposure_clearance",
        "evidence_levels_reviewed",
        "test_pair_verified",
        "root_cause_reviewed_by_two",
    )
    for field in required_true:
        if row.get(field) is not True:
            blockers.append(f"{case_id}: scientific acceptance gate not passed: {field}.")

    ground_truth_ids = _reviewer_panel(
        row, "ground_truth_reviewer_ids", "ground-truth", case_id, blockers
    )
    evidence_ids = _reviewer_panel(
        row, "evidence_reviewer_ids", "evidence-sufficiency", case_id, blockers
    )
    if ground_truth_ids & evidence_ids:
        blockers.append(f"{case_id}: ground-truth and evidence-sufficiency panels must be disjoint.")

    for field in ("buggy_test_log_sha256", "fixed_test_log_sha256", "runtime_fingerprint_sha256"):
        value = row.get(field)
        if not isinstance(value, str) or not HEX64.fullmatch(value):
            blockers.append(f"{case_id}: missing or invalid SHA-256: {field}.")

    packet_hashes = row.get("evidence_packet_sha256")
    for level in EVIDENCE_LEVELS:
        value = packet_hashes.get(level) if isinstance(packet_hashes, dict) else None
        if not isinstance(value, str) or not HEX64.fullmatch(value):
            blockers.append(f"{case_id}: missing or invalid evidence-packet SHA-256 for {level}.")


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
        if model.get("dtype") != "float16" or model.get("quantization", "none") != "none":
            blockers.append("Model precision must be the reviewed non-quantized float16 configuration.")

    case_ids = manifest.get("case_ids")
    if (
        not isinstance(case_ids, list)
        or any(not isinstance(value, str) or not value.strip() for value in case_ids)
        or len(case_ids) != len(set(case_ids))
    ):
        blockers.append("Case IDs are missing, malformed, empty, or duplicated.")
        case_ids = []

    project_count = 0
    try:
        registry_path_value = manifest.get("case_registry_path")
        if not isinstance(registry_path_value, str) or not registry_path_value:
            raise ValueError("case_registry_path is missing")
        registry_path = root / registry_path_value
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        records = registry.get("records") if isinstance(registry, dict) else None
        if not isinstance(records, list):
            raise ValueError("registry records must be a list")
        accepted = [
            row for row in records
            if isinstance(row, dict) and row.get("accepted_for_confirmatory") is True
        ]
        accepted_ids = []
        for row in accepted:
            case_id = row.get("case_id")
            accepted_ids.append(case_id)
            _validate_accepted_case(row, blockers)
        if case_ids != accepted_ids:
            blockers.append("Manifest case IDs do not match the ordered accepted case registry.")
        if len(accepted) < int(manifest.get("minimum_confirmatory_cases", 60)):
            blockers.append("Accepted independent case count is below the required minimum.")
        project_count = len({
            row.get("upstream_project")
            for row in accepted
            if isinstance(row.get("upstream_project"), str) and row.get("upstream_project").strip()
        })
        if project_count < int(manifest.get("minimum_upstream_projects", 8)):
            blockers.append("Upstream project count is below the required minimum.")
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        blockers.append("Case registry missing or invalid: " + str(exc))

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


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Read-only uncertainty inference preflight; never runs the model.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("research_candidates/evidence_abstention/UNCERTAINTY_EXPERIMENT_MANIFEST.json"),
    )
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args(argv)
    report = evaluate_gate(args.root, args.manifest)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.require_ready and not report["ready"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
