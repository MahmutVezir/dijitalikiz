import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "research_candidates" / "evidence_abstention" / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))
SPEC = importlib.util.spec_from_file_location(
    "evidence_level_packet_set",
    IMPLEMENTATION / "evidence_level_packet_set.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

PACKET_PATH = (
    ROOT / "research_candidates" / "evidence_abstention" / "numpyro_1916"
    / "OPERATIONAL_EVIDENCE_PACKET_SET_PROPOSED_V0_2_2026-11-20.json"
)
PROVENANCE_PATH = (
    ROOT / "research_candidates" / "evidence_abstention" / "numpyro_1916"
    / "EVIDENCE_PACKET_PROVENANCE_PROPOSED_V0_2_2026-11-20.json"
)


class Numpyro1916ProposedPacketSetTests(unittest.TestCase):
    def test_proposed_packet_set_is_structurally_valid_and_semantics_unassessed(self):
        packet_set = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        result = MODULE.validate_packet_set(packet_set)
        self.assertEqual(result["status"], "valid", result["blockers"])
        self.assertTrue(result["strictly_nested"])
        self.assertEqual(
            {level: len(packet_set["packets"][level]["evidence_items"]) for level in ("E1", "E2", "E3")},
            {"E1": 5, "E2": 2, "E3": 1},
        )
        self.assertEqual(
            result["additional_evidence_ids"]["E1_over_E2"],
            [
                "NP1916_BASE_ENSEMBLE_INIT_KEY_NORMALIZATION",
                "NP1916_BASE_ENSEMBLE_SPLIT",
                "NP1916_BASE_MCMC_RUN_HANDOFF",
            ],
        )
        self.assertFalse(result["semantic_sufficiency_assessed"])
        self.assertFalse(result["model_inference_performed"])

    def test_proposed_provenance_matches_packet_set_and_review_stays_pending(self):
        packet_set = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(provenance["packet_set_sha256"], packet_set["packet_set_sha256"])
        self.assertEqual(
            provenance["packet_set_path"],
            str(PACKET_PATH.relative_to(ROOT)),
        )
        self.assertEqual(
            provenance["semantic_review"]["status"],
            "pending_independent_human_panel",
        )
        self.assertFalse(provenance["structural_validation"]["semantic_sufficiency_assessed"])
        self.assertFalse(provenance["structural_validation"]["model_inference_performed"])


if __name__ == "__main__":
    unittest.main()
