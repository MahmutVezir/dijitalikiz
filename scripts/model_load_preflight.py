from __future__ import annotations

"""Validate the readiness receipt produced by the single compatibility gate."""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data/pilot/compatibility_report.json"
MANIFEST = ROOT / "data/pilot/pilot_manifest.json"
SOURCE_COMMIT = ROOT / "data/pilot/kaggle_source_commit.txt"




REQUIRED_RECEIPT_CHECKS = frozenset([
    "frozen_manifest_and_record_contract",
    "package_version_torch",
    "package_version_transformers",
    "package_version_accelerate",
    "package_version_jsonschema",
    "package_version_numpy",
    "package_version_datasets",
    "package_version_pyarrow",
    "package_version_fsspec",
    "transformers_runtime_version",
    "torch_runtime_version",
    "prompt_sha256",
    "system_prompt_sha256",
    "requirements_sha256",
    "pip_dependency_consistency",
    "cuda_gpu_visibility",
    "exact_model_revision",
    "model_architecture",
    "quantization_backend",
    "checkpoint_weights_match_model",
    "smoke_logits_finite",
    "pilot_sampling_smoke",
    "model_loading_and_smoke_inference",
    "diagnostic_output_schema"
])


def validate_compatibility_receipt(
    report: object,
    manifest: object,
    current_manifest_sha256: str,
    expected_source_commit: str,
) -> tuple[bool, str]:
    """Validate a readiness receipt against the current frozen manifest and required gate checks."""
    if not isinstance(report, dict) or not isinstance(manifest, dict):
        return False, "report and manifest must both be JSON objects"
    if report.get("schema_version") != 1:
        return False, "unsupported or missing compatibility receipt schema_version"
    if report.get("status") != "pass" or report.get("pilot_authorized") is not True:
        return False, "compatibility gate did not authorize the pilot"
    if report.get("manifest_sha256") != current_manifest_sha256:
        return False, "compatibility receipt is stale for the current manifest"
    if report.get("model_id") != manifest.get("model", {}).get("model_id"):
        return False, "model_id mismatch"
    if report.get("model_revision") != manifest.get("model", {}).get("revision"):
        return False, "model_revision mismatch"
    if report.get("expected_records") != manifest.get("expected_records"):
        return False, "expected_records mismatch"
    if not isinstance(expected_source_commit, str) or not re.fullmatch(r"[0-9a-fA-F]{40}", expected_source_commit.strip()):
        return False, "frozen source-commit marker is missing or invalid"
    source_commit = report.get("source_commit")
    if not isinstance(source_commit, str) or source_commit.strip().lower() == "unknown":
        return False, "receipt source_commit is missing or unknown"
    if source_commit.strip().lower() != expected_source_commit.strip().lower():
        return False, "receipt was generated from a different source commit"

    checks = report.get("checks")
    if not isinstance(checks, list) or not checks:
        return False, "receipt checks must be a non-empty list"
    indexed: dict[str, dict[str, object]] = {}
    for item in checks:
        if not isinstance(item, dict):
            return False, "receipt contains a malformed check record"
        name = item.get("name")
        if not isinstance(name, str) or not name.strip() or name in indexed:
            return False, "receipt check names must be non-empty and unique"
        indexed[name] = item
    missing_checks = sorted(REQUIRED_RECEIPT_CHECKS - set(indexed))
    if missing_checks:
        return False, "required checks are missing: " + ", ".join(missing_checks)
    failed_checks = sorted(name for name, item in indexed.items() if item.get("status") != "pass")
    if failed_checks:
        return False, "one or more checks did not pass: " + ", ".join(failed_checks)
    return True, "current receipt, frozen model, record count, and all required checks verified"


def main() -> int:
    try:
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        manifest_bytes = MANIFEST.read_bytes()
        manifest = json.loads(manifest_bytes)
        expected_source_commit = SOURCE_COMMIT.read_text(encoding="utf-8").strip()
    except Exception as exc:
        print(f"COMPATIBILITY RECEIPT MISSING/INVALID: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    valid, reason = validate_compatibility_receipt(
        report,
        manifest,
        hashlib.sha256(manifest_bytes).hexdigest(),
        expected_source_commit,
    )
    if not valid:
        print(f"COMPATIBILITY RECEIPT REJECTED: {reason}; frozen pilot must not start.", file=sys.stderr)
        return 1

    print(f"COMPATIBILITY RECEIPT VERIFIED: {reason}.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
