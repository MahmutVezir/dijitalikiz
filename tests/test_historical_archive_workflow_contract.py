from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "research-validation.yml"


class HistoricalArchiveWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_current_research_validation_is_independent_of_legacy_ccdg_archive(self):
        self.assertIn("validate-repository:", self.source)
        self.assertNotIn("validate-historical-archive:", self.source)
        self.assertNotIn("confirmatory_artifact_2026-10-09.zip", self.source)
        self.assertNotIn("scripts/audit_historical_artifact.py", self.source)

    def test_no_inference_and_read_only_controls_remain(self):
        self.assertIn("contents: read", self.source)
        self.assertIn("pytest -q", self.source)
        self.assertIn("python -m compileall -q scripts dijitalikiz", self.source)
        self.assertIn("Confirm no model execution command is invoked by this workflow", self.source)
        self.assertNotIn("kaggle kernels push", self.source)
        self.assertNotIn("kaggle kernels start", self.source)


if __name__ == "__main__":
    unittest.main()
