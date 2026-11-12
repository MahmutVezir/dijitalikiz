import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research_candidates" / "evidence_abstention" / "implementation" / "uncertainty_inference_gate.py"
SPEC = importlib.util.spec_from_file_location("uncertainty_inference_gate", SCRIPT)
GATE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(GATE)

UNION_RELATIVE = "research_candidates/evidence_abstention/EXPOSURE_UNION_2026-11-11.json"
MANIFEST_RELATIVE = "research_candidates/evidence_abstention/UNCERTAINTY_EXPERIMENT_MANIFEST.json"


class UncertaintyInferenceGateTests(unittest.TestCase):
    def test_gate_pins_the_canonical_105_id_exposure_union(self):
        union_path = ROOT / UNION_RELATIVE
        union = json.loads(union_path.read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / MANIFEST_RELATIVE).read_text(encoding="utf-8"))
        ids = union["excluded_case_ids"]
        self.assertEqual(GATE.EXPECTED_ARTIFACT_PATHS["exposure_union"], UNION_RELATIVE)
        self.assertEqual(GATE.EXPECTED_EXPOSURE_EXCLUSION_COUNT, 105)
        self.assertEqual(len(ids), 105)
        self.assertEqual(len(set(ids)), 105)
        self.assertEqual(union["unique_exclusion_count"], 105)
        self.assertEqual(GATE.sha256_file(union_path), GATE.EXPECTED_EXPOSURE_UNION_SHA256)
        self.assertEqual(manifest["exposure_union_path"], UNION_RELATIVE)
        self.assertEqual(manifest["exposure_union_sha256"], GATE.EXPECTED_EXPOSURE_UNION_SHA256)
        self.assertEqual(manifest["permanent_exclusion_count"], 105)
        self.assertEqual(manifest["frozen_artifacts"]["exposure_union"]["path"], UNION_RELATIVE)
        self.assertEqual(manifest["frozen_artifacts"]["exposure_union"]["sha256"], GATE.EXPECTED_EXPOSURE_UNION_SHA256)

    def test_current_manifest_remains_closed_and_never_loads_the_model(self):
        report = GATE.evaluate_gate(ROOT, Path(MANIFEST_RELATIVE), env={})
        self.assertFalse(report["ready"])
        self.assertFalse(report["model_inference_performed"])
        self.assertIn("Manifest does not explicitly authorize inference.", report["blockers"])
        self.assertIn("Dataset-level license/permission is not cleared.", report["blockers"])
        self.assertIn("Exact upstream project licenses are not cleared.", report["blockers"])
        self.assertIn("Exact model revision license has not been cleared for this non-commercial research use.", report["blockers"])
        self.assertIn("Required human-review institutional approval is not recorded.", report["blockers"])
        self.assertIn("Required human-review consent is not complete.", report["blockers"])
        self.assertNotIn(
            "Exposure exclusion union missing or invalid: exposure_union_path must point to the canonical dated exposure union",
            report["blockers"],
        )


if __name__ == "__main__":
    unittest.main()
