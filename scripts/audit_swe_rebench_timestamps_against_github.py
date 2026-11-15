#!/usr/bin/env python3
"""Reconcile historical SWE-rebench candidate dates with authoritative GitHub issue timestamps.

This is a no-inference metadata audit. The old naive-UTC interpretation is used
only to reconstruct the historical candidate search frame. Candidate eligibility
for any rebuilt cohort is determined from GitHub REST API created_at values.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

try:
    from .audit_swe_rebench_filtered_verified import (
        CUTOFF,
        EXPECTED_BYTES,
        EXPECTED_ROWS,
        EXPECTED_SHA256,
        SAFE_COLUMNS,
        audit_records,
        sha256_file,
    )
except ImportError:
    from audit_swe_rebench_filtered_verified import (
        CUTOFF,
        EXPECTED_BYTES,
        EXPECTED_ROWS,
        EXPECTED_SHA256,
        SAFE_COLUMNS,
        audit_records,
        sha256_file,
    )

REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
OUTPUT_FIELDS = [
    "instance_id",
    "repo",
    "github_issue_number",
    "base_commit",
    "created_at_utc",
    "dataset_created_at_historical_utc",
    "github_api_created_at_utc",
    "dataset_vs_api_delta_seconds",
    "timestamp_verification_status",
    "issue_url",
    "issue_is_pull_request",
    "language",
    "license",
    "fail_to_pass_count",
    "screen_status",
]


def parse_instance_issue_number(repo: str, instance_id: str) -> int | None:
    """Extract the terminal numeric issue ID only when instance/repo prefixes agree."""
    if not isinstance(repo, str) or not REPO_PATTERN.fullmatch(repo):
        return None
    if not isinstance(instance_id, str):
        return None
    expected_prefix = repo.replace("/", "__").casefold() + "-"
    if not instance_id.casefold().startswith(expected_prefix):
        return None
    suffix = instance_id[len(expected_prefix):]
    if not suffix.isdigit():
        return None
    number = int(suffix)
    return number if number > 0 else None


def parse_utc_timestamp(value: Any) -> datetime | None:
    """Parse an explicit UTC ISO-8601 timestamp; reject naive or non-UTC values."""
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        return None
    return parsed.astimezone(timezone.utc)


def reconcile_candidate_row(
    row: dict[str, Any],
    issue_payload: dict[str, Any],
    cutoff: datetime = CUTOFF,
) -> dict[str, Any]:
    """Compare an API issue record with the historical candidate's date and use API time."""
    result = dict(row)
    repo = str(row.get("repo", ""))
    instance_id = str(row.get("instance_id", ""))
    issue_number = parse_instance_issue_number(repo, instance_id)
    result["github_issue_number"] = issue_number or ""
    result["dataset_created_at_historical_utc"] = row.get("created_at_utc", "")
    result["github_api_created_at_utc"] = ""
    result["dataset_vs_api_delta_seconds"] = ""
    result["timestamp_verification_status"] = "unverified"
    result["issue_url"] = ""
    result["issue_is_pull_request"] = False

    if issue_number is None:
        status = "instance_id_repo_mapping_invalid"
    elif issue_payload.get("_http_status") == 404:
        status = "github_issue_not_found"
    elif issue_payload.get("_http_status") is not None:
        status = "github_api_http_error_" + str(issue_payload.get("_http_status"))
    elif issue_payload.get("_error"):
        status = "github_api_request_error"
    else:
        if issue_payload.get("number") != issue_number:
            status = "github_issue_number_mismatch"
        else:
            expected_repo_url = "https://api.github.com/repos/" + repo
            actual_repo_url = issue_payload.get("repository_url")
            if not isinstance(actual_repo_url, str) or actual_repo_url.rstrip("/").casefold() != expected_repo_url.casefold():
                status = "github_repository_identity_mismatch"
            else:
                api_time = parse_utc_timestamp(issue_payload.get("created_at"))
                dataset_time = parse_utc_timestamp(row.get("created_at_utc"))
                if api_time is None:
                    status = "github_created_at_not_explicit_utc"
                elif dataset_time is None:
                    status = "historical_dataset_date_invalid"
                else:
                    delta = int((api_time - dataset_time).total_seconds())
                    result["github_api_created_at_utc"] = api_time.isoformat().replace("+00:00", "Z")
                    result["dataset_vs_api_delta_seconds"] = delta
                    result["issue_url"] = str(issue_payload.get("html_url") or "")
                    result["issue_is_pull_request"] = isinstance(issue_payload.get("pull_request"), dict)
                    if delta == 0:
                        status = "exact_match"
                    elif abs(delta) == 1:
                        status = "one_second_difference"
                    else:
                        status = "timestamp_mismatch"

                    # Never use the historical assumed value for selection. Use the
                    # explicit UTC time returned by GitHub, and retain a mismatch flag.
                    result["created_at_utc"] = result["github_api_created_at_utc"]
                    if abs(delta) <= 1 and api_time >= cutoff:
                        result["screen_status"] = "metadata_candidate_api_timestamp_verified"
                    elif abs(delta) <= 1:
                        status = "api_timestamp_before_cutoff"
                        result["screen_status"] = "excluded_api_timestamp_before_cutoff"
                    else:
                        result["screen_status"] = "excluded_timestamp_reconciliation_required"

    result["timestamp_verification_status"] = status
    if status not in {"exact_match", "one_second_difference"}:
        result["screen_status"] = "excluded:" + status
        result["created_at_utc"] = ""
    elif status == "one_second_difference" and issue_payload.get("created_at"):
        result["screen_status"] = "review_one_second_difference"
    return result


def fetch_github_issue(repo: str, number: int, token: str | None = None, retries: int = 3) -> dict[str, Any]:
    """Fetch one public GitHub issue/PR metadata record, with bounded retries."""
    url = "https://api.github.com/repos/" + quote(repo, safe="/") + "/issues/" + str(number)
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "SWE-rebench-V2-timestamp-provenance-audit",
    }
    if token:
        headers["Authorization"] = "Bearer " + token

    for attempt in range(retries + 1):
        request = Request(url, headers=headers, method="GET")
        try:
            with urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
                if not isinstance(payload, dict):
                    return {"_error": "GitHub API response was not a JSON object"}
                return payload
        except HTTPError as exc:
            if exc.code == 404:
                return {"_http_status": 404}
            if exc.code in {403, 429, 500, 502, 503, 504} and attempt < retries:
                retry_after = exc.headers.get("Retry-After")
                delay = min(max(float(retry_after), 0.0), 15.0) if retry_after else min(2 ** attempt, 8)
                time.sleep(delay)
                continue
            return {"_http_status": exc.code}
        except (URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            if attempt < retries:
                time.sleep(min(2 ** attempt, 8))
                continue
            return {"_error": type(exc).__name__}
    return {"_error": "retry_exhausted"}


def load_historical_candidates(parquet_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Reconstruct the former screening pool only for API reconciliation, never acceptance."""
    if parquet_path.stat().st_size != EXPECTED_BYTES:
        raise ValueError("Pinned Parquet size mismatch")
    if sha256_file(parquet_path) != EXPECTED_SHA256:
        raise ValueError("Pinned Parquet SHA-256 mismatch")

    import pyarrow.parquet as pq

    parquet = pq.ParquetFile(parquet_path)
    if parquet.metadata.num_rows != EXPECTED_ROWS:
        raise ValueError("Pinned Parquet row count mismatch")
    schema_types = {name: str(parquet.schema_arrow.field(name).type) for name in SAFE_COLUMNS}
    table = parquet.read(columns=SAFE_COLUMNS, use_threads=True)
    records = table.to_pylist()

    # This is intentionally labelled historical-only: it reproduces the old
    # screening pool so its issue identifiers can be checked against GitHub.
    summary, candidates = audit_records(
        records,
        schema_types,
        naive_policy="assume_utc_historical_only",
    )
    summary["candidate_inventory_use"] = "historical_id_reconstruction_for_github_api_reconciliation_only"
    summary["not_valid_for_confirmatory_selection_until_api_reconciliation"] = True
    return candidates, summary


def reconcile_candidates(
    candidates: list[dict[str, Any]],
    token: str | None = None,
    max_workers: int = 6,
) -> list[dict[str, Any]]:
    def one(row: dict[str, Any]) -> dict[str, Any]:
        number = parse_instance_issue_number(str(row.get("repo", "")), str(row.get("instance_id", "")))
        if number is None:
            return reconcile_candidate_row(row, {"_error": "invalid instance_id/repo mapping"})
        payload = fetch_github_issue(str(row["repo"]), number, token=token)
        return reconcile_candidate_row(row, payload)

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(one, candidates))


def write_report(
    candidates: list[dict[str, Any]],
    reconciled: list[dict[str, Any]],
    audit_summary: dict[str, Any],
    output_csv: Path,
    output_json: Path,
) -> dict[str, Any]:
    counts = Counter(row["timestamp_verification_status"] for row in reconciled)
    eligible = [
        row for row in reconciled
        if row["timestamp_verification_status"] == "exact_match"
        and row.get("created_at_utc")
        and row.get("screen_status") == "metadata_candidate_api_timestamp_verified"
    ]
    one_second = [
        row for row in reconciled
        if row["timestamp_verification_status"] == "one_second_difference"
        and row.get("created_at_utc")
        and row.get("screen_status") == "review_one_second_difference"
    ]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(eligible)

    summary = {
        "record_type": "swe_rebench_v2_github_issue_created_at_reconciliation",
        "dataset_id": "PrimeIntellect/SWE-rebench-V2-Filtered-Verified",
        "dataset_revision": "fb9aa226b2ce37c708ea7732e7b980abacdadb67",
        "dataset_sha256": EXPECTED_SHA256,
        "candidate_input_scope": "historical metadata-screen candidates only; not all 6,272 rows",
        "historical_candidate_rows": len(candidates),
        "api_results": dict(sorted(counts.items())),
        "exact_api_timestamp_matches": counts.get("exact_match", 0),
        "one_second_differences_requiring_explicit_review": counts.get("one_second_difference", 0),
        "timestamp_mismatches": counts.get("timestamp_mismatch", 0),
        "exact_api_verified_post_cutoff_rows": len(eligible),
        "one_second_difference_rows_not_auto_admitted": len(one_second),
        "candidate_inventory_audit": audit_summary,
        "github_rest_timestamps_returned_in_utc_iso8601": True,
        "cohort_rebuild_gate": (
            "PASS_FOR_HISTORICAL_CANDIDATE_POOL_ONLY"
            if len(eligible) == len(candidates)
            else "BLOCKED_REQUIRES_ROW_LEVEL_REVIEW"
        ),
        "accepted_confirmatory_cases": 0,
        "model_loaded": False,
        "model_inference_performed": False,
        "fine_tuning_performed": False,
        "upstream_tests_executed": False,
        "limitations": [
            "The GitHub issue API timestamp, not the timezone-naive dataset string, is used for the verified output CSV.",
            "Only rows in the historical 347-row candidate inventory are reconciled; this does not re-evaluate all possible false negatives in the 6,272-row source snapshot.",
            "One-second differences are retained separately and are not automatically admitted to the verified candidate CSV.",
            "A passing date reconciliation does not establish source-code license eligibility, defect validity, independence, ground truth, E1/E2/E3 sufficiency, human review approval, or inference authorization.",
        ],
    }
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Exact pinned Parquet file")
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--max-workers", type=int, default=6)
    args = parser.parse_args(argv)
    if args.max_workers < 1 or args.max_workers > 12:
        parser.error("--max-workers must be between 1 and 12")

    try:
        candidates, audit_summary = load_historical_candidates(args.input)
        summary = write_report(
            candidates,
            reconcile_candidates(candidates, token=os.environ.get("GITHUB_TOKEN"), max_workers=args.max_workers),
            audit_summary,
            args.output_csv,
            args.output_json,
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
