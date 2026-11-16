#!/usr/bin/env python3
"""Audit the committed row-level GitHub timestamp reconciliation register.

This verifies the stored CSV register's internal consistency. It does not make
new GitHub API requests or independently authenticate the original API payloads.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
import re
import sys

TRACK = Path("research_candidates/evidence_abstention")
PART_PATTERN = "timestamp_reconciliation_part_{:02d}_2026-11-15.csv"
EXPECTED_PARTS = 14
EXPECTED_TOTAL = 113
EXPECTED_PRIMARY = 96
EXPECTED_RESERVE = 17
EXPECTED_EXACT = 112
EXPECTED_ONE_SECOND = 1
REQUIRED_FIELDS = {
    "instance_id", "selection_role", "dataset_repo", "issue_number",
    "dataset_created_at_utc", "github_api_created_at_utc",
    "delta_seconds", "match_status", "issue_url", "error",
}


def parse_utc(value: str) -> datetime:
    if not value.endswith("Z"):
        raise ValueError("timestamp must have explicit Z UTC suffix")
    parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    if parsed.utcoffset().total_seconds() != 0:
        raise ValueError("timestamp must be UTC")
    return parsed


def audit_register(root: Path) -> dict:
    rows: list[dict[str, str]] = []
    file_hashes: dict[str, str] = {}
    for index in range(1, EXPECTED_PARTS + 1):
        path = root / TRACK / PART_PATTERN.format(index)
        if not path.is_file():
            raise ValueError(f"missing reconciliation part: {path}")
        raw = path.read_bytes()
        file_hashes[str(path)] = hashlib.sha256(raw).hexdigest()
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = set(reader.fieldnames or [])
            missing = REQUIRED_FIELDS - fields
            if missing:
                raise ValueError(f"{path}: missing columns {sorted(missing)}")
            rows.extend(dict(row) for row in reader)

    if len(rows) != EXPECTED_TOTAL:
        raise ValueError(f"expected {EXPECTED_TOTAL} rows, found {len(rows)}")

    ids = [row["instance_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate instance_id values in reconciliation register")

    repositories = [row["dataset_repo"].casefold() for row in rows]
    if len(repositories) != len(set(repositories)):
        raise ValueError("duplicate repository identities in reconciliation register")

    counts = Counter(row["match_status"] for row in rows)
    role_counts = Counter(row["selection_role"] for row in rows)
    deltas = Counter()
    for row in rows:
        if row["error"]:
            raise ValueError(f"API error recorded for {row['instance_id']}")
        repo = row["dataset_repo"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            raise ValueError(f"invalid repository identity for {row['instance_id']}")
        expected_prefix = repo.replace("/", "__").casefold() + "-"
        if not row["instance_id"].casefold().startswith(expected_prefix):
            raise ValueError(f"instance/repository mismatch: {row['instance_id']}")
        issue_number = row["issue_number"]
        if not issue_number.isdigit() or int(issue_number) <= 0:
            raise ValueError(f"invalid issue number for {row['instance_id']}")
        if not row["issue_url"].startswith("https://github.com/"):
            raise ValueError(f"missing canonical GitHub issue URL for {row['instance_id']}")
        if not row["issue_url"].rstrip("/").casefold().endswith(
            f"/{repo}/{ 'issues' if '/issues/' in row['issue_url'] else 'pull' }/{issue_number}".casefold()
        ):
            raise ValueError(f"issue URL does not match repo/number for {row['instance_id']}")

        dataset_time = parse_utc(row["dataset_created_at_utc"])
        api_time = parse_utc(row["github_api_created_at_utc"])
        delta = int((api_time - dataset_time).total_seconds())
        if str(delta) != row["delta_seconds"]:
            raise ValueError(f"delta mismatch for {row['instance_id']}")
        deltas[delta] += 1
        expected_status = "exact_match" if delta == 0 else (
            "one_second_difference" if abs(delta) == 1 else "timestamp_mismatch"
        )
        if row["match_status"] != expected_status:
            raise ValueError(f"status/delta mismatch for {row['instance_id']}")
        if row["selection_role"] not in {"primary", "project_reserve"}:
            raise ValueError(f"unknown selection role for {row['instance_id']}")

    if role_counts != Counter({"primary": EXPECTED_PRIMARY, "project_reserve": EXPECTED_RESERVE}):
        raise ValueError(f"unexpected role counts: {dict(role_counts)}")
    if counts != Counter({"exact_match": EXPECTED_EXACT, "one_second_difference": EXPECTED_ONE_SECOND}):
        raise ValueError(f"unexpected timestamp status counts: {dict(counts)}")

    exceptions = [
        {
            "instance_id": row["instance_id"],
            "repo": row["dataset_repo"],
            "issue_number": row["issue_number"],
            "delta_seconds": int(row["delta_seconds"]),
            "issue_url": row["issue_url"],
            "selection_role": row["selection_role"],
            "status": row["match_status"],
        }
        for row in rows if row["match_status"] != "exact_match"
    ]
    return {
        "audit_type": "stored_timestamp_reconciliation_register_integrity",
        "status": "FULL_REGISTER_PASS_ONE_SECOND_CASE_REQUIRES_HUMAN_REVIEW",
        "scope": "113 stored rows across 14 committed CSV parts; no new GitHub API requests",
        "row_count": len(rows),
        "unique_instance_count": len(set(ids)),
        "unique_repository_count": len({row["dataset_repo"].casefold() for row in rows}),
        "selection_role_counts": dict(sorted(role_counts.items())),
        "timestamp_status_counts": dict(sorted(counts.items())),
        "delta_seconds_counts": dict(sorted(deltas.items())),
        "exceptions": exceptions,
        "input_sha256": file_hashes,
        "limitations": [
            "This audit validates CSV structure and internal consistency only.",
            "It does not independently authenticate the original GitHub API response payloads.",
            "The committed register contains all 96 primary rows and all 17 declared project reserves; timestamp coverage does not establish candidate eligibility.",
            "The one-second difference is not auto-admitted and requires an explicit documented decision.",
            "Timestamp reconciliation does not establish defect validity, independence, source-code licensing, human adjudication, or model execution readiness."
        ],
        "confirmatory_cases_accepted": 0,
        "model_inference_performed": False,
        "inference_authorized": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = audit_register(args.root)
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}, indent=2))
        return 2
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
