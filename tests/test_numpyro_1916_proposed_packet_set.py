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
            {"E1": 7, "E2": 4, "E3": 1},
        )
        self.assertEqual(
            result["additional_evidence_ids"]["E2_over_E3"],
            [
                "NP1916_BASE_MCMC_RUN_KEY_CONTRACT",
                "NP1916_BASE_MCMC_WARMUP_METHOD_CONTRACT",
                "NP1916_ISSUE_TRACEBACK",
            ],
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

    def test_project_lead_gold_is_approved_while_tier_review_stays_pending(self):
        packet_set = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(provenance["packet_set_sha256"], packet_set["packet_set_sha256"])
        self.assertEqual(
            provenance["packet_set_path"],
            str(PACKET_PATH.relative_to(ROOT)),
        )
        semantic_review = provenance["semantic_review"]
        self.assertEqual(
            semantic_review["status"],
            "project_lead_gold_mechanism_approved; packet_membership_construction_approved; semantic_sufficiency_pending",
        )
        self.assertEqual(
            semantic_review["project_lead_gold_decision"]["decision"],
            "APPROVED",
        )
        self.assertEqual(
            semantic_review["project_lead_gold_decision"]["approved_gold_mechanism_tr"],
            "MCMC.run(), warmup sonrasında saklanan sampler durumundaki skaler PRNG anahtarını vektörleştirilmiş zincirler için oluşturulan anahtar dizisiyle değiştiriyor. EnsembleSampler.sample() ise bu alanı skaler kabul ederek random.split() çağırıyor. Hata, sampler durumundaki anahtar biçiminin bu iki aşama arasında tutarsız hale gelmesinden kaynaklanıyor.",
        )
        self.assertEqual(
            semantic_review["tier_membership_decision"],
            "PENDING_separate_project_lead_decision",
        )
        amendment = semantic_review["packet_membership_construction_decision"]
        self.assertEqual(amendment["decision"], "APPROVED_FOR_PACKET_CONSTRUCTION_AND_STRUCTURAL_VALIDATION")
        self.assertEqual(amendment["approved_membership"], {"E3": 1, "E2": 4, "E1": 7})
        provenance_items = {item["id"]: item for item in provenance["evidence_items"]}
        packet_items = {
            level: {item["id"]: item for item in packet_set["packets"][level]["evidence_items"]}
            for level in ("E1", "E2", "E3")
        }
        for evidence_id, line_span, marker in (
            ("NP1916_BASE_MCMC_WARMUP_METHOD_CONTRACT", [584, 586], "post_warmup_state"),
            ("NP1916_BASE_MCMC_RUN_KEY_CONTRACT", [624, 626], "num_chains"),
        ):
            source_record = provenance_items[evidence_id]
            self.assertEqual(source_record["source_commit"], "07e4c9bc4524cc0a741ba8f8ad41339d34a0288d")
            self.assertEqual(source_record["source_git_blob_sha1"], "dd3ec0c3a782c1e1530b138153d821392ee5bebd")
            self.assertEqual(source_record["source_lines_1based"], line_span)
            for level in ("E1", "E2"):
                item = packet_items[level][evidence_id]
                self.assertIn(marker, item["content"])
                self.assertEqual(item["content_sha256"], source_record["content_sha256"])
                self.assertEqual(item["source_snapshot_sha256"], source_record["source_snapshot_sha256"])
            self.assertNotIn(evidence_id, packet_items["E3"])
        self.assertEqual(
            provenance["structural_validation"]["status"],
            "PENDING_BRANCH_HEAD_VALIDATION_OF_AMENDED_PACKET",
        )
        self.assertIn("NOT_ACCEPTED", semantic_review["final_case_acceptance"])
        self.assertFalse(provenance["structural_validation"]["semantic_sufficiency_assessed"])
        self.assertFalse(provenance["structural_validation"]["model_inference_performed"])


if __name__ == "__main__":
    unittest.main()
