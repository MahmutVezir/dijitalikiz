import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_evidence_abstention_intake.py"
SPEC = importlib.util.spec_from_file_location("evidence_abstention_intake", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def candidate(case_id, project, exposed=False):
    return {
        "case_id": case_id,
        "project": project,
        "permanently_excluded_feasibility_case": str(exposed).lower(),
        "metadata_complete": "true",
        "accepted_for_confirmatory": "false",
    }


def queue_row(case_id, project):
    return {
        "case_id": case_id,
        "project": project,
        "metadata_complete": "true",
        "accepted_for_confirmatory": "false",
    }


def write_addendum(path, excluded):
    path.write_text(json.dumps({
        "excluded_case_ids": excluded,
        "additional_batch_records": [
            {"category": "test", "cases": excluded}
        ],
    }), encoding="utf-8")


class MetadataIntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inventory_path = self.root / "inventory.csv"
        self.queue_path = self.root / "queue.csv"
        self.output_path = self.root / "intake.json"
        self.exposure_path = self.root / "exposure.json"
        self.inventory_rows = [
            candidate("BugsInPy-demo-1", "demo1", True),
            candidate("BugsInPy-demo-2", "demo2", False),
        ] + [
            candidate(f"BugsInPy-demo-{i}", f"project{i}", False)
            for i in range(3, 11)
        ]
        self.queue_rows = [
            queue_row(f"BugsInPy-demo-{i}", f"project{i}")
            for i in range(3, 11)
        ]
        write_csv(self.inventory_path, [
            "case_id", "project", "permanently_excluded_feasibility_case",
            "metadata_complete", "accepted_for_confirmatory",
        ], self.inventory_rows)
        write_csv(self.queue_path, [
            "case_id", "project", "metadata_complete", "accepted_for_confirmatory",
        ], self.queue_rows)
        write_addendum(self.exposure_path, ["BugsInPy-demo-1", "BugsInPy-demo-2"])

    def tearDown(self):
        self.temp.cleanup()

    def test_builds_first_n_metadata_only_intake_with_hashes(self):
        output = MODULE.build_intake(
            self.inventory_path, self.queue_path, self.output_path,
            cohort_size=8, exposure_addendum_path=self.exposure_path,
        )
        self.assertEqual(output["case_ids"], [row["case_id"] for row in self.queue_rows])
        self.assertEqual(output["cohort_size"], 8)
        self.assertEqual(output["upstream_project_count"], 8)
        self.assertEqual(output["accepted_confirmatory_cases"], 0)
        self.assertFalse(output["llm_inference_performed"])
        self.assertEqual(output["source_inventory_sha256"], hashlib.sha256(self.inventory_path.read_bytes()).hexdigest())
        self.assertEqual(output["source_queue_sha256"], hashlib.sha256(self.queue_path.read_bytes()).hexdigest())
        self.assertIn("BugsInPy-demo-1", output["excluded_prior_exposure"])

    def test_rejects_exposed_case_reintroduced_into_queue(self):
        self.queue_rows[0] = queue_row("BugsInPy-demo-1", "project3")
        write_csv(self.queue_path, [
            "case_id", "project", "metadata_complete", "accepted_for_confirmatory",
        ], self.queue_rows)
        with self.assertRaisesRegex(ValueError, "documented prior-exposure"):
            MODULE.build_intake(
                self.inventory_path, self.queue_path, self.output_path,
                cohort_size=8, exposure_addendum_path=self.exposure_path,
            )

    def test_rejects_duplicate_queue_ids(self):
        self.queue_rows[1] = dict(self.queue_rows[0])
        write_csv(self.queue_path, [
            "case_id", "project", "metadata_complete", "accepted_for_confirmatory",
        ], self.queue_rows)
        with self.assertRaisesRegex(ValueError, "duplicate case IDs"):
            MODULE.build_intake(
                self.inventory_path, self.queue_path, self.output_path,
                cohort_size=8, exposure_addendum_path=self.exposure_path,
            )

    def test_rejects_queue_case_missing_from_inventory(self):
        self.queue_rows[0] = queue_row("BugsInPy-not-in-inventory", "project3")
        write_csv(self.queue_path, [
            "case_id", "project", "metadata_complete", "accepted_for_confirmatory",
        ], self.queue_rows)
        with self.assertRaisesRegex(ValueError, "absent from the source inventory"):
            MODULE.build_intake(
                self.inventory_path, self.queue_path, self.output_path,
                cohort_size=8, exposure_addendum_path=self.exposure_path,
            )

    def test_rejects_intake_with_fewer_than_minimum_upstream_projects(self):
        duplicate_project_rows = [
            queue_row(f"BugsInPy-case-{i}", "same-project") for i in range(8)
        ]
        write_csv(self.queue_path, [
            "case_id", "project", "metadata_complete", "accepted_for_confirmatory",
        ], duplicate_project_rows)
        # Ensure the queue IDs exist in inventory.
        self.inventory_rows.extend([
            candidate(row["case_id"], row["project"])
            for row in duplicate_project_rows
        ])
        write_csv(self.inventory_path, [
            "case_id", "project", "permanently_excluded_feasibility_case",
            "metadata_complete", "accepted_for_confirmatory",
        ], self.inventory_rows)
        with self.assertRaisesRegex(ValueError, "upstream projects"):
            MODULE.build_intake(
                self.inventory_path, self.queue_path, self.output_path,
                cohort_size=8, exposure_addendum_path=self.exposure_path,
            )


if __name__ == "__main__":
    unittest.main()
