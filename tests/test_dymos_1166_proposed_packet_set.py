import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "research_candidates" / "evidence_abstention" / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))
SPEC = importlib.util.spec_from_file_location(
    "evidence_level_packet_set",
    IMPLEMENTATION / "evidence_level_packet_set.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

DYMOS = ROOT / "research_candidates" / "evidence_abstention" / "dymos_1166"
PACKET_PATH = DYMOS / "OPERATIONAL_EVIDENCE_PACKET_SET_PROPOSED_V0_1_2026-11-20.json"
PROVENANCE_PATH = DYMOS / "EVIDENCE_PACKET_PROVENANCE_PROPOSED_V0_1_2026-11-20.json"
LICENSE_PATH = DYMOS / "DYMOS_1166_DEPENDENCY_LICENSE_SCOPE_REVIEW_V0_1_2026-11-20.json"
INDEPENDENCE_PATH = DYMOS / "DYMOS_1166_ISSUE_FAMILY_INDEPENDENCE_REVIEW_V0_1_2026-11-20.json"
EXPOSURE_PATH = DYMOS / "PROJECT_LEAD_EXPOSURE_DECISION_DYMOS_1166_2026-11-20.md"
EXPOSURE_SHA256 = "3d38e3b45f2d27cc6531ede3d73d8f2439deee0b6970c6d4618d4e02e55733ea"
DECISION_PATH = DYMOS / "PROJECT_LEAD_GOLD_AND_EVIDENCE_TIERS_DECISION_DYMOS_1166_2026-11-20.md"
DECISION_SHA256 = "9ae99f74020479bdfc7d7b686b7dd7d7b3ca5afa24c827b08e4cc5108ccfd392"
SCOPE_PROPOSAL_PATH = DYMOS / "PROJECT_LEAD_BOUNDED_LICENSE_SCOPE_ACKNOWLEDGEMENT_PROPOSAL_DYMOS_1166_2026-11-20.md"
SCOPE_PROPOSAL_SHA256 = "e8185465d8466512d3de08e622115a9442450f5665fbde4857facddc76341405"
LEDGER_PATH = ROOT / "research_candidates" / "evidence_abstention" / "SWE_REBENCH_V2_STAGE2_STAGE3_PROGRESS_LEDGER_V0_1_2026-11-16.json"


class Dymos1166ProposedPacketSetTests(unittest.TestCase):
    def test_packet_set_is_hash_valid_strictly_nested_and_semantics_unassessed(self):
        packet_set = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        result = MODULE.validate_packet_set(packet_set)
        self.assertEqual(result["status"], "valid", result["blockers"])
        self.assertTrue(result["strictly_nested"])
        self.assertEqual(
            {level: len(packet_set["packets"][level]["evidence_items"]) for level in ("E1", "E2", "E3")},
            {"E1": 7, "E2": 3, "E3": 1},
        )
        self.assertEqual(
            result["additional_evidence_ids"]["E1_over_E2"],
            [
                "DYMOS_BASE_ADD_CONTROL_FORWARDS_VALUE",
                "DYMOS_BASE_ONES_INPUT_DEFAULT",
                "DYMOS_BASE_PHASE_STORES_CONTROL_VALUE",
                "DYMOS_BASE_TRANSCRIPTION_PASSES_CONTROL_OPTIONS",
            ],
        )
        self.assertFalse(result["semantic_sufficiency_assessed"])
        self.assertFalse(result["model_inference_performed"])

    def test_e1_uses_active_api_to_component_source_chain(self):
        packet_set = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
        items = {item["id"]: item for item in packet_set["packets"]["E1"]["evidence_items"]}
        source_records = {item["id"]: item for item in provenance["evidence_items"]}

        phase_id = "DYMOS_BASE_PHASE_STORES_CONTROL_VALUE"
        trans_id = "DYMOS_BASE_TRANSCRIPTION_PASSES_CONTROL_OPTIONS"
        ones_id = "DYMOS_BASE_ONES_INPUT_DEFAULT"
        api_id = "DYMOS_BASE_ADD_CONTROL_FORWARDS_VALUE"
        self.assertIn("self.set_control_options(name", items[api_id]["content"])
        self.assertIn("val=val", items[api_id]["content"])
        self.assertIn("self.control_options[name]['val'] = val", items[phase_id]["content"])
        self.assertEqual(source_records[api_id]["source_path"], "dymos/phase/phase.py")
        self.assertEqual(source_records[api_id]["source_lines_1based"], [638, 640])
        self.assertIn("ControlInterpComp(control_options=phase.control_options", items[trans_id]["content"])
        self.assertIn("if options['control_type'] == 'polynomial':", items[ones_id]["content"])
        self.assertIn("val=np.ones(input_shape)", items[ones_id]["content"])
        self.assertEqual(source_records[ones_id]["source_lines_1based"], [95, 120])
        self.assertEqual(source_records[phase_id]["source_path"], "dymos/phase/phase.py")
        self.assertEqual(source_records[phase_id]["source_lines_1based"], [785, 786])
        self.assertEqual(source_records[trans_id]["source_path"], "dymos/transcriptions/transcription_base.py")
        self.assertEqual(source_records[trans_id]["source_lines_1based"], [145, 147])
        self.assertEqual(source_records[phase_id]["source_commit"], "3efd1035c3bf62890034eb9e07de543f3d117867")
        self.assertEqual(source_records[trans_id]["source_commit"], "3efd1035c3bf62890034eb9e07de543f3d117867")
        self.assertNotIn("DYMOS_BASE_COMMENTED_VAL_NORMALIZATION", items)
        self.assertNotIn("DYMOS_BASE_COMMENTED_INPUT_DEFAULT", items)

    def test_packet_provenance_matches_external_packet_hash_and_gold_tier_decision_is_approved(self):
        packet_set = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(provenance["packet_set_sha256"], packet_set["packet_set_sha256"])
        self.assertEqual(
            provenance["packet_set_path"],
            str(PACKET_PATH.relative_to(ROOT)),
        )
        self.assertEqual(
            provenance["semantic_review"]["status"],
            "approved_source_aware_project_lead_gold_and_tier_decision",
        )
        self.assertTrue(provenance["semantic_review"]["adjudication_completed"])
        self.assertEqual(provenance["semantic_review"]["project_lead_decision"]["decision"], "APPROVED")
        self.assertFalse(provenance["structural_validation"]["semantic_sufficiency_assessed"])
        self.assertFalse(provenance["structural_validation"]["model_inference_performed"])

    def test_stage2_and_independent_reproducer_artifacts_are_recorded_without_inference(self):
        provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
        stage2 = provenance["reproduction_evidence"]["dataset_selector"]
        independent = provenance["reproduction_evidence"]["independent_public_api_reproducer"]
        self.assertEqual(stage2["artifact_id"], 14341424466)
        self.assertEqual(stage2["archive_integrity"]["internal_sha256_entries"], "18/18 PASS")
        self.assertIn("failed", stage2["base_result"])
        self.assertIn("passed", stage2["fixed_result"])
        self.assertEqual(independent["artifact_id"], 14629598269)
        self.assertEqual(independent["archive_integrity"]["internal_sha256_entries"], "15/15 PASS")
        self.assertIn("expected", independent["base_result"])
        self.assertIn("passed", independent["fixed_result"])
        self.assertFalse(provenance["structural_validation"]["model_inference_performed"])

    def test_license_inventory_is_documented_but_not_legal_clearance(self):
        record = json.loads(LICENSE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(record["upstream_source"]["root_license_spdx"], "Apache-2.0")
        self.assertEqual(len(record["upstream_source"]["changed_files"]), 6)
        self.assertEqual(record["reproduction_environment"]["stage2_artifact_id"], 14341424466)
        self.assertEqual(record["reproduction_environment"]["dependency_inventory_sha256"],
                         "6e8f21e813fd0332fa3a5c370f76a0a52653d49868348d4316cb0eb40d0c3c89")
        self.assertEqual(len(record["reproduction_environment"]["runtime_packages"]), 14)
        self.assertFalse(record["human_review"]["accepted_as_legal_clearance"])
        self.assertEqual(record["human_review"]["project_lead_scope_acknowledgement"], "acknowledged_with_scientific_independence_condition")
        self.assertEqual(record["project_lead_scope_acknowledgement_proposal"]["path"],
                         "research_candidates/evidence_abstention/dymos_1166/PROJECT_LEAD_CONDITIONAL_SCOPE_ACKNOWLEDGEMENT_DYMOS_1166_2026-11-20.md")
        self.assertEqual(record["project_lead_scope_acknowledgement_proposal"]["sha256"],
                         SCOPE_PROPOSAL_SHA256)
        scope_proposal = SCOPE_PROPOSAL_PATH.read_bytes()
        self.assertEqual(hashlib.sha256(scope_proposal).hexdigest(), SCOPE_PROPOSAL_SHA256)
        self.assertEqual(record["human_review"]["project_lead_scope_acknowledgement"], "pending")
        self.assertTrue(record["dataset"]["exact_pinned_dataset_card_license_verified"])
        self.assertEqual(record["dataset"]["pinned_card_verification"]["revision"],
                         "fb9aa226b2ce37c708ea7732e7b980abacdadb67")
        self.assertEqual(record["dataset"]["pinned_card_verification"]["license_displayed_at_exact_revision"],
                         "CC-BY-4.0")
        self.assertEqual(record["reproduction_environment"]["package_inventory"]["runtime_package_count"], 14)
        self.assertEqual(record["reproduction_environment"]["package_inventory"]["dependency_inventory_sha256"],
                         "6e8f21e813fd0332fa3a5c370f76a0a52653d49868348d4316cb0eb40d0c3c89")
        bundles = record["reproduction_environment"]["package_inventory"]["runtime_packages"]
        numpy = next(item for item in bundles if item["name"] == "numpy")
        scipy = next(item for item in bundles if item["name"] == "scipy")
        self.assertIn({"name": "libquadmath", "license": "LGPL-2.1-or-later"}, numpy["binary_bundles"])
        self.assertIn({"name": "GCC runtime library", "license": "GPL-3.0-with-GCC-exception"}, scipy["binary_bundles"])
        self.assertEqual(record["project_lead_scope_acknowledgement_proposal"]["status"],
                         "pending_project_lead_acknowledgement")
        self.assertFalse(record["human_review"]["accepted_as_legal_clearance"])
        self.assertFalse(record["inference_authorized"])

    def test_related_default_value_issue_is_clustered_not_double_counted(self):
        record = json.loads(INDEPENDENCE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(record["counting_rule"]["issue_count"], 1)
        self.assertEqual(record["counting_rule"]["dataset_row_count"], 1)
        self.assertEqual(record["counting_rule"]["frozen_dataset_selector_count"], 1)
        self.assertEqual(record["counting_rule"]["accepted_case_contribution_cap_for_repository"], 1)
        self.assertTrue(record["cross_project_independence"]["distinct_from_numpyro_project"])
        self.assertTrue(record["cross_project_independence"]["distinct_from_first_accepted_project"])
        self.assertTrue(record["issue_family_disposition"]["related_predecessor_found"])
        self.assertFalse(record["issue_family_disposition"]["exact_duplicate_found"])
        self.assertEqual(record["issue_family_disposition"]["duplicate_candidates_excluded_from_independent_case_count"], [531])
        self.assertEqual(record["independence_status"]["final_case_acceptance"], "not_accepted")
        self.assertEqual(record["exposure_and_roles"]["prior_candidate_specific_pipeline_debug_exposure"].split(" ")[0], "none")
        self.assertEqual(record["exposure_and_roles"]["researcher_source_exposure"].split(" ")[0], "full")
        self.assertEqual(record["exposure_and_roles"]["prior_pipeline_debug_exposure_decision_record"]["sha256"], EXPOSURE_SHA256)
        self.assertFalse(record["independence_status"]["inference_authorized"])

    def test_project_lead_gold_tier_decision_is_hashed_and_does_not_accept_case(self):
        content = DECISION_PATH.read_bytes()
        self.assertEqual(hashlib.sha256(content).hexdigest(), DECISION_SHA256)
        decision = content.decode("utf-8")
        self.assertIn("APPROVED", decision)
        self.assertIn("ABSTAIN", decision)
        self.assertIn("ANSWER", decision)
        self.assertIn("final acceptance of Dymos #1166 into the accepted case registry", decision)

        provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
        semantic = provenance["semantic_review"]
        self.assertEqual(semantic["status"], "approved_source_aware_project_lead_gold_and_tier_decision")
        self.assertEqual(semantic["project_lead_decision"]["decision"], "APPROVED")
        self.assertEqual(semantic["project_lead_decision"]["decision_record_sha256"], DECISION_SHA256)
        self.assertEqual(semantic["project_lead_decision"]["approved_evidence_tier_outcomes"]["E3"].split(" ")[0], "ABSTAIN")
        self.assertEqual(semantic["project_lead_decision"]["approved_evidence_tier_outcomes"]["E2"].split(" ")[0], "ABSTAIN")
        self.assertEqual(semantic["project_lead_decision"]["approved_evidence_tier_outcomes"]["E1"].split(" ")[0], "ANSWER")

        independence = json.loads(INDEPENDENCE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(independence["independence_status"]["final_case_acceptance"], "not_accepted")
        self.assertEqual(independence["source_aware_gold_tier_decision"]["status"], "approved_by_project_lead")
        self.assertFalse(independence["independence_status"]["inference_authorized"])

        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        dymos = next(item for item in ledger["records"] if item["repository"] == "OpenMDAO/dymos")
        self.assertEqual(dymos["stage3_gold_and_tiers_decision"]["decision"], "APPROVED")
        self.assertEqual(dymos["stage3_gold_and_tiers_decision"]["decision_record_sha256"], DECISION_SHA256)
        self.assertEqual(dymos["stage3_gold_and_tiers_decision"]["final_case_acceptance"], "not_accepted")
        self.assertFalse(dymos["stage3_gold_and_tiers_decision"]["inference_authorized"])
        self.assertNotEqual(dymos["final_case_acceptance"], "accepted")
        self.assertFalse(dymos["model_inference_authorized"])

    def test_prior_pipeline_debug_exposure_decision_is_hashed_and_separate_from_source_exposure(self):
        record = json.loads(INDEPENDENCE_PATH.read_text(encoding="utf-8"))
        decision = record["exposure_and_roles"]["prior_pipeline_debug_exposure_decision_record"]
        content = EXPOSURE_PATH.read_bytes()
        self.assertEqual(hashlib.sha256(content).hexdigest(), EXPOSURE_SHA256)
        self.assertEqual(decision["path"], str(EXPOSURE_PATH.relative_to(ROOT)))
        self.assertEqual(decision["declared_value"], "none")
        self.assertEqual(decision["evidence_class"], "direct_project_lead_self_report_in_conversation")
        self.assertFalse(decision["independent_witnessed_audit"])
        self.assertEqual(record["exposure_and_roles"]["researcher_source_exposure"].split(" ")[0], "full")

        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        dymos = next(item for item in ledger["records"] if item["repository"] == "OpenMDAO/dymos")
        self.assertEqual(dymos["stage3_exposure_decision"]["prior_pipeline_debug_exposure"], "none")
        self.assertEqual(dymos["stage3_exposure_decision"]["researcher_source_exposure"], "full")
        self.assertEqual(dymos["stage3_exposure_decision"]["decision_record_sha256"], EXPOSURE_SHA256)
        self.assertNotEqual(dymos["final_case_acceptance"], "accepted")
        self.assertFalse(dymos["model_inference_authorized"])


if __name__ == "__main__":
    unittest.main()
