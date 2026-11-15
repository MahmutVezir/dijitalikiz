#!/usr/bin/env python3
"""Metadata-only audit of a pinned SWE-rebench V2 Filtered-Verified Parquet file."""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

DATASET_ID = "PrimeIntellect/SWE-rebench-V2-Filtered-Verified"
DATASET_REVISION = "fb9aa226b2ce37c708ea7732e7b980abacdadb67"
EXPECTED_SHA256 = "7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9"
EXPECTED_BYTES = 226272977
EXPECTED_ROWS = 6272
CUTOFF = datetime(2024, 9, 20, 0, 0, 0, tzinfo=timezone.utc)
SAFE_COLUMNS = [
    "instance_id", "repo", "base_commit", "created_at", "language",
    "license", "FAIL_TO_PASS", "problem_statement",
]
CSV_FIELDS = [
    "instance_id", "repo", "base_commit", "created_at_utc",
    "language", "license", "fail_to_pass_count", "screen_status",
]
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_created_at(value, naive_policy="reject"):
    """Return (UTC datetime or None, representation, naive_assumed_utc).

    Naive timestamps are rejected by default. The only permissive mode is
    explicitly named for historical reproduction and must never be used for
    confirmatory cohort construction.
    """
    if naive_policy not in {"reject", "assume_utc_historical_only"}:
        raise ValueError("naive_policy must be reject or assume_utc_historical_only")
    if value is None or value == "":
        return None, "missing", False
    if isinstance(value, datetime):
        if value.tzinfo is None:
            if naive_policy == "reject":
                return None, "datetime_naive_timezone_unverified", False
            return value.replace(tzinfo=timezone.utc), "datetime_naive_assumed_utc_historical_only", True
        return value.astimezone(timezone.utc), "datetime_tz", False
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc), "unix_ms", False
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            if naive_policy == "reject":
                return None, "string_naive_timezone_unverified", False
            return parsed.replace(tzinfo=timezone.utc), "string_naive_assumed_utc_historical_only", True
        return parsed.astimezone(timezone.utc), "string_tz", False
    return None, "unsupported_type:" + type(value).__name__, False


def audit_records(records, schema_types, naive_policy="reject"):
    if naive_policy not in {"reject", "assume_utc_historical_only"}:
        raise ValueError("naive_policy must be reject or assume_utc_historical_only")
    language_counts = Counter()
    license_counts = Counter()
    date_representation_counts = Counter()
    exclusions = Counter()
    ids = Counter(str(row.get("instance_id") or "") for row in records)
    normalized = []
    python_rows = 0
    python_post_cutoff = 0
    naive_utc_assumptions = 0
    malformed_dates = 0
    missing_dates = 0
    timezone_unverified_dates = 0

    for row in records:
        language = str(row.get("language") or "<MISSING>").strip()
        license_name = str(row.get("license") or "<MISSING>").strip()
        language_counts[language] += 1
        license_counts[license_name] += 1
        try:
            created, representation, naive = parse_created_at(row.get("created_at"), naive_policy=naive_policy)
        except (ValueError, OverflowError, OSError, TypeError):
            created, representation, naive = None, "invalid", False
        date_representation_counts[representation] += 1
        if representation == "missing":
            missing_dates += 1
        if representation == "invalid" or representation.startswith("unsupported_type:"):
            malformed_dates += 1
        if representation in {"string_naive_timezone_unverified", "datetime_naive_timezone_unverified"}:
            timezone_unverified_dates += 1
        if naive:
            naive_utc_assumptions += 1

        is_python = language.casefold() == "python"
        if is_python:
            python_rows += 1
        is_post_cutoff = created is not None and created >= CUTOFF
        if is_python and is_post_cutoff:
            python_post_cutoff += 1

        reasons = []
        instance_id = str(row.get("instance_id") or "").strip()
        repo = str(row.get("repo") or "").strip()
        base_commit = str(row.get("base_commit") or "").strip()
        statement = row.get("problem_statement")
        fail_to_pass = row.get("FAIL_TO_PASS")
        if not is_python:
            reasons.append("not_python")
        if representation in {"string_naive_timezone_unverified", "datetime_naive_timezone_unverified"}:
            reasons.append("created_at_timezone_unverified")
        elif not is_post_cutoff:
            reasons.append("missing_or_pre_cutoff_date")
        if not instance_id:
            reasons.append("missing_instance_id")
        if ids[instance_id] > 1:
            reasons.append("duplicate_instance_id")
        if not REPO_RE.fullmatch(repo):
            reasons.append("invalid_repo_identifier")
        if not SHA_RE.fullmatch(base_commit):
            reasons.append("invalid_base_commit")
        if not isinstance(statement, str) or not statement.strip():
            reasons.append("empty_problem_statement")
        if not isinstance(fail_to_pass, (list, tuple)) or not fail_to_pass:
            reasons.append("empty_fail_to_pass")
        if not license_name or license_name == "<MISSING>":
            reasons.append("missing_source_license")

        is_candidate = not reasons
        if not is_candidate:
            exclusions.update(reasons)
        normalized.append({
            "instance_id": instance_id,
            "repo": repo,
            "base_commit": base_commit,
            "created_at_utc": created.isoformat().replace("+00:00", "Z") if created else "",
            "language": language,
            "license": license_name,
            "fail_to_pass_count": len(fail_to_pass) if isinstance(fail_to_pass, (list, tuple)) else 0,
            "screen_status": "metadata_candidate_unreviewed" if is_candidate else "excluded:" + ";".join(reasons),
            "_candidate": is_candidate,
        })

    candidate_rows = [row for row in normalized if row.pop("_candidate")]
    distinct_repos = sorted({row["repo"] for row in candidate_rows})
    candidate_license_counts = Counter(row["license"] for row in candidate_rows)
    candidate_language_counts = Counter(row["language"] for row in candidate_rows)
    summary = {
        "record_type": "swe_rebench_filtered_verified_metadata_feasibility",
        "dataset_id": DATASET_ID,
        "dataset_file_revision": DATASET_REVISION,
        "dataset_file_sha256": EXPECTED_SHA256,
        "expected_file_bytes": EXPECTED_BYTES,
        "expected_train_rows": EXPECTED_ROWS,
        "observed_train_rows": len(records),
        "cutoff_utc_inclusive": CUTOFF.isoformat().replace("+00:00", "Z"),
        "safe_columns_read": SAFE_COLUMNS,
        "excluded_solution_bearing_columns": ["patch", "test_patch", "pr_description", "interface", "meta"],
        "parquet_schema_types_for_read_columns": schema_types,
        "date_representation_counts": dict(sorted(date_representation_counts.items())),
        "naive_timestamp_assumed_utc_count": naive_utc_assumptions,
        "timezone_unverified_created_at_count": timezone_unverified_dates,
        "created_at_timezone_review": "UNRESOLVED_SOURCE_SCHEMA_LINEAGE",
        "created_at_parser_policy": naive_policy,
        "created_at_naive_utc_assumptions_permitted_for_confirmatory_use": False,
        "missing_created_at_count": missing_dates,
        "malformed_created_at_count": malformed_dates,
        "language_counts": dict(sorted(language_counts.items())),
        "distinct_language_values_observed": len(language_counts),
        "source_license_counts": dict(sorted(license_counts.items())),
        "python_rows": python_rows,
        "python_rows_on_or_after_cutoff": python_post_cutoff,
        "metadata_candidates_after_required_field_and_duplicate_checks": len(candidate_rows),
        "candidate_distinct_repositories": len(distinct_repos),
        "candidate_repositories": distinct_repos,
        "candidate_license_counts": dict(sorted(candidate_license_counts.items())),
        "candidate_language_counts": dict(sorted(candidate_language_counts.items())),
        "exclusion_reason_counts_nonexclusive": dict(sorted(exclusions.items())),
        "accepted_confirmatory_cases": 0,
        "upstream_tests_executed": False,
        "model_loaded": False,
        "model_inference_performed": False,
        "fine_tuning_performed": False,
        "limitations": [
            "Metadata candidates are not accepted confirmatory cases.",
            "No source-repository license file was inspected in this workflow.",
            "No buggy/fixed test pair was run in this workflow.",
            "No root-cause or E1/E2/E3 human adjudication was performed.",
            "No cross-source exposure, issue duplication, or training-contamination review was performed.",
            "The upstream dataset card describes created_at as int64 Unix milliseconds, while the filtered dataset card describes it as string; source schema lineage remains unresolved.",
            "Naive created_at values are rejected by default and cannot enter the candidate cohort until their timezone is independently verified.",
            "The historical assume_utc_historical_only option exists solely to reproduce the old feasibility screen and is not confirmatory evidence."
            "Only safe metadata columns were read; solution-bearing columns were not loaded into the Arrow table.",
        ],
    }
    return summary, candidate_rows


def run_audit(input_path: Path, output_json: Path, output_csv: Path, require_pinned: bool = True, naive_policy: str = "reject"):
    if not input_path.is_file():
        raise FileNotFoundError(input_path)
    file_bytes = input_path.stat().st_size
    file_hash = sha256_file(input_path)
    if require_pinned and file_bytes != EXPECTED_BYTES:
        raise ValueError(f"File size mismatch: expected {EXPECTED_BYTES}, got {file_bytes}")
    if require_pinned and file_hash != EXPECTED_SHA256:
        raise ValueError(f"SHA-256 mismatch: expected {EXPECTED_SHA256}, got {file_hash}")

    import pyarrow.parquet as pq

    parquet = pq.ParquetFile(input_path)
    if require_pinned and parquet.metadata.num_rows != EXPECTED_ROWS:
        raise ValueError(f"Parquet row count mismatch: expected {EXPECTED_ROWS}, got {parquet.metadata.num_rows}")
    schema_types = {name: str(parquet.schema_arrow.field(name).type) for name in SAFE_COLUMNS}
    table = parquet.read(columns=SAFE_COLUMNS, use_threads=True)
    records = table.to_pylist()
    if len(records) != parquet.metadata.num_rows:
        raise ValueError("Arrow row count differs from Parquet footer")

    summary, candidates = audit_records(records, schema_types, naive_policy=naive_policy)
    summary["observed_file_bytes"] = file_bytes
    summary["observed_file_sha256"] = file_hash
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, extrasaction="raise")
        writer.writeheader()
        writer.writerows(candidates)
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--allow-unpinned-fixture", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        summary = run_audit(args.input, args.output_json, args.output_csv, require_pinned=not args.allow_unpinned_fixture)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
