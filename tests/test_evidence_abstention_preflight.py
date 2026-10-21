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


    def test_rejects_accepted_case_with_unreproduced_bug_or_runtime_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            project = root / "research_candidates" / "evidence_abstention"
            manifest_path = project / "EXPERIMENT_MANIFEST_STAGE3.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["case_ids"] = ["BugsInPy-demo-1"]
            manifest["minimum_confirmatory_cases"] = 1
            manifest["minimum_upstream_projects"] = 1
            manifest["target_independent_cases"] = 1
            manifest["planned_model_outputs_at_target"] = 6
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            registry_path = project / "CASE_REGISTRY.json"
            record = {
                "case_id": "BugsInPy-demo-1",
                "accepted_for_confirmatory": True,
                "upstream_project": "demo",
                "source_repository": "https://example.invalid/demo",
                "license_reference": "LICENSE",
                "buggy_commit": "a" * 40,
                "fixed_commit": "b" * 40,
                "test_command": "pytest tests/test_demo.py",
                "runtime_fingerprint": "python 3.8.18; pinned dependencies",
                "root_cause_reference": "internal blind ground-truth record",
                "metadata_python_version": "3.6.9",
                "runtime_python_version": "3.8.18",
                "buggy_test_log_uri": "artifact://buggy.log",
                "fixed_test_log_uri": "artifact://fixed.log",
                "license_reviewed": True,
                "leakage_reviewed": True,
                "prior_exposure_clearance": True,
                "evidence_levels_reviewed": True,
                "test_pair_verified": True,
                "buggy_test_outcome": "environment_error",
                "fixed_test_outcome": "target_test_passed",
                "ground_truth_reviewer_ids": ["gt-r1", "gt-r2"],
                "evidence_reviewer_ids": ["ev-r1", "ev-r2"],
                "buggy_test_log_sha256": "c" * 64,
                "fixed_test_log_sha256": "d" * 64,
                "runtime_fingerprint_sha256": "e" * 64,
                "evidence_packet_sha256": {
                    "E1_sufficient": "1" * 64,
                    "E2_partial": "2" * 64,
                    "E3_insufficient": "3" * 64,
                },
            }
            registry_path.write_text(json.dumps({"records": [record]}), encoding="utf-8")
            report = MODULE.evaluate(root)
            self.assertFalse(report["ready"])
            self.assertTrue(any("runtime Python does not match" in b for b in report["blockers"]))
            self.assertTrue(any("buggy-side target failure was not reproduced" in b for b in report["blockers"]))

    def test_rejects_overlapping_ground_truth_and_evidence_review_panels(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            project = root / "research_candidates" / "evidence_abstention"
            manifest_path = project / "EXPERIMENT_MANIFEST_STAGE3.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["case_ids"] = ["BugsInPy-demo-1"]
            manifest["minimum_confirmatory_cases"] = 1
            manifest["minimum_upstream_projects"] = 1
            manifest["target_independent_cases"] = 1
            manifest["planned_model_outputs_at_target"] = 6
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            record = {
                "case_id": "BugsInPy-demo-1",
                "accepted_for_confirmatory": True,
                "upstream_project": "demo",
                "source_repository": "https://example.invalid/demo",
                "license_reference": "LICENSE",
                "buggy_commit": "a" * 40,
                "fixed_commit": "b" * 40,
                "test_command": "pytest tests/test_demo.py",
                "runtime_fingerprint": "python 3.11.0; pinned dependencies",
                "root_cause_reference": "ground-truth record",
                "metadata_python_version": "3.11.0",
                "runtime_python_version": "3.11.0",
                "buggy_test_log_uri": "artifact://buggy.log",
                "fixed_test_log_uri": "artifact://fixed.log",
                "license_reviewed": True,
                "leakage_reviewed": True,
                "prior_exposure_clearance": True,
                "evidence_levels_reviewed": True,
                "test_pair_verified": True,
                "buggy_test_outcome": "target_failure_reproduced",
                "fixed_test_outcome": "target_test_passed",
                "ground_truth_reviewer_ids": ["r1", "r2"],
                "evidence_reviewer_ids": ["r2", "r3"],
                "buggy_test_log_sha256": "c" * 64,
                "fixed_test_log_sha256": "d" * 64,
                "runtime_fingerprint_sha256": "e" * 64,
                "evidence_packet_sha256": {
                    "E1_sufficient": "1" * 64,
                    "E2_partial": "2" * 64,
                    "E3_insufficient": "3" * 64,
                },
            }
            (project / "CASE_REGISTRY.json").write_text(json.dumps({"records": [record]}), encoding="utf-8")
            report = MODULE.evaluate(root)
            self.assertFalse(report["ready"])
            self.assertTrue(any("reviewer IDs must be distinct between ground-truth and evidence review panels" in b for b in report["blockers"]))

if __name__ == "__main__":
    unittest.main()
