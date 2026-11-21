import copy
import hashlib
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


def test_v02_accepted_registry_is_valid_but_does_not_authorize_inference():
    registry = json.loads((RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json").read_text())
    result = validate_registry(registry)
    assert result["status"] == "structurally_valid_candidate_registry"
    assert result["accepted_case_count"] == 2
    assert result["accepted_project_count"] == 2
    assert result["minimum_feasibility_count_met"] is True
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



def test_registry_fails_closed_on_non_object_record_without_crashing():
    registry = json.loads((RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json").read_text())
    registry["records"] = [None]
    registry["accepted_case_count"] = 1
    registry["accepted_project_count"] = 0
    registry["status"] = "contains_structurally_complete_candidates"
    result = validate_registry(registry)
    assert result["status"] == "invalid"
    assert any("registry record must be an object" in item for item in result["blockers"])

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


def test_dishka_real_accepted_case_is_structurally_complete_and_not_inference_authorized():
    case_path = (
        RESEARCH
        / "reproduction"
        / "dishka_issue_435"
        / "SWE_REBENCH_V2_DISHKA_435_CASE_ACCEPTANCE_PROPOSED_V0_2.json"
    )
    record = json.loads(case_path.read_text(encoding="utf-8"))

    result = validate_case_record(record)

    assert result["status"] == "structurally_complete_candidate", result["blockers"]
    assert result["case_id"] == "SRV2E-DISHKA_435"
    assert result["acceptance_decision"] == "accepted"
    assert result["eligible_for_registry"] is True
    assert result["inference_authorized"] is False
    assert record["final_acceptance"]["status"] == "approved"
    assert record["final_acceptance"]["decision_timestamp_utc"] == "2026-11-20T10:59:00Z"
    assert record["final_acceptance"]["decision_record"]["sha256"] == "57d309d5ab02164612eda6f7e950673f9a1d505aa4f223504551caee7f946b80"
    assert record["exposure"]["prior_pipeline_debug_exposure"] == "none"
    assert record["exposure"]["researcher_source_exposure"] == "full"
    assert record["license_review"]["scope_limitation"] == "documentary_screening_only_not_legal_advice"
    assert record["evidence_tiers"]["E1"]["surviving_mechanism_ids"] == [
        "G1_STALE_PER_SCOPE_FACTORY_REGISTRATION"
    ]
    assert len(record["evidence_tiers"]["E1"]["evidence_items"]) == 13
    assert len(record["evidence_tiers"]["E2"]["evidence_items"]) == 9
    assert len(record["evidence_tiers"]["E3"]["evidence_items"]) == 7


def test_dishka_accepted_case_is_in_the_v02_registry():
    case_path = (
        RESEARCH
        / "reproduction"
        / "dishka_issue_435"
        / "SWE_REBENCH_V2_DISHKA_435_CASE_ACCEPTANCE_PROPOSED_V0_2.json"
    )
    proposed = json.loads(case_path.read_text(encoding="utf-8"))
    registry = json.loads(
        (RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json").read_text(encoding="utf-8")
    )

    assert proposed["acceptance_decision"] == "accepted"
    assert len(registry["records"]) == 2
    result = validate_registry(registry)
    assert result["status"] == "structurally_valid_candidate_registry", result["blockers"]
    assert result["accepted_case_count"] == 2
    assert result["accepted_project_count"] == 2
    assert result["minimum_feasibility_count_met"] is True
    assert result["primary_target_met"] is False
    assert result["inference_authorized"] is False



def test_dishka_accepted_case_document_hash_references_match_current_files():
    case_path = (
        RESEARCH
        / "reproduction"
        / "dishka_issue_435"
        / "SWE_REBENCH_V2_DISHKA_435_CASE_ACCEPTANCE_PROPOSED_V0_2.json"
    )
    record = json.loads(case_path.read_text(encoding="utf-8"))

    references = [
        (
            record["dataset"]["timestamp_review_record"],
            RESEARCH / "reproduction" / "dishka_issue_435" / "DISHKA_435_POST_RUN_PROVENANCE_CORRECTION_V0_1_2026-11-16.md",
        ),
        (
            record["independence"]["review_record"],
            RESEARCH / "reproduction" / "dishka_issue_435" / "DISHKA_435_CASE_ACCEPTANCE_READINESS_2026-11-18.md",
        ),
        (
            record["exposure"]["review_record"],
            RESEARCH / "reproduction" / "dishka_issue_435" / "PROJECT_LEAD_EXPOSURE_DECISION_2026-11-19.md",
        ),
        (
            record["license_review"]["review_record"],
            RESEARCH / "reproduction" / "dishka_issue_435" / "PROJECT_LEAD_LICENSE_SCOPE_DECISION_2026-11-19.md",
        ),
        (
            record["license_review"]["changed_file_license_manifest"],
            RESEARCH / "REAGENTO_DISHKA_436_CHANGED_FILE_LICENSE_MANIFEST_V0_1.json",
        ),
        (
            record["technical_reproduction"]["review_record"],
            RESEARCH / "reproduction" / "dishka_issue_435" / "DISHKA_435_STAGE2_STAGE3_GATE_REVIEW_V0_1_2026-11-16.md",
        ),
        (
            record["gold_standard"]["review_record"],
            RESEARCH / "reproduction" / "dishka_issue_435" / "HUMAN_ADJUDICATION_DECISION_DISHKA_435_V0_1_DRAFT_2026-11-16.md",
        ),
        (
            record["evidence_tiers"]["tier_decision_record"],
            RESEARCH / "reproduction" / "dishka_issue_435" / "HUMAN_ADJUDICATION_DECISION_DISHKA_435_V0_1_DRAFT_2026-11-16.md",
        ),
        (
            record["evidence_tiers"]["E1"]["packet"],
            RESEARCH / "reproduction" / "dishka_issue_435" / "E1_PACKET_MANIFEST_V0_1.json",
        ),
        (
            record["evidence_tiers"]["E2"]["packet"],
            RESEARCH / "reproduction" / "dishka_issue_435" / "E2_PACKET_MANIFEST_V0_1.json",
        ),
        (
            record["evidence_tiers"]["E3"]["packet"],
            RESEARCH / "reproduction" / "dishka_issue_435" / "E3_PACKET_MANIFEST_V0_1.json",
        ),
    ]

    pinned_commit = "1a87e6ce4b468cadff75b366b012b994803abae0"
    for artifact_ref, source_path in references:
        actual_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest()
        relative_path = str(source_path.relative_to(ROOT)).replace("\\", "/")
        assert actual_sha256 == artifact_ref["sha256"], (
            f"Stale SHA-256 reference for {relative_path}: "
            f"record has {artifact_ref['sha256']}, file has {actual_sha256}"
        )
        assert f"/blob/{pinned_commit}/" in artifact_ref["uri"], (
            f"Evidence URI is not pinned to the reviewed commit: {artifact_ref['uri']}"
        )
        assert artifact_ref["uri"].endswith("/" + relative_path), (
            f"Evidence URI points to a different file than the hashed record: {artifact_ref['uri']}"
        )


def test_dishka_patch_and_reproduction_artifact_references_are_pinned():
    case_path = (
        RESEARCH
        / "reproduction"
        / "dishka_issue_435"
        / "SWE_REBENCH_V2_DISHKA_435_CASE_ACCEPTANCE_PROPOSED_V0_2.json"
    )
    record = json.loads(case_path.read_text(encoding="utf-8"))

    assert record["source"]["patch"] == {
        "uri": (
            "https://github.com/MahmutVezir/dijitalikiz/actions/runs/"
            "44602442485/artifacts/14569001619#path=full-pr.diff"
        ),
        "sha256": "c5a6e5edc41d5a321fb95dc0bdb81ee449870eb53278a5d91582c2478395efde",
    }
    latest_artifact = {
        "uri": "https://github.com/MahmutVezir/dijitalikiz/actions/runs/44602442485/artifacts/14569001619",
        "sha256": "064e8aec01eaccb30849bfb7535e856c721db628c983d2207f7f0efec136419e",
    }
    assert record["technical_reproduction"]["buggy_baseline"]["run_record"] == latest_artifact
    assert record["technical_reproduction"]["fixed_revision"]["run_record"] == latest_artifact

def test_dishka_final_decision_artifacts_are_hashed_and_inference_remains_disabled():
    case_path = RESEARCH / "reproduction" / "dishka_issue_435" / "SWE_REBENCH_V2_DISHKA_435_CASE_ACCEPTANCE_PROPOSED_V0_2.json"
    record = json.loads(case_path.read_text(encoding="utf-8"))
    for ref in (record["human_decision"]["ai_critique_record"], record["final_acceptance"]["decision_record"]):
        relative = ref["uri"].split("/blob/research/2026-11-16-followup-evidence-validation/", 1)[1]
        content = (ROOT / relative).read_bytes()
        assert hashlib.sha256(content).hexdigest() == ref["sha256"]
    registry = json.loads((RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json").read_text())
    result = validate_registry(registry)
    assert result["status"] == "structurally_valid_candidate_registry", result["blockers"]
    assert result["accepted_case_count"] == 2
    assert result["accepted_project_count"] == 2
    assert result["inference_authorized"] is False


def test_dymos_proposed_case_record_is_structurally_complete_without_acceptance_or_inference():
    case_path = (
        RESEARCH
        / "dymos_1166"
        / "SWE_REBENCH_V2_DYMOS_1166_CASE_RECORD_PROPOSED_V0_1_2026-11-20.json"
    )
    record = json.loads(case_path.read_text(encoding="utf-8"))

    result = validate_case_record(record)

    assert result["status"] == "structurally_complete_candidate", result["blockers"]
    assert result["case_id"] == "SRV2E-DYMOS_1166"
    assert result["acceptance_decision"] == "proposed"
    assert result["eligible_for_registry"] is False
    assert result["inference_authorized"] is False
    assert record["final_acceptance"]["status"] == "pending"
    assert record["final_acceptance"]["decision_timestamp_utc"] is None
    assert record["final_acceptance"]["decision_record"] is None
    assert record["evidence_tiers"]["E1"]["surviving_mechanism_ids"] == [
        "G1_POLYNOMIAL_CONTROL_INPUT_DEFAULT_DISCARDED"
    ]
    assert set(record["evidence_tiers"]["E2"]["surviving_mechanism_ids"]) == {
        "G1_POLYNOMIAL_CONTROL_INPUT_DEFAULT_DISCARDED",
        "A1_POLYNOMIAL_VALUE_SHAPE_NORMALIZATION",
    }
    assert len(record["evidence_tiers"]["E1"]["evidence_items"]) == 7
    assert len(record["evidence_tiers"]["E2"]["evidence_items"]) == 3
    assert len(record["evidence_tiers"]["E3"]["evidence_items"]) == 1


def test_dymos_real_proposed_case_is_structurally_complete_but_not_accepted():
    case_path = (
        RESEARCH
        / "dymos_1166"
        / "SWE_REBENCH_V2_DYMOS_1166_CASE_RECORD_PROPOSED_V0_1_2026-11-20.json"
    )
    record = json.loads(case_path.read_text(encoding="utf-8"))

    result = validate_case_record(record)

    assert result["status"] == "structurally_complete_candidate", result["blockers"]
    assert result["case_id"] == "SRV2E-DYMOS_1166"
    assert result["acceptance_decision"] == "proposed"
    assert result["eligible_for_registry"] is False
    assert result["inference_authorized"] is False
    assert record["final_acceptance"]["status"] == "pending"
    assert record["final_acceptance"]["decision_timestamp_utc"] is None
    assert record["final_acceptance"]["decision_record"] is None
    assert record["exposure"]["prior_pipeline_debug_exposure"] == "none"
    assert record["exposure"]["researcher_source_exposure"] == "full"
    assert record["gold_standard"]["gold_mechanism_id"] == "G1_POLYNOMIAL_CONTROL_INPUT_DEFAULT_DISCARDED"
    assert record["evidence_tiers"]["E3"]["surviving_mechanism_ids"] == [
        "G1_POLYNOMIAL_CONTROL_INPUT_DEFAULT_DISCARDED",
        "A1_POLYNOMIAL_VALUE_SHAPE_NORMALIZATION",
        "A2_STALE_TEST_SETUP_VALUE_OVERRIDE",
        "A3_ODE_TARGET_UNITS_OR_STATE_CONFIGURATION",
    ]
    assert record["evidence_tiers"]["E2"]["surviving_mechanism_ids"] == [
        "G1_POLYNOMIAL_CONTROL_INPUT_DEFAULT_DISCARDED",
        "A1_POLYNOMIAL_VALUE_SHAPE_NORMALIZATION",
    ]
    assert record["evidence_tiers"]["E1"]["surviving_mechanism_ids"] == [
        "G1_POLYNOMIAL_CONTROL_INPUT_DEFAULT_DISCARDED"
    ]
    assert [
        len(record["evidence_tiers"][level]["evidence_items"])
        for level in ("E3", "E2", "E1")
    ] == [1, 3, 7]

    license_review_path = (
        RESEARCH / "dymos_1166"
        / "DYMOS_1166_DEPENDENCY_LICENSE_SCOPE_REVIEW_V0_1_2026-11-20.json"
    )
    license_review = json.loads(license_review_path.read_text(encoding="utf-8"))
    assert license_review["human_review"]["project_lead_scope_acknowledgement"] == (
        "acknowledged_with_scientific_independence_condition"
    )
    assert license_review["human_review"]["accepted_as_legal_clearance"] is False
    assert license_review["human_review"]["external_legal_review"] == "not_performed"
    assert license_review["dataset"]["revision"] == "fb9aa226b2ce37c708ea7732e7b980abacdadb67"
    assert license_review["dataset"]["pinned_card_verification"]["license_displayed_at_exact_revision"] == "CC-BY-4.0"

    pinned_commit = "9b2036cf455e50ac5668c72870b3ed1822ad397a"
    references = [
        (
            record["dataset"]["timestamp_review_record"],
            RESEARCH / "dymos_1166" / "DYMOS_1166_ISSUE_FAMILY_INDEPENDENCE_REVIEW_V0_1_2026-11-20.json",
        ),
        (
            record["independence"]["review_record"],
            RESEARCH / "dymos_1166" / "DYMOS_1166_ISSUE_FAMILY_INDEPENDENCE_REVIEW_V0_1_2026-11-20.json",
        ),
        (
            record["exposure"]["review_record"],
            RESEARCH / "dymos_1166" / "PROJECT_LEAD_EXPOSURE_DECISION_DYMOS_1166_2026-11-20.md",
        ),
        (
            record["license_review"]["review_record"],
            license_review_path,
        ),
        (
            record["license_review"]["changed_file_license_manifest"],
            RESEARCH / "dymos_1166" / "DYMOS_1166_CHANGED_FILE_LICENSE_MANIFEST_V0_1_2026-11-20.json",
        ),
        (
            record["technical_reproduction"]["review_record"],
            RESEARCH / "dymos_1166" / "EVIDENCE_PACKET_PROVENANCE_PROPOSED_V0_1_2026-11-20.json",
        ),
        (
            record["gold_standard"]["review_record"],
            RESEARCH / "dymos_1166" / "PROJECT_LEAD_GOLD_AND_EVIDENCE_TIERS_DECISION_DYMOS_1166_2026-11-20.md",
        ),
        (
            record["evidence_tiers"]["tier_decision_record"],
            RESEARCH / "dymos_1166" / "PROJECT_LEAD_GOLD_AND_EVIDENCE_TIERS_DECISION_DYMOS_1166_2026-11-20.md",
        ),
        (
            record["human_decision"]["ai_critique_record"],
            RESEARCH / "dymos_1166" / "DYMOS_1166_AI_ADVISORY_STRUCTURAL_CASE_REVIEW_2026-11-20.md",
        ),
    ]
    for artifact_ref, source_path in references:
        relative_path = str(source_path.relative_to(ROOT)).replace("\\\\", "/")
        actual_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest()
        assert actual_sha256 == artifact_ref["sha256"], relative_path
        assert f"/blob/{pinned_commit}/" in artifact_ref["uri"], artifact_ref["uri"]
        assert artifact_ref["uri"].split("#", 1)[0].endswith("/" + relative_path)

    packet_uri = record["evidence_tiers"]["E1"]["packet"]["uri"]
    assert f"/blob/{pinned_commit}/" in packet_uri
    assert packet_uri.split("#", 1)[0].endswith(
        "/research_candidates/evidence_abstention/dymos_1166/"
        "OPERATIONAL_EVIDENCE_PACKET_SET_PROPOSED_V0_1_2026-11-20.json"
    )

    registry = json.loads(
        (RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json").read_text(
            encoding="utf-8"
        )
    )
    registry_result = validate_registry(registry)
    assert registry_result["status"] == "structurally_valid_candidate_registry"
    assert registry_result["accepted_case_count"] == 2
    assert registry_result["accepted_project_count"] == 2
    assert "SRV2E-DYMOS_1166" not in {item["case_id"] for item in registry["records"]}
    assert registry_result["inference_authorized"] is False

def test_meltano_3090_stage3_project_lead_gold_tier_approved_but_case_gates_remain_fail_closed():
    candidate_dir = RESEARCH / "meltano_3090"
    gold_proposal = (
        candidate_dir
        / "MELTANO_3090_SOURCE_AWARE_GOLD_AND_EVIDENCE_TIERS_PROPOSAL_2026-11-21.md"
    ).read_text(encoding="utf-8")
    integrity_review = (
        candidate_dir
        / "MELTANO_3090_STAGE2_ARTIFACT_INTEGRITY_REVIEW_2026-11-21.md"
    ).read_text(encoding="utf-8")
    independence = json.loads(
        (
            candidate_dir
            / "MELTANO_3090_ISSUE_FAMILY_INDEPENDENCE_REVIEW_V0_1_2026-11-21.json"
        ).read_text(encoding="utf-8")
    )
    license_review = json.loads(
        (
            candidate_dir
            / "MELTANO_3090_DEPENDENCY_LICENSE_SCOPE_REVIEW_V0_1_2026-11-21.json"
        ).read_text(encoding="utf-8")
    )

    assert "PROJECT-LEAD APPROVED" in gold_proposal
    assert "E3" in gold_proposal and "ABSTAIN" in gold_proposal
    assert "E2" in gold_proposal and "ABSTAIN" in gold_proposal
    assert "E1" in gold_proposal and "ANSWER" in gold_proposal
    assert "project lead explicitly declared `prior_pipeline_debug_exposure = none`" in gold_proposal
    exposure_record = (
        candidate_dir / "PROJECT_LEAD_EXPOSURE_DECISION_MELTANO_3090_2026-11-21.md"
    ).read_text(encoding="utf-8")
    assert "**Declared value:** `none`" in exposure_record
    assert "`researcher_source_exposure = full`" in exposure_record
    assert "not an independently witnessed audit" in exposure_record
    decision_record = (candidate_dir / "PROJECT_LEAD_GOLD_AND_EVIDENCE_TIER_DECISION_MELTANO_3090_2026-11-21.md").read_text(encoding="utf-8")
    assert "E3 — ABSTAIN" in decision_record
    assert "E2 — ABSTAIN" in decision_record
    assert "E1 — ANSWER" in decision_record
    assert "does **not** accept Meltano into the v0.2 exploratory registry" in decision_record
    assert "14/14 files matched" in integrity_review
    assert "14/14" in integrity_review

    assert independence["candidate"]["case_id"] == "SRV2E-MELTANO_3090"
    assert independence["project_lead_selection"]["decision"] == (
        "ACCEPTED_FOR_STAGE3_CASE_EVALUATION"
    )
    assert independence["independence_disposition"]["one_case_per_repository_rule_preserved"] is True
    assert independence["exposure"]["prior_pipeline_debug_exposure"] == "none"
    assert independence["exposure"]["researcher_source_exposure"] == "full"
    assert independence["exposure"]["blind_adjudication_claimed"] is False
    assert independence["boundaries"]["prior_pipeline_debug_exposure_gate"] == "closed_on_project_lead_self_report"
    progress_ledger = json.loads(
        (
            RESEARCH
            / "SWE_REBENCH_V2_STAGE2_STAGE3_PROGRESS_LEDGER_V0_1_2026-11-16.json"
        ).read_text(encoding="utf-8")
    )
    assert progress_ledger["meltano_3090_exposure_declaration"]["decision"] == "none"
    assert progress_ledger["meltano_3090_exposure_declaration"]["researcher_source_exposure"] == "full"
    assert progress_ledger["meltano_3090_exposure_declaration"]["gate_status"] == "closed"
    scope_ledger = progress_ledger["meltano_3090_license_scope_acknowledgement"]
    assert scope_ledger["decision"] == "acknowledged_bounded_research_scope_in_principle_with_open_verification_gates"
    assert scope_ledger["legal_clearance"] is False
    assert scope_ledger["redistribution_authorized"] is False
    assert scope_ledger["final_case_acceptance"] == "not_accepted"
    assert scope_ledger["accepted_case_count_unchanged"] == 2
    assert independence["boundaries"]["final_case_acceptance"] == "not_accepted"
    assert independence["boundaries"]["registry_inclusion"] is False
    assert independence["boundaries"]["inference_authorized"] is False

    assert license_review["human_review"]["project_lead_scope_acknowledgement"] == (
        "acknowledged_in_principle_with_explicit_conditions"
    )
    assert license_review["human_review"]["bounded_research_scope_acknowledged_in_principle"] is True
    assert license_review["human_review"]["accepted_research_scope"] is False
    assert license_review["human_review"]["nested_dependency_review"] == "open"
    assert license_review["human_review"]["notice_and_provenance_review"] == "open"
    assert license_review["human_review"]["research_use_decision"].startswith(
        "bounded_scope_acknowledged_in_principle;"
    )
    assert license_review["dataset_scope"]["exact_pinned_card_review"].startswith("pending;")
    assert license_review["boundaries"]["legal_clearance"] is False
    assert license_review["boundaries"]["redistribution_authorized"] is False
    assert license_review["boundaries"]["final_case_acceptance"] is False
    assert license_review["boundaries"]["inference_authorized"] is False

    scope_decision = (
        candidate_dir
        / "PROJECT_LEAD_BOUNDED_RESEARCH_SCOPE_ACKNOWLEDGEMENT_MELTANO_3090_2026-11-21.md"
    ).read_text(encoding="utf-8")
    assert "bounded_research_scope_acknowledged_in_principle_with_open_verification_gates" in scope_decision
    assert "This is not legal advice" in scope_decision
    assert "complete Meltano repository or complete dataset" in scope_decision

    registry = json.loads(
        (RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json").read_text(
            encoding="utf-8"
        )
    )
    registry_result = validate_registry(registry)
    assert registry_result["status"] == "structurally_valid_candidate_registry"
    assert registry_result["accepted_case_count"] == 2
    assert registry_result["accepted_project_count"] == 2
    assert "SRV2E-MELTANO_3090" not in {item["case_id"] for item in registry["records"]}
    assert registry_result["inference_authorized"] is False


def test_pyfar_721_gold_tier_approved_but_case_acceptance_remains_pending_and_fail_closed():
    candidate_dir = RESEARCH / "pyfar_721"
    proposal_path = candidate_dir / "PYFAR_721_SOURCE_AWARE_GOLD_AND_EVIDENCE_TIERS_PROPOSAL_2026-11-21.md"
    independence_path = candidate_dir / "PYFAR_721_ISSUE_FAMILY_INDEPENDENCE_REVIEW_V0_1_2026-11-21.json"
    license_path = candidate_dir / "PYFAR_721_DEPENDENCY_LICENSE_SCOPE_REVIEW_V0_1_2026-11-21.json"
    integrity_path = candidate_dir / "PYFAR_721_STAGE2_ARTIFACT_INTEGRITY_REVIEW_2026-11-21.md"
    gold_decision_path = candidate_dir / "PROJECT_LEAD_GOLD_TIER_DECISION_PYFAR_721_2026-11-21.md"

    proposal = proposal_path.read_text(encoding="utf-8")
    gold_decision = gold_decision_path.read_text(encoding="utf-8")
    independence = json.loads(independence_path.read_text(encoding="utf-8"))
    license_review = json.loads(license_path.read_text(encoding="utf-8"))
    integrity = integrity_path.read_text(encoding="utf-8")
    ledger = json.loads(
        (RESEARCH / "SWE_REBENCH_V2_STAGE2_STAGE3_PROGRESS_LEDGER_V0_1_2026-11-16.json").read_text(
            encoding="utf-8"
        )
    )
    pyfar = next(item for item in ledger["records"] if item["repository"] == "pyfar/pyfar")

    assert "G1 GOLD MECHANISM AND E3/E2/E1 OUTCOMES PROJECT-LEAD APPROVED" in proposal
    assert "E3 ABSTAIN, E2 ABSTAIN, E1 ANSWER" in proposal
    assert "GOLD MECHANISM AND EVIDENCE-TIER DECISIONS APPROVED; CASE NOT ACCEPTED" in gold_decision
    assert "ENERGY_POWER_TARGET_AND_REFERENCE_NOT_SQUARE_ROOTED" in gold_decision
    assert "not a separately authored issue-level reproducer" in proposal
    assert "14/14" in integrity
    assert "23/23" in integrity
    assert independence["candidate"]["case_id"] == "SRV2E-PYFAR_721"
    assert independence["independence_disposition"]["exact_duplicate_found"] is False
    assert independence["exposure"]["prior_pipeline_debug_exposure"] == "none"
    assert independence["exposure"]["researcher_source_exposure"] == (
        "full_for_issue_PR_exact_base_source_and_stage2_outputs"
    )
    assert independence["exposure"]["prior_pipeline_debug_exposure_gate"] == (
        "closed_on_project_lead_self_report"
    )
    assert independence["exposure"]["evidence_class"] == (
        "direct_project_lead_self_report_in_conversation"
    )
    assert independence["exposure"]["decision_record_path"] == (
        "research_candidates/evidence_abstention/pyfar_721/"
        "PROJECT_LEAD_EXPOSURE_DECISION_PYFAR_721_2026-11-21.md"
    )
    assert independence["exposure"]["independent_witnessed_or_audited"] is False
    assert independence["exposure"]["blind_adjudication_claimed"] is False
    assert independence["exposure"]["inter_rater_claimed"] is False
    assert independence["boundaries"]["final_case_acceptance"] == "not_accepted"
    assert independence["boundaries"]["registry_inclusion"] is False
    assert license_review["human_review"]["project_lead_scope_acknowledgement"] == "pending"
    assert license_review["human_review"]["nested_dependency_review"] == "open"
    assert license_review["human_review"]["native_component_and_notice_review"] == "open"
    assert license_review["human_review"]["exact_pinned_dataset_card_review"] == "open"
    assert license_review["human_review"]["accepted_as_legal_clearance"] is False
    assert license_review["boundaries"]["legal_clearance"] is False
    assert license_review["boundaries"]["redistribution_authorized"] is False
    assert license_review["boundaries"]["final_case_acceptance"] is False
    assert license_review["boundaries"]["inference_authorized"] is False
    assert pyfar["stage2_artifact_local_integrity"]["buggy_base_expected_failures"] == "23/23"
    assert pyfar["stage2_artifact_local_integrity"]["fixed_revision_passes"] == "23/23"
    assert pyfar["stage3_proposed_tiers"]["tier_decision_status"] == (
        "project_lead_approved_2026_11_21"
    )
    assert pyfar["stage3_project_lead_gold_tier_decision"]["decision"] == "approved"
    assert pyfar["stage3_project_lead_gold_tier_decision"]["approved_gold"] == (
        "ENERGY_POWER_TARGET_AND_REFERENCE_NOT_SQUARE_ROOTED"
    )
    assert pyfar["stage3_project_lead_gold_tier_decision"]["approved_tiers"] == {
        "E3": "ABSTAIN", "E2": "ABSTAIN", "E1": "ANSWER"
    }
    assert ledger["pyfar_721_gold_tier_decision"]["decision"] == "approved"
    assert pyfar["final_case_acceptance"] == "not_accepted"
    assert pyfar["model_inference_authorized"] is False
    assert ledger["summary"]["accepted_exploratory_cases"] == 2
    assert ledger["summary"]["accepted_exploratory_projects"] == 2

    registry = json.loads(
        (RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json").read_text(
            encoding="utf-8"
        )
    )
    registry_result = validate_registry(registry)
    assert registry_result["status"] == "structurally_valid_candidate_registry"
    assert registry_result["accepted_case_count"] == 2
    assert registry_result["accepted_project_count"] == 2
    assert "SRV2E-PYFAR_721" not in {item["case_id"] for item in registry["records"]}
    assert registry_result["inference_authorized"] is False
