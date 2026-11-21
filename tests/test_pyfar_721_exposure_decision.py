import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research_candidates" / "evidence_abstention"
PYFAR = RESEARCH / "pyfar_721"


class PyFar721ExposureDecisionTests(unittest.TestCase):
    def test_project_lead_none_declaration_closes_only_exposure_gate(self):
        decision_path = PYFAR / "PROJECT_LEAD_EXPOSURE_DECISION_PYFAR_721_2026-11-21.md"
        independence_path = PYFAR / "PYFAR_721_ISSUE_FAMILY_INDEPENDENCE_REVIEW_V0_1_2026-11-21.json"
        proposal_path = PYFAR / "PYFAR_721_SOURCE_AWARE_GOLD_AND_EVIDENCE_TIERS_PROPOSAL_2026-11-21.md"
        gold_decision_path = PYFAR / "PROJECT_LEAD_GOLD_TIER_DECISION_PYFAR_721_2026-11-21.md"
        ledger_path = (
            RESEARCH / "SWE_REBENCH_V2_STAGE2_STAGE3_PROGRESS_LEDGER_V0_1_2026-11-16.json"
        )
        registry_path = RESEARCH / "SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json"

        decision = decision_path.read_text(encoding="utf-8")
        gold_decision = gold_decision_path.read_text(encoding="utf-8")
        proposal = proposal_path.read_text(encoding="utf-8")
        independence = json.loads(independence_path.read_text(encoding="utf-8"))
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        pyfar = next(item for item in ledger["records"] if item["repository"] == "pyfar/pyfar")
        registry = json.loads(registry_path.read_text(encoding="utf-8"))

        self.assertIn("Declared prior pipeline/debug exposure: `none`", decision)
        self.assertIn("Researcher source exposure therefore remains **`full`**", decision)
        self.assertIn("Blinded adjudication claimed: **no**", decision)
        self.assertIn("Inter-rater reliability claimed: **no**", decision)

        exposure = independence["exposure"]
        self.assertEqual(exposure["prior_pipeline_debug_exposure"], "none")
        self.assertEqual(exposure["researcher_source_exposure"], "full_for_issue_PR_exact_base_source_and_stage2_outputs")
        self.assertEqual(exposure["prior_pipeline_debug_exposure_gate"], "closed_on_project_lead_self_report")
        self.assertEqual(exposure["evidence_class"], "direct_project_lead_self_report_in_conversation")
        self.assertFalse(exposure["independent_witnessed_or_audited"])
        self.assertFalse(exposure["blind_adjudication_claimed"])
        self.assertFalse(exposure["inter_rater_claimed"])
        self.assertEqual(exposure["decision_record_commit"], "c4f2633ca2270c2682f12290cb3e07f5c800c285")

        self.assertEqual(pyfar["stage3_exposure"]["prior_pipeline_debug_exposure"], "none")
        self.assertEqual(pyfar["stage3_exposure"]["researcher_source_exposure"], "full_for_issue_PR_exact_base_source_and_stage2_outputs")
        self.assertEqual(pyfar["stage3_exposure"]["prior_pipeline_debug_exposure_gate"], "closed_on_project_lead_self_report")
        self.assertNotIn("prior_pipeline_debug_exposure_declaration_pending", pyfar["stage3_status"])
        self.assertNotIn("prior pipeline/debug exposure declaration", pyfar["next_required_gate"].lower())
        self.assertEqual(pyfar["stage3_proposed_tiers"]["tier_decision_status"], "project_lead_approved_2026_11_21")
        gold = pyfar["stage3_project_lead_gold_tier_decision"]
        self.assertEqual(gold["decision"], "approved")
        self.assertEqual(gold["approved_gold"], "ENERGY_POWER_TARGET_AND_REFERENCE_NOT_SQUARE_ROOTED")
        self.assertEqual(gold["approved_tiers"], {"E3": "ABSTAIN", "E2": "ABSTAIN", "E1": "ANSWER"})
        self.assertFalse(gold["registry_inclusion"])
        self.assertFalse(gold["inference_authorized"])
        self.assertIn("23 upstream PR-derived selectors remain a single selector set", gold_decision)
        self.assertIn("This approval does not approve the prepared issue-family independence review", gold_decision)
        self.assertIn("E3", gold_decision)
        self.assertIn("E2", gold_decision)
        self.assertIn("E1", gold_decision)
        self.assertIn("APPROVED ON 2026-11-21", proposal)
        self.assertEqual(pyfar["final_case_acceptance"], "not_accepted")
        self.assertFalse(pyfar["model_inference_authorized"])
        self.assertIn("prior_pipeline_debug_exposure = none", proposal)
        self.assertNotIn("pending a direct project-lead declaration", proposal)
        self.assertIn("source exposure remains `full`", proposal.lower())

        self.assertEqual(registry["accepted_case_count"], 2)
        self.assertEqual(registry["accepted_project_count"], 2)
        self.assertFalse(registry["inference_authorized"])
        self.assertNotIn("SRV2E-PYFAR_721", {item["case_id"] for item in registry["records"]})
        self.assertEqual(ledger["summary"]["accepted_exploratory_cases"], 2)
        self.assertEqual(ledger["summary"]["accepted_exploratory_projects"], 2)


if __name__ == "__main__":
    unittest.main()
