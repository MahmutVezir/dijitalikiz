import csv
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_swe_rebench_timestamp_register import TRACK, PART_PATTERN, audit_register


def row(instance, repo, issue, role="primary", delta=0):
    dataset = "2025-01-01T00:00:00Z"
    api = "2025-01-01T00:00:00Z" if delta == 0 else "2025-01-01T00:00:01Z"
    return {
        "instance_id": instance,
        "selection_role": role,
        "dataset_repo": repo,
        "issue_number": str(issue),
        "dataset_created_at_utc": dataset,
        "github_api_created_at_utc": api,
        "delta_seconds": str(delta),
        "match_status": "exact_match" if delta == 0 else "one_second_difference",
        "issue_url": f"https://github.com/{repo}/issues/{issue}",
        "error": "",
    }


class TimestampRegisterAuditTests(unittest.TestCase):
    def build_register(self, root, rows):
        folder = root / TRACK
        folder.mkdir(parents=True)
        fields = list(rows[0])
        for part in range(1, 15):
            selected = rows[(part - 1) * 8:(part * 8 if part < 14 else len(rows))]
            with (folder / PART_PATTERN.format(part)).open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(selected)

    def test_audits_expected_register_and_keeps_one_second_case_open(self):
        rows = [
            row(f"org{i}__repo{i}-{i+1}", f"org{i}/repo{i}", i+1,
                "primary" if i < 96 else "project_reserve",
                1 if i == 0 else 0)
            for i in range(113)
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_register(root, rows)
            result = audit_register(root)
        self.assertEqual(result["row_count"], 113)
        self.assertEqual(result["unique_repository_count"], 113)
        self.assertEqual(result["selection_role_counts"], {"primary": 96, "project_reserve": 17})
        self.assertEqual(result["timestamp_status_counts"], {"exact_match": 112, "one_second_difference": 1})
        self.assertEqual(result["status"], "FULL_REGISTER_PASS_ONE_SECOND_CASE_REQUIRES_HUMAN_REVIEW")
        self.assertFalse(result["inference_authorized"])

    def test_rejects_duplicate_instance(self):
        rows = [row(f"org{i}__repo{i}-{i+1}", f"org{i}/repo{i}", i+1) for i in range(104)]
        rows[1]["instance_id"] = rows[0]["instance_id"]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_register(root, rows)
            with self.assertRaisesRegex(ValueError, "duplicate"):
                audit_register(root)

    def test_rejects_wrong_delta(self):
        rows = [row(f"org{i}__repo{i}-{i+1}", f"org{i}/repo{i}", i+1) for i in range(104)]
        rows[0]["delta_seconds"] = "2"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_register(root, rows)
            with self.assertRaisesRegex(ValueError, "delta mismatch"):
                audit_register(root)

    def test_rejects_missing_part(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "missing reconciliation part"):
                audit_register(Path(tmp))


if __name__ == "__main__":
    unittest.main()
