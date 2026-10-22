import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from qwen_runtime_preflight import (
    canonical_sha256,
    run_no_output_preflight,
    validate_configuration,
    validate_versions,
)


MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"
REVISION = "aa8e72537993ba99e69dfaafa59ed015b17504d1"
VERSIONS = {"python": "3.11.9", "torch": "2.2.1", "transformers": "4.43.2", "accelerate": "0.33.0"}


def configuration():
    model = {
        "id": MODEL_ID,
        "revision": REVISION,
        "tokenizer_id": MODEL_ID,
        "tokenizer_revision": REVISION,
        "dtype": "float16",
        "quantization": "none",
    }
    generation = {
        "candidate_count": 5,
        "do_sample": True,
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 0,
        "max_new_tokens": 240,
        "seed_policy": "base_seed_plus_candidate_index",
        "selected_output_policy": "first_candidate_is_the_predeclared_selected_output",
    }
    manifest = {"model": model, "generation": generation}
    lock = {
        "model": {**model, "trust_remote_code": False},
        "generation": {**generation, "generation_performed_during_preflight": False},
        "proposed_environment": VERSIONS,
    }
    return manifest, lock


class QwenRuntimePreflightTests(unittest.TestCase):
    def test_manifest_and_lock_must_match_exact_checkpoint_and_generation_policy(self):
        manifest, lock = configuration()
        self.assertEqual(validate_configuration(manifest, lock), [])
        lock["model"]["revision"] = "f" * 40
        self.assertTrue(any("revision" in item for item in validate_configuration(manifest, lock)))

    def test_generation_policy_mismatch_blocks_preflight(self):
        manifest, lock = configuration()
        lock["generation"]["temperature"] = 0.2
        self.assertTrue(any("generation.temperature" in item for item in validate_configuration(manifest, lock)))

    def test_runtime_versions_require_exact_pins(self):
        self.assertEqual(validate_versions(VERSIONS, VERSIONS), [])
        observed = {**VERSIONS, "torch": "2.2.2"}
        self.assertTrue(any("torch" in item for item in validate_versions(observed, VERSIONS)))

    def test_fingerprint_is_stable_under_key_order(self):
        self.assertEqual(canonical_sha256({"a": 1, "b": 2}), canonical_sha256({"b": 2, "a": 1}))

    def test_version_mismatch_writes_blocked_record_without_model_load(self):
        manifest, lock = configuration()
        lock["proposed_environment"]["python"] = "0.0.0"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = root / "manifest.json"
            lock_path = root / "lock.json"
            output_path = root / "preflight.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            lock_path.write_text(json.dumps(lock), encoding="utf-8")
            with patch("qwen_runtime_preflight.installed_versions", return_value=VERSIONS):
                result = run_no_output_preflight(manifest_path, lock_path, output_path)
            stored = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "blocked_before_model_download")
            self.assertFalse(stored["model_generation_called"])
            self.assertFalse(stored["model_output_generated"])
            self.assertFalse(stored["model_inference_performed"])


if __name__ == "__main__":
    unittest.main()

