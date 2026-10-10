from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "followup_v2_lead_source_review_response.schema.json"


def read_jsonl(path: Path, issues: list[str], label: str) -> list[dict[str, Any]]:
    if not path.is_file():
        issues.append(f"missing_{label}:{path}")
        return []
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        issues.append(f"unreadable_{label}:{exc}")
        return []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(f"{label}_invalid_json_line_{line_number}:{exc.msg}")
            continue
        if not isinstance(row, dict):
            issues.append(f"{label}_row_{line_number}_not_object")
            continue
        rows.append(row)
    if not rows:
        issues.append(f"empty_{label}")
    return rows


def validate_review_responses(
    *,
    packet_path: Path,
    response_path: Path,
    schema_path: Path = DEFAULT_SCHEMA,
) -> dict[str, Any]:
    issues: list[str] = []
    packet = read_jsonl(packet_path, issues, "packet")
    responses = read_jsonl(response_path, issues, "responses")
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"schema_unavailable:{exc}")
        schema = None

    packet_ids = [row.get("review_id") for row in packet]
    response_ids = [row.get("review_id") for row in responses]
    for label, values in (("packet", packet_ids), ("responses", response_ids)):
        counts = Counter(value for value in values if isinstance(value, str))
        for review_id, count in counts.items():
            if count > 1:
                issues.append(f"{label}_duplicate_review_id:{review_id}")
        if any(not isinstance(value, str) or not value.strip() for value in values):
            issues.append(f"{label}_missing_or_invalid_review_id")

    expected = {value for value in packet_ids if isinstance(value, str)}
    observed = {value for value in response_ids if isinstance(value, str)}
    missing = sorted(expected - observed)
    extra = sorted(observed - expected)
    if missing:
        issues.append(f"responses_missing_review_ids:{missing}")
    if extra:
        issues.append(f"responses_contain_unknown_review_ids:{extra}")

    reviewer_ids = {
        row.get("reviewer_id")
        for row in responses
        if isinstance(row.get("reviewer_id"), str) and row.get("reviewer_id").strip()
    }
    if len(reviewer_ids) != 1:
        issues.append(f"response_file_must_have_one_consistent_reviewer_id:{sorted(reviewer_ids)}")

    if schema is not None:
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for line_number, row in enumerate(responses, start=1):
            errors = sorted(validator.iter_errors(row), key=lambda error: list(error.path))
            for error in errors[:10]:
                path = "/".join(str(part) for part in error.absolute_path)
                issues.append(f"responses_line_{line_number}_schema_error:{path}:{error.message}")

    return {
        "status": "pass" if not issues else "blocked",
        "review_packet_path": str(packet_path),
        "response_path": str(response_path),
        "expected_response_count": len(expected),
        "observed_response_count": len(responses),
        "reviewer_id": next(iter(reviewer_ids)) if len(reviewer_ids) == 1 else None,
        "missing_review_ids": missing,
        "unknown_review_ids": extra,
        "issue_count": len(issues),
        "issues": issues,
        "limitations": "This validator checks response format and coverage only. It cannot establish reviewer independence, evidence quality, or root-cause truth.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate one blind source-review response against its packet and schema."
    )
    parser.add_argument("--packet", type=Path, required=True, help="Exact packet JSONL sent to this reviewer.")
    parser.add_argument("--response", type=Path, required=True, help="Reviewer response JSONL.")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--output", type=Path, help="Optional path for a machine-readable audit JSON.")
    args = parser.parse_args()

    result = validate_review_responses(
        packet_path=args.packet,
        response_path=args.response,
        schema_path=args.schema,
    )
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
