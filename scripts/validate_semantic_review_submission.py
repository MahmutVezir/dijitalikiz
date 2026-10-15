#!/usr/bin/env python3
"""Fail-closed validator for completed v1.2 blinded semantic-review JSONL.

Checks submission structure and immutable fields only. It does not judge semantic
correctness, establish ground truth, prove reviewer independence, or calculate agreement.
It never prints response text or reviewer notes.
"""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

EXPECTED_PACKET_VERSION = "1.2"
EXPECTED_PACKET_KIND = "post_hoc_exploratory_semantic_review"
EXPECTED_N_RECORDS = 160
REVIEW_FIELDS = {
    "root_cause_correctness",
    "component_localization",
    "evidence_consistency",
    "dependency_reasoning",
    "overall_diagnostic_status",
    "reviewer_notes_with_evidence",
}
ENUMS = {
    "root_cause_correctness": {"correct", "partially_correct", "incorrect", "unscorable"},
    "component_localization": {"correct", "partially_correct", "incorrect", "unscorable"},
    "evidence_consistency": {"consistent", "partially_consistent", "inconsistent", "unscorable"},
    "dependency_reasoning": {"correct", "partially_correct", "incorrect", "not_applicable", "unscorable"},
    "overall_diagnostic_status": {"correct", "partially_correct", "incorrect", "unscorable"},
}


class ValidationError(Exception):
    """Submission violates the fail-closed review contract."""


def read_jsonl(text: str, label: str) -> list[dict[str, Any]]:
    if not text:
        raise ValidationError(f"{label}: empty file")
    lines = text.splitlines()
    if any(not line.strip() for line in lines):
        raise ValidationError(f"{label}: blank lines are not allowed")
    records: list[dict[str, Any]] = []
    for n, line in enumerate(lines, start=1):
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"{label}: line {n} is invalid JSON (column {exc.colno})") from exc
        if not isinstance(value, dict):
            raise ValidationError(f"{label}: line {n} must be a JSON object")
        records.append(value)
    return records


def read_assigned_packet(path: Path) -> list[dict[str, Any]]:
    try:
        with zipfile.ZipFile(path, "r") as zf:
            if zf.namelist().count("review_packet.jsonl") != 1:
                raise ValidationError("assigned ZIP must contain exactly one review_packet.jsonl")
            content = zf.read("review_packet.jsonl").decode("utf-8")
    except (OSError, zipfile.BadZipFile, UnicodeDecodeError) as exc:
        raise ValidationError(f"cannot read assigned ZIP ({type(exc).__name__})") from exc
    return read_jsonl(content, "assigned packet")


def validate_records(original: list[dict[str, Any]], submitted: list[dict[str, Any]]) -> dict[str, Any]:
    expected_lines = EXPECTED_N_RECORDS + 1
    if len(original) != expected_lines:
        raise ValidationError(f"assigned packet must have {expected_lines} lines; found {len(original)}")
    if len(submitted) != len(original):
        raise ValidationError(f"submission must have {len(original)} lines including metadata; found {len(submitted)}")

    header = original[0]
    if (
        header.get("record_type") != "metadata"
        or header.get("packet_kind") != EXPECTED_PACKET_KIND
        or header.get("packet_version") != EXPECTED_PACKET_VERSION
        or header.get("n_records") != EXPECTED_N_RECORDS
    ):
        raise ValidationError("assigned packet is not the expected frozen v1.2 160-row packet")
    if submitted[0] != header:
        raise ValidationError("metadata row changed; only response-row review fields may be edited")

    identifiers: list[str] = []
    counts: dict[str, Counter[str]] = {field: Counter() for field in ENUMS}
    for line_no, (expected, actual) in enumerate(zip(original[1:], submitted[1:]), start=2):
        if set(actual) != set(expected):
            raise ValidationError(f"line {line_no}: top-level fields changed")
        for key in ("review_id", "case_ref", "response", "source_evidence"):
            if key not in expected or actual.get(key) != expected.get(key):
                raise ValidationError(f"line {line_no}: immutable field {key} changed or is missing")
        review_id = actual.get("review_id")
        if not isinstance(review_id, str) or review_id in identifiers:
            raise ValidationError(f"line {line_no}: missing or duplicate review_id")
        identifiers.append(review_id)

        review = actual.get("review")
        if not isinstance(review, dict) or set(review) != REVIEW_FIELDS:
            raise ValidationError(f"line {line_no}: review fields do not match the six-field schema")
        expected_review = expected.get("review")
        if not isinstance(expected_review, dict) or set(expected_review) != REVIEW_FIELDS:
            raise ValidationError("assigned packet review schema is unexpected")

        for field, allowed in ENUMS.items():
            value = review.get(field)
            if not isinstance(value, str) or value not in allowed:
                raise ValidationError(f"line {line_no}: invalid or blank value for {field}")
            counts[field][value] += 1
        notes = review.get("reviewer_notes_with_evidence")
        if not isinstance(notes, str) or len(notes.strip()) < 10:
            raise ValidationError(f"line {line_no}: rationale notes must contain at least 10 characters")

        # Prove only the review subobject differs from the assigned original.
        reset = dict(actual)
        reset["review"] = expected_review
        if reset != expected:
            raise ValidationError(f"line {line_no}: a non-review field changed")

    if len(set(identifiers)) != EXPECTED_N_RECORDS:
        raise ValidationError("submission does not contain 160 unique review IDs")

    return {
        "status": "PASS",
        "scope": "structure and immutable-field integrity only; not semantic scoring or ground-truth verification",
        "packet_version": EXPECTED_PACKET_VERSION,
        "review_rows_validated": len(submitted) - 1,
        "unique_review_ids": len(set(identifiers)),
        "metadata_unchanged": True,
        "responses_and_evidence_unchanged": True,
        "all_required_labels_valid_and_nonblank": True,
        "all_rationale_notes_nonblank": True,
        "label_counts": {field: dict(counter) for field, counter in counts.items()},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True, type=Path, help="Assigned original reviewer ZIP")
    parser.add_argument("--submission", required=True, type=Path, help="Completed JSONL returned by reviewer")
    args = parser.parse_args(argv)
    try:
        original = read_assigned_packet(args.packet)
        submitted = read_jsonl(args.submission.read_text(encoding="utf-8"), "submission")
        result = validate_records(original, submitted)
    except (ValidationError, OSError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
