import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_evidence_abstention_triage_artifact.py"
SPEC = importlib.util.spec_from_file_location("triage_artifact_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_artifact(root, accepted=False, inference=False, valid_pair=True):
    (root / "source-metadata-hashes.txt").write_text(
        "a" * 64 + "  /runner/BugsInPy/projects/demo/bugs/1/bug.info\n"
        + "b" * 64 + "  /runner/BugsInPy/projects/demo/bugs/1/run_test.sh\n",
        encoding="utf-8",
    )
    summary = {
        "case_id": "BugsInPy-demo-1",
        "dataset_recorded_python": "3.8.3",
        "runtime_python_observed": "3.8.3",
        "runtime_matches_metadata": True,
        "expected_buggy_commit": "c" * 40,
        "observed_buggy_base_commit": "c" * 40,
        "expected_fixed_commit_reference": "d" * 40,
        "expected_run_test_sha256": "b" * 64,
        "buggy_target_test_exit_code": 1 if valid_pair else None,
        "fixed_target_test_exit_code": 0 if valid_pair else None,
        "buggy_failure_signature_present": valid_pair,
        "fixed_pass_marker_present": valid_pair,
        "accepted_for_confirmatory": accepted,
        "confirmatory_eligible": False,
        "llm_inference_performed": inference,
    }
    (root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    files = sorted(p for p in root.iterdir() if p.is_file() and p.name != "SHA256SUMS")
    (root / "SHA256SUMS").write_text("".join(f"{digest(p)}  ./{p.name}\n" for p in files), encoding="utf-8")


class TriageArtifactAuditTests(unittest.TestCase):
    def test_intact_triage_artifact_reports_signals_but_never_accepts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_artifact(root)
            result = MODULE.audit(root)
            self.assertTrue(result["integrity_pass"])
            self.assertTrue(result["technical_buggy_fail_fixed_pass_signals_present"])
            self.assertTrue(result["manual_review_required"])
            self.assertFalse(result["accepted_for_confirmatory"])
            self.assertFalse(result["confirmatory_eligible"])

    def test_changed_file_fails_checksum(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_artifact(root)
            (root / "summary.json").write_text("{}", encoding="utf-8")
            result = MODULE.audit(root)
            self.assertFalse(result["integrity_pass"])
            self.assertTrue(any("SHA-256 mismatch" in b for b in result["blockers"]))

    def test_accepted_or_inference_true_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_artifact(root, accepted=True, inference=True)
            result = MODULE.audit(root)
            self.assertFalse(result["integrity_pass"])
            self.assertTrue(any("accepted_for_confirmatory" in b for b in result["blockers"]))
            self.assertTrue(any("llm_inference_performed" in b for b in result["blockers"]))

    def test_incomplete_pair_is_warning_not_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_artifact(root, valid_pair=False)
            result = MODULE.audit(root)
            self.assertTrue(result["integrity_pass"])
            self.assertFalse(result["technical_buggy_fail_fixed_pass_signals_present"])
            self.assertFalse(result["accepted_for_confirmatory"])


    def test_missing_regression_fixture_is_not_a_bug_failure_signal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_artifact(root)
            (root / "buggy-test.log").write_text(
                "ERROR: test_demo.py::test_bug\nFileNotFoundError: [Errno 2] No such file or directory: '/tmp/buggy/tests/data/fixture.json'\n",
                encoding="utf-8",
            )
            files = sorted(p for p in root.iterdir() if p.is_file() and p.name != "SHA256SUMS")
            (root / "SHA256SUMS").write_text("".join(f"{digest(p)}  ./{p.name}\n" for p in files), encoding="utf-8")
            result = MODULE.audit(root)
            self.assertTrue(result["integrity_pass"], result["blockers"])
            self.assertTrue(result["raw_buggy_fail_fixed_pass_signals_present"])
            self.assertFalse(result["technical_buggy_fail_fixed_pass_signals_present"])
            self.assertTrue(result["likely_fixture_or_harness_error"])
            self.assertTrue(any("fixture or harness" in w for w in result["warnings"]))

    def test_tox_invocation_wrapper_does_not_mask_target_assertion_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_artifact(root)
            (root / "buggy-test.log").write_text(
                "plugins: cov-4.0.0, mock-3.6.1\\n"
                "E AssertionError: expected_pre == actual_hook_path[0]\\n"
                "FAILED tests/test_hooks.py::TestFindHooks::test_find_hook - AssertionError\\n"
                "ERROR: InvocationError for command pytest (exited with code 1)\\n",
                encoding="utf-8",
            )
            files = sorted(p for p in root.iterdir() if p.is_file() and p.name != "SHA256SUMS")
            (root / "SHA256SUMS").write_text("".join(f"{digest(p)}  ./{p.name}\\n" for p in files), encoding="utf-8")
            result = MODULE.audit(root)
            self.assertTrue(result["integrity_pass"], result["blockers"])
            self.assertTrue(result["raw_buggy_fail_fixed_pass_signals_present"])
            self.assertTrue(result["technical_buggy_fail_fixed_pass_signals_present"])
            self.assertFalse(result["likely_environment_or_harness_error"])

    def test_cuda_driver_warning_does_not_mask_target_assertion_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_artifact(root)
            (root / "buggy-test.log").write_text(
                "E tensorflow/stream_executor/cuda/cuda_driver.cc:318] failed call to cuInit: UNKNOWN ERROR (303)\\n"
                "E AssertionError: assert 0.0 > 0.0\\n"
                "FAILED tests/keras/initializers_test.py::test_statefulness[normal] - AssertionError\\n",
                encoding="utf-8",
            )
            files = sorted(p for p in root.iterdir() if p.is_file() and p.name != "SHA256SUMS")
            (root / "SHA256SUMS").write_text("".join(f"{digest(p)}  ./{p.name}\\n" for p in files), encoding="utf-8")
            result = MODULE.audit(root)
            self.assertTrue(result["integrity_pass"], result["blockers"])
            self.assertTrue(result["technical_buggy_fail_fixed_pass_signals_present"])
            self.assertFalse(result["likely_environment_or_harness_error"])

    def test_missing_dependency_is_not_a_bug_failure_signal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_artifact(root)
            (root / "buggy-test.log").write_text(
                "ImportError while loading conftest\nModuleNotFoundError: No module named 'sanic'\n",
                encoding="utf-8",
            )
            files = sorted(p for p in root.iterdir() if p.is_file() and p.name != "SHA256SUMS")
            (root / "SHA256SUMS").write_text("".join(f"{digest(p)}  ./{p.name}\n" for p in files), encoding="utf-8")
            result = MODULE.audit(root)
            self.assertTrue(result["integrity_pass"], result["blockers"])
            self.assertTrue(result["raw_buggy_fail_fixed_pass_signals_present"])
            self.assertFalse(result["technical_buggy_fail_fixed_pass_signals_present"])
            self.assertTrue(result["likely_environment_or_harness_error"])
            self.assertTrue(any("environment/dependency/plugin error" in w for w in result["warnings"]))

if __name__ == "__main__":
    unittest.main()
