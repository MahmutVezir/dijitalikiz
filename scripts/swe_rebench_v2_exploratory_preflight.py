#!/usr/bin/env python3
"""Read-only readiness report for the v0.2 exploratory evidence-abstention study.

This script deliberately does not load a model, perform inference, train, or
authorize inference. Historical v0.1 confirmatory preflight rules are not used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "research_candidates" / "evidence_abstention"
IMPLEMENTATION = TRACK / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

MANIFEST_PATH = TRACK / "SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json"
REGISTRY_PATH = TRACK / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json"
SCHEMA_PATH = TRACK / "SWE_REBENCH_V2_EXPLORATORY_CASE_ACCEPTANCE_SCHEMA_V0_1.json"
VALIDATOR_PATH = IMPLEMENTATION / "swe_rebench_v2_exploratory_case_acceptance.py"

ARTIFACT_PATHS = {
    "design_decision": TRACK / "STUDY_DESIGN_DECISION_V0_2_EXPLORATORY_2026-11-16.md",
    "protocol": TRACK / "SWE_REBENCH_V2_PROTOCOL_V0_2_EXPLORATORY_DRAFT_2026-11-16.md",
    "analysis_plan": TRACK / "SWE_REBENCH_V2_ANALYSIS_PLAN_V0_2_EXPLORATORY_DRAFT_2026-11-16.md",
    "human_evaluator_amendment": TRACK / "HUMAN_EVALUATOR_AMENDMENT_V0_1_2026-11-18.md",
    "dual_human_scoring_rubric": TRACK / "SWE_REBENCH_V2_DUAL_HUMAN_OUTPUT_SCORING_RUBRIC_V0_1_DRAFT_2026-11-18.md",
    "rater_b_consent_and_exposure_template": TRACK / "RATER_B_CONSENT_AND_EXPOSURE_SCREEN_TEMPLATE_V0_1_2026-11-18.md",
    "ctapipe_exposure_decision_proposal": TRACK / "CTAPIPE_2732_EXPOSURE_DECISION_PROPOSAL_2026-11-18.md",
    "candidate_ledger": TRACK / "SWE_REBENCH_V2_COHORT_96_STATIC_TRIAGE_LEDGER_V0_1_2026-11-16.json",
}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evaluate(root: Path = ROOT) -> dict[str, Any]:
    root = Path(root)
    track = root / "research_candidates" / "evidence_abstention"
    manifest_path = track / MANIFEST_PATH.relative_to(TRACK)
    registry_path = track / REGISTRY_PATH.relative_to(TRACK)
    schema_path = track / SCHEMA_PATH.relative_to(TRACK)
    validator_path = track / VALIDATOR_PATH.relative_to(TRACK)

    blockers: list[str] = []
    hashes: dict[str, str | None] = {}
    for label, path in {
        "manifest": manifest_path,
        "case_registry": registry_path,
        "case_acceptance_schema": schema_path,
        "case_acceptance_validator": validator_path,
        **{name: root / p.relative_to(ROOT) for name, p in ARTIFACT_PATHS.items()},
    }.items():
        hashes[label] = _sha256(path) if path.is_file() else None
        if hashes[label] is None:
            blockers.append(f"Required v0.2 artifact is missing: {label} ({path.relative_to(root) if path.is_relative_to(root) else path}).")

    manifest: dict[str, Any] = {}
    registry: dict[str, Any] = {}
    registry_validation: dict[str, Any] = {}
    schema_valid = False

    try:
        manifest = _read_json(manifest_path)
    except Exception as exc:  # report a fail-closed blocker, do not crash
        blockers.append(f"Unable to read the v0.2 exploratory manifest: {type(exc).__name__}: {exc}")

    try:
        registry = _read_json(registry_path)
    except Exception as exc:
        blockers.append(f"Unable to read the v0.2 exploratory case registry: {type(exc).__name__}: {exc}")

    if schema_path.is_file():
        try:
            from jsonschema import Draft202012Validator

            schema = _read_json(schema_path)
            Draft202012Validator.check_schema(schema)
            schema_valid = True
        except Exception as exc:
            blockers.append(f"v0.2 case-acceptance schema validation failed: {type(exc).__name__}: {exc}")

    if registry:
        try:
            from swe_rebench_v2_exploratory_case_acceptance import validate_registry

            registry_validation = validate_registry(registry)
            if registry_validation.get("blockers"):
                blockers.extend(
                    f"v0.2 case registry: {item}"
                    for item in registry_validation["blockers"]
                )
        except Exception as exc:
            blockers.append(f"v0.2 case-registry validator failed: {type(exc).__name__}: {exc}")

    design = manifest.get("design", {})
    dataset = manifest.get("dataset", {})
    model = manifest.get("model", {})
    human = manifest.get("human_review", {})
    preregistration = manifest.get("preregistration", {})
    generation = manifest.get("generation", {})
    frozen_artifacts = manifest.get("frozen_artifacts", [])

    primary_target = 15
    stretch_target = 20
    minimum_feasibility = 1
    if design.get("study_type") != "exploratory_feasibility":
        blockers.append("The active design must remain exploratory_feasibility.")
    if design.get("minimum_independent_cases") != minimum_feasibility:
        blockers.append("The feasibility minimum must remain one valid independent case.")
    if design.get("primary_target_independent_cases") != primary_target:
        blockers.append("The primary target must remain 15 independent upstream projects.")
    if design.get("stretch_target_independent_cases") != stretch_target:
        blockers.append("The stretch target must remain 20 independent upstream projects.")
    if design.get("primary_target_upstream_projects") != primary_target:
        blockers.append("The primary upstream-project target must remain 15.")
    if design.get("stretch_target_upstream_projects") != stretch_target:
        blockers.append("The stretch upstream-project target must remain 20.")
    if design.get("sequential_candidate_intake", {}).get("acceptance_criteria_relaxed") is not False:
        blockers.append("Candidate acceptance criteria must remain unchanged during sequential intake.")

    if manifest.get("case_registry_path") != str(registry_path.relative_to(root)):
        blockers.append("The manifest must point to the v0.2 exploratory case registry.")
    if manifest.get("case_acceptance_schema_path") != str(schema_path.relative_to(root)):
        blockers.append("The manifest must point to the v0.2 exploratory case-acceptance schema.")
    if registry.get("acceptance_schema_path") != str(schema_path.relative_to(root)):
        blockers.append("The v0.2 registry schema path does not match the manifest schema.")
    if registry.get("acceptance_validator") != str(validator_path.relative_to(root)):
        blockers.append("The v0.2 registry validator path does not match the active validator.")

    if dataset.get("id") != "PrimeIntellect/SWE-rebench-V2-Filtered-Verified":
        blockers.append("The pinned SWE-rebench dataset identity is missing or changed.")
    if dataset.get("file_revision") != "fb9aa226b2ce37c708ea7732e7b980abacdadb67":
        blockers.append("The pinned SWE-rebench dataset revision is missing or changed.")
    if dataset.get("file_sha256") != "7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9":
        blockers.append("The pinned SWE-rebench Parquet SHA-256 is missing or changed.")
    if manifest.get("dataset_validation_gate") != "CLOSED":
        blockers.append("Dataset validation gate remains open: source provenance/license and raw timestamp authentication are not fully closed.")
    if not str(dataset.get("underlying_source_license_review", "")).startswith("CLOSED"):
        blockers.append("Underlying upstream source and changed-file license review is not closed.")
    reconciliation = dataset.get("created_at_reconciliation_register", {})
    if reconciliation.get("status") != "raw_payload_authenticated_and_field_level_reconciled":
        blockers.append("Dataset timestamp provenance is not yet authenticated against raw upstream payloads.")

    if model.get("license_review_status") != "approved_for_research_use":
        blockers.append("The exact immutable model revision's license/use review is not approved.")
    if model.get("runtime_verification") != "verified":
        blockers.append("The exact model/tokenizer/runtime environment has not been verified.")
    if generation.get("status") != "frozen":
        blockers.append("Generation settings are still draft and have not been frozen.")
    if preregistration.get("hash_freeze_complete") is not True:
        blockers.append("The protocol, analysis plan, generation settings, and scoring rules have not completed the internal hash freeze.")

    if not frozen_artifacts:
        blockers.append("No v0.2 frozen-artifact register is present.")
    for item in frozen_artifacts:
        if item.get("status") != "frozen" or not item.get("sha256"):
            blockers.append(f"Artifact is not frozen and hash-recorded: {item.get('path', '<unknown>')}.")

    if human.get("human_human_second_rater") is not True:
        blockers.append("The v0.2 dual-human output-scoring plan must identify a second human rater.")
    rater_b = human.get("second_human_rater", {})
    if rater_b.get("status") != "consent_confirmed_and_case_specific_independence_screen_passed":
        blockers.append("Rater B participation and case-specific independence/exposure screening are not confirmed.")
    if human.get("human_human_interrater_reliability_claimed") is not False:
        blockers.append("Human-human agreement must not be claimed before both original ratings exist.")
    if human.get("cohen_kappa_calculated") is not False:
        blockers.append("Cohen's kappa must remain uncalculated until blinded human ratings exist.")
    if human.get("ai_critique_is_human_rating") is not False:
        blockers.append("AI critique must remain advisory and must not be counted as a human rating.")
    if not human.get("scoring_rubric_path"):
        blockers.append("The dual-human output-scoring rubric path must be present.")
    if human.get("second_human_tier_review") is not False:
        blockers.append("Rater B must remain blind to and must not adjudicate hidden gold or E1/E2/E3 tier sufficiency.")

    accepted_count = registry.get("accepted_case_count", 0)
    accepted_projects = registry.get("accepted_project_count", 0)
    if accepted_count < minimum_feasibility:
        blockers.append("No accepted case is registered; at least one fully accepted independent-project case is required before any model inference.")
    if manifest.get("accepted_case_count") != accepted_count:
        blockers.append("Manifest and v0.2 registry accepted-case counts disagree.")
    if manifest.get("accepted_project_count") != accepted_projects:
        blockers.append("Manifest and v0.2 registry accepted-project counts disagree.")

    accepted_candidate_records = [
        item for item in manifest.get("candidate_review_records", [])
        if item.get("case_acceptance") == "accepted"
    ]
    if len(accepted_candidate_records) != accepted_count:
        blockers.append("Candidate review records and accepted case registry do not agree on accepted-case count.")

    if manifest.get("model_loading_performed") is not False:
        blockers.append("The manifest must explicitly confirm that model loading has not occurred.")
    if manifest.get("model_inference_performed") is not False:
        blockers.append("The manifest must explicitly confirm that model inference has not occurred.")
    if manifest.get("fine_tuning_performed") is not False:
        blockers.append("The manifest must explicitly confirm that fine-tuning has not occurred.")
    if manifest.get("inference_authorized") is not False or registry.get("inference_authorized") is not False:
        blockers.append("Inference authorization must remain explicitly false until a separate user authorization.")

    # External preregistration, Panel A/B, reviewer consent, institutional approval,
    # and a 60-case confirmatory sample are intentionally not v0.2 exploratory gates.
    external_registration_required = preregistration.get("external_registration_required", False)

    return {
        "protocol_id": manifest.get("protocol_id"),
        "protocol_version": manifest.get("protocol_version"),
        "study_type": design.get("study_type"),
        "status": "blocked_before_inference" if blockers else "gates_satisfied_waiting_for_separate_authorization",
        "ready_for_inference": not blockers,
        "primary_target_cases": primary_target,
        "stretch_target_cases": stretch_target,
        "minimum_feasibility_cases": minimum_feasibility,
        "preferred_analysis_threshold_cases": primary_target,
        "accepted_case_count": accepted_count,
        "accepted_project_count": accepted_projects,
        "primary_target_met": accepted_count >= primary_target and accepted_projects >= primary_target,
        "stretch_target_met": accepted_count >= stretch_target and accepted_projects >= stretch_target,
        "registry_status": registry_validation.get("status"),
        "registry_validation": registry_validation,
        "case_acceptance_schema_valid": schema_valid,
        "dataset_validation_gate": manifest.get("dataset_validation_gate"),
        "model_license_review_status": model.get("license_review_status"),
        "model_runtime_verification": model.get("runtime_verification"),
        "generation_status": generation.get("status"),
        "protocol_hash_freeze_complete": preregistration.get("hash_freeze_complete"),
        "external_preregistration_required": external_registration_required,
        "human_review_mode": "two_human_raters_for_model_outputs_single_project_lead_for_gold_and_tiers",
        "second_human_rater_required": human.get("human_human_second_rater"),
        "second_human_rater_status": rater_b.get("status"),
        "interrater_reliability_claimed": human.get("human_human_interrater_reliability_claimed"),
        "agreement_statistics_planned": human.get("agreement_statistics_planned", []),
        "model_loading_performed": manifest.get("model_loading_performed"),
        "model_inference_performed": manifest.get("model_inference_performed"),
        "fine_tuning_performed": manifest.get("fine_tuning_performed"),
        "inference_authorized": False,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "artifact_sha256": hashes,
        "report_scope": "Read-only v0.2 exploratory readiness report; no model loading, inference, or training.",
        "legacy_v0_1_requirements_applied": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    report = evaluate()
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if args.require_ready and not report["ready_for_inference"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
