import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "evidence_abstention_preflight.py"
SPEC = importlib.util.spec_from_file_location("preflight", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def fixture(root):
    project = root / "research_candidates" / "evidence_abstention"
    project.mkdir(parents=True)
    manifest = {
        "inference_allowed": False, "dataset_validation_gate": "OPEN",
        "preregistration_status": "draft", "preregistration_uri": "",
        "two_rater_protocol_frozen": False, "reviewer_calibration_complete": False,
        "model": {"id": "test/model", "revision": "abc123", "runtime_verification": "not_run", "quantization": "none"},
        "frozen_hashes": {}, "case_ids": [], "minimum_confirmatory_cases": 60,
        "minimum_upstream_projects": 8, "target_independent_cases": 80,
        "cells_per_case": 6, "planned_model_outputs_at_target": 480
    }
    (project / "EXPERIMENT_MANIFEST_STAGE3.json").write_text(json.dumps(manifest), encoding="utf-8")
    (project / "CASE_REGISTRY.json").write_text(json.dumps({"records": []}), encoding="utf-8")
    (project / "RUNTIME_LOCK.json").write_text(json.dumps({"status": "draft", "inference_performed": False}), encoding="utf-8")
    required = ["decision", "root_cause", "evidence_refs", "rationale", "alternative_hypotheses", "missing_evidence"]
    (project / "OUTPUT_SCHEMA.json").write_text(json.dumps({"type": "object", "required": required}), encoding="utf-8")
    for name in ("PROMPT_CONDITIONS.md", "ANALYSIS_PLAN_STAGE3.md", "STAGE3_EXPERIMENT_DESIGN.md", "RUBRIC_AND_ADJUDICATION.md"):
        (project / name).write_text("fixture only", encoding="utf-8")


class PreflightTests(unittest.TestCase):
    def test_fails_closed_without_cases_and_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            report = MODULE.evaluate(root)
            self.assertFalse(report["ready"])
            self.assertEqual(report["accepted_case_count"], 0)
            self.assertFalse(report["model_inference_performed"])
            self.assertTrue(any("accepted independent cases" in b for b in report["blockers"]))
            self.assertTrue(any("Frozen SHA-256" in b for b in report["blockers"]))

    def test_sha256_format(self):
        self.assertFalse(MODULE.HEX64.fullmatch("bad"))
        self.assertTrue(MODULE.HEX64.fullmatch("a" * 64))

    def test_preflight_is_read_only_and_never_runs_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            report = MODULE.evaluate(root)
            self.assertEqual(report["mode"], "read_only_preflight_no_model_execution")
            self.assertIs(report["model_inference_performed"], False)


if __name__ == "__main__":
    unittest.main()
