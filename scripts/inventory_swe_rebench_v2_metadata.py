from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

DATASET_ID = "PrimeIntellect/SWE-rebench-V2-Filtered-Verified"
DATASET_REVISION = "6a0d56b425a893b018616587cdb71aa499c5fc99"
PARQUET_PATH = "data/train-00000-of-00001.parquet"
EXPECTED_SHA256 = "7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9"
MODEL_RELEASE_CUTOFF = datetime(2024, 9, 20, tzinfo=timezone.utc)
BASE_URL = (
    "https://huggingface.co/datasets/"
    f"{DATASET_ID}/resolve/{DATASET_REVISION}/{PARQUET_PATH}"
)
READ_COLUMNS = (
    "instance_id",
    "repo",
    "base_commit",
    "created_at",
    "language",
    "license",
    "FAIL_TO_PASS",
    "problem_statement",
)
CANDIDATE_FIELDS = (
    "instance_id",
    "repo",
    "base_commit",
    "created_at_utc",
    "language",
    "license",
    "status",
)
SHA40 = re.compile(r"^[0-9a-fA-F]{40}$")


class InventoryError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_pinned_parquet(destination: Path, retries: int = 3) -> str:
    request = urllib.request.Request(
        BASE_URL,
        headers={"User-Agent": "dijitalikiz-metadata-audit/1.0"},
    )
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            digest = hashlib.sha256()
            with urllib.request.urlopen(request, timeout=90) as response:
                with destination.open("wb") as output:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        output.write(chunk)
                        digest.update(chunk)
            actual = digest.hexdigest()
            if actual != EXPECTED_SHA256:
                destination.unlink(missing_ok=True)
                raise InventoryError(
                    f"Parquet SHA-256 mismatch: expected {EXPECTED_SHA256}, got {actual}"
                )
            return actual
        except Exception as exc:
            last_error = exc
            destination.unlink(missing_ok=True)
            if attempt < retries:
                time.sleep(attempt * 3)
    raise InventoryError(f"Could not download pinned Parquet: {last_error}") from last_error


def parse_created_at(value: Any, arrow_type: str) -> datetime:
    if value is None:
        raise ValueError("created_at is null")
    if isinstance(value, datetime):
        parsed = value
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    if isinstance(value, bool):
        raise ValueError("created_at cannot be boolean")
    if isinstance(value, int):
        if "int" not in arrow_type.lower():
            raise ValueError(f"integer created_at disagrees with Arrow type {arrow_type}")
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
    if isinstance(value, str):
        if "string" not in arrow_type.lower():
            raise ValueError(f"string created_at disagrees with Arrow type {arrow_type}")
        raw = value.strip().replace("Z", "+00:00")
        parsed = datetime.fromisoformat(raw)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    raise ValueError(f"unsupported created_at value type: {type(value).__name__}")


def inspect_parquet(path: Path, parquet_sha256: str) -> tuple[dict[str, Any], list[dict[str, str]]]:
    parquet = pq.ParquetFile(path)
    schema = parquet.schema_arrow
    available = set(schema.names)
    missing = sorted(set(READ_COLUMNS) - available)
    if missing:
        raise InventoryError(f"Required metadata columns are missing: {missing}")

    schema_types = {name: str(schema.field(name).type) for name in READ_COLUMNS}
    created_at_type = schema_types["created_at"]
    if created_at_type not in {"int64", "timestamp[ms]", "timestamp[us]", "timestamp[ns]"}:
        raise InventoryError(
            f"Unexpected created_at Parquet type {created_at_type!r}; "
            "stop rather than silently coercing a schema change."
        )

    total_rows = parquet.metadata.num_rows
    language_counts: Counter[str] = Counter()
    license_counts: Counter[str] = Counter()
    rows: list[dict[str, Any]] = []
    min_created: datetime | None = None
    max_created: datetime | None = None

    for batch in parquet.iter_batches(batch_size=128, columns=list(READ_COLUMNS)):
        columns = {name: batch.column(batch.schema.get_field_index(name)).to_pylist() for name in READ_COLUMNS}
        for index in range(batch.num_rows):
            language = str(columns["language"][index] or "").strip()
            license_value = str(columns["license"][index] or "").strip()
            language_counts[language or "<MISSING>"] += 1
            license_counts[license_value or "<MISSING>"] += 1

            record = {
                "instance_id": str(columns["instance_id"][index] or "").strip(),
                "repo": str(columns["repo"][index] or "").strip(),
                "base_commit": str(columns["base_commit"][index] or "").strip(),
                "created_at_raw": columns["created_at"][index],
                "language": language,
                "license": license_value,
                "fail_to_pass_count": len(columns["FAIL_TO_PASS"][index] or []),
                "problem_statement_present": bool(
                    str(columns["problem_statement"][index] or "").strip()
                ),
            }
            try:
                created = parse_created_at(record.pop("created_at_raw"), created_at_type)
            except Exception as exc:
                raise InventoryError(
                    f"Cannot parse created_at for instance_id={record['instance_id']!r}: {exc}"
                ) from exc
            record["created_at"] = created
            min_created = created if min_created is None else min(min_created, created)
            max_created = created if max_created is None else max(max_created, created)
            rows.append(record)

    if len(rows) != total_rows:
        raise InventoryError(f"Row count mismatch: Parquet metadata={total_rows}, scanned={len(rows)}")

    all_ids = Counter(row["instance_id"] for row in rows)
    python_rows = [row for row in rows if row["language"].casefold() == "python"]
    post_release_rows = [
        row for row in python_rows if row["created_at"] >= MODEL_RELEASE_CUTOFF
    ]

    exclusion_counts: Counter[str] = Counter()
    candidates: list[dict[str, str]] = []
    for row in post_release_rows:
        reasons: list[str] = []
        if not row["instance_id"]:
            reasons.append("missing_instance_id")
        elif all_ids[row["instance_id"]] > 1:
            reasons.append("duplicate_instance_id")
        if not row["repo"]:
            reasons.append("missing_repo")
        if not row["base_commit"] or not SHA40.fullmatch(row["base_commit"]):
            reasons.append("invalid_base_commit")
        if not row["license"]:
            reasons.append("missing_source_license")
        if row["fail_to_pass_count"] == 0:
            reasons.append("empty_fail_to_pass")
        if not row["problem_statement_present"]:
            reasons.append("empty_problem_statement")

        if reasons:
            exclusion_counts.update(reasons)
            continue

        candidates.append(
            {
                "instance_id": row["instance_id"],
                "repo": row["repo"],
                "base_commit": row["base_commit"].lower(),
                "created_at_utc": row["created_at"].isoformat().replace("+00:00", "Z"),
                "language": row["language"],
                "license": row["license"],
                "status": "METADATA_CANDIDATE_ONLY_NOT_ACCEPTED",
            }
        )

    candidate_licenses = Counter(row["license"] for row in candidates)
    candidate_projects = Counter(row["repo"] for row in candidates)
    post_date_licenses = Counter(row["license"] for row in post_release_rows)
    candidate_dates = [datetime.fromisoformat(r["created_at_utc"].replace("Z", "+00:00")) for r in candidates]

    report: dict[str, Any] = {
        "record_type": "swe_rebench_v2_filtered_verified_metadata_only_inventory",
        "status": "METADATA_ONLY_NO_CASES_ACCEPTED",
        "dataset_id": DATASET_ID,
        "dataset_revision": DATASET_REVISION,
        "parquet_path": PARQUET_PATH,
        "parquet_sha256_expected": EXPECTED_SHA256,
        "parquet_sha256_observed": parquet_sha256,
        "parquet_bytes": path.stat().st_size,
        "parquet_rows": total_rows,
        "parquet_schema_types_read": schema_types,
        "created_at_schema_result": "PASS_PINNED_PARQUET_SCHEMA",
        "dataset_created_at_min_utc": min_created.isoformat().replace("+00:00", "Z") if min_created else None,
        "dataset_created_at_max_utc": max_created.isoformat().replace("+00:00", "Z") if max_created else None,
        "model_id": "Qwen/Qwen2.5-3B-Instruct",
        "model_revision": "aa8e72537993ba99e69dfaafa59ed015b17504d1",
        "model_public_release_cutoff_utc_exclusive_start": MODEL_RELEASE_CUTOFF.isoformat().replace("+00:00", "Z"),
        "language_distinct_values": sorted(language_counts),
        "language_counts_all_rows": dict(sorted(language_counts.items())),
        "license_distinct_values": sorted(license_counts),
        "license_counts_all_rows": dict(sorted(license_counts.items())),
        "python_rows": len(python_rows),
        "python_rows_created_on_or_after_cutoff": len(post_release_rows),
        "python_post_cutoff_license_counts": dict(sorted(post_date_licenses.items())),
        "metadata_candidate_rows_after_basic_checks": len(candidates),
        "metadata_candidate_distinct_projects": len(candidate_projects),
        "metadata_candidate_license_counts": dict(sorted(candidate_licenses.items())),
        "metadata_candidate_project_counts": dict(sorted(candidate_projects.items())),
        "metadata_candidate_date_min_utc": min(candidate_dates).isoformat().replace("+00:00", "Z") if candidate_dates else None,
        "metadata_candidate_date_max_utc": max(candidate_dates).isoformat().replace("+00:00", "Z") if candidate_dates else None,
        "metadata_candidate_exclusion_reason_counts": dict(sorted(exclusion_counts.items())),
        "distinct_instance_id_count": len(all_ids),
        "duplicate_instance_id_value_count": sum(1 for count in all_ids.values() if count > 1),
        "accepted_confirmatory_cases": 0,
        "technical_buggy_fixed_tests_run": False,
        "source_repository_licenses_independently_reviewed": False,
        "human_root_cause_adjudication_complete": False,
        "evidence_tier_adjudication_complete": False,
        "model_inference_performed": False,
        "fine_tuning_performed": False,
        "important_limitations": [
            "Metadata candidates are not accepted confirmatory cases.",
            "The source license field is a publisher-provided metadata value and must be checked against the exact repository and commit.",
            "No project tests, root causes, evidence tiers, or model outputs were validated in this inventory.",
            "The release-date cutoff mitigates exact issue/PR post-release exposure but does not prove zero training contamination.",
            "Patch, test_patch, pr_description, interface, and meta columns were not read by the inventory scanner.",
        ],
    }
    return report, candidates


def write_outputs(output_dir: Path, report: dict[str, Any], candidates: list[dict[str, str]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "SWE_REBENCH_V2_METADATA_INVENTORY.json"
    csv_path = output_dir / "SWE_REBENCH_V2_METADATA_CANDIDATES.csv"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CANDIDATE_FIELDS)
        writer.writeheader()
        writer.writerows(candidates)

    report["output_files"] = {
        json_path.name: {
            "sha256": sha256_bytes(json_path.read_bytes()),
            "byte_length": json_path.stat().st_size,
        },
        csv_path.name: {
            "sha256": sha256_bytes(csv_path.read_bytes()),
            "byte_length": csv_path.stat().st_size,
        },
    }
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Metadata-only SWE-rebench V2 feasibility inventory.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--parquet-path", type=Path, help="Optional local Parquet for deterministic tests/manual runs.")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    downloaded = args.parquet_path is None
    parquet_path = args.parquet_path or (args.output_dir / "source.parquet")
    try:
        if downloaded:
            observed_sha = download_pinned_parquet(parquet_path)
        else:
            observed_sha = sha256_file(parquet_path)
            if observed_sha != EXPECTED_SHA256:
                raise InventoryError(
                    f"Local Parquet SHA-256 mismatch: expected {EXPECTED_SHA256}, got {observed_sha}"
                )
        report, candidates = inspect_parquet(parquet_path, observed_sha)
        write_outputs(args.output_dir, report, candidates)
        print(json.dumps({
            "status": report["status"],
            "dataset_revision": DATASET_REVISION,
            "parquet_sha256": observed_sha,
            "parquet_rows": report["parquet_rows"],
            "python_rows": report["python_rows"],
            "python_rows_created_on_or_after_cutoff": report["python_rows_created_on_or_after_cutoff"],
            "metadata_candidate_rows_after_basic_checks": report["metadata_candidate_rows_after_basic_checks"],
            "metadata_candidate_distinct_projects": report["metadata_candidate_distinct_projects"],
            "accepted_confirmatory_cases": 0,
            "model_inference_performed": False,
            "fine_tuning_performed": False,
        }, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(f"METADATA_INVENTORY_BLOCKED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    finally:
        if downloaded:
            parquet_path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
