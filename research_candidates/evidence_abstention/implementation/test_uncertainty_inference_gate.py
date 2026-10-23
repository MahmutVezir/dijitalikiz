import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from uncertainty_inference_gate import EXPECTED_ARTIFACT_PATHS, evaluate_gate, load_authorized_qwen


def accepted_case():
    return {
        "case_id": "case-1",
        "accepted_for_confirmatory": True,
        "upstream_project": "demo-project",
        "source_repository": "https://example.org/demo",
        "license_reference": "https://example.org/demo/LICENSE",
        "buggy_commit": "a" * 40,
        "fixed_commit": "b" * 40,
        "test_command": "pytest tests/test_demo.py::test_target",
        "runtime_fingerprint": "pinned test runtime",
        "root_cause_reference": "blinded ground-truth record gt-case-1",
        "metadata_python_version": "3.11.9",
        "runtime_python_version": "3.11.9",
        "buggy_test_outcome": "target_failure_reproduced",
        "fixed_test_outcome": "target_test_passed",
        "buggy_test_log_uri": "artifact://case-1/buggy.log",
        "fixed_test_log_uri": "artifact://case-1/fixed.log",
        "buggy_test_log_sha256": "c" * 64,
        "fixed_test_log_sha256": "d" * 64,
        "runtime_fingerprint_sha256": "e" * 64,
        "evidence_packet_sha256": {
            "E1_sufficient": "1" * 64,
            "E2_partial": "2" * 64,
            "E3_insufficient": "3" * 64,
        },
        "license_reviewed": True,
        "leakage_reviewed": True,
        "prior_exposure_clearance": True,
        "evidence_levels_reviewed": True,
        "test_pair_verified": True,
        "root_cause_reviewed_by_two": True,
        "ground_truth_reviewer_ids": ["gt-r1", "gt-r2"],
        "evidence_reviewer_ids": ["ev-r1", "ev-r2"],
    }


def write_ready_gate_fixture(root: Path, record: dict, excluded_case_ids=None) -> Path:
    excluded_case_ids = [] if excluded_case_ids is None else excluded_case_ids
    frozen_artifacts = {}

    for name, relative_path in EXPECTED_ARTIFACT_PATHS.items():
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if name == "case_registry":
            payload = json.dumps({"records": [record]}, indent=2) + "\n"
        elif name == "exposure_union":
            payload = json.dumps({
                "record_type": "synthetic_test_fixture",
                "excluded_case_ids": excluded_case_ids,
                "unique_exclusion_count": len(excluded_case_ids),
            }, indent=2) + "\n"
        else:
            payload = "{}\n"
        target.write_text(payload, encoding="utf-8")
        frozen_artifacts[name] = {
            "path": relative_path,
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        }

    manifest = {
        "inference_allowed": True,
        "dataset_validation_gate": "CLOSED",
        "preregistration_status": "registered",
        "preregistration_uri": "https://example.org/preregistration",
        "reviewer_protocol_frozen": True,
        "calibration_complete": True,
        "model": {
            "id": "Qwen/Qwen2.5-3B-Instruct",
            "revision": "aa8e72537993ba99e69dfaafa59ed015b17504d1",
            "tokenizer_id": "Qwen/Qwen2.5-3B-Instruct",
            "tokenizer_revision": "aa8e72537993ba99e69dfaafa59ed015b17504d1",
            "runtime_verification": "passed",
            "dtype": "float16",
            "quantization": "none",
        },
        "case_ids": [record["case_id"]],
        "case_registry_path": EXPECTED_ARTIFACT_PATHS["case_registry"],
        "exposure_union_path": EXPECTED_ARTIFACT_PATHS["exposure_union"],
        "minimum_confirmatory_cases": 1,
        "minimum_upstream_projects": 1,
        "frozen_artifacts": frozen_artifacts,
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


class InferenceGateTests(unittest.TestCase):
    def test_current_manifest_stays_closed(self):
        root = Path(__file__).resolve().parents[3]
        report = evaluate_gate(
            root,
            Path("research_candidates/evidence_abstention/UNCERTAINTY_EXPERIMENT_MANIFEST.json"),
            {},
        )
        self.assertFalse(report["ready"])
        self.assertFalse(report["model_inference_performed"])
        self.assertTrue(any("does not explicitly authorize" in item for item in report["blockers"]))

    def test_current_manifest_blocks_model_loading_before_import(self):
        root = Path(__file__).resolve().parents[3]
        with self.assertRaisesRegex(RuntimeError, "Inference blocked"):
            load_authorized_qwen(root, Path("research_candidates/evidence_abstention/UNCERTAINTY_EXPERIMENT_MANIFEST.json"))

    def test_empty_or_malformed_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "manifest.json"
            path.write_text("{", encoding="utf-8")
            report = evaluate_gate(root, path, {})
            self.assertFalse(report["ready"])
            self.assertFalse(report["model_inference_performed"])

    def test_missing_case_registry_and_hashes_block_inference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "manifest.json"
            manifest = {
                "inference_allowed": True,
                "dataset_validation_gate": "CLOSED",
                "preregistration_status": "registered",
                "preregistration_uri": "https://example.org/preregistration",
                "reviewer_protocol_frozen": True,
                "calibration_complete": True,
                "model": {"id": "model", "revision": "pinned", "runtime_verification": "passed"},
                "case_ids": ["case-1"],
                "case_registry_path": "registry.json",
                "minimum_confirmatory_cases": 1,
                "minimum_upstream_projects": 1,
                "frozen_artifacts": {},
            }
            path.write_text(json.dumps(manifest), encoding="utf-8")
            report = evaluate_gate(root, path, {"EVIDENCE_UNCERTAINTY_INFERENCE_APPROVED": "YES"})
            self.assertFalse(report["ready"])
            self.assertTrue(any("Case registry" in item for item in report["blockers"]))
            self.assertTrue(any("Frozen artifact entry missing" in item for item in report["blockers"]))
            self.assertTrue(any("Model ID/revision differs" in item for item in report["blockers"]))
            self.assertTrue(any("Tokenizer ID/revision differs" in item for item in report["blockers"]))

    def test_artifact_hash_mismatch_blocks_inference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = write_ready_gate_fixture(root, accepted_case())
            manifest = json.loads(path.read_text(encoding="utf-8"))
            for entry in manifest["frozen_artifacts"].values():
                entry["sha256"] = "a" * 64
            path.write_text(json.dumps(manifest), encoding="utf-8")

            report = evaluate_gate(root, path, {})

            self.assertFalse(report["ready"])
            self.assertTrue(any("SHA-256 mismatch" in item for item in report["blockers"]))


    def test_alternate_registry_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = write_ready_gate_fixture(root, accepted_case())
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["case_registry_path"] = "alternate-registry.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")

            report = evaluate_gate(
                root, path, {"EVIDENCE_UNCERTAINTY_INFERENCE_APPROVED": "YES"}
            )

            self.assertFalse(report["ready"])
            self.assertTrue(
                any("canonical confirmatory case registry" in item for item in report["blockers"]),
                report["blockers"],
            )

    def test_alternate_frozen_artifact_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = write_ready_gate_fixture(root, accepted_case())
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["frozen_artifacts"]["output_schema"]["path"] = "../../outside.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")

            report = evaluate_gate(
                root, path, {"EVIDENCE_UNCERTAINTY_INFERENCE_APPROVED": "YES"}
            )

            self.assertFalse(report["ready"])
            self.assertTrue(
                any("safe repository-relative path" in item for item in report["blockers"]),
                report["blockers"],
            )

    def test_accepted_case_requires_independent_review_and_reproducible_test_pair(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = accepted_case()
            record["ground_truth_reviewer_ids"] = []
            record["evidence_reviewer_ids"] = []
            record["metadata_python_version"] = "3.7.3"
            record["runtime_python_version"] = "3.11.9"
            record["buggy_test_outcome"] = "environment_error"
            path = write_ready_gate_fixture(root, record)

            report = evaluate_gate(root, path, {"EVIDENCE_UNCERTAINTY_INFERENCE_APPROVED": "YES"})

            self.assertFalse(report["ready"])
            self.assertTrue(any("two ground-truth reviewer IDs" in item for item in report["blockers"]))
            self.assertTrue(any("two evidence-sufficiency reviewer IDs" in item for item in report["blockers"]))
            self.assertTrue(any("runtime Python does not match" in item for item in report["blockers"]))
            self.assertTrue(any("buggy target failure was not reproduced" in item for item in report["blockers"]))

    def test_ground_truth_and_evidence_review_panels_must_be_disjoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = accepted_case()
            record["evidence_reviewer_ids"] = ["ev-r1", "gt-r2"]
            path = write_ready_gate_fixture(root, record)

            report = evaluate_gate(root, path, {"EVIDENCE_UNCERTAINTY_INFERENCE_APPROVED": "YES"})

            self.assertFalse(report["ready"])
            self.assertTrue(any("panels must be disjoint" in item for item in report["blockers"]))

    def test_malformed_case_ids_fail_closed_without_raising(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "manifest.json"
            path.write_text(json.dumps({"case_ids": [{}]}), encoding="utf-8")

            report = evaluate_gate(root, path, {})

            self.assertFalse(report["ready"])
            self.assertTrue(any("Case IDs are missing, malformed" in item for item in report["blockers"]))


    def test_complete_synthetic_gate_fixture_is_ready_without_running_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = write_ready_gate_fixture(root, accepted_case())

            report = evaluate_gate(
                root, path, {"EVIDENCE_UNCERTAINTY_INFERENCE_APPROVED": "YES"}
            )

            self.assertTrue(report["ready"], report["blockers"])
            self.assertFalse(report["model_inference_performed"])

    def test_exposure_union_blocks_previously_exposed_case_even_if_registry_flags_clear(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = accepted_case()
            record["case_id"] = "BugsInPy-keras-5"
            record["upstream_project"] = "keras"
            path = write_ready_gate_fixture(
                root, record, excluded_case_ids=["BugsInPy-keras-5"]
            )

            report = evaluate_gate(
                root, path, {"EVIDENCE_UNCERTAINTY_INFERENCE_APPROVED": "YES"}
            )

            self.assertFalse(report["ready"])
            self.assertTrue(
                any("permanent exposure exclusion union" in item for item in report["blockers"]),
                report["blockers"],
            )

if __name__ == "__main__":
    unittest.main()
