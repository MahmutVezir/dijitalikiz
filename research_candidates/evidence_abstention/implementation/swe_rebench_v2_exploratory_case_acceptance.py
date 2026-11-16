"""Fail-closed structural and consistency checks for v0.2 case acceptance.

This module does not authenticate artifact URIs, execute upstream tests, decide
legal questions, establish semantic truth, or authorize model loading/inference.
"""
from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any
import json

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "SWE_REBENCH_V2_EXPLORATORY_CASE_ACCEPTANCE_SCHEMA_V0_1.json"
DATASET_ID = "PrimeIntellect/SWE-rebench-V2-Filtered-Verified"
DATASET_REVISION = "fb9aa226b2ce37c708ea7732e7b980abacdadb67"
DATASET_SHA256 = "7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9"
MAX_CASES = 20
MIN_CASES = 15


def load_schema() -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def _errors(record: Any) -> list[str]:
    validator = Draft202012Validator(load_schema(), format_checker=FormatChecker())
    return [f"{'/'.join(str(x) for x in error.absolute_path) or '<root>'}: {error.message}"
            for error in sorted(validator.iter_errors(record), key=lambda e: list(map(str, e.absolute_path)))]


def validate_case_record(record: Any) -> dict[str, Any]:
    """Validate JSON shape and deterministic cross-field invariants only."""
    blockers = _errors(record)
    if blockers:
        return {"status": "invalid", "blockers": blockers, "structural_only": True, "inference_authorized": False}

    source = record["source"]
    independence = record["independence"]
    technical = record["technical_reproduction"]
    gold = record["gold_standard"]
    tiers = record["evidence_tiers"]
    mechanisms = {item["mechanism_id"] for item in gold["candidate_mechanisms"]}
    gold_id = gold["gold_mechanism_id"]

    dataset = record["dataset"]
    if dataset["timestamp_reconciliation_status"] == "exact_match" and dataset["created_at_dataset_utc"] != dataset["created_at_upstream_utc"]:
        blockers.append("timestamp status claims exact_match but the dataset and upstream timestamps differ.")
    if source["base_commit_sha"] == source["fixed_commit_sha"]:
        blockers.append("base and fixed commit SHAs must differ.")
    if technical["buggy_baseline"]["commit_sha"] != source["base_commit_sha"]:
        blockers.append("buggy baseline commit must equal source base commit.")
    if technical["fixed_revision"]["commit_sha"] != source["fixed_commit_sha"]:
        blockers.append("fixed reproduction commit must equal source fixed commit.")
    if technical["buggy_baseline"]["exit_code"] == 0:
        blockers.append("buggy baseline must have a non-zero exit code.")
    if technical["buggy_baseline"]["failure_signature"] == "":
        blockers.append("buggy baseline failure signature is required.")
    if gold_id not in mechanisms:
        blockers.append("gold mechanism must be one of the predeclared candidate mechanisms.")

    tier_survivors = {}
    tier_evidence = {}
    for level in ("E1", "E2", "E3"):
        tier = tiers[level]
        survivors = set(tier["surviving_mechanism_ids"])
        if not survivors <= mechanisms:
            blockers.append(f"{level} references an undeclared mechanism.")
        tier_survivors[level] = survivors
        evidence_map = {}
        for item in tier["evidence_items"]:
            evidence_id = item["evidence_id"]
            if evidence_id in evidence_map:
                blockers.append(f"{level} repeats evidence ID {evidence_id}.")
            evidence_map[evidence_id] = (item["content_sha256"], item["source_snapshot_sha256"],
                                         item["source_uri"], item["source_commit_sha"], item["source_path"])
        tier_evidence[level] = evidence_map

    if tier_survivors["E1"] != {gold_id}:
        blockers.append("E1 must leave exactly the technical gold mechanism.")
    if len(tier_survivors["E2"]) < 2 or gold_id not in tier_survivors["E2"]:
        blockers.append("E2 must retain the gold mechanism and at least one alternative.")
    if tier_survivors["E3"] != mechanisms:
        blockers.append("E3 must leave all predeclared mechanisms unresolved.")
    if not tier_survivors["E1"] < tier_survivors["E2"] or not tier_survivors["E2"] < tier_survivors["E3"]:
        blockers.append("Surviving mechanisms must be proper nested sets: E1 subset E2 subset E3.")

    ids = {level: set(tier_evidence[level]) for level in ("E1", "E2", "E3")}
    if not ids["E3"] < ids["E2"] or not ids["E2"] < ids["E1"]:
        blockers.append("Evidence packets must be proper nested sets: E3 subset E2 subset E1.")
    for lower, upper in (("E3", "E2"), ("E2", "E1")):
        for evidence_id in ids[lower] & ids[upper]:
            if tier_evidence[lower][evidence_id] != tier_evidence[upper][evidence_id]:
                blockers.append(f"Evidence item {evidence_id} changes provenance/content between {lower} and {upper}.")
    if gold_id not in mechanisms:
        blockers.append("Gold mechanism is not present in the candidate mechanism set.")

    if source["repository_full_name"] != independence["upstream_project_id"]:
        blockers.append("source repository and canonical upstream_project_id must match after fork/mirror normalization.")
    if independence["upstream_project_id"] == "":
        blockers.append("upstream project identity is required.")
    if record["exposure"]["prior_pipeline_debug_exposure"] != "none":
        blockers.append("prior pipeline/debug exposure permanently excludes this candidate.")
    if record["human_decision"]["ai_critique_used"] and record["human_decision"]["ai_critique_record"] is None:
        blockers.append("AI critique use must have a separate, hashed advisory record.")
    if not record["human_decision"]["ai_critique_used"] and record["human_decision"]["ai_critique_record"] is not None:
        blockers.append("AI critique record must be null when no AI critique was used.")

    return {
        "status": "structurally_complete_candidate" if not blockers else "invalid",
        "blockers": blockers,
        "case_id": record["case_id"],
        "upstream_project_id": independence["upstream_project_id"],
        "defect_cluster_id": independence["defect_cluster_id"],
        "structural_only": True,
        "inference_authorized": False,
    }


def validate_registry(registry: Any) -> dict[str, Any]:
    blockers: list[str] = []
    if not isinstance(registry, Mapping):
        return {"status": "invalid", "blockers": ["registry must be an object."],
                "accepted_case_count": 0, "accepted_project_count": 0, "inference_authorized": False}
    if registry.get("registry_version") != "0.2-exploratory-draft":
        blockers.append("registry_version must be 0.2-exploratory-draft.")
    if registry.get("study_protocol") != "swe-rebench-v2-evidence-abstention":
        blockers.append("study_protocol mismatch.")
    if registry.get("study_type") != "exploratory_feasibility":
        blockers.append("study_type must remain exploratory_feasibility.")
    if registry.get("target_case_count") != MAX_CASES or registry.get("minimum_feasibility_case_count") != MIN_CASES:
        blockers.append("sample thresholds must remain target 20 and feasibility floor 15.")
    records = registry.get("records")
    if not isinstance(records, list):
        blockers.append("records must be a list.")
        records = []
    results = [validate_case_record(record) for record in records]
    for index, result in enumerate(results):
        if result["status"] != "structurally_complete_candidate":
            blockers.extend(f"records[{index}]: {item}" for item in result["blockers"])
    case_ids = [result.get("case_id") for result in results if result.get("case_id")]
    project_ids = [result.get("upstream_project_id") for result in results if result.get("upstream_project_id")]
    if len(case_ids) != len(set(case_ids)):
        blockers.append("case IDs must be unique.")
    if len(project_ids) != len(set(project_ids)):
        blockers.append("one case per distinct upstream project is required.")
    if len(records) > MAX_CASES:
        blockers.append("registry exceeds the target maximum of 20 cases.")
    if registry.get("accepted_case_count") != len(records):
        blockers.append("accepted_case_count must equal the number of records.")
    if registry.get("accepted_project_count") != len(set(project_ids)):
        blockers.append("accepted_project_count must equal distinct upstream project count.")
    if registry.get("inference_authorized") is not False:
        blockers.append("case acceptance validation must never authorize inference.")
    expected_status = "empty_no_cases_accepted" if not records else "contains_structurally_complete_candidates"
    if registry.get("status") != expected_status:
        blockers.append(f"registry status must be {expected_status}.")
    count = len(records)
    return {
        "status": "valid_empty_registry" if not blockers and count == 0 else
                  "structurally_valid_candidate_registry" if not blockers else "invalid",
        "blockers": blockers,
        "accepted_case_count": count if not blockers else 0,
        "accepted_project_count": len(set(project_ids)) if not blockers else 0,
        "feasibility_floor_met": count >= MIN_CASES if not blockers else False,
        "target_met": count == MAX_CASES if not blockers else False,
        "comparative_efficacy_claim_permitted": False,
        "structural_only": True,
        "inference_authorized": False,
    }
