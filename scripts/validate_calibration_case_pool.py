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


HEX64 = re.compile(r"^[0-9a-f]{64}$", re.IGNORECASE)


def _valid_sha256(value: Any) -> bool:
    return isinstance(value, str) and bool(HEX64.fullmatch(value))


def _validate_human_review_audit(
    *,
    root: Path,
    manifest: dict[str, Any],
    selected_case_ids: list[Any],
    candidates: dict[str, dict[str, Any]],
    issues: list[str],
) -> None:
    """Require review evidence; do not trust manifest flags alone."""
    if not selected_case_ids:
        return

    gate = manifest.get("review_gate")
    if not isinstance(gate, dict):
        issues.append("missing_case_ground_truth_review_gate")
        return
    if gate.get("status") != "adjudicated" or gate.get("frozen") is not True:
        issues.append("case_ground_truth_review_gate_not_frozen")
    audit_path = _resolve(root, gate.get("audit_path"), "case_ground_truth_review_audit", issues)
    if audit_path is None:
        return
    audit = _read_json(audit_path, issues, "case_ground_truth_review_audit")
    if audit is None:
        return

    try:
        audit_sha256 = hashlib.sha256(audit_path.read_bytes()).hexdigest()
    except OSError as exc:
        issues.append(f"cannot_hash_case_ground_truth_review_audit: {exc}")
        return
    if not _valid_sha256(gate.get("audit_sha256")):
        issues.append("case_ground_truth_review_gate_missing_audit_sha256")
    elif gate.get("audit_sha256") != audit_sha256:
        issues.append("case_ground_truth_review_audit_sha256_mismatch")

    if audit.get("protocol_version") != "case-ground-truth-review-v1":
        issues.append("case_ground_truth_review_audit_protocol_mismatch")
    if audit.get("status") != "adjudicated" or audit.get("frozen") is not True:
        issues.append("case_ground_truth_review_audit_not_frozen")
    if not _valid_sha256(audit.get("review_packet_manifest_sha256")):
        issues.append("case_ground_truth_review_audit_missing_packet_manifest_hash")

    reviewers = audit.get("reviewers")
    reviewer_ids: list[str] = []
    if not isinstance(reviewers, list) or len(reviewers) != 2:
        issues.append("case_ground_truth_review_requires_exactly_two_reviewers")
        reviewers = []
    for index, reviewer in enumerate(reviewers):
        if not isinstance(reviewer, dict):
            issues.append(f"case_ground_truth_reviewer_{index}_not_object")
            continue
        reviewer_id = reviewer.get("reviewer_id")
        if not isinstance(reviewer_id, str) or not reviewer_id.strip():
            issues.append(f"case_ground_truth_reviewer_{index}_missing_id")
        else:
            reviewer_ids.append(reviewer_id)
        if reviewer.get("independent_review_attestation") is not True:
            issues.append(f"case_ground_truth_reviewer_{index}_independence_not_attested")
        if reviewer.get("source_revision_review_attestation") is not True:
            issues.append(f"case_ground_truth_reviewer_{index}_source_review_not_attested")
        if not _valid_sha256(reviewer.get("reviewed_packet_sha256")):
            issues.append(f"case_ground_truth_reviewer_{index}_missing_packet_hash")
        if not _valid_sha256(reviewer.get("response_sha256")):
            issues.append(f"case_ground_truth_reviewer_{index}_missing_response_hash")
    if len(reviewer_ids) != 2 or len(set(reviewer_ids)) != 2:
        issues.append("case_ground_truth_reviewers_not_distinct")

    adjudicator = audit.get("adjudicator")
    if not isinstance(adjudicator, dict):
        issues.append("case_ground_truth_review_missing_adjudicator")
        adjudicator = {}
    adjudicator_id = adjudicator.get("reviewer_id")
    if not isinstance(adjudicator_id, str) or not adjudicator_id.strip():
        issues.append("case_ground_truth_review_adjudicator_id_missing")
    elif adjudicator_id in reviewer_ids:
        issues.append("case_ground_truth_adjudicator_not_independent_of_reviewers")
    if adjudicator.get("source_evidence_reviewed") is not True:
        issues.append("case_ground_truth_adjudicator_source_review_not_attested")
    if not isinstance(adjudicator.get("completed_at_utc"), str) or not adjudicator["completed_at_utc"].strip():
        issues.append("case_ground_truth_adjudicator_timestamp_missing")

    case_decisions = audit.get("case_decisions")
    if not isinstance(case_decisions, list):
        issues.append("case_ground_truth_review_missing_case_decisions")
        case_decisions = []
    decisions_by_id: dict[str, dict[str, Any]] = {}
    for item in case_decisions:
        if not isinstance(item, dict):
            issues.append("case_ground_truth_decision_not_object")
            continue
        case_id = item.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip():
            issues.append("case_ground_truth_decision_missing_case_id")
            continue
        if case_id in decisions_by_id:
            issues.append(f"{case_id}_duplicate_case_ground_truth_decision")
            continue
        decisions_by_id[case_id] = item

    for raw_case_id in selected_case_ids:
        if not isinstance(raw_case_id, str):
            issues.append(f"selected_case_id_not_string: {raw_case_id!r}")
            continue
        case_id = raw_case_id
        item = decisions_by_id.get(case_id)
        if item is None:
            issues.append(f"{case_id}_missing_independent_ground_truth_review_evidence")
            continue
        candidate = candidates.get(case_id, {})
        for field, manifest_field in (
            ("pre_fix_revision", "pre_fix_revision"),
            ("fixed_revision", "fix_revision"),
        ):
            if item.get(field) != candidate.get(manifest_field):
                issues.append(f"{case_id}_review_audit_{field}_mismatch")
        if item.get("review_a_decision") not in {"keep", "revise", "exclude"}:
            issues.append(f"{case_id}_review_a_decision_invalid")
        if item.get("review_b_decision") not in {"keep", "revise", "exclude"}:
            issues.append(f"{case_id}_review_b_decision_invalid")
        if item.get("final_decision") != "keep_for_scoring_calibration":
            issues.append(f"{case_id}_not_adjudicated_for_calibration")
        if item.get("root_cause_adjudicated") is not True:
            issues.append(f"{case_id}_root_cause_not_adjudicated")
        if item.get("dependency_edges_adjudicated") is not True:
            issues.append(f"{case_id}_dependency_edges_not_adjudicated")
        if item.get("single_coherent_defect") is not True:
            issues.append(f"{case_id}_not_a_single_coherent_defect")
        if item.get("disagreement_resolved") is not True:
            issues.append(f"{case_id}_review_disagreement_not_resolved")
        suitability = item.get("ccdg_suitability")
        if suitability not in {"strong", "moderate", "weak"}:
            issues.append(f"{case_id}_invalid_adjudicated_ccdg_suitability")
        if not isinstance(item.get("rationale"), str) or len(item["rationale"].strip()) < 30:
            issues.append(f"{case_id}_review_rationale_too_short")
        evidence = item.get("evidence_urls")
        if not isinstance(evidence, list) or len(evidence) < 2 or not all(
            isinstance(url, str) and url.startswith("https://") for url in evidence
        ):
            issues.append(f"{case_id}_insufficient_version_specific_evidence_urls")


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
    case_records: dict[str, dict[str, Any]] = {}
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
        repository_url = candidate.get("repository_url")
        if not isinstance(repository_url, str) or not repository_url.startswith("https://github.com/"):
            issues.append(f"{case_id}_invalid_repository_url")
        test_targets = candidate.get("regression_test_targets")
        if not isinstance(test_targets, list) or not test_targets or not all(
            isinstance(target, str) and "#" in target and target.strip() for target in test_targets
        ):
            issues.append(f"{case_id}_invalid_regression_test_targets")

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
        case_records[case_id] = record
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

        case_record = case_records.get(case_id)
        snapshot = case_record.get("software_twin_snapshot") if case_record else None
        if not isinstance(snapshot, dict):
            issues.append(f"{case_id}_missing_version_bound_software_twin_snapshot")
        else:
            if snapshot.get("repository_url") != candidate.get("repository_url"):
                issues.append(f"{case_id}_twin_snapshot_repository_mismatch")
            if snapshot.get("snapshot_revision") != candidate.get("pre_fix_revision"):
                issues.append(f"{case_id}_twin_snapshot_revision_mismatch")
            if snapshot.get("regression_test") not in candidate.get("regression_test_targets", []):
                issues.append(f"{case_id}_twin_snapshot_regression_test_mismatch")
            if not isinstance(snapshot.get("observed_failure_signal"), str) or len(
                snapshot["observed_failure_signal"].strip()
            ) < 15:
                issues.append(f"{case_id}_twin_snapshot_failure_signal_missing")

    _validate_human_review_audit(
        root=root,
        manifest=manifest,
        selected_case_ids=selected,
        candidates=indexed,
        issues=issues,
    )

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
