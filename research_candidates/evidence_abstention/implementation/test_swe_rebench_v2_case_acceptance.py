import copy
import json
import unittest
from pathlib import Path

from swe_rebench_v2_case_acceptance import validate_case_record, validate_registry
from swe_rebench_v2_contract import DATASET_FILE_REVISION, DATASET_FILE_SHA256, DATASET_ID

SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
SHA_D = "d" * 64
COMMIT_A = "1" * 40
COMMIT_B = "2" * 40


def artifact(label, digest=SHA_A):
    return {"artifact_uri": "https://example.org/" + label, "sha256": digest}


def reviewer(reviewer_id, label, digest=SHA_A, extra=None):
    result = {
        "reviewer_id": reviewer_id,
        "decision": "approved",
        "review_record": artifact(label, digest),
    }
    if extra:
        result.update(extra)
    return result


def valid_case():
    mechanisms = [
        {"mechanism_id": "CAUSE_A", "description": "Candidate mechanism A"},
        {"mechanism_id": "ALT_B", "description": "Candidate mechanism B"},
        {"mechanism_id": "ALT_C", "description": "Candidate mechanism C"},
    ]
    return {
        "case_id": "SRV2-CASE_001",
        "acceptance_state": "accepted_confirmatory",
        "dataset": {
            "dataset_id": DATASET_ID,
            "file_revision": DATASET_FILE_REVISION,
            "file_sha256": DATASET_FILE_SHA256,
            "cohort_role": "primary",
            "row_locator": {"field": "instance_id", "value": "example-instance-001"},
            "row_sha256": SHA_A,
        },
        "source": {
            "repository_full_name": "example/project",
            "issue_or_pr_url": "https://github.com/example/project/pull/12",
            "pull_request_number": 12,
            "base_commit_sha": COMMIT_A,
            "fixed_commit_sha": COMMIT_B,
            "changed_paths": ["src/module.py", "tests/test_module.py"],
            "patch": artifact("patch", SHA_A),
            "base_source_snapshot": artifact("base-snapshot", SHA_B),
            "fixed_source_snapshot": artifact("fixed-snapshot", SHA_C),
        },
        "independence": {
            "review_status": "passed",
            "is_independent": True,
            "upstream_project_id": "example/project",
            "defect_cluster_id": "example/project#12:mechanism-1",
            "same_or_related_case_ids": [],
            "review_record": artifact("independence", SHA_D),
        },
        "exposure": {
            "review_status": "passed",
            "confirmatory_analyst_id": "ANALYST_01",
            "confirmatory_analyst_saw_gold_or_fix": False,
            "prior_pipeline_debug_exposure_status": "none",
            "packet_preparer_id": "PACKET_PREPARER_01",
            "source_exposed_person_ids": ["TECH_01", "LEGAL_01", "PACKET_PREPARER_01", "PANEL_A_01", "PANEL_A_02", "EXTERNAL_AUDITOR_01"],
            "review_record": artifact("exposure"),
        },
        "license_review": {
            "source_license_expression": "MIT",
            "exact_base_license_review": "passed",
            "changed_file_license_review": "passed",
            "third_party_content_review": "passed",
            "research_use_decision": "approved",
            "reviewer_id": "LEGAL_01",
            "root_license_file": {
                "path": "LICENSE",
                "commit_sha": COMMIT_A,
                "blob_sha": "3" * 40,
                "content_sha256": SHA_A,
                "license_expression": "MIT",
            },
            "changed_file_license_manifest": artifact("changed-file-license-manifest", SHA_B),
            "review_record": artifact("license"),
        },
        "technical_reproduction": {
            "status": "passed",
            "environment_lock_sha256": SHA_D,
            "reviewer_id": "TECH_01",
            "buggy_baseline": {
                "commit_sha": COMMIT_A,
                "exit_code": 1,
                "test_selector": "tests/test_module.py::test_regression",
                "failure_is_targeted_regression": True,
                "failure_signature": "expected assertion failure in regression test",
                "run_record": artifact("buggy-run", SHA_A),
            },
            "fixed_revision": {
                "commit_sha": COMMIT_B,
                "exit_code": 0,
                "test_selector": "tests/test_module.py::test_regression",
                "same_test_passed": True,
                "run_record": artifact("fixed-run", SHA_B),
            },
            "review_record": artifact("technical-review", SHA_C),
        },
        "gold_standard": {
            "status": "approved",
            "agreement_status": "unanimous",
            "final_gold_mechanism_id": "CAUSE_A",
            "candidate_mechanisms": mechanisms,
            "panel_a_reviews": [
                reviewer("PANEL_A_01", "panel-a-1", SHA_A, {"gold_mechanism_id": "CAUSE_A"}),
                reviewer("PANEL_A_02", "panel-a-2", SHA_B, {"gold_mechanism_id": "CAUSE_A"}),
            ],
        },
        "evidence_tiers": {
            "status": "approved",
            "panel_b_blind_to_gold": True,
            "panel_b_blind_to_fix": True,
            "tier_labels_hidden_until_rating_lock": True,
            "rating_lock_before_gold_unblinding": True,
            "panel_b_reviews": [
                reviewer("PANEL_B_01", "panel-b-1", SHA_C),
                reviewer("PANEL_B_02", "panel-b-2", SHA_D),
            ],
            "final_tier_decisions": {
                "E1": {"surviving_mechanism_ids": ["CAUSE_A"], "locked_rating_record": artifact("e1", SHA_A)},
                "E2": {"surviving_mechanism_ids": ["CAUSE_A", "ALT_B"], "locked_rating_record": artifact("e2", SHA_B)},
                "E3": {"surviving_mechanism_ids": ["CAUSE_A", "ALT_B", "ALT_C"], "locked_rating_record": artifact("e3", SHA_C)},
            },
            "packet_set": artifact("packet-set", SHA_D),
            "panel_b_consensus_record": artifact("panel-b-consensus", SHA_A),
        },
        "external_audit": {
            "status": "passed",
            "auditor_id": "EXTERNAL_AUDITOR_01",
            "reviewed_after_panel_b_lock": True,
            "artifact_authenticity_review": "passed",
            "semantic_record_review": "passed",
            "license_and_reproduction_record_review": "passed",
            "review_record": artifact("external-audit", SHA_D),
        },
    }


def valid_registry():
    return {
        "registry_version": "0.1-draft",
        "study_protocol": "swe-rebench-v2-evidence-abstention",
        "status": "contains_cases_with_documented_external_audit_attestation",
        "accepted_case_count": 1,
        "accepted_project_count": 1,
        "records": [valid_case()],
    }


class SweRebenchV2CaseAcceptanceTests(unittest.TestCase):
    def test_empty_committed_registry_is_valid_and_remains_empty(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "SWE_REBENCH_V2_CASE_REGISTRY_V0_1.json").read_text(encoding="utf-8"))
        result = validate_registry(registry)
        self.assertEqual(result["status"], "valid_empty_registry")
        self.assertEqual(result["accepted_case_count"], 0)
        self.assertEqual(result["accepted_project_count"], 0)
        self.assertFalse(result["inference_authorized"])

    def test_committed_case_acceptance_schema_is_strict_and_parseable(self):
        root = Path(__file__).resolve().parents[1]
        schema = json.loads(
            (root / "SWE_REBENCH_V2_CASE_ACCEPTANCE_SCHEMA_V0_1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertIs(schema["additionalProperties"], False)
        self.assertIn("exposure", schema["required"])
        self.assertIn("prior_pipeline_debug_exposure_status", schema["properties"]["exposure"]["required"])

    def test_complete_synthetic_record_passes_only_structural_gate(self):
        result = validate_case_record(valid_case())
        self.assertEqual(
            result["status"],
            "structurally_complete_with_external_audit_attestation",
        )
        self.assertTrue(result["structural_only"])
        self.assertFalse(result["inference_authorized"])

    def test_external_audit_attestation_is_required_before_registry_acceptance(self):
        record = valid_case()
        del record["external_audit"]
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("external_audit" in item for item in result["blockers"]))

    def test_external_auditor_must_be_independent_and_source_exposure_logged(self):
        record = valid_case()
        record["external_audit"]["auditor_id"] = "PANEL_B_01"
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("external auditor must be separate" in item for item in result["blockers"]))

    def test_external_audit_must_follow_panel_b_rating_lock(self):
        record = valid_case()
        record["external_audit"]["reviewed_after_panel_b_lock"] = False
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("after Panel B ratings are locked" in item for item in result["blockers"]))
    def test_missing_exact_license_review_blocks_acceptance(self):
        record = valid_case()
        record["license_review"]["changed_file_license_review"] = "pending"
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("changed_file_license_review" in item for item in result["blockers"]))

    def test_root_license_must_be_pinned_to_exact_buggy_base(self):
        record = valid_case()
        record["license_review"]["root_license_file"]["commit_sha"] = COMMIT_B
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("exact buggy base commit" in item for item in result["blockers"]))

    def test_license_reviewer_must_be_in_source_exposure_list(self):
        record = valid_case()
        record["exposure"]["source_exposed_person_ids"].remove("LEGAL_01")
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("source_exposed_person_ids must include" in item for item in result["blockers"]))

    def test_buggy_baseline_must_fail_and_fixed_revision_must_pass(self):
        record = valid_case()
        record["technical_reproduction"]["buggy_baseline"]["exit_code"] = 0
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("buggy_baseline.exit_code" in item for item in result["blockers"]))

    def test_buggy_and_fixed_runs_must_use_same_targeted_regression(self):
        record = valid_case()
        record["technical_reproduction"]["fixed_revision"]["test_selector"] = "tests/test_other.py::test_other"
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("same test_selector" in item for item in result["blockers"]))

    def test_confirmatory_analyst_cannot_be_source_exposed_or_on_review_panels(self):
        record = valid_case()
        record["exposure"]["confirmatory_analyst_id"] = "PANEL_B_01"
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("confirmatory analyst" in item for item in result["blockers"]))

    def test_panel_a_and_panel_b_must_be_disjoint(self):
        record = valid_case()
        record["evidence_tiers"]["panel_b_reviews"][0]["reviewer_id"] = "PANEL_A_01"
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("Panel A and Panel B" in item for item in result["blockers"]))

    def test_prior_pipeline_debug_exposure_permanently_excludes_case(self):
        record = valid_case()
        record["exposure"]["prior_pipeline_debug_exposure_status"] = "present"
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("permanently excluded" in item for item in result["blockers"]))

    def test_source_exposed_person_cannot_join_panel_b(self):
        record = valid_case()
        record["exposure"]["source_exposed_person_ids"].append("PANEL_B_01")
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("no source-exposed person" in item for item in result["blockers"]))

    def test_panel_b_must_be_blind_to_gold_and_fix(self):
        record = valid_case()
        record["evidence_tiers"]["panel_b_blind_to_gold"] = False
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("panel_b_blind_to_gold" in item for item in result["blockers"]))

    def test_evidence_tiers_must_have_correct_nested_survivor_sets(self):
        record = valid_case()
        record["evidence_tiers"]["final_tier_decisions"]["E2"]["surviving_mechanism_ids"] = ["CAUSE_A"]
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("E2 must retain" in item or "nested" in item for item in result["blockers"]))

    def test_gold_cause_must_be_the_only_e1_survivor(self):
        record = valid_case()
        record["evidence_tiers"]["final_tier_decisions"]["E1"]["surviving_mechanism_ids"] = ["ALT_B"]
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("E1 must leave only" in item for item in result["blockers"]))

    def test_registry_rejects_count_mismatch_and_duplicate_project(self):
        registry = valid_registry()
        registry["accepted_case_count"] = 1
        registry["records"].append(copy.deepcopy(registry["records"][0]))
        result = validate_registry(registry)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("accepted_case_count" in item for item in result["blockers"]))
        self.assertTrue(any("upstream_project_id values must be unique" in item for item in result["blockers"]))

    def test_record_cannot_enter_registry_without_confirmatory_acceptance_state(self):
        record = valid_case()
        record["acceptance_state"] = "candidate"
        result = validate_case_record(record)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("acceptance_state" in item for item in result["blockers"]))


if __name__ == "__main__":
    unittest.main()
