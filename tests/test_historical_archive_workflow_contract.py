from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "research-validation.yml"


class HistoricalArchiveWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_uses_repository_local_recovered_archive(self):
        self.assertIn("data/historical/confirmatory_artifact_2026-10-09.zip", self.source)
        self.assertIn("EXPECTED_SHA256: \"e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd\"", self.source)
        self.assertIn("EXPECTED_RECORDS: \"160\"", self.source)

    def test_does_not_depend_on_expired_actions_artifact_metadata(self):
        self.assertNotIn("11640450681", self.source)
        self.assertNotIn("actions/artifacts/$ARTIFACT_ID", self.source)
        self.assertNotIn("steps.download.outputs.archive_path", self.source)

    def test_fails_closed_until_archive_is_in_repository(self):
        self.assertIn("BLOCKED/REPOSITORY_UPLOAD_REQUIRED", self.source)
        self.assertIn("Historical archive recovered but not stored in the canonical GitHub repository.", self.source)
        self.assertIn("scripts/audit_historical_artifact.py", self.source)


if __name__ == "__main__":
    unittest.main()
