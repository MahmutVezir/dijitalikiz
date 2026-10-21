import tempfile
import unittest
from pathlib import Path

from scripts.inventory_bugsinpy_candidates import (
    DATASET_COMMIT,
    build_summary,
    inventory_rows,
)


class InventoryTests(unittest.TestCase):
    def _fixture(self, root):
        project = root / "projects" / "demo-project"
        bug = project / "bugs" / "1"
        bug.mkdir(parents=True)
        (project / "project.info").write_text('github_url="https://github.com/example/demo"\n', encoding="utf-8")
        (bug / "bug.info").write_text(
            'python_version="3.10.1"\n'
            'pythonpath="src"\n'
            'buggy_commit_id="abc123"\n'
            'fixed_commit_id="def456"\n'
            'test_file="tests/test_demo.py"\n',
            encoding="utf-8",
        )
        (bug / "bug_patch.txt").write_text("hash only for integrity\n", encoding="utf-8")
        (bug / "run_test.sh").write_text("python -m pytest tests/test_demo.py::test_bug\n", encoding="utf-8")
        (bug / "setup.sh").write_text("python -m pip install -e .\n", encoding="utf-8")
        return bug

    def test_inventory_is_metadata_only_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self._fixture(root)
            rows = inventory_rows(root, DATASET_COMMIT)
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row["case_id"], "BugsInPy-demo-project-1")
            self.assertEqual(row["source_repository"], "https://github.com/example/demo")
            self.assertEqual(row["metadata_complete"], "true")
            self.assertEqual(row["screening_status"], "unreviewed_metadata_only")
            self.assertEqual(row["accepted_for_confirmatory"], "false")
            self.assertEqual(row["test_pair_verified"], "false")
            self.assertEqual(row["license_reviewed"], "false")
            self.assertTrue(row["patch_sha256"])

    def test_missing_metadata_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bug = self._fixture(root)
            (bug / "bug.info").write_text('python_version="3.10.1"\n', encoding="utf-8")
            row = inventory_rows(root)[0]
            self.assertEqual(row["metadata_complete"], "false")
            self.assertEqual(row["accepted_for_confirmatory"], "false")
            self.assertEqual(row["screening_status"], "metadata_incomplete")

    def test_summary_never_claims_test_or_llm_execution(self):
        summary = build_summary([], DATASET_COMMIT)
        self.assertEqual(summary["accepted_confirmatory_cases"], 0)
        self.assertEqual(summary["test_pairs_verified_by_this_script"], 0)
        self.assertIs(summary["llm_inference_performed"], False)


if __name__ == "__main__":
    unittest.main()
