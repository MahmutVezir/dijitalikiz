from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from dijitalikiz.context_v2 import (
    render_ccdg_context_v2,
    render_dependency_prose_context_v2,
    render_standard_context_v2,
)
from dijitalikiz.models import ResearchCase

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "calibration" / "case_pool_manifest.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)


def _read_json(path: Path, issues: list[str], label: str) -> dict[str, Any] | None:
    if not path.is_file():
        issues.append(f"missing_{label}: {path}")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"invalid_{label}: {exc}")
        return None
    if not isinstance(value, dict):
        issues.append(f"invalid_{label}: expected a JSON object")
        return None
    return value


def _case_ids(path: Path, field: str, issues: list[str], label: str) -> set[str]:
    data = _read_json(path, issues, label)
    if data is None:
        return set()
    values = data.get(field)
    if not isinstance(values, list):
        issues.append(f"invalid_{label}_ids: expected list field {field!r}")
        return set()
    return {value for value in values if isinstance(value, str)}


def _resolve(root: Path, value: Any, label: str, issues: list[str]) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        issues.append(f"invalid_{label}_path")
        return None
    path = Path(value)
    return path if path.is_absolute() else root / path


def _normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _valid_sha(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA40.fullmatch(value))


def audit_case_pool(
    *,
    manifest_path: Path = DEFAULT_MANIFEST,
    pilot_manifest_path: Path | None = None,
    benchmark_manifest_path: Path | None = None,
) -> dict[str, Any]:
    issues: list[str] = []
    manifest_path = manifest_path.resolve()
    root = manifest_path.parents[2] if len(manifest_path.parents) >= 3 else ROOT

    manifest = _read_json(manifest_path, issues, "calibration_case_pool_manifest")
    if manifest is None:
        return {
            "status": "blocked",
            "model_inference_permitted": False,
            "candidate_count": 0,
            "selected_count": 0,
            "issues": issues,
        }

    pilot_manifest_path = pilot_manifest_path or root / "data" / "pilot" / "pilot_manifest.json"
    benchmark_manifest_path = benchmark_manifest_path or root / "data" / "benchmark" / "benchmark_manifest.json"

    pilot_ids = _case_ids(pilot_manifest_path, "cases", issues, "pilot_manifest")
    confirmatory_ids = _case_ids(benchmark_manifest_path, "case_ids", issues, "benchmark_manifest")
    historical_ids = pilot_ids | confirmatory_ids

    schema_path = root / "schemas" / "research_case.schema.json"
    schema = _read_json(schema_path, issues, "research_case_schema")
    validator = Draft202012Validator(schema, format_checker=FormatChecker()) if schema is not None else None

    candidates = manifest.get("candidates")
    if not isinstance(candidates, list):
        issues.append("invalid_candidates: expected array")
        candidates = []

    indexed: dict[str, dict[str, Any]] = {}
    seen_case_paths: set[str] = set()
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            issues.append(f"candidate_{index}_not_object")
            continue

        case_id = candidate.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip():
            issues.append(f"candidate_{index}_missing_case_id")
            continue
        if case_id in indexed:
            issues.append(f"duplicate_candidate_case_id: {case_id}")
            continue
        indexed[case_id] = candidate

        if case_id in historical_ids:
            issues.append(f"{case_id}_overlaps_frozen_historical_cases")
        if not isinstance(candidate.get("source_url"), str) or not candidate["source_url"].startswith("https://"):
            issues.append(f"{case_id}_invalid_source_url")
        if not _valid_sha(candidate.get("fix_revision")):
            issues.append(f"{case_id}_invalid_fix_revision")
        if not _valid_sha(candidate.get("pre_fix_revision")):
            issues.append(f"{case_id}_invalid_pre_fix_revision")

        record_path = _resolve(root, candidate.get("case_record_path"), f"{case_id}_case_record", issues)
        if record_path is None:
            continue
        rel_path = str(record_path)
        if rel_path in seen_case_paths:
            issues.append(f"{case_id}_duplicate_case_record_path")
        seen_case_paths.add(rel_path)

        record = _read_json(record_path, issues, f"{case_id}_case_record")
        if record is None:
            continue
        if validator is not None:
            schema_errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
            for error in schema_errors[:10]:
                issues.append(f"{case_id}_research_case_schema_error: {error.message}")
        if record.get("case_id") != case_id:
            issues.append(f"{case_id}_case_record_id_mismatch")
        if record.get("source_url") != candidate.get("source_url"):
            issues.append(f"{case_id}_case_record_source_url_mismatch")
        provenance = record.get("provenance", {})
        if provenance.get("fix_commit") != candidate.get("fix_revision"):
            issues.append(f"{case_id}_case_record_fix_revision_mismatch")
        if provenance.get("pre_fix_revision") != candidate.get("pre_fix_revision"):
            issues.append(f"{case_id}_case_record_pre_fix_revision_mismatch")

        try:
            case = ResearchCase.from_dict(record)
            contexts = (
                render_standard_context_v2(case),
                render_dependency_prose_context_v2(case),
                render_ccdg_context_v2(case),
            )
            gold_phrase = _normalise(case.ground_truth.root_cause)
            if not gold_phrase:
                issues.append(f"{case_id}_empty_ground_truth_root_cause")
            elif any(gold_phrase in _normalise(context) for context in contexts):
                issues.append(f"{case_id}_ground_truth_root_cause_label_leaked_into_context")
        except Exception as exc:
            issues.append(f"{case_id}_context_v2_validation_error: {type(exc).__name__}: {exc}")

    freeze = manifest.get("selection_freeze", {})
    selected = freeze.get("eligible_case_ids", []) if isinstance(freeze, dict) else []
    if not isinstance(selected, list):
        issues.append("selection_freeze_eligible_case_ids_not_list")
        selected = []
    if len(selected) != len(set(selected)):
        issues.append("selection_freeze_has_duplicate_case_ids")

    minimum_count = manifest.get("rules", {}).get("minimum_calibration_case_count", 7)
    if not isinstance(minimum_count, int) or minimum_count < 1:
        issues.append("invalid_minimum_calibration_case_count")
        minimum_count = 7
    if len(selected) < minimum_count:
        issues.append(f"insufficient_selected_cases: {len(selected)} < {minimum_count}")

    for case_id in selected:
        if not isinstance(case_id, str) or case_id not in indexed:
            issues.append(f"selected_case_not_in_candidate_pool: {case_id}")
            continue
        candidate = indexed[case_id]
        if case_id in historical_ids:
            issues.append(f"{case_id}_selected_from_historical_split")
        if candidate.get("reproduction_status") != "independent_pre_fix_failure_and_fixed_revision_pass":
            issues.append(f"{case_id}_independent_red_green_reproduction_not_complete")
        if not isinstance(candidate.get("reproduction_evidence_url"), str) or not candidate["reproduction_evidence_url"].startswith("https://"):
            issues.append(f"{case_id}_missing_reproduction_evidence")
        if candidate.get("ground_truth_adjudication_status") != "independently_adjudicated":
            issues.append(f"{case_id}_ground_truth_not_independently_adjudicated")
        if candidate.get("inference_allowed") is not True:
            issues.append(f"{case_id}_inference_allowed_flag_not_set")

    if manifest.get("status") != "frozen":
        issues.append("case_pool_manifest_not_frozen")
    if manifest.get("model_inference_permitted") is not True:
        issues.append("case_pool_manifest_model_inference_not_permitted")
    if not isinstance(freeze, dict) or freeze.get("frozen") is not True:
        issues.append("case_pool_selection_freeze_not_frozen")
    if not isinstance(freeze, dict) or not freeze.get("date_utc"):
        issues.append("case_pool_selection_freeze_missing_date")

    may_run = not issues
    return {
        "status": "pass" if may_run else "blocked",
        "model_inference_permitted": may_run,
        "manifest_status": manifest.get("status"),
        "candidate_count": len(indexed),
        "selected_count": len(selected),
        "historical_pilot_case_count": len(pilot_ids),
        "historical_confirmatory_case_count": len(confirmatory_ids),
        "selected_case_ids": selected,
        "issues": issues,
        "purpose": "Pre-inference eligibility gate only; it does not itself prove ground-truth correctness or model performance.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed eligibility gate for scoring-calibration case pool.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--pilot-manifest", type=Path)
    parser.add_argument("--benchmark-manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = audit_case_pool(
        manifest_path=args.manifest,
        pilot_manifest_path=args.pilot_manifest,
        benchmark_manifest_path=args.benchmark_manifest,
    )
    payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
