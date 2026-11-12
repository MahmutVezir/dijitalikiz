import unittest
from datetime import datetime, timezone

from scripts.audit_swe_rebench_filtered_verified import audit_records, parse_created_at


class SweRebenchMetadataAuditTests(unittest.TestCase):
    def row(self, **updates):
        row = {
            "instance_id": "org_repo-123",
            "repo": "org/repo",
            "base_commit": "a" * 40,
            "created_at": "2024-09-20 00:00:00",
            "language": "Python",
            "license": "MIT",
            "FAIL_TO_PASS": ["test_one"],
            "problem_statement": "A reproducible issue description.",
        }
        row.update(updates)
        return row

    def test_naive_date_string_is_reported_and_explicitly_assumed_utc(self):
        parsed, representation, assumed = parse_created_at("2024-09-20 00:00:00")
        self.assertEqual(parsed, datetime(2024, 9, 20, tzinfo=timezone.utc))
        self.assertEqual(representation, "string_naive")
        self.assertTrue(assumed)

    def test_utc_z_string_is_parsed_without_assumption(self):
        parsed, representation, assumed = parse_created_at("2024-09-20T00:00:00Z")
        self.assertEqual(parsed, datetime(2024, 9, 20, tzinfo=timezone.utc))
        self.assertEqual(representation, "string_tz")
        self.assertFalse(assumed)

    def test_only_python_post_cutoff_with_required_metadata_enters_candidate_pool(self):
        records = [
            self.row(),
            self.row(instance_id="old-1", created_at="2024-09-19 23:59:59"),
            self.row(instance_id="js-1", language="JavaScript"),
            self.row(instance_id="bad-sha", base_commit="not-a-sha"),
        ]
        summary, candidates = audit_records(records, {"created_at": "string"})
        self.assertEqual(summary["python_rows"], 3)
        self.assertEqual(summary["python_rows_on_or_after_cutoff"], 2)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["instance_id"], "org_repo-123")
        self.assertEqual(summary["accepted_confirmatory_cases"], 0)
        self.assertIs(summary["model_inference_performed"], False)

    def test_duplicate_instance_ids_are_not_candidates(self):
        records = [self.row(), self.row(repo="other/repo")]
        summary, candidates = audit_records(records, {"created_at": "string"})
        self.assertEqual(len(candidates), 0)
        self.assertEqual(summary["exclusion_reason_counts_nonexclusive"]["duplicate_instance_id"], 2)

    def test_missing_license_or_fail_to_pass_is_excluded(self):
        records = [
            self.row(instance_id="no-license", license=""),
            self.row(instance_id="no-ftp", **{"FAIL_TO_PASS": []}),
        ]
        summary, candidates = audit_records(records, {"created_at": "string"})
        self.assertEqual(candidates, [])
        self.assertEqual(summary["exclusion_reason_counts_nonexclusive"]["missing_source_license"], 1)
        self.assertEqual(summary["exclusion_reason_counts_nonexclusive"]["empty_fail_to_pass"], 1)

    def test_csv_allowlisted_fields_do_not_include_solution_bearing_content(self):
        summary, candidates = audit_records([self.row()], {"created_at": "string"})
        self.assertEqual(set(candidates[0]), {
            "instance_id", "repo", "base_commit", "created_at_utc", "language",
            "license", "fail_to_pass_count", "screen_status"
        })
        self.assertNotIn("patch", summary["safe_columns_read"])
        self.assertNotIn("test_patch", summary["safe_columns_read"])
        self.assertNotIn("problem_statement", candidates[0])


if __name__ == "__main__":
    unittest.main()
