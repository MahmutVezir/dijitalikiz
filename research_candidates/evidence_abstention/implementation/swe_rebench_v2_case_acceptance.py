"""Fail-closed, no-inference acceptance gate for SWE-rebench V2 cases.

This module checks the structure and consistency of documented human reviews and
reproduction artifacts. It does not fetch/verify external artifacts, execute tests,
judge legal questions, inspect source code, or authorize model inference.
"""
from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from swe_rebench_v2_contract import (
    DATASET_FILE_REVISION,
    DATASET_FILE_SHA256,
    DATASET_ID,
)

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CASE_ID_RE = re.compile(r"^SRV2-[A-Z0-9_-]{1,48}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REGISTRY_VERSION = "0.1-draft"


def _mapping(value: Any, path: str, blockers: list[str]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        blockers.append(path + " must be an object.")
        return {}
    return value


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _artifact(value: Any, path: str, blockers: list[str]) -> None:
    item = _mapping(value, path, blockers)
    uri = item.get("artifact_uri")
    digest = item.get("sha256")
    if not _nonempty(uri) or not (
        str(uri).startswith("https://") or str(uri).startswith("artifacts/")
    ):
        blockers.append(path + ".artifact_uri must be a non-empty HTTPS URL or repository artifact path.")
    if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
        blockers.append(path + ".sha256 must be a lowercase SHA-256 digest.")


def _reviewers(
    value: Any,
    path: str,
    blockers: list[str],
    minimum: int = 2,
) -> set[str]:
    if not isinstance(value, list) or len(value) < minimum:
        blockers.append(path + " must contain at least " + str(minimum) + " reviewers.")
        return set()
    identifiers: list[str] = []
    for index, reviewer in enumerate(value):
        item_path = path + "[" + str(index) + "]"
        item = _mapping(reviewer, item_path, blockers)
        reviewer_id = item.get("reviewer_id")
        if not _nonempty(reviewer_id):
            blockers.append(item_path + ".reviewer_id is required.")
        else:
            identifiers.append(reviewer_id)
        if item.get("decision") != "approved":
            blockers.append(item_path + ".decision must be approved.")
        _artifact(item.get("review_record"), item_path + ".review_record", blockers)
    if len(identifiers) != len(set(identifiers)):
        blockers.append(path + " reviewer IDs must be unique.")
    return set(identifiers)


def validate_case_record(record: Any) -> dict[str, Any]:
    """Check a proposed accepted case; never verifies artifacts or semantic claims."""
    blockers: list[str] = []
    if not isinstance(record, Mapping):
        return {
            "status": "invalid",
            "blockers": ["case record must be an object."],
            "structural_only": True,
            "inference_authorized": False,
        }

    if record.get("acceptance_state") != "accepted_confirmatory":
        blockers.append("acceptance_state must be accepted_confirmatory.")

    case_id = record.get("case_id")
    if not isinstance(case_id, str) or CASE_ID_RE.fullmatch(case_id) is None:
        blockers.append("case_id must match SRV2- followed by an opaque uppercase identifier.")

    dataset = _mapping(record.get("dataset"), "dataset", blockers)
    if dataset.get("dataset_id") != DATASET_ID:
        blockers.append("dataset.dataset_id differs from the pinned SWE-rebench V2 dataset.")
    if dataset.get("file_revision") != DATASET_FILE_REVISION:
        blockers.append("dataset.file_revision differs from the pinned immutable revision.")
    if dataset.get("file_sha256") != DATASET_FILE_SHA256:
        blockers.append("dataset.file_sha256 differs from the pinned Parquet digest.")
    if dataset.get("cohort_role") not in {"primary", "project_reserve"}:
        blockers.append("dataset.cohort_role must be primary or project_reserve.")
    row_locator = _mapping(dataset.get("row_locator"), "dataset.row_locator", blockers)
    if not _nonempty(row_locator.get("field")) or not _nonempty(row_locator.get("value")):
        blockers.append("dataset.row_locator must identify the exact source row.")
    if not isinstance(dataset.get("row_sha256"), str) or SHA256_RE.fullmatch(dataset.get("row_sha256", "")) is None:
        blockers.append("dataset.row_sha256 must bind the exact selected row.")

    source = _mapping(record.get("source"), "source", blockers)
    repository = source.get("repository_full_name")
    if not isinstance(repository, str) or repository.count("/") != 1 or any(not p for p in repository.split("/")):
        blockers.append("source.repository_full_name must be owner/repository.")
    if not _nonempty(source.get("issue_or_pr_url")) or not str(source.get("issue_or_pr_url")).startswith("https://"):
        blockers.append("source.issue_or_pr_url must be an HTTPS source URL.")
    if not isinstance(source.get("pull_request_number"), int) or source.get("pull_request_number", 0) <= 0:
        blockers.append("source.pull_request_number must be a positive integer.")
    for field in ("base_commit_sha", "fixed_commit_sha"):
        value = source.get(field)
        if not isinstance(value, str) or COMMIT_RE.fullmatch(value) is None:
            blockers.append("source." + field + " must be a full 40-character commit SHA.")
    if source.get("base_commit_sha") == source.get("fixed_commit_sha"):
        blockers.append("base and fixed commits must differ.")
    paths = source.get("changed_paths")
    if not isinstance(paths, list) or not paths or any(not _nonempty(p) for p in paths):
        blockers.append("source.changed_paths must list at least one changed path.")
    for field in ("patch", "base_source_snapshot", "fixed_source_snapshot"):
        _artifact(source.get(field), "source." + field, blockers)

    independence = _mapping(record.get("independence"), "independence", blockers)
    if independence.get("review_status") != "passed" or independence.get("is_independent") is not True:
        blockers.append("independence review must explicitly pass.")
    for field in ("upstream_project_id", "defect_cluster_id"):
        if not _nonempty(independence.get(field)):
            blockers.append("independence." + field + " is required.")
    if independence.get("same_or_related_case_ids") != []:
        blockers.append("independence.same_or_related_case_ids must be empty for an independent confirmatory case.")
    _artifact(independence.get("review_record"), "independence.review_record", blockers)

    exposure = _mapping(record.get("exposure"), "exposure", blockers)
    if exposure.get("review_status") != "passed":
        blockers.append("exposure review must pass.")
    if exposure.get("confirmatory_analyst_saw_gold_or_fix") is not False:
        blockers.append("confirmatory analyst must attest they did not see the gold cause or fix.")
    if exposure.get("prior_pipeline_debug_exposure_status") != "none":
        blockers.append("candidate with prior pipeline/debug exposure is permanently excluded.")
    if not _nonempty(exposure.get("confirmatory_analyst_id")):
        blockers.append("exposure.confirmatory_analyst_id is required.")
    if not _nonempty(exposure.get("packet_preparer_id")):
        blockers.append("exposure.packet_preparer_id is required.")
    source_exposed = exposure.get("source_exposed_person_ids")
    if not isinstance(source_exposed, list) or any(not _nonempty(x) for x in source_exposed):
        blockers.append("exposure.source_exposed_person_ids must list every person who saw restricted source/gold material.")
        source_exposed = []
    if len(source_exposed) != len(set(source_exposed)):
        blockers.append("exposure.source_exposed_person_ids must be unique.")
    _artifact(exposure.get("review_record"), "exposure.review_record", blockers)

    license_review = _mapping(record.get("license_review"), "license_review", blockers)
    if license_review.get("source_license_expression") is None or not _nonempty(license_review.get("source_license_expression")):
        blockers.append("license_review.source_license_expression is required.")
    for field in ("exact_base_license_review", "changed_file_license_review", "third_party_content_review"):
        if license_review.get(field) != "passed":
            blockers.append("license_review." + field + " must be passed.")
    if license_review.get("research_use_decision") != "approved":
        blockers.append("license_review.research_use_decision must be approved.")
    if not _nonempty(license_review.get("reviewer_id")):
        blockers.append("license_review.reviewer_id is required.")
    root_license = _mapping(license_review.get("root_license_file"), "license_review.root_license_file", blockers)
    if not _nonempty(root_license.get("path")):
        blockers.append("license_review.root_license_file.path is required.")
    if root_license.get("commit_sha") != source.get("base_commit_sha"):
        blockers.append("root license file must be pinned to the exact buggy base commit.")
    if not isinstance(root_license.get("blob_sha"), str) or re.fullmatch(r"[0-9a-f]{40}", root_license.get("blob_sha", "")) is None:
        blockers.append("license_review.root_license_file.blob_sha must be a full Git blob SHA.")
    if not isinstance(root_license.get("content_sha256"), str) or SHA256_RE.fullmatch(root_license.get("content_sha256", "")) is None:
        blockers.append("license_review.root_license_file.content_sha256 must be a SHA-256 digest.")
    if root_license.get("license_expression") != license_review.get("source_license_expression"):
        blockers.append("root license file expression must match the reviewed source_license_expression.")
    _artifact(license_review.get("changed_file_license_manifest"), "license_review.changed_file_license_manifest", blockers)
    _artifact(license_review.get("review_record"), "license_review.review_record", blockers)

    technical = _mapping(record.get("technical_reproduction"), "technical_reproduction", blockers)
    if technical.get("status") != "passed":
        blockers.append("technical_reproduction.status must be passed.")
    if not isinstance(technical.get("environment_lock_sha256"), str) or SHA256_RE.fullmatch(technical.get("environment_lock_sha256", "")) is None:
        blockers.append("technical_reproduction.environment_lock_sha256 must be a SHA-256 digest.")
    baseline = _mapping(technical.get("buggy_baseline"), "technical_reproduction.buggy_baseline", blockers)
    fixed = _mapping(technical.get("fixed_revision"), "technical_reproduction.fixed_revision", blockers)
    if baseline.get("commit_sha") != source.get("base_commit_sha"):
        blockers.append("buggy_baseline.commit_sha must equal source.base_commit_sha.")
    if fixed.get("commit_sha") != source.get("fixed_commit_sha"):
        blockers.append("fixed_revision.commit_sha must equal source.fixed_commit_sha.")
    if not isinstance(baseline.get("exit_code"), int) or baseline.get("exit_code") == 0:
        blockers.append("buggy_baseline.exit_code must be non-zero.")
    if fixed.get("exit_code") != 0:
        blockers.append("fixed_revision.exit_code must be zero.")
    if not _nonempty(baseline.get("failure_signature")):
        blockers.append("buggy_baseline.failure_signature is required.")
    if baseline.get("test_selector") is None or not _nonempty(baseline.get("test_selector")):
        blockers.append("buggy_baseline.test_selector is required.")
    if fixed.get("test_selector") != baseline.get("test_selector"):
        blockers.append("the exact same test_selector must be run on buggy and fixed revisions.")
    if baseline.get("failure_is_targeted_regression") is not True:
        blockers.append("buggy baseline failure must be confirmed as the targeted regression, not an unrelated command failure.")
    if fixed.get("same_test_passed") is not True:
        blockers.append("the same targeted regression test must pass on the fixed revision.")
    for key, path in ((baseline, "technical_reproduction.buggy_baseline"), (fixed, "technical_reproduction.fixed_revision")):
        _artifact(key.get("run_record"), path + ".run_record", blockers)
    if not _nonempty(technical.get("reviewer_id")):
        blockers.append("technical_reproduction.reviewer_id is required.")
    _artifact(technical.get("review_record"), "technical_reproduction.review_record", blockers)

    gold = _mapping(record.get("gold_standard"), "gold_standard", blockers)
    if gold.get("status") != "approved" or gold.get("agreement_status") not in {"unanimous", "adjudicated"}:
        blockers.append("gold_standard must be approved by agreement or documented adjudication.")
    mechanisms = gold.get("candidate_mechanisms")
    if not isinstance(mechanisms, list) or len(mechanisms) < 3:
        blockers.append("gold_standard.candidate_mechanisms must contain the gold cause and at least two plausible alternatives.")
        mechanisms = []
    mechanism_ids = [
        item.get("mechanism_id")
        for item in mechanisms
        if isinstance(item, Mapping)
        and _nonempty(item.get("mechanism_id"))
        and _nonempty(item.get("description"))
    ]
    if len(mechanism_ids) != len(mechanisms) or len(mechanism_ids) != len(set(mechanism_ids)):
        blockers.append("candidate mechanism IDs and descriptions must be present and IDs unique.")
    gold_id = gold.get("final_gold_mechanism_id")
    if gold_id not in mechanism_ids:
        blockers.append("gold_standard.final_gold_mechanism_id must identify one candidate mechanism.")
    panel_a_ids = _reviewers(gold.get("panel_a_reviews"), "gold_standard.panel_a_reviews", blockers)
    panel_a_decisions = [
        item.get("gold_mechanism_id")
        for item in gold.get("panel_a_reviews", [])
        if isinstance(item, Mapping)
    ]
    if gold.get("agreement_status") == "unanimous" and (
        len(panel_a_decisions) < 2 or any(value != gold_id for value in panel_a_decisions)
    ):
        blockers.append("unanimous Panel A ratings must independently identify the final gold mechanism.")
    if gold.get("agreement_status") == "adjudicated":
        adjudication = _mapping(gold.get("adjudication"), "gold_standard.adjudication", blockers)
        if adjudication.get("final_gold_mechanism_id") != gold_id:
            blockers.append("Panel A adjudication must identify the final gold mechanism.")
        adjudicator_id = adjudication.get("reviewer_id")
        if not _nonempty(adjudicator_id) or adjudicator_id in panel_a_ids:
            blockers.append("Panel A adjudicator must be identified and separate from the two raters.")
        _artifact(adjudication.get("review_record"), "gold_standard.adjudication.review_record", blockers)

    tiers = _mapping(record.get("evidence_tiers"), "evidence_tiers", blockers)
    if tiers.get("status") != "approved":
        blockers.append("evidence_tiers.status must be approved.")
    for field in ("panel_b_blind_to_gold", "panel_b_blind_to_fix", "tier_labels_hidden_until_rating_lock"):
        if tiers.get(field) is not True:
            blockers.append("evidence_tiers." + field + " must be true.")
    if tiers.get("rating_lock_before_gold_unblinding") is not True:
        blockers.append("Panel B ratings must be locked before gold unblinding.")
    panel_b_ids = _reviewers(tiers.get("panel_b_reviews"), "evidence_tiers.panel_b_reviews", blockers)
    if panel_a_ids & panel_b_ids:
        blockers.append("Panel A and Panel B reviewer identities must be disjoint.")

    all_reviewers = set(panel_a_ids) | set(panel_b_ids)
    technical_id = technical.get("reviewer_id")
    license_id = license_review.get("reviewer_id")
    analyst_id = exposure.get("confirmatory_analyst_id")
    packet_preparer_id = exposure.get("packet_preparer_id")
    adjudication = gold.get("adjudication") if gold.get("agreement_status") == "adjudicated" else {}
    adjudicator_id = adjudication.get("reviewer_id") if isinstance(adjudication, Mapping) else None
    if technical_id in all_reviewers or license_id in all_reviewers:
        blockers.append("technical and legal reviewers must be separate from blinded scientific panels.")
    if technical_id == license_id:
        blockers.append("technical reproduction and license review must have different reviewers.")
    if not _nonempty(analyst_id) or analyst_id in all_reviewers or analyst_id in {technical_id, license_id, packet_preparer_id, adjudicator_id}:
        blockers.append("confirmatory analyst must be identified and separate from every source-exposed reviewer and both panels.")
    if not _nonempty(packet_preparer_id) or packet_preparer_id in all_reviewers or packet_preparer_id in {analyst_id, license_id, adjudicator_id}:
        blockers.append("packet preparer must be identified and separate from both blinded panels, legal reviewer, analyst, and adjudicator.")
    required_source_exposed = set(panel_a_ids) | {technical_id, license_id, packet_preparer_id}
    if adjudicator_id:
        required_source_exposed.add(adjudicator_id)
    if not required_source_exposed.issubset(set(source_exposed)):
        blockers.append("source_exposed_person_ids must include technical reviewer, packet preparer, Panel A raters, and any gold adjudicator.")
    if set(source_exposed) & set(panel_b_ids):
        blockers.append("no source-exposed person may serve on blinded Panel B.")
    if analyst_id in set(source_exposed):
        blockers.append("confirmatory analyst must not appear in the source-exposed person list.")
    if adjudicator_id in panel_b_ids or adjudicator_id in {technical_id, license_id, analyst_id, packet_preparer_id}:
        blockers.append("Panel A adjudicator must be separate from Panel B and other operational roles.")

    decisions = _mapping(tiers.get("final_tier_decisions"), "evidence_tiers.final_tier_decisions", blockers)
    tier_survivors: dict[str, set[str]] = {}
    for level in ("E1", "E2", "E3"):
        item = _mapping(decisions.get(level), "evidence_tiers.final_tier_decisions." + level, blockers)
        survivors = item.get("surviving_mechanism_ids")
        if not isinstance(survivors, list) or not survivors or any(not _nonempty(x) for x in survivors):
            blockers.append(level + " must list surviving candidate mechanisms.")
            survivors = []
        if len(survivors) != len(set(survivors)):
            blockers.append(level + " surviving mechanism IDs must be unique.")
        if set(survivors) - set(mechanism_ids):
            blockers.append(level + " references a mechanism absent from Panel A's candidate set.")
        tier_survivors[level] = set(survivors)
        _artifact(item.get("locked_rating_record"), "evidence_tiers.final_tier_decisions." + level + ".locked_rating_record", blockers)

    if tier_survivors["E1"] != {gold_id}:
        blockers.append("E1 must leave only the independently established gold mechanism.")
    if len(tier_survivors["E2"]) < 2 or gold_id not in tier_survivors["E2"]:
        blockers.append("E2 must retain the gold mechanism and at least one plausible alternative.")
    if tier_survivors["E3"] != set(mechanism_ids):
        blockers.append("E3 must leave every preregistered candidate mechanism unresolved.")
    if not tier_survivors["E1"].issubset(tier_survivors["E2"]) or not tier_survivors["E2"].issubset(tier_survivors["E3"]):
        blockers.append("Surviving mechanisms must be nested E1 subset E2 subset E3.")
    _artifact(tiers.get("packet_set"), "evidence_tiers.packet_set", blockers)
    _artifact(tiers.get("panel_b_consensus_record"), "evidence_tiers.panel_b_consensus_record", blockers)

    if not blockers:
        return {
            "status": "structurally_complete_pending_external_authenticity_and_semantic_audit",
            "blockers": [],
            "case_id": case_id,
            "upstream_project_id": independence.get("upstream_project_id"),
            "defect_cluster_id": independence.get("defect_cluster_id"),
            "structural_only": True,
            "inference_authorized": False,
        }
    return {
        "status": "invalid",
        "blockers": blockers,
        "case_id": case_id,
        "structural_only": True,
        "inference_authorized": False,
    }


def validate_registry(registry: Any) -> dict[str, Any]:
    """Check registry counts, uniqueness, and case-record completeness."""
    blockers: list[str] = []
    if not isinstance(registry, Mapping):
        return {
            "status": "invalid",
            "blockers": ["registry must be an object."],
            "accepted_case_count": 0,
            "accepted_project_count": 0,
            "inference_authorized": False,
        }

    if registry.get("registry_version") != REGISTRY_VERSION:
        blockers.append("registry_version must equal 0.1-draft.")
    if registry.get("study_protocol") != "swe-rebench-v2-evidence-abstention":
        blockers.append("study_protocol does not identify the SWE-rebench V2 protocol.")
    records = registry.get("records")
    if not isinstance(records, list):
        blockers.append("records must be a list.")
        records = []

    declared_cases = registry.get("accepted_case_count")
    declared_projects = registry.get("accepted_project_count")
    if declared_cases != len(records):
        blockers.append("accepted_case_count must equal the number of registry records.")

    case_ids: list[str] = []
    project_ids: list[str] = []
    defect_ids: list[str] = []
    for index, record in enumerate(records):
        result = validate_case_record(record)
        if result["status"] != "structurally_complete_pending_external_authenticity_and_semantic_audit":
            blockers.append("records[" + str(index) + "] failed case acceptance validation.")
            blockers.extend("records[" + str(index) + "]: " + item for item in result["blockers"])
            continue
        case_ids.append(result["case_id"])
        project_ids.append(result["upstream_project_id"])
        defect_ids.append(result["defect_cluster_id"])

    for field, values in (
        ("case_id", case_ids),
        ("upstream_project_id", project_ids),
        ("defect_cluster_id", defect_ids),
    ):
        if len(values) != len(set(values)):
            blockers.append(field + " values must be unique across accepted confirmatory records.")

    actual_projects = len(set(project_ids))
    if declared_projects != actual_projects:
        blockers.append("accepted_project_count must equal the distinct accepted upstream project count.")

    if not records:
        if registry.get("status") != "empty_no_confirmatory_cases_accepted":
            blockers.append("empty registry status must be empty_no_confirmatory_cases_accepted.")
        status = "valid_empty_registry"
    else:
        if registry.get("status") != "contains_documented_acceptances_pending_external_audit":
            blockers.append("non-empty registry status must disclose pending external authenticity and semantic audit.")
        status = "structurally_valid_pending_external_audit"

    if blockers:
        status = "invalid"
    return {
        "status": status,
        "blockers": blockers,
        "accepted_case_count": len(records),
        "accepted_project_count": actual_projects,
        "minimum_sample_thresholds_met": len(records) >= 60 and actual_projects >= 8,
        "structural_only": True,
        "inference_authorized": False,
    }
