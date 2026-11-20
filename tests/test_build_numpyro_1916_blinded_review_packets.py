import importlib.util
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPL = ROOT / "research_candidates" / "evidence_abstention" / "implementation"
SCRIPT = IMPL / "build_numpyro_1916_blinded_review_packets.py"
PACKET_PATH = ROOT / "research_candidates" / "evidence_abstention" / "numpyro_1916" / "OPERATIONAL_EVIDENCE_PACKET_SET_PROPOSED_V0_2_2026-11-20.json"
sys.path.insert(0, str(IMPL))
SPEC = importlib.util.spec_from_file_location("build_numpyro_1916_blinded_review_packets", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class Numpyro1916BlindedReviewPacketBuilderTests(unittest.TestCase):
    def test_builds_two_separate_reviewer_bundles_and_private_mapping(self):
        packet_set = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "panel-b-delivery"
            private_dir = Path(tmp) / "panel-b-custodian-private"
            result = MODULE.build_review_bundles(packet_set, out, private_dir)
            self.assertEqual(result["status"], "created")
            self.assertFalse(result["semantic_sufficiency_assessed"])
            self.assertFalse(result["model_inference_performed"])
            private_map_path = private_dir / "CUSTODIAN_MAPPING_PRIVATE.json"
            self.assertTrue(private_map_path.is_file())
            self.assertFalse((out / "CUSTODIAN_MAPPING_PRIVATE.json").exists())
            private_map = json.loads(private_map_path.read_text(encoding="utf-8"))
            self.assertEqual(private_map["packet_set_sha256"], packet_set["packet_set_sha256"])
            self.assertIn("hidden_level", json.dumps(private_map))
            reviewer_packet_codes = {}
            reviewer_contents = {}
            for reviewer in ("A", "B"):
                path = out / result["reviewer_bundles"][reviewer]["bundle"]
                with zipfile.ZipFile(path) as archive:
                    names = set(archive.namelist())
                    self.assertEqual(names, {"README_REVIEWER.md", "review_packet.jsonl", "PANEL_B_REVIEW_FORM.md"})
                    self.assertNotIn("CUSTODIAN_MAPPING_PRIVATE.json", names)
                    rows = [json.loads(line) for line in archive.read("review_packet.jsonl").decode("utf-8").splitlines()]
                self.assertEqual(len(rows), 3)
                self.assertEqual(len({row["packet_code"] for row in rows}), 3)
                reviewer_packet_codes[reviewer] = {row["packet_code"] for row in rows}
                contents = []
                for row in rows:
                    self.assertEqual(set(row), {"packet_code", "items"})
                    for item in row["items"]:
                        self.assertEqual(set(item), {"item_id", "kind", "content"})
                        self.assertTrue(item["item_id"].startswith("item-"))
                        contents.append(item["content"])
                reviewer_contents[reviewer] = sorted(contents)
            self.assertTrue(reviewer_packet_codes["A"].isdisjoint(reviewer_packet_codes["B"]))
            self.assertEqual(reviewer_contents["A"], reviewer_contents["B"])

    def test_rejects_nested_or_shared_mapping_directory(self):
        packet_set = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "delivery"
            with self.assertRaises(ValueError):
                MODULE.build_review_bundles(packet_set, out, out / "custodian")
            with self.assertRaises(ValueError):
                MODULE.build_review_bundles(packet_set, out, out)

    def test_refuses_to_overwrite_existing_output_directory(self):
        packet_set = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "not-empty"
            out.mkdir()
            (out / "keep.txt").write_text("do not overwrite", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                MODULE.build_review_bundles(packet_set, out)


if __name__ == "__main__":
    unittest.main()
