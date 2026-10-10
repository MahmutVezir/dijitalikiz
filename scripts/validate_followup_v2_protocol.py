from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from scripts.power_mcnemar import exact_mcnemar_power, required_n

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "followup_v2" / "protocol_manifest.json"
SHA40 = re.compile(r"^[0-9a-fA-F]{40}$")
SHA64 = re.compile(r"^[0-9a-fA-F]{64}$")


def read_json(path: Path, issues: list[str], label: str) -> dict[str, Any] | None:
    if not path.is_file():
        issues.append(f"missing_{label}:{path.as_posix()}")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"invalid_{label}:{type(exc).__name__}")
        return None
    if not isinstance(value, dict):
        issues.append(f"invalid_{label}:expected_object")
        return None
    return value


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect_ids(root: Path, rel_path: str, fields: tuple[str, ...], issues: list[str]) -> set[str]:
    value = read_json(root / rel_path, issues, rel_path)
    ids: set[str] = set()
    if value is None:
        return ids
    for field in fields:
        rows = value.get(field, [])
        if isinstance(rows, list):
            ids.update(row for row in rows if isinstance(row, str))
    return ids


def validate_protocol(manifest: dict[str, Any], root: Path) -> dict[str, Any]:
    issues: list[str] = []
    schema = read_json(root / "schemas" / "followup_v2_protocol.schema.json", issues, "protocol_schema")
    if schema is not None:
        errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda e: list(e.path))
        issues.extend(f"schema:{'/'.join(map(str, e.path))}:{e.message}" for e in errors)

    if manifest.get("historical_artifacts_immutable") is not True:
        issues.append("historical_artifacts_must_remain_immutable")
    design = manifest.get("design", {})
    conditions = [row.get("id") for row in design.get("conditions", []) if isinstance(row, dict)]
    if conditions != ["A", "B", "C"]:
        issues.append("conditions_must_be_ordered_A_B_C")
    if design.get("primary_contrast") != ["C", "B"]:
        issues.append("primary_contrast_must_be_C_vs_B")

    sample = manifest.get("sample_size", {})
    assumption = sample.get("assumptions", {})
    p_prose = assumption.get("p_prose_only")
    p_graph = assumption.get("p_graph_only")
    if isinstance(p_prose, (int, float)) and not isinstance(p_prose, bool) and isinstance(p_graph, (int, float)) and not isinstance(p_graph, bool):
        required = required_n(
            float(p_prose), float(p_graph),
            target_power=float(sample.get("target_power", 0.8)),
            alpha=float(sample.get("alpha", 0.05)), max_n=1000,
        )
        if required != sample.get("required_case_count_under_assumptions"):
            issues.append("power_required_case_count_mismatch")
        if required is not None:
            achieved = exact_mcnemar_power(required, float(p_prose), float(p_graph), alpha=float(sample.get("alpha", 0.05)))
            if abs(achieved - float(sample.get("achieved_power_under_assumptions", -1))) > 0.00011:
                issues.append("power_value_mismatch")
    else:
        issues.append("power_assumptions_invalid")

    target = sample.get("target_independent_case_count")
    reps = sample.get("replications_per_condition")
    arms = sample.get("conditions")
    if all(isinstance(x, int) and not isinstance(x, bool) for x in (target, reps, arms)):
        if sample.get("target_model_outputs") != target * reps * arms:
            issues.append("target_output_count_mismatch")
        if isinstance(sample.get("required_case_count_under_assumptions"), int) and target < sample["required_case_count_under_assumptions"]:
            issues.append("target_case_count_below_power_requirement")

    model = manifest.get("model", {})
    if not SHA40.fullmatch(str(model.get("revision", ""))):
        issues.append("model_revision_must_be_immutable_commit")
    if model.get("status") != "frozen":
        issues.append("model_not_frozen")
    if manifest.get("generation", {}).get("status") != "frozen":
        issues.append("generation_not_frozen")

    prompts = manifest.get("prompts", {})
    for path_key, hash_key in (("system_prompt_path", "system_prompt_sha256"), ("task_prompt_path", "task_prompt_sha256")):
        path = root / str(prompts.get(path_key, ""))
        if not path.is_file():
            issues.append(f"missing_prompt:{path_key}")
        elif file_sha256(path) != prompts.get(hash_key):
            issues.append(f"prompt_hash_mismatch:{path_key}")
    token_path = root / str(prompts.get("tokenizer_audit_path", ""))
    token_report = read_json(token_path, issues, "tokenizer_audit")
    token_hash = prompts.get("tokenizer_audit_sha256")
    if token_report is None:
        issues.append("tokenizer_audit_unavailable")
    else:
        if token_report.get("status") != "pass" or token_report.get("all_prompts_fit_context_budget") is not True:
            issues.append("tokenizer_audit_not_pass")
        if token_report.get("case_count") != len(manifest.get("case_pool", {}).get("case_ids", [])):
            issues.append("tokenizer_audit_case_count_mismatch")
        if not SHA64.fullmatch(str(token_hash or "")) or file_sha256(token_path) != token_hash:
            issues.append("tokenizer_audit_hash_mismatch")
    if prompts.get("tokenizer_audit_status") != "pass":
        issues.append("tokenizer_gate_pending")

    case_pool = manifest.get("case_pool", {})
    case_ids = case_pool.get("case_ids", [])
    if not isinstance(case_ids, list) or not all(isinstance(v, str) and v for v in case_ids):
        issues.append("case_ids_invalid")
        case_ids = []
    if len(case_ids) != len(set(case_ids)):
        issues.append("case_ids_not_unique")
    if len(case_ids) < int(case_pool.get("minimum_independent_case_count", 61)):
        issues.append("heldout_case_pool_below_minimum")
    excluded = set()
    excluded |= collect_ids(root, "data/pilot/pilot_manifest.json", ("cases",), issues)
    excluded |= collect_ids(root, "data/benchmark/benchmark_manifest.json", ("case_ids", "pilot_case_ids"), issues)
    pool = read_json(root / "data/calibration/case_pool_manifest.json", issues, "calibration_case_pool")
    if pool is not None:
        for row in pool.get("candidates", []):
            if isinstance(row, dict) and isinstance(row.get("case_id"), str):
                excluded.add(row["case_id"])
    overlap = sorted(set(case_ids) & excluded)
    if overlap:
        issues.append(f"heldout_case_overlap:{overlap}")

    case_dir = root / str(case_pool.get("case_directory", ""))
    for case_id in case_ids:
        payload = read_json(case_dir / f"{case_id}.json", issues, f"case:{case_id}")
        if payload is None:
            continue
        if payload.get("case_id") != case_id or payload.get("split") != case_pool.get("split_name"):
            issues.append(f"case_id_or_split_mismatch:{case_id}")
        snapshot = payload.get("software_twin_snapshot")
        if not isinstance(snapshot, dict) or any(not isinstance(snapshot.get(k), str) or not snapshot[k].strip() for k in ("repository_url", "snapshot_revision", "regression_test", "observed_failure_signal")):
            issues.append(f"case_snapshot_incomplete:{case_id}")
        assessment = read_json(root / case_pool["assessments_directory"] / f"{case_id}.json", issues, f"assessment:{case_id}")
        if assessment is not None and assessment.get("eligible_for_followup_v2") is not True:
            issues.append(f"case_assessment_not_eligible:{case_id}")

    review_path = root / str(case_pool.get("source_review_audit_path", ""))
    review = read_json(review_path, issues, "heldout_review_audit")
    review_hash = case_pool.get("source_review_audit_sha256")
    if review is None:
        issues.append("heldout_review_audit_unavailable")
    else:
        review_schema = read_json(root / "schemas" / "followup_v2_heldout_case_review.schema.json", issues, "heldout_review_schema")
        if review_schema:
            errors = list(Draft202012Validator(review_schema).iter_errors(review))
            issues.extend(f"review_schema:{'/'.join(map(str, e.path))}:{e.message}" for e in errors)
        if review.get("status") != "adjudicated" or review.get("frozen") is not True:
            issues.append("heldout_review_not_frozen_adjudicated")
        reviewers = review.get("reviewers", [])
        ids = [row.get("reviewer_id") for row in reviewers if isinstance(row, dict)]
        adjudicator = review.get("adjudicator", {}).get("reviewer_id")
        if len(set(ids)) != 2 or adjudicator in set(ids):
            issues.append("reviewers_and_adjudicator_not_independent")
        decisions = review.get("case_decisions", [])
        decided_ids = [row.get("case_id") for row in decisions if isinstance(row, dict)]
        if set(decided_ids) != set(case_ids) or len(decided_ids) != len(set(decided_ids)):
            issues.append("review_case_coverage_mismatch")
        for row in decisions:
            if not isinstance(row, dict):
                continue
            if row.get("final_decision") != "keep_for_followup_confirmatory":
                issues.append(f"case_not_kept:{row.get('case_id')}")
            required_true = ("root_cause_adjudicated", "dependency_edges_adjudicated", "single_coherent_defect", "disagreement_resolved", "license_reviewed")
            if any(row.get(field) is not True for field in required_true):
                issues.append(f"case_review_evidence_incomplete:{row.get('case_id')}")
            if row.get("ccdg_suitability") not in {"strong", "moderate"} or row.get("contamination_risk") == "unresolved":
                issues.append(f"case_not_suitable_or_risk_unresolved:{row.get('case_id')}")
        if not SHA64.fullmatch(str(review_hash or "")) or file_sha256(review_path) != review_hash:
            issues.append("heldout_review_hash_mismatch")

    calibration = read_json(root / "data/calibration/manifest.json", issues, "calibration_manifest")
    if calibration is None or calibration.get("status") != "adjudicated" or calibration.get("frozen") is not True:
        issues.append("scoring_calibration_not_frozen_adjudicated")
    calibration_audit_path = root / "data/calibration" / "calibration_audit.json"
    calibration_audit = read_json(calibration_audit_path, issues, "calibration_audit")
    freeze = manifest.get("freeze_metadata", {})
    calibration_hash = freeze.get("calibration_audit_sha256")
    if calibration_audit is None:
        issues.append("calibration_audit_unavailable")
    else:
        metrics = calibration_audit.get("metrics") or {}
        if calibration_audit.get("status") != "pass" or calibration_audit.get("ready_for_new_confirmatory_inference") is not True:
            issues.append("calibration_audit_not_ready")
        if metrics.get("initial_review_exact_agreement", -1) < 0.8:
            issues.append("calibration_agreement_below_threshold")
        if metrics.get("initial_review_cohen_kappa") is None or metrics.get("initial_review_cohen_kappa", -1) < 0.7:
            issues.append("calibration_kappa_below_threshold")
        if not SHA64.fullmatch(str(calibration_hash or "")) or file_sha256(calibration_audit_path) != calibration_hash:
            issues.append("calibration_audit_hash_mismatch")

    compatibility = read_json(root / "data/followup_v2/runtime_compatibility_audit.json", issues, "runtime_compatibility_audit")
    if compatibility is None or compatibility.get("status") != "pass":
        issues.append("runtime_compatibility_not_pass")
    elif compatibility.get("model_id") != model.get("model_id") or compatibility.get("model_revision") != model.get("revision") or compatibility.get("uses_calibration_case_only") is not True or compatibility.get("single_sample_inference_schema_passed") is not True:
        issues.append("runtime_compatibility_evidence_mismatch")

    schedule_path = root / "data/followup_v2/randomized_schedule.json"
    schedule = read_json(schedule_path, issues, "randomized_schedule")
    schedule_hash = freeze.get("randomized_schedule_sha256")
    if schedule is None:
        issues.append("randomized_schedule_unavailable")
    else:
        expected_cells = {(case_id, cond, seed) for case_id in case_ids for cond in ("A", "B", "C") for seed in manifest.get("generation", {}).get("seeds", [])}
        actual = [(row.get("case_id"), row.get("condition_id"), row.get("seed")) for row in schedule.get("cells", []) if isinstance(row, dict)]
        if schedule.get("status") != "frozen" or len(actual) != len(set(actual)) or set(actual) != expected_cells:
            issues.append("randomized_schedule_cells_mismatch")
        if not SHA64.fullmatch(str(schedule_hash or "")) or file_sha256(schedule_path) != schedule_hash:
            issues.append("randomized_schedule_hash_mismatch")

    analysis_path = root / "scripts" / "analyze_followup_v2.py"
    analysis_hash = freeze.get("analysis_code_sha256")
    if not analysis_path.is_file() or not SHA64.fullmatch(str(analysis_hash or "")) or (analysis_path.is_file() and file_sha256(analysis_path) != analysis_hash):
        issues.append("analysis_script_missing_or_hash_mismatch")

    for name, status in manifest.get("gates", {}).items():
        if status != "passed":
            issues.append(f"gate_pending:{name}")
    if manifest.get("status") != "frozen" or model.get("status") != "frozen" or manifest.get("generation", {}).get("status") != "frozen":
        issues.append("protocol_model_or_generation_not_frozen")
    if manifest.get("model_inference_permitted") is not True:
        issues.append("manifest_does_not_permit_inference")
    for field in ("frozen_at_utc", "frozen_source_commit", "review_audit_sha256", "calibration_audit_sha256", "prompt_token_audit_sha256", "randomized_schedule_sha256", "analysis_code_sha256", "student_researcher_approval"):
        if not freeze.get(field):
            issues.append(f"freeze_metadata_missing:{field}")

    ready = not issues
    return {
        "status": "ready" if ready else "blocked",
        "model_inference_permitted": ready and manifest.get("model_inference_permitted") is True,
        "protocol_version": manifest.get("protocol_version"),
        "manifest_status": manifest.get("status"),
        "heldout_case_count": len(case_pool.get("case_ids", [])) if isinstance(case_pool.get("case_ids"), list) else 0,
        "required_independent_case_count": sample.get("target_independent_case_count"),
        "target_model_outputs": sample.get("target_model_outputs"),
        "issue_count": len(issues),
        "issues": issues,
        "interpretation": "Readiness only. This validator never loads a model, starts inference, or mutates the manifest."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed v2 protocol gate; does not run model inference.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    manifest = read_json(path, [], "manifest")
    if manifest is None:
        return 2
    report = validate_protocol(manifest, root)
    if args.output:
        output = args.output if args.output.is_absolute() else root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "model_inference_permitted": report["model_inference_permitted"], "heldout_case_count": report["heldout_case_count"], "required_independent_case_count": report["required_independent_case_count"], "issue_count": report["issue_count"], "issues": report["issues"]}, indent=2, ensure_ascii=False))
    return 1 if args.require_ready and report["status"] != "ready" else 0


if __name__ == "__main__":
    raise SystemExit(main())
