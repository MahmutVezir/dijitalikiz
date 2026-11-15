import unittest

from scripts.audit_swe_rebench_timestamps_against_github import (
    parse_instance_issue_number,
    parse_utc_timestamp,
    reconcile_candidate_row,
)


def row(**updates):
    value = {
        "instance_id": "owner__repo-42",
        "repo": "owner/repo",
        "base_commit": "a" * 40,
        "created_at_utc": "2025-01-01T12:00:00Z",
        "language": "python",
        "license": "MIT",
        "fail_to_pass_count": 1,
        "screen_status": "metadata_candidate_unreviewed",
    }
    value.update(updates)
    return value


def issue_payload(**updates):
    value = {
        "number": 42,
        "repository_url": "https://api.github.com/repos/owner/repo",
        "created_at": "2025-01-01T12:00:00Z",
        "html_url": "https://github.com/owner/repo/issues/42",
    }
    value.update(updates)
    return value


class SweRebenchTimestampApiAuditTests(unittest.TestCase):
    def test_instance_id_must_match_repository_prefix_and_numeric_issue_suffix(self):
        self.assertEqual(parse_instance_issue_number("owner/repo", "owner__repo-42"), 42)
        self.assertIsNone(parse_instance_issue_number("other/repo", "owner__repo-42"))
        self.assertIsNone(parse_instance_issue_number("owner/repo", "owner__repo-not-a-number"))
        self.assertIsNone(parse_instance_issue_number("invalid-repo", "invalid-repo-42"))

    def test_api_timestamp_parser_requires_explicit_utc(self):
        self.assertIsNotNone(parse_utc_timestamp("2025-01-01T12:00:00Z"))
        self.assertIsNotNone(parse_utc_timestamp("2025-01-01T12:00:00+00:00"))
        self.assertIsNone(parse_utc_timestamp("2025-01-01 12:00:00"))
        self.assertIsNone(parse_utc_timestamp("2025-01-01T15:00:00+03:00"))

    def test_exact_api_timestamp_match_uses_github_time_for_candidate_output(self):
        result = reconcile_candidate_row(row(), issue_payload())
        self.assertEqual(result["timestamp_verification_status"], "exact_match")
        self.assertEqual(result["created_at_utc"], "2025-01-01T12:00:00Z")
        self.assertEqual(result["screen_status"], "metadata_candidate_api_timestamp_verified")
        self.assertEqual(result["dataset_vs_api_delta_seconds"], 0)
        self.assertFalse(result["issue_is_pull_request"])

    def test_one_second_difference_is_flagged_and_api_timestamp_is_preserved(self):
        result = reconcile_candidate_row(
            row(),
            issue_payload(created_at="2025-01-01T12:00:01Z"),
        )
        self.assertEqual(result["timestamp_verification_status"], "one_second_difference")
        self.assertEqual(result["dataset_vs_api_delta_seconds"], 1)
        self.assertEqual(result["created_at_utc"], "2025-01-01T12:00:01Z")
        self.assertEqual(result["screen_status"], "review_one_second_difference")

    def test_difference_greater_than_one_second_is_excluded(self):
        result = reconcile_candidate_row(
            row(),
            issue_payload(created_at="2025-01-01T12:00:03Z"),
        )
        self.assertEqual(result["timestamp_verification_status"], "timestamp_mismatch")
        self.assertEqual(result["created_at_utc"], "")
        self.assertTrue(result["screen_status"].startswith("excluded:"))

    def test_github_issue_id_mismatch_is_excluded(self):
        result = reconcile_candidate_row(row(), issue_payload(number=43))
        self.assertEqual(result["timestamp_verification_status"], "github_issue_number_mismatch")
        self.assertEqual(result["created_at_utc"], "")

    def test_github_repository_identity_mismatch_is_excluded(self):
        result = reconcile_candidate_row(
            row(),
            issue_payload(repository_url="https://api.github.com/repos/someone/else"),
        )
        self.assertEqual(result["timestamp_verification_status"], "github_repository_identity_mismatch")
        self.assertEqual(result["created_at_utc"], "")

    def test_not_found_and_http_errors_fail_closed(self):
        missing = reconcile_candidate_row(row(), {"_http_status": 404})
        denied = reconcile_candidate_row(row(), {"_http_status": 403})
        self.assertEqual(missing["timestamp_verification_status"], "github_issue_not_found")
        self.assertEqual(denied["timestamp_verification_status"], "github_api_http_error_403")
        self.assertEqual(missing["created_at_utc"], "")
        self.assertEqual(denied["created_at_utc"], "")

    def test_api_timestamp_before_cutoff_overrides_historical_candidate_inclusion(self):
        cutoff = "2024-09-20T00:00:00Z"
        result = reconcile_candidate_row(
            row(created_at_utc=cutoff),
            issue_payload(created_at="2024-09-19T23:59:59Z"),
        )
        self.assertEqual(result["timestamp_verification_status"], "api_timestamp_before_cutoff")
        self.assertEqual(result["created_at_utc"], "")
        self.assertEqual(result["screen_status"], "excluded:api_timestamp_before_cutoff")

    def test_pull_request_marker_is_preserved_without_changing_timestamp_source(self):
        result = reconcile_candidate_row(
            row(),
            issue_payload(pull_request={"url": "https://api.github.com/repos/owner/repo/pulls/42"}),
        )
        self.assertEqual(result["timestamp_verification_status"], "exact_match")
        self.assertTrue(result["issue_is_pull_request"])


if __name__ == "__main__":
    unittest.main()
