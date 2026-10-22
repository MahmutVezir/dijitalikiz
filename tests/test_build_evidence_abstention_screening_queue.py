import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_evidence_abstention_screening_queue.py"
SPEC = importlib.util.spec_from_file_location("screening_queue", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)

FIELDS = [
    "source_dataset", "dataset_revision", "project", "bug_id", "case_id",
    "source_repository", "project_info_sha256", "bug_info_sha256", "patch_sha256",
    "run_test_sha256", "setup_sha256", "python_version", "pythonpath",
    "buggy_commit_id", "fixed_commit_id", "test_file", "run_test_command",
    "metadata_complete", "permanently_excluded_feasibility_case", "test_pair_verified",
    "license_reviewed", "ground_truth_reviewed", "evidence_levels_reviewed",
    "leakage_reviewed", "prior_exposure_clear", "accepted_for_confirmatory", "screening_status",
]


def row(project, bug_id, **overrides):
    item = {name: "" for name in FIELDS}
    item.update({
        "source_dataset": "BugsInPy",
        "dataset_revision": "pinned",
        "project": project,
        "bug_id": str(bug_id),
        "case_id": f"BugsInPy-{project}-{bug_id}",
        "source_repository": f"https://example.invalid/{project}",
        "python_version": "3.11.0",
        "buggy_commit_id": "a" * 40,
        "fixed_commit_id": "b" * 40,
        "test_file": "tests/test_demo.py",
        "run_test_command": "pytest tests/test_demo.py::test_bug",
        "metadata_complete": "true",
        "permanently_excluded_feasibility_case": "false",
        "accepted_for_confirmatory": "false",
        "prior_exposure_clear": "unknown",
    })
    item.update(overrides)
    return item


class ScreeningQueueTests(unittest.TestCase):
    def test_queue_interleaves_projects_and_keeps_all_acceptance_gates_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "inventory.csv"
            output = root / "queue.csv"
            summary_path = root / "summary.json"
            rows = [
                row("zeta", 1), row("zeta", 2), row("alpha", 1), row("alpha", 2),
                row("black", 1, case_id="BugsInPy-black-1"),
                row("fastapi", 1, case_id="BugsInPy-fastapi-1"),
                row("bad", 1, buggy_commit_id="c" * 40, fixed_commit_id="c" * 40),
            ]
            with source.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)

            summary = MODULE.build_queue(source, output, summary_path, first_batch_per_project=1)
            with output.open(newline="", encoding="utf-8") as f:
                queued = list(csv.DictReader(f))
            self.assertEqual([item["case_id"] for item in queued], [
                "BugsInPy-alpha-1", "BugsInPy-zeta-1", "BugsInPy-alpha-2", "BugsInPy-zeta-2"
            ])
            self.assertTrue(all(item["accepted_for_confirmatory"] == "false" for item in queued))
            self.assertTrue(all(item["test_pair_verified"] == "false" for item in queued))
            self.assertTrue(all(item["prior_exposure_clear"] == "unknown" for item in queued))
            self.assertEqual(summary["queue_rows"], 4)
            self.assertEqual(summary["projects_in_queue"], 2)
            self.assertEqual(summary["accepted_confirmatory_cases"], 0)
            self.assertEqual(summary["exclusions_by_reason"]["previously_exposed_permanent_exclusion"], 2)
            self.assertEqual(summary["exclusions_by_reason"]["invalid_or_identical_commit_ids"], 1)

    def test_current_exposure_ledger_excludes_recent_v9_screened_cases(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "inventory.csv"
            output = root / "queue.csv"
            summary_path = root / "summary.json"
            rows = [
                row("tqdm", 6),
                row("youtube-dl", 7),
                row("newproject", 1),
            ]
            with source.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)

            summary = MODULE.build_queue(source, output, summary_path, first_batch_per_project=1)
            with output.open(newline="", encoding="utf-8") as f:
                queued = list(csv.DictReader(f))
            queued_ids = {item["case_id"] for item in queued}
            self.assertNotIn("BugsInPy-tqdm-6", queued_ids)
            self.assertNotIn("BugsInPy-youtube-dl-7", queued_ids)
            self.assertIn("BugsInPy-newproject-1", queued_ids)
            self.assertEqual(summary["exclusions_by_reason"]["previously_exposed_permanent_exclusion"], 2)
            self.assertEqual(summary["documented_exposure_exclusion_count"], 32)
            self.assertEqual(len(summary["exposure_addendum_sha256"]), 64)
            self.assertEqual(summary["accepted_confirmatory_cases"], 0)

    def test_exposure_addendum_excludes_an_id_not_in_static_legacy_list(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "inventory.csv"
            output = root / "queue.csv"
            summary_path = root / "summary.json"
            addendum = root / "exposure.json"
            rows = [row("tqdm", 6), row("newproject", 1)]
            with source.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            addendum.write_text(json.dumps({
                "excluded_case_ids": ["BugsInPy-tqdm-6"],
                "additional_batch_records": [],
            }), encoding="utf-8")

            summary = MODULE.build_queue(
                source, output, summary_path, first_batch_per_project=1,
                exposure_addendum_path=addendum,
            )
            with output.open(newline="", encoding="utf-8") as f:
                queued = list(csv.DictReader(f))
            self.assertEqual([item["case_id"] for item in queued], ["BugsInPy-newproject-1"])
            self.assertEqual(summary["documented_exposure_exclusion_count"], 1)
            self.assertEqual(summary["exposure_addendum_sha256"], __import__("hashlib").sha256(addendum.read_bytes()).hexdigest())

    def test_inconsistent_exposure_addendum_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "inventory.csv"
            addendum = root / "exposure.json"
            rows = [row("tqdm", 6), row("newproject", 1)]
            with source.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            addendum.write_text(json.dumps({
                "excluded_case_ids": [],
                "additional_batch_records": [
                    {"category": "screen", "cases": ["BugsInPy-tqdm-6"]}
                ],
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing from excluded_case_ids"):
                MODULE.build_queue(
                    source, root / "queue.csv", root / "summary.json",
                    exposure_addendum_path=addendum,
                )

    def test_malformed_exposure_addendum_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "inventory.csv"
            with source.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerow(row("demo", 1))
            addendum = root / "exposure.json"
            addendum.write_text("{", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Exposure exclusion addendum is missing or invalid"):
                MODULE.build_queue(
                    source, root / "queue.csv", root / "summary.json",
                    exposure_addendum_path=addendum,
                )

    def test_missing_columns_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "inventory.csv"
            source.write_text("case_id,project\nBugsInPy-demo-1,demo\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing required columns"):
                MODULE.build_queue(source, root / "queue.csv", root / "summary.json")


if __name__ == "__main__":
    unittest.main()
