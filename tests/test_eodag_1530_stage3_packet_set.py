import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research_candidates" / "evidence_abstention"
EODAG = RESEARCH / "eodag_1530"
IMPLEMENTATION = RESEARCH / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from evidence_level_packet_set import validate_packet_set
from swe_rebench_v2_exploratory_case_acceptance import validate_case_record, validate_registry


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
    assert semantic["prior_pipeline_debug_exposure"] == "none"
    assert semantic["prior_pipeline_debug_exposure_decision_record"] == {
        "path": "research_candidates/evidence_abstention/eodag_1530/PROJECT_LEAD_PRIOR_PIPELINE_DEBUG_EXPOSURE_DECLARATION_EODAG_1530_2026-11-21.md",
        "sha256": "5a51adf26ae3597e398d5aad5494a55e5a553fe4a787a79de4bc8d3afb89ae38",
        "decision_date": "2026-11-21",
        "decision": "none",
    }
    assert semantic["final_case_acceptance"] == "accepted_v0_2_exploratory_feasibility_only"
    assert semantic["decision_record"]["sha256"] == "b48db64273f6d552c12ef82e5b9d75992f85e266e987491feb9cf7db23e8e52e"
    assert provenance["structural_validation"]["semantic_sufficiency_assessed"] is False
    assert provenance["structural_validation"]["model_inference_performed"] is False


def test_eodag_1530_independence_and_license_reviews_preserve_limits_after_acceptance():
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
    assert independence["exposure_and_roles"]["prior_pipeline_debug_exposure_status"] == "none"
    assert independence["exposure_and_roles"]["prior_pipeline_debug_exposure_decision_record"]["sha256"] == (
        "5a51adf26ae3597e398d5aad5494a55e5a553fe4a787a79de4bc8d3afb89ae38"
    )
    assert independence["independence_status"]["final_case_acceptance"] == "accepted_v0_2_exploratory_feasibility_only"
    assert independence["independence_status"]["inference_authorized"] is False

    assert license_review["upstream_source"]["root_license_expression"] == "Apache-2.0"
    assert license_review["dataset"]["exact_pinned_dataset_card_license"] == "CC-BY-4.0"
    assert license_review["dataset"]["exact_pinned_dataset_card_license_verified"] is True
    assert license_review["reproduction_environment"]["resolved_distribution_count"] == 52
    assert license_review["reproduction_environment"]["internal_sha256_entries_verified"] == 22
    assert license_review["human_review"]["project_lead_bounded_scope_acknowledgement"] == "approved_bounded_scope_only"
    assert license_review["human_review"]["bounded_scope_acknowledgement_record"] == {
        "path": "research_candidates/evidence_abstention/eodag_1530/PROJECT_LEAD_BOUNDED_LICENSE_SCOPE_ACKNOWLEDGEMENT_EODAG_1530_2026-11-21.md",
        "sha256": "6513f066df7130173deb8ba9316ab24ed4cded73b25487e88c9013bff01a8af6",
        "decision_date": "2026-11-21",
        "decision": "acknowledged_bounded_documentary_scope_only",
    }
    assert license_review["human_review"]["external_legal_review"] == "not_performed"
    assert license_review["human_review"]["accepted_as_legal_clearance"] is False
    assert license_review["project_lead_acknowledged_scope"]["exclusions"] == [
        "complete SWE-rebench dataset redistribution",
        "complete EODAG repository redistribution",
        "installed wheels, binaries, native libraries, or complete 52-distribution environment redistribution",
        "blanket permission for optional extras, third-party provider data, or commercial product use",
    ]
    assert license_review["project_lead_acknowledged_scope"]["limits"]["legal_clearance"] is False
    assert license_review["human_review"]["accepted_as_legal_clearance"] is False
    assert license_review["human_review"]["final_case_acceptance"] == "accepted_v0_2_exploratory_feasibility_only"
    assert license_review["human_review"]["final_case_acceptance_decision_record"]["sha256"] == (
        "5f363c0b4e20752e5591704f1fd540f238bd9af8ab961aa8ce0380b074d6e76d"
    )
    assert license_review["inference_authorized"] is False



def test_eodag_1530_final_decision_is_in_manifest_and_ledger_and_registry():
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
    provenance = json.loads(
        (EODAG / "EVIDENCE_PACKET_PROVENANCE_PROPOSED_V0_1_2026-11-20.json")
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
    assert decision["boundaries"]["prior_pipeline_debug_exposure"] == (
        "none; project-lead self-declaration recorded separately"
    )
    assert decision["boundaries"]["prior_pipeline_debug_exposure_decision_record_sha256"] == (
        "5a51adf26ae3597e398d5aad5494a55e5a553fe4a787a79de4bc8d3afb89ae38"
    )
    assert decision["boundaries"]["final_case_acceptance"] == (
        "not_accepted until mandatory gates, schema record and registry validation pass"
    )
    assert decision["boundaries"]["inference_authorized"] is False

    license_decisions = [
        item for item in manifest["project_lead_decisions"]
        if item.get("scope") == "EODAG_1530_bounded_documentary_license_scope_acknowledgement"
    ]
    assert len(license_decisions) == 1
    assert license_decisions[0]["decision"] == "acknowledged_bounded_documentary_scope_only"
    assert license_decisions[0]["decision_record"]["sha256"] == (
        "6513f066df7130173deb8ba9316ab24ed4cded73b25487e88c9013bff01a8af6"
    )
    assert license_decisions[0]["boundaries"]["legal_clearance"] is False

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
    assert row["prior_pipeline_debug_exposure"] == "none"
    assert row["exposure_decision_record_sha256"] == (
        "5a51adf26ae3597e398d5aad5494a55e5a553fe4a787a79de4bc8d3afb89ae38"
    )
    assert row["bounded_license_scope_acknowledgement"] == "approved_bounded_documentary_scope_only_2026-11-21"
    assert row["bounded_license_scope_decision_record_sha256"] == (
        "6513f066df7130173deb8ba9316ab24ed4cded73b25487e88c9013bff01a8af6"
    )
    assert row["final_case_acceptance"] == "accepted_v0_2_exploratory_feasibility_only"
    assert row["final_acceptance_decision_record_sha256"] == (
        "5f363c0b4e20752e5591704f1fd540f238bd9af8ab961aa8ce0380b074d6e76d"
    )
    assert row["model_inference_authorized"] is False

    assert registry["accepted_case_count"] == 3
    assert "license_scope_acknowledgement" in provenance
    assert provenance["license_scope_acknowledgement"]["status"] == "approved_bounded_documentary_scope_only"
    assert provenance["license_scope_acknowledgement"]["inference_authorized"] is False
    assert any(record.get("case_id") == "SRV2E-EODAG_1530" for record in registry["records"])
    assert registry["accepted_project_count"] == 3
    assert [record["case_id"] for record in registry["records"]] == [
        "SRV2E-DISHKA_435", "SRV2E-EODAG_1530", "SRV2E-GEOFILEOPS_649"
    ]
    final_decisions = [
        item for item in manifest["project_lead_decisions"]
        if item.get("scope") == "EODAG_1530_final_case_acceptance"
    ]
    assert len(final_decisions) == 1
    assert final_decisions[0]["decision"] == "accepted"
    assert final_decisions[0]["decision_record"]["sha256"] == (
        "5f363c0b4e20752e5591704f1fd540f238bd9af8ab961aa8ce0380b074d6e76d"
    )
    assert manifest["accepted_case_count"] == 3
    assert manifest["accepted_project_count"] == 3



def test_eodag_1530_case_record_is_accepted_and_registry_is_structurally_valid():
    case_record = json.loads(
        (EODAG / "SWE_REBENCH_V2_EODAG_1530_CASE_ACCEPTANCE_PROPOSED_V0_2.json")
        .read_text(encoding="utf-8")
    )

    result = validate_case_record(case_record)

    assert result["status"] == "structurally_complete_candidate", result["blockers"]
    assert result["case_id"] == "SRV2E-EODAG_1530"
    assert result["acceptance_decision"] == "accepted"
    assert result["eligible_for_registry"] is True
    assert result["inference_authorized"] is False
    assert case_record["human_decision"]["decision_timestamp_utc"] == "2026-11-21T10:07:34Z"
    assert "exact interaction time is not captured" in case_record["human_decision"]["rationale"]
    assert case_record["final_acceptance"]["status"] == "approved"
    assert case_record["final_acceptance"]["decision_timestamp_utc"] == "2026-11-21T13:36:50+03:00"
    assert case_record["final_acceptance"]["decision_record"]["sha256"] == (
        "5f363c0b4e20752e5591704f1fd540f238bd9af8ab961aa8ce0380b074d6e76d"
    )

    registry = json.loads(
        (RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json")
        .read_text(encoding="utf-8")
    )
    registry_result = validate_registry(registry)

    assert registry_result["status"] == "structurally_valid_candidate_registry", registry_result["blockers"]
    assert registry_result["accepted_case_count"] == 2
    assert registry_result["accepted_project_count"] == 2
    assert [item["case_id"] for item in registry["records"]] == [
        "SRV2E-DISHKA_435", "SRV2E-EODAG_1530", "SRV2E-GEOFILEOPS_649"
    ]
    assert any(item["case_id"] == "SRV2E-EODAG_1530" for item in registry["records"])
