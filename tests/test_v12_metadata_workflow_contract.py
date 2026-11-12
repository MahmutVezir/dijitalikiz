from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "evidence-abstention-metadata-inventory.yml"


class V12MetadataWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_uses_corrected_105_id_exposure_union(self):
        expected = "research_candidates/evidence_abstention/EXPOSURE_UNION_2026-11-11.json"
        self.assertGreaterEqual(self.source.count(expected), 2)
        self.assertIn("== 105", self.source)
        self.assertNotIn("== 97", self.source)

    def test_generates_v12_metadata_only_intake(self):
        self.assertIn("SCREENING_COHORT_100_V12_2026-11-12.json", self.source)
        self.assertIn('intake.get("accepted_confirmatory_cases") != 0', self.source)
        self.assertIn('"llm_inference_performed"] is not False', self.source)

    def test_commits_generated_inventory_and_evidence_to_canonical_repository(self):
        self.assertIn("generated_v12", self.source)
        self.assertIn("V12_METADATA_EVIDENCE_MANIFEST_2026-11-12.json", self.source)
        self.assertIn('git push origin "HEAD:$TARGET_BRANCH"', self.source)
        self.assertIn("contents: write", self.source)

    def test_actions_artifacts_are_secondary_to_durable_repository_commit(self):
        self.assertIn("retention-days: 90", self.source)
        self.assertLess(
            self.source.index("Persist V12 inventory, queue, cohort and evidence manifest"),
            self.source.index("Upload metadata inventory and manual screening queue"),
        )


if __name__ == "__main__":
    unittest.main()
