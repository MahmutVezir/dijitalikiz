"""Synthetic tests for the v1.2 completed-review submission validator."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_semantic_review_submission import EXPECTED_N_RECORDS, ValidationError, validate_records


def make_packet():
    header = {
        "record_type": "metadata",
        "packet_kind": "post_hoc_exploratory_semantic_review",
        "packet_version": "1.2",
        "reviewer_code": "TEST",
        "n_records": EXPECTED_N_RECORDS,
    }
    blank_review = {
        "root_cause_correctness": "",
        "component_localization": "",
        "evidence_consistency": "",
        "dependency_reasoning": "",
        "overall_diagnostic_status": "",
        "reviewer_notes_with_evidence": "",
    }
    rows = [header]
    for i in range(EXPECTED_N_RECORDS):
        rows.append({
            "review_id": f"synthetic-review-{i:03}",
            "case_ref": f"synthetic-case-{i % 16:02}",
            "response": f"Synthetic model response {i}",
            "source_evidence": {"summary": f"Synthetic evidence {i}"},
            "review": dict(blank_review),
        })
    return rows


def completed_copy(original):
    rows = [dict(original[0])]
    for row in original[1:]:
        item = dict(row)
        item["review"] = {
            "root_cause_correctness": "partially_correct",
            "component_localization": "correct",
            "evidence_consistency": "consistent",
            "dependency_reasoning": "not_applicable",
            "overall_diagnostic_status": "partially_correct",
            "reviewer_notes_with_evidence": "Problem summary supports part of this mechanism; B2 is consistent.",
        }
        rows.append(item)
    return rows


class SubmissionValidatorTests(unittest.TestCase):
    def setUp(self):
        self.original = make_packet()
        self.submitted = completed_copy(self.original)

    def test_complete_synthetic_submission_passes(self):
        result = validate_records(self.original, self.submitted)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["review_rows_validated"], 160)
        self.assertTrue(result["responses_and_evidence_unchanged"])

    def test_missing_row_fails(self):
        with self.assertRaisesRegex(ValidationError, "must have 161 lines"):
            validate_records(self.original, self.submitted[:-1])

    def test_blank_label_fails(self):
        self.submitted[1]["review"]["root_cause_correctness"] = ""
        with self.assertRaisesRegex(ValidationError, "root_cause_correctness"):
            validate_records(self.original, self.submitted)

    def test_invalid_enum_fails(self):
        self.submitted[1]["review"]["evidence_consistency"] = "probably"
        with self.assertRaisesRegex(ValidationError, "evidence_consistency"):
            validate_records(self.original, self.submitted)

    def test_edited_response_fails(self):
        self.submitted[1]["response"] += " changed"
        with self.assertRaisesRegex(ValidationError, "immutable field response"):
            validate_records(self.original, self.submitted)

    def test_reordered_rows_fail(self):
        self.submitted[1], self.submitted[2] = self.submitted[2], self.submitted[1]
        with self.assertRaisesRegex(ValidationError, "immutable field review_id"):
            validate_records(self.original, self.submitted)

    def test_short_rationale_fails(self):
        self.submitted[1]["review"]["reviewer_notes_with_evidence"] = "wrong"
        with self.assertRaisesRegex(ValidationError, "at least 10"):
            validate_records(self.original, self.submitted)

    def test_changed_metadata_fails(self):
        self.submitted[0]["review_status"] = "reviewed"
        with self.assertRaisesRegex(ValidationError, "metadata row changed"):
            validate_records(self.original, self.submitted)

    def test_extra_review_field_fails(self):
        self.submitted[1]["review"]["confidence"] = "high"
        with self.assertRaisesRegex(ValidationError, "six-field schema"):
            validate_records(self.original, self.submitted)


if __name__ == "__main__":
    unittest.main()
