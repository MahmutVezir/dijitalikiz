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


def test_eodag_1530_provenance_matches_packet_set_and_records_project_lead_decision():
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
    semantic = provenance["semantic_review"]
    assert semantic["adjudication_completed"] is True
    assert semantic["project_lead_decision"] == "approved"
    assert semantic["approved_tier_outcomes"] == {
        "E3": "ABSTAIN — issue narrative alone does not establish exact pinned parser output or fixture path.",
        "E2": "ABSTAIN — exact pinned YAML parse output is visible, but the packaged-template fixture/loading path is not; A2 and A3 remain plausible.",
        "E1": "ANSWER — active test-fixture source connects packaged template loading via yaml.safe_load to provider-configuration generation; only G1 survives under the project lead's source-aware adjudication.",
    }
    assert semantic["approved_surviving_mechanisms"] == {
        "E3": ["G1", "A1", "A2", "A3"],
        "E2": ["G1", "A2", "A3"],
        "E1": ["G1"],
    }
    assert semantic["independent_blinded_validation"] == "not_claimed"
    assert semantic["prior_pipeline_debug_exposure"] == "pending_project_lead_self_declaration"
    assert semantic["final_case_acceptance"] == "pending_remaining_mandatory_gates"
    assert semantic["decision_record"]["sha256"] == "b48db64273f6d552c12ef82e5b9d75992f85e266e987491feb9cf7db23e8e52e"
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



def test_eodag_1530_project_decision_is_in_manifest_and_ledger_but_not_registry():
    manifest = json.loads(
        (RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json")
        .read_text(encoding="utf-8")
    )
    ledger = json.loads(
        (RESEARCH / "SWE_REBENCH_V2_STAGE2_STAGE3_PROGRESS_LEDGER_V0_1_2026-11-16.json")
        .read_text(encoding="utf-8")
    )
    registry = json.loads(
        (RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json")
        .read_text(encoding="utf-8")
    )

    decisions = [
        item for item in manifest["project_lead_decisions"]
        if item.get("scope") == "EODAG_1530_source_aware_gold_and_tier_adjudication_and_case_continuation"
    ]
    assert len(decisions) == 1
    decision = decisions[0]
    assert decision["eodag_gold"]["status"] == "approved"
    assert decision["eodag_tiers"] == {
        "status": "approved",
        "E3": "ABSTAIN",
        "E2": "ABSTAIN",
        "E1": "ANSWER",
        "surviving_mechanisms": {
            "E3": ["G1", "A1", "A2", "A3"],
            "E2": ["G1", "A2", "A3"],
            "E1": ["G1"],
        },
    }
    assert decision["decision_record"]["sha256"] == (
        "b48db64273f6d552c12ef82e5b9d75992f85e266e987491feb9cf7db23e8e52e"
    )
    assert decision["boundaries"]["final_case_acceptance"] == (
        "not_accepted until mandatory gates, schema record and registry validation pass"
    )
    assert decision["boundaries"]["inference_authorized"] is False

    rows = [
        row for row in ledger["records"]
        if row.get("repository") == "CS-SI/eodag" and row.get("pull_request_number") == 1536
    ]
    assert len(rows) == 1
    row = rows[0]
    assert row["project_lead_gold_tier_decision"]["status"] == "approved"
    assert row["project_lead_gold_tier_decision"]["tier_decisions"] == {
        "E3": "ABSTAIN", "E2": "ABSTAIN", "E1": "ANSWER"
    }
    assert row["prior_pipeline_debug_exposure"] == "pending_project_lead_self_declaration"
    assert row["bounded_license_scope_acknowledgement"] == "pending"
    assert row["final_case_acceptance"] == "not_accepted"
    assert row["model_inference_authorized"] is False

    assert registry["accepted_case_count"] == 1
    assert registry["accepted_project_count"] == 1
    assert [record["case_id"] for record in registry["records"]] == ["SRV2E-DISHKA_435"]
