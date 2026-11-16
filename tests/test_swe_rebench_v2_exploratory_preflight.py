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

    def test_empty_registry_blocks_inference_without_becoming_invalid(self):
        report = evaluate(ROOT)
        self.assertEqual(report["registry_status"], "valid_empty_registry")
        self.assertEqual(report["accepted_case_count"], 0)
        self.assertEqual(report["accepted_project_count"], 0)
        self.assertFalse(report["ready_for_inference"])
        self.assertIn(
            "No accepted case is registered; at least one fully accepted independent-project case is required before any model inference.",
            report["blockers"],
        )

    def test_single_human_design_does_not_require_second_rater(self):
        report = evaluate(ROOT)
        self.assertEqual(report["human_review_mode"], "single_researcher_adjudicator")
        self.assertFalse(report["second_human_rater_required"])
        self.assertFalse(report["interrater_reliability_claimed"])

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
