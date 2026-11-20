import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research_candidates" / "evidence_abstention"
EODAG = RESEARCH / "eodag_1530"
IMPLEMENTATION = RESEARCH / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from evidence_level_packet_set import validate_packet_set


def test_eodag_1530_packet_set_is_hash_valid_and_strictly_nested():
    packet_set = json.loads(
        (EODAG / "OPERATIONAL_EVIDENCE_PACKET_SET_PROPOSED_V0_1_2026-11-20.json")
        .read_text(encoding="utf-8")
    )

    result = validate_packet_set(packet_set)

    assert result["status"] == "valid", result["blockers"]
    assert result["strictly_nested"] is True
    assert result["packet_set_sha256"] == (
        "e1c15239ba0599c13d19c35ffad922d77ae10bb570aced8199d6db97163d3189"
    )
    assert {
        level: len(packet_set["packets"][level]["evidence_items"])
        for level in ("E1", "E2", "E3")
    } == {"E1": 7, "E2": 4, "E3": 1}
    assert result["additional_evidence_ids"]["E2_over_E3"] == [
        "EODAG_BASE_TEMPLATE_DUPLICATE_KEYS",
        "EODAG_BASE_YAML_PARSE_FAILURE",
        "EODAG_INDEPENDENT_YAML_REPRODUCER",
    ]
    assert result["additional_evidence_ids"]["E1_over_E2"] == [
        "EODAG_BASE_SUPPORTED_PROVIDER_LIST",
        "EODAG_TEST_FIXTURE_SAFE_LOAD_PATH",
        "EODAG_TEST_SELECTOR_CALL_PATH",
    ]
    assert result["semantic_sufficiency_assessed"] is False
    assert result["gold_root_cause_read"] is False
    assert result["model_inference_performed"] is False


def test_eodag_1530_provenance_matches_packet_set_and_human_decision_is_pending():
    packet_set = json.loads(
        (EODAG / "OPERATIONAL_EVIDENCE_PACKET_SET_PROPOSED_V0_1_2026-11-20.json")
        .read_text(encoding="utf-8")
    )
    provenance = json.loads(
        (EODAG / "EVIDENCE_PACKET_PROVENANCE_PROPOSED_V0_1_2026-11-20.json")
        .read_text(encoding="utf-8")
    )

    assert provenance["packet_set_path"] == str(
        (EODAG / "OPERATIONAL_EVIDENCE_PACKET_SET_PROPOSED_V0_1_2026-11-20.json")
        .relative_to(ROOT)
    )
    assert provenance["packet_set_sha256"] == packet_set["packet_set_sha256"]
    assert provenance["semantic_review"]["adjudication_completed"] is False
    assert provenance["semantic_review"]["project_lead_decision"] == "pending"
    assert provenance["structural_validation"]["semantic_sufficiency_assessed"] is False
    assert provenance["structural_validation"]["model_inference_performed"] is False


def test_eodag_1530_independence_and_license_reviews_are_not_final_acceptance():
    independence = json.loads(
        (EODAG / "EODAG_1530_ISSUE_FAMILY_INDEPENDENCE_REVIEW_V0_1_2026-11-20.json")
        .read_text(encoding="utf-8")
    )
    license_review = json.loads(
        (EODAG / "EODAG_1530_DEPENDENCY_LICENSE_SCOPE_REVIEW_V0_1_2026-11-20.json")
        .read_text(encoding="utf-8")
    )

    assert independence["counting_rule"]["issue_count"] == 1
    assert independence["counting_rule"]["dataset_row_count"] == 1
    assert independence["counting_rule"]["frozen_dataset_selector_count"] == 2
    assert independence["counting_rule"]["independent_yaml_reproducer_count"] == 1
    assert independence["counting_rule"]["reproduction_routes_are_not_additional_cases"] is True
    assert independence["issue_family_disposition"]["exact_duplicate_found"] is False
    assert 1517 in independence["issue_family_disposition"][
        "duplicate_candidates_excluded_from_independent_case_count"
    ]
    assert independence["exposure_and_roles"]["prior_pipeline_debug_exposure_status"] == (
        "pending_project_lead_self_declaration"
    )
    assert independence["independence_status"]["final_case_acceptance"] == "not_accepted"
    assert independence["independence_status"]["inference_authorized"] is False

    assert license_review["upstream_source"]["root_license_expression"] == "Apache-2.0"
    assert license_review["dataset"]["exact_pinned_dataset_card_license"] == "CC-BY-4.0"
    assert license_review["dataset"]["exact_pinned_dataset_card_license_verified"] is True
    assert license_review["reproduction_environment"]["resolved_distribution_count"] == 52
    assert license_review["reproduction_environment"]["internal_sha256_entries_verified"] == 22
    assert license_review["human_review"]["project_lead_bounded_scope_acknowledgement"] == "pending"
    assert license_review["human_review"]["accepted_as_legal_clearance"] is False
    assert license_review["human_review"]["final_case_acceptance"] == "not_accepted"
    assert license_review["inference_authorized"] is False
