import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_evidence_abstention_v10_intake.py"
SPEC = importlib.util.spec_from_file_location("verify_v10_intake", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class V10IntakeReproducibilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inventory_path = self.root / "inventory.csv"
        self.queue_path = self.root / "queue.csv"
        self.generated_path = self.root / "generated.json"
        self.frozen_path = self.root / "frozen.json"
        self.exposure_path = self.root / "exposure.json"

        self.excluded = ["BugsInPy-demo-1", "BugsInPy-demo-2", "BugsInPy-demo-3"]
        inventory = [
            {
                "case_id": f"BugsInPy-demo-{i}",
                "project": f"project{i}",
                "permanently_excluded_feasibility_case": str(i <= 3).lower(),
            }
            for i in range(1, 16)
        ]
        queue = [
            {
                "case_id": row["case_id"],
                "project": row["project"],
                "metadata_complete": "true",
                "accepted_for_confirmatory": "false",
                "acceptance_status": "NOT_ACCEPTED",
            }
            for row in inventory
            if row["case_id"] not in self.excluded
        ]
        write_csv(
            self.inventory_path,
            ["case_id", "project", "permanently_excluded_feasibility_case"],
            inventory,
        )
        write_csv(
            self.queue_path,
            ["case_id", "project", "metadata_complete", "accepted_for_confirmatory", "acceptance_status"],
            queue,
        )
        self.queue_ids = [row["case_id"] for row in queue]
        self.selected = self.queue_ids[:10]
        self.selected_rows = [row for row in queue if row["case_id"] in self.selected]
        counts = {}
        for row in self.selected_rows:
            counts[row["project"]] = counts.get(row["project"], 0) + 1
        counts = dict(sorted(counts.items()))
        manifest = {
            "record_type": "metadata_only_screening_intake_not_confirmatory_dataset",
            "cohort_size": len(self.selected),
            "upstream_project_count": len(counts),
            "counts_by_project": counts,
            "source_inventory_sha256": sha256(self.inventory_path),
            "source_queue_sha256": sha256(self.queue_path),
            "accepted_confirmatory_cases": 0,
            "llm_inference_performed": False,
            "excluded_prior_exposure": self.excluded,
            "case_ids": self.selected,
        }
        self.generated_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        frozen = dict(manifest, status="locally_rebuilt_metadata_order_pending_remote_builder_run")
        self.frozen_path.write_text(json.dumps(frozen, indent=2), encoding="utf-8")
        self.exposure_path.write_text(json.dumps({
            "unique_exclusion_count": len(self.excluded),
            "excluded_case_ids": self.excluded,
        }), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def verify(self):
        return MODULE.verify_v10_intake(
            self.inventory_path,
            self.queue_path,
            self.generated_path,
            self.frozen_path,
            self.exposure_path,
            expected_inventory_rows=15,
            expected_inventory_projects=15,
            expected_queue_rows=12,
            expected_cohort_size=10,
            expected_project_count=10,
            expected_exclusion_count=3,
        )

    def test_exact_queue_prefix_and_exposure_union_pass(self):
        report = self.verify()
        self.assertTrue(report["ready"], report["blockers"])
        self.assertEqual(report["selected_candidates"], 10)
        self.assertEqual(report["selected_projects"], 10)
        self.assertEqual(report["exposure_union_ids"], 3)
        self.assertEqual(report["selected_exposure_intersection"], 0)
        self.assertEqual(report["model_inference_performed"], False)
        self.assertEqual(report["accepted_confirmatory_cases"], 0)

    def test_rejects_different_frozen_selection_order(self):
        frozen = json.loads(self.frozen_path.read_text(encoding="utf-8"))
        frozen["case_ids"] = list(reversed(frozen["case_ids"]))
        self.frozen_path.write_text(json.dumps(frozen), encoding="utf-8")
        report = self.verify()
        self.assertFalse(report["ready"])
        self.assertTrue(any("order differs" in item for item in report["blockers"]))

    def test_rejects_queue_hash_change(self):
        self.queue_path.write_text(self.queue_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        report = self.verify()
        self.assertFalse(report["ready"])
        self.assertTrue(any("Queue SHA-256" in item for item in report["blockers"]))

    def test_rejects_reintroduced_exposure(self):
        queue = list(csv.DictReader(self.queue_path.open("r", newline="", encoding="utf-8")))
        queue[0]["case_id"] = self.excluded[0]
        write_csv(
            self.queue_path,
            ["case_id", "project", "metadata_complete", "accepted_for_confirmatory", "acceptance_status"],
            queue,
        )
        report = self.verify()
        self.assertFalse(report["ready"])
        self.assertTrue(any("reintroduces previously exposed IDs" in item for item in report["blockers"]))

    def test_rejects_exposure_union_id_absent_from_inventory(self):
        exposure = json.loads(self.exposure_path.read_text(encoding="utf-8"))
        exposure["excluded_case_ids"].append("BugsInPy-not-in-inventory")
        exposure["unique_exclusion_count"] = len(exposure["excluded_case_ids"])
        self.exposure_path.write_text(json.dumps(exposure), encoding="utf-8")
        report = self.verify()
        self.assertFalse(report["ready"])
        self.assertTrue(any("absent from the inventory" in item for item in report["blockers"]))

    def test_rejects_malformed_exclusion_list_without_raising(self):
        generated = json.loads(self.generated_path.read_text(encoding="utf-8"))
        generated["excluded_prior_exposure"] = [{"unexpected": "object"}]
        self.generated_path.write_text(json.dumps(generated), encoding="utf-8")
        report = self.verify()
        self.assertFalse(report["ready"])
        self.assertTrue(any("missing or malformed" in item for item in report["blockers"]))

    def test_rejects_preaccepted_metadata_case(self):
        generated = json.loads(self.generated_path.read_text(encoding="utf-8"))
        generated["accepted_confirmatory_cases"] = 1
        self.generated_path.write_text(json.dumps(generated), encoding="utf-8")
        report = self.verify()
        self.assertFalse(report["ready"])
        self.assertTrue(any("zero accepted" in item for item in report["blockers"]))


if __name__ == "__main__":
    unittest.main()
