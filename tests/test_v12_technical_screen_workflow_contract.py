from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
V12 = ROOT / ".github" / "workflows" / "evidence-abstention-v12-technical-screen.yml"
V11 = ROOT / ".github" / "workflows" / "evidence-abstention-v11-technical-screen.yml"


class V12TechnicalScreenWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v12 = V12.read_text(encoding="utf-8")
        cls.v11 = V11.read_text(encoding="utf-8")

    def test_v12_screen_is_manual_only(self):
        self.assertIn("workflow_dispatch:", self.v12)
        self.assertNotIn("\n  push:", self.v12)
        self.assertNotIn("\n  pull_request:", self.v12)
        for name in (
            "confirm_dataset_license",
            "confirm_upstream_licenses",
            "confirm_protocol_frozen",
            "confirm_technical_screen",
        ):
            self.assertIn(name + ":", self.v12)
        self.assertIn("default: false", self.v12)

    def test_v12_screen_requires_105_id_and_legal_gates_before_upstream_clone(self):
        gate = self.v12.index("Require explicit license, protocol and manual authorization")
        clone = self.v12.index("Fetch exact pinned BugsInPy metadata tree")
        self.assertLess(gate, clone)
        self.assertIn('dataset_license_status") == "cleared"', self.v12)
        self.assertIn('upstream_project_license_status") == "cleared"', self.v12)
        self.assertIn('technical_screen_protocol_status") == "frozen"', self.v12)
        self.assertIn('technical_screen_authorized") is True', self.v12)
        self.assertIn("== 105", self.v12)
        self.assertIn("9f41451bb06582ea65647f67829e97ac190cb884946b1f4f09c75d8167acb7c1", self.v12)
        self.assertNotIn("== 97", self.v12)
        self.assertNotIn("97-exclusion", self.v12)

    def test_v12_selection_matches_committed_metadata_and_never_accepts_cases(self):
        self.assertIn("SCREENING_COHORT_100_V12_2026-11-12.json", self.v12)
        self.assertIn("V12_FIRST_BATCH_SELECTION_2026-11-12.json", self.v12)
        self.assertIn("rebuilt V12 cohort differs from committed 100-case index", self.v12)
        self.assertIn("rebuilt first batch differs from committed V12 selection", self.v12)
        self.assertIn('"accepted_confirmatory_cases"] == 0', self.v12)
        self.assertIn('"llm_inference_performed"] is False', self.v12)
        self.assertIn("retention-days: 90", self.v12)

    def test_workflow_is_read_only_and_legacy_v11_manual_dispatch_is_removed(self):
        self.assertIn("contents: read", self.v12)
        self.assertIn("uses: actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09", self.v12)
        self.assertIn("uses: actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1", self.v12)
        self.assertNotIn("contents: write", self.v12)
        self.assertNotIn("git push", self.v12.lower())
        self.assertNotIn("workflow_dispatch:", self.v11)
        self.assertIn("ARCHIVED V11 Technical Screen", self.v11)


if __name__ == "__main__":
    unittest.main()
