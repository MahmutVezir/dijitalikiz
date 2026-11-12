from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "evidence-abstention-metadata-inventory.yml"


class V12MetadataWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_uses_corrected_105_id_exposure_union_for_queue_and_intake(self):
        expected = "research_candidates/evidence_abstention/EXPOSURE_UNION_2026-11-11.json"
        self.assertGreaterEqual(self.source.count(expected), 2)
        self.assertIn("== 105", self.source)
        self.assertNotIn("== 97", self.source)

    def test_generates_metadata_only_v12_and_never_accepts_cases(self):
        self.assertIn("SCREENING_COHORT_100_V12_2026-11-12.json", self.source)
        self.assertIn('assert intake["accepted_confirmatory_cases"] == 0', self.source)
        self.assertIn('assert intake["llm_inference_performed"] is False', self.source)
        self.assertIn('"model_inference_performed": False', self.source)

    def test_artifact_contains_inventory_queue_cohort_selection_and_hash_manifest(self):
        for name in (
            "bugsinpy-metadata-inventory.csv",
            "bugsinpy-screening-queue.csv",
            "SCREENING_COHORT_100_V12_2026-11-12.json",
            "v12-first-batch-matrix.json",
            "V12_METADATA_EVIDENCE_MANIFEST_2026-11-12.json",
        ):
            self.assertIn(name, self.source)
        self.assertIn("retention-days: 90", self.source)

    def test_workflow_does_not_write_tokens_or_upstream_source_to_repository(self):
        self.assertIn("permissions:\n  contents: read", self.source)
        self.assertNotIn("contents: write", self.source)
        self.assertNotIn("git push", self.source)
        self.assertIn("git clone --filter=blob:none https://github.com/soarsmu/BugsInPy.git", self.source)
        self.assertIn("RUNNER_TEMP/BugsInPy", self.source)


if __name__ == "__main__":
    unittest.main()
