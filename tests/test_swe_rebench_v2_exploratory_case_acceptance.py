import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research_candidates" / "evidence_abstention"
sys.path.insert(0, str(RESEARCH / "implementation"))
from swe_rebench_v2_exploratory_case_acceptance import load_schema, validate_case_record, validate_registry


def test_v02_acceptance_schema_is_valid_json_schema():
    schema = load_schema()
    assert schema["$schema"].endswith("/2020-12/schema")
    assert set(schema["properties"]["acceptance_decision"]["enum"]) == {"proposed", "accepted", "rejected"}
    assert "final_acceptance" in schema["required"]


def test_v02_empty_registry_is_valid_but_does_not_authorize_inference():
    registry = json.loads((RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json").read_text())
    result = validate_registry(registry)
    assert result["status"] == "valid_empty_registry"
    assert result["accepted_case_count"] == 0
    assert result["inference_authorized"] is False
    assert result["comparative_efficacy_claim_permitted"] is False


def _minimal_case():
    sha = "a" * 64
    commit_a, commit_b = "1" * 40, "2" * 40
    artifact = {"uri": "artifacts/example.json", "sha256": sha}
    mechanisms = [
        {"mechanism_id":"gold","description":"Documented defect mechanism","testable_prediction":"Targeted test fails before fix."},
        {"mechanism_id":"alt1","description":"Alternative one","testable_prediction":"Would produce a distinct observable."},
        {"mechanism_id":"alt2","description":"Alternative two","testable_prediction":"Would produce another distinct observable."}
    ]
    def item(eid):
        return {"evidence_id":eid,"content_sha256":sha,"source_snapshot_sha256":sha,
                "source_uri":"https://example.org/source","source_commit_sha":commit_a,"source_path":"src/file.py"}
    e1_items = [item("A"),item("B"),item("C")]
    e2_items = [item("B"),item("C")]
    e3_items = [item("C")]
    def tier(ids, survivors, packet_sha):
        return {"packet":{"uri":"artifacts/packet.json","sha256":packet_sha},
                "surviving_mechanism_ids":survivors,"semantic_rationale":"Recorded source-grounded rationale.",
                "evidence_items":ids}
    return {
      "schema_version":"0.1-v02-exploratory","case_id":"SRV2E-CASE1","acceptance_decision":"accepted",
      "final_acceptance":{"status":"approved","decision_maker_role":"student_project_lead",
                          "decision_timestamp_utc":"2026-11-19T13:00:00Z",
                          "rationale":"Separate project-lead case-acceptance decision recorded after all candidate gates passed.",
                          "decision_record":artifact},
      "dataset":{"dataset_id":"PrimeIntellect/SWE-rebench-V2-Filtered-Verified","file_revision":"fb9aa226b2ce37c708ea7732e7b980abacdadb67",
                 "file_sha256":"7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9",
                 "created_at_dataset_utc":"2024-01-01T00:00:00Z","created_at_upstream_utc":"2024-01-01T00:00:00Z",
                 "timestamp_reconciliation_status":"exact_match","timestamp_review_record":artifact,
                 "row_locator":{"field":"instance_id","value":"candidate-1"},"row_sha256":sha,"cohort_role":"primary"},
      "source":{"repository_full_name":"org/repo","issue_or_pr_url":"https://github.com/org/repo/pull/1","resource_type":"pull_request",
                "base_commit_sha":commit_a,"fixed_commit_sha":commit_b,"changed_paths":["src/file.py"],
                "patch":artifact,"base_source_snapshot":artifact,"fixed_source_snapshot":artifact},
      "independence":{"status":"passed","upstream_project_id":"org/repo","defect_cluster_id":"defect-1",
                      "is_fork_or_mirror":False,"related_case_ids":[],"review_record":artifact},
      "exposure":{"prior_pipeline_debug_exposure":"none","researcher_source_exposure":"full",
                  "exposure_notes":"Researcher reviewed upstream source before model output scoring.",
                  "review_record":artifact},
      "license_review":{"root_license_expression":"MIT","exact_base_review":"passed","changed_file_review":"passed",
                        "nested_dependency_review":"passed","notice_and_provenance_review":"passed","research_use_decision":"no_obvious_prohibition_identified","scope_limitation":"documentary_screening_only_not_legal_advice",
                        "reviewer_role":"student_project_lead","review_record":artifact,"changed_file_license_manifest":artifact,
                        "root_license_file":{"path":"LICENSE","commit_sha":commit_a,"blob_sha":commit_a,"content_sha256":sha,"license_expression":"MIT"}},
      "technical_reproduction":{"status":"passed","environment_lock_sha256":sha,"test_selector":"tests/test_issue.py::test_regression",
                                "buggy_baseline":{"commit_sha":commit_a,"exit_code":1,"failure_signature":"Expected regression failure","test_selector":"tests/test_issue.py::test_regression","run_record":artifact},
                                "fixed_revision":{"commit_sha":commit_b,"exit_code":0,"same_test_passed":True,"test_selector":"tests/test_issue.py::test_regression","run_record":artifact},
                                "review_record":artifact},
      "gold_standard":{"status":"human_recorded","gold_mechanism_id":"gold","candidate_mechanisms":mechanisms,
                       "technical_rationale":"Patch and targeted reproduction identify the mechanism.","evidence_refs":["C"],"review_record":artifact},
      "evidence_tiers":{"status":"human_recorded","tier_decision_record":artifact,
                        "E1":tier(e1_items,["gold"],"b"*64),"E2":tier(e2_items,["gold","alt1"],"c"*64),
                        "E3":tier(e3_items,["gold","alt1","alt2"],"d"*64)},
      "human_decision":{"decision_maker_role":"student_project_lead","decision_timestamp_utc":"2026-11-16T10:00:00Z",
                        "rationale":"All mandatory gates were reviewed.","ai_critique_used":False,"ai_critique_record":None}
    }


def test_valid_structural_case_is_candidate_not_inference_authorization():
    result = validate_case_record(_minimal_case())
    assert result["status"] == "structurally_complete_candidate"
    assert result["inference_authorized"] is False



def test_proposed_case_can_be_structurally_checked_without_premature_acceptance():
    record = _minimal_case()
    record["acceptance_decision"] = "proposed"
    record["final_acceptance"] = {
        "status": "pending",
        "decision_maker_role": "student_project_lead",
        "decision_timestamp_utc": None,
        "rationale": "Awaiting the separate project-lead yes/no decision.",
        "decision_record": None,
    }
    result = validate_case_record(record)
    assert result["status"] == "structurally_complete_candidate"
    assert result["acceptance_decision"] == "proposed"
    assert result["eligible_for_registry"] is False
    assert result["inference_authorized"] is False


def test_accepted_case_requires_timestamped_hashed_final_project_lead_decision():
    record = _minimal_case()
    record["final_acceptance"]["decision_record"] = None
    result = validate_case_record(record)
    assert result["status"] == "invalid"
    assert any("final_acceptance" in item for item in result["blockers"])


def test_accepted_registry_rejects_proposed_case_even_if_structurally_complete():
    registry = json.loads((RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json").read_text())
    record = _minimal_case()
    record["acceptance_decision"] = "proposed"
    record["final_acceptance"] = {
        "status": "pending",
        "decision_maker_role": "student_project_lead",
        "decision_timestamp_utc": None,
        "rationale": "Awaiting decision.",
        "decision_record": None,
    }
    registry["records"] = [record]
    registry["accepted_case_count"] = 1
    registry["accepted_project_count"] = 1
    registry["status"] = "contains_structurally_complete_candidates"
    result = validate_registry(registry)
    assert result["status"] == "invalid"
    assert any("only explicitly accepted cases" in item for item in result["blockers"])


def test_case_rejects_non_nested_evidence_and_mechanisms():
    record = _minimal_case()
    record["evidence_tiers"]["E2"]["evidence_items"] = [record["evidence_tiers"]["E3"]["evidence_items"][0]]
    result = validate_case_record(record)
    assert result["status"] == "invalid"
    assert any("proper nested sets" in item for item in result["blockers"])


def test_case_rejects_prior_pipeline_exposure():
    record = _minimal_case()
    record["exposure"]["prior_pipeline_debug_exposure"] = "prior_exposure"
    result = validate_case_record(record)
    assert result["status"] == "invalid"


def test_case_rejects_gold_leak_into_e3():
    record = _minimal_case()
    record["evidence_tiers"]["E3"]["surviving_mechanism_ids"] = ["gold"]
    result = validate_case_record(record)
    assert result["status"] == "invalid"
    assert any("E3 must leave all" in item for item in result["blockers"])


def test_case_rejects_mismatched_github_resource_type():
    record = _minimal_case()
    record["source"]["resource_type"] = "issue"
    result = validate_case_record(record)
    assert result["status"] == "invalid"
    assert any("issue resource_type" in item for item in result["blockers"])


def test_case_rejects_different_buggy_and_fixed_test_selectors():
    record = _minimal_case()
    record["technical_reproduction"]["fixed_revision"]["test_selector"] = "tests/test_other.py::test_other"
    result = validate_case_record(record)
    assert result["status"] == "invalid"
    assert any("exact same defect-specific test selector" in item for item in result["blockers"])


def test_registry_accepts_valid_smaller_sample_below_primary_target():
    registry = json.loads((RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json").read_text())
    record = _minimal_case()
    registry["records"] = [record]
    registry["accepted_case_count"] = 1
    registry["accepted_project_count"] = 1
    registry["status"] = "contains_structurally_complete_candidates"

    result = validate_registry(registry)

    assert result["status"] == "structurally_valid_candidate_registry"
    assert result["accepted_case_count"] == 1
    assert result["accepted_project_count"] == 1
    assert result["minimum_feasibility_count_met"] is True
    assert result["primary_target_met"] is False
    assert result["stretch_target_met"] is False
    assert result["inference_authorized"] is False
    assert result["comparative_efficacy_claim_permitted"] is False
