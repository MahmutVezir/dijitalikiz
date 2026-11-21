import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from swe_rebench_v2_exploratory_preflight import evaluate


class TestV02ExploratoryPreflight(unittest.TestCase):
    def test_report_uses_15_primary_and_20_stretch_targets(self):
        report = evaluate(ROOT)
        self.assertEqual(report["primary_target_cases"], 15)
        self.assertEqual(report["stretch_target_cases"], 20)
        self.assertEqual(report["minimum_feasibility_cases"], 1)
        self.assertEqual(report["preferred_analysis_threshold_cases"], 15)
        self.assertFalse(report["primary_target_met"])
        self.assertFalse(report["stretch_target_met"])

    def test_accepted_registry_is_valid_but_global_gates_still_block_inference(self):
        report = evaluate(ROOT)
        self.assertEqual(report["registry_status"], "structurally_valid_candidate_registry")
        self.assertEqual(report["accepted_case_count"], 3)
        self.assertEqual(report["accepted_project_count"], 3)
        self.assertFalse(report["ready_for_inference"])
        self.assertNotIn(
            "No accepted case is registered; at least one fully accepted independent-project case is required before any model inference.",
            report["blockers"],
        )
        self.assertIn("The exact immutable model revision's license/use review is not approved.", report["blockers"])
        self.assertIn("Rater B participation and case-specific independence/exposure screening are not confirmed.", report["blockers"])

    def test_meltano_bounded_scope_acknowledgement_keeps_open_gates_fail_closed(self):
        license_path = ROOT / "research_candidates/evidence_abstention/meltano_3090/MELTANO_3090_DEPENDENCY_LICENSE_SCOPE_REVIEW_V0_1_2026-11-21.json"
        ledger_path = ROOT / "research_candidates/evidence_abstention/SWE_REBENCH_V2_STAGE2_STAGE3_PROGRESS_LEDGER_V0_1_2026-11-16.json"
        registry_path = ROOT / "research_candidates/evidence_abstention/SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json"
        decision_path = ROOT / "research_candidates/evidence_abstention/meltano_3090/PROJECT_LEAD_BOUNDED_RESEARCH_SCOPE_ACKNOWLEDGEMENT_MELTANO_3090_2026-11-21.md"

        license_review = json.loads(license_path.read_text(encoding="utf-8"))
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        decision = decision_path.read_text(encoding="utf-8")

        human = license_review["human_review"]
        self.assertTrue(human["bounded_research_scope_acknowledged_in_principle"])
        self.assertEqual(
            human["project_lead_scope_acknowledgement"],
            "acknowledged_in_principle_with_explicit_conditions",
        )
        self.assertEqual(human["nested_dependency_review"], "open")
        self.assertEqual(human["notice_and_provenance_review"], "open")
        self.assertFalse(human["accepted_research_scope"])
        self.assertFalse(human["accepted_as_legal_clearance"])
        self.assertFalse(license_review["boundaries"]["legal_clearance"])
        self.assertFalse(license_review["boundaries"]["redistribution_authorized"])
        self.assertFalse(license_review["boundaries"]["final_case_acceptance"])
        self.assertFalse(license_review["boundaries"]["inference_authorized"])
        self.assertEqual(
            license_review["dataset_scope"]["exact_pinned_card_review"].split(";")[0],
            "pending",
        )

        meltano = next(record for record in ledger["records"] if record["repository"] == "meltano/sdk")
        self.assertEqual(meltano["final_case_acceptance"], "not_accepted")
        self.assertFalse(meltano["model_inference_authorized"])
        self.assertEqual(ledger["summary"]["accepted_exploratory_cases"], 3)
        self.assertEqual(ledger["summary"]["accepted_exploratory_projects"], 3)
        self.assertFalse(any(
            case.get("case_id") == "SRV2E-MELTANO_3090"
            for case in registry.get("cases", [])
        ))
        self.assertIn("not legal advice", decision.lower())
        self.assertIn("does not", decision.lower())

    def test_dual_human_output_scoring_requires_rater_b_confirmation(self):
        report = evaluate(ROOT)
        self.assertEqual(
            report["human_review_mode"],
            "two_human_raters_for_model_outputs_single_project_lead_for_gold_and_tiers",
        )
        self.assertTrue(report["second_human_rater_required"])
        self.assertEqual(
            report["second_human_rater_status"],
            "identified_pending_explicit_consent_and_case_specific_independence_screen",
        )
        self.assertFalse(report["interrater_reliability_claimed"])
        self.assertIn(
            "Rater B participation and case-specific independence/exposure screening are not confirmed.",
            report["blockers"],
        )

    def test_external_preregistration_is_not_a_v02_gate(self):
        report = evaluate(ROOT)
        self.assertFalse(report["external_preregistration_required"])
        joined = "\n".join(report["blockers"]).lower()
        self.assertNotIn("external preregistration", joined)
        self.assertNotIn("external registration", joined)

    def test_legacy_v01_confirmatory_requirements_are_not_applied(self):
        report = evaluate(ROOT)
        self.assertFalse(report["legacy_v0_1_requirements_applied"])
        joined = "\n".join(report["blockers"]).lower()
        for legacy_text in (
            "minimum of 60",
            "60 independent",
            "panel a",
            "panel b",
            "reviewer consent",
            "institutional/mentor approval",
            "external audit",
        ):
            self.assertNotIn(legacy_text, joined)

    def test_model_execution_and_authorization_remain_closed(self):
        report = evaluate(ROOT)
        self.assertFalse(report["model_loading_performed"])
        self.assertFalse(report["model_inference_performed"])
        self.assertFalse(report["fine_tuning_performed"])
        self.assertFalse(report["inference_authorized"])
        self.assertIn("Dataset validation gate remains open", "\n".join(report["blockers"]))
        self.assertIn("The exact model/tokenizer/runtime environment has not been verified.", report["blockers"])
        self.assertIn("Generation settings are still draft", "\n".join(report["blockers"]))


if __name__ == "__main__":
    unittest.main()
