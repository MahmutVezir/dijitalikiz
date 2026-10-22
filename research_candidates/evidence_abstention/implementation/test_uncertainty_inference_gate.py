import json
import tempfile
import unittest
from pathlib import Path

from uncertainty_inference_gate import evaluate_gate, load_authorized_qwen


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
            (root / "registry.json").write_text(json.dumps({"records": []}), encoding="utf-8")
            (root / "artifact.json").write_text("{}", encoding="utf-8")
            manifest = {
                "inference_allowed": False,
                "dataset_validation_gate": "OPEN",
                "preregistration_status": "draft",
                "preregistration_uri": "",
                "reviewer_protocol_frozen": False,
                "calibration_complete": False,
                "model": {"id": "model", "revision": "pinned", "runtime_verification": "not_run"},
                "case_ids": [],
                "case_registry_path": "registry.json",
                "minimum_confirmatory_cases": 60,
                "minimum_upstream_projects": 8,
                "frozen_artifacts": {
                    name: {"path": "artifact.json", "sha256": "a" * 64}
                    for name in (
                        "case_registry", "output_schema", "prompt_template",
                        "analysis_plan", "runtime_lock", "calibration_data", "evidence_audit_protocol"
                    )
                },
            }
            path = root / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            report = evaluate_gate(root, path, {})
            self.assertFalse(report["ready"])
            self.assertTrue(any("SHA-256 mismatch" in item for item in report["blockers"]))


if __name__ == "__main__":
    unittest.main()
