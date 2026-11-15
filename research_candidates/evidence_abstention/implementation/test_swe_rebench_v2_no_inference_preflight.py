import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from swe_rebench_v2_no_inference_preflight import evaluate



class SweRebenchV2NoInferencePreflightTests(unittest.TestCase):
    def test_committed_v2_track_reports_blockers_and_never_authorizes_inference(self):
        report = evaluate(ROOT)
        self.assertEqual(report["track"], "SWE-rebench-V2")
        self.assertEqual(report["mode"], "read_only_preflight_no_model_execution")
        self.assertFalse(report["ready"])
        self.assertEqual(report["accepted_case_count"], 0)
        self.assertEqual(report["accepted_project_count"], 0)
        self.assertGreater(report["blocker_count"], 0)
        self.assertFalse(report["model_loading_performed"])
        self.assertFalse(report["model_inference_performed"])
        self.assertFalse(report["fine_tuning_performed"])
        self.assertFalse(report["inference_authorized"])

    def test_readiness_blockers_include_legal_runtime_human_sample_and_preregistration(self):
        report = evaluate(ROOT)
        joined = "\n".join(report["blockers"])
        for expected in (
            "source-license review",
            "timezone",
            "model-revision license",
            "runtime verification",
            "scoring rubric",
            "calibration",
            "Reviewer consent",
            "Institutional/mentor approval",
            "Generation settings",
            "External preregistration",
            "Accepted independent case count",
            "Accepted independent upstream project count",
        ):
            self.assertIn(expected.lower(), joined.lower())

    def test_draft_manifest_is_not_an_execution_authorization(self):
        report = evaluate(ROOT)
        self.assertFalse(report["inference_authorized"])
        self.assertIn("model_inference_performed", report)
        self.assertIs(report["model_inference_performed"], False)

    def test_schema_and_acceptance_validator_are_reported_as_hashed_artifacts(self):
        report = evaluate(ROOT)
        self.assertRegex(report["artifact_sha256"]["case_acceptance_schema"], r"^[0-9a-f]{64}$")
        self.assertRegex(report["artifact_sha256"]["case_acceptance_validator"], r"^[0-9a-f]{64}$")

    def test_nonexistent_root_fails_closed(self):
        report = evaluate(ROOT / "does-not-exist")
        self.assertFalse(report["ready"])
        self.assertGreater(report["blocker_count"], 0)
        self.assertFalse(report["inference_authorized"])


if __name__ == "__main__":
    unittest.main()
