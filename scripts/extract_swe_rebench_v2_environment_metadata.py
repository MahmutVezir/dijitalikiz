#!/usr/bin/env python3
"""Extract one pinned SWE-rebench V2 environment record; never execute upstream code.

This is metadata-only. It does not install upstream packages, run tests/builds,
load a model, or perform inference.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

DATASET_ID = "PrimeIntellect/SWE-rebench-V2-Filtered-Verified"
DATASET_REVISION = "fb9aa226b2ce37c708ea7732e7b980abacdadb67"
EXPECTED_PARQUET_SHA256 = "7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9"
EXPECTED_PARQUET_BYTES = 226272977
EXPECTED_PARQUET_ROWS = 6272
EXPECTED_PYARROW_VERSION = "19.0.1"

ROW_FIELDS = (
    "instance_id",
    "repo",
    "base_commit",
    "image_name",
    "language",
    "license",
    "created_at",
    "install_config",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def json_safe(value: Any) -> Any:
    """Convert Arrow/Python values into deterministic JSON-safe values."""
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("Non-finite float in environment metadata.")
        return value
    if isinstance(value, Mapping):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if hasattr(value, "isoformat") and callable(value.isoformat):
        return value.isoformat()
    raise TypeError(f"Unsupported metadata value type: {type(value).__name__}")


def extract_environment_record(table: pa.Table, instance_id: str) -> dict[str, Any]:
    missing = sorted(set(ROW_FIELDS) - set(table.column_names))
    if missing:
        raise ValueError("Parquet columns missing: " + ", ".join(missing))

    install_type = table.schema.field("install_config").type
    if not pa.types.is_struct(install_type):
        raise ValueError("install_config must be a Parquet struct; refusing schema coercion.")

    mask = pc.equal(table["instance_id"], pa.scalar(instance_id))
    selected = table.filter(mask)
    if selected.num_rows != 1:
        raise ValueError(
            f"Expected exactly one row for {instance_id}; found {selected.num_rows}."
        )

    arrow_row = selected.slice(0, 1).to_pylist()[0]
    record = {field: json_safe(arrow_row[field]) for field in ROW_FIELDS}
    config = record["install_config"]
    if not isinstance(config, dict) or not config:
        raise ValueError("The target row has no non-empty structured install_config.")
    for field in ("repo", "base_commit", "image_name", "language"):
        if not isinstance(record[field], str) or not record[field].strip():
            raise ValueError(f"Target row has missing/invalid {field}.")
    if record["instance_id"] != instance_id:
        raise ValueError("Extracted row identity mismatch.")
    return record


def build_output(
    record: dict[str, Any],
    parquet_sha256: str,
    parquet_bytes: int,
    parquet_rows: int,
) -> dict[str, Any]:
    metadata_hash = hashlib.sha256(canonical_json_bytes(record)).hexdigest()
    return {
        "record_type": "swe_rebench_v2_environment_metadata_only",
        "dataset": {
            "dataset_id": DATASET_ID,
            "revision": DATASET_REVISION,
            "parquet_sha256": parquet_sha256,
            "parquet_bytes": parquet_bytes,
            "parquet_rows": parquet_rows,
            "reader": {"pyarrow": pa.__version__},
        },
        "row_locator": {"field": "instance_id", "value": record["instance_id"]},
        "environment_metadata": record,
        "environment_metadata_sha256": metadata_hash,
        "execution_boundary": {
            "upstream_repository_checkout": False,
            "upstream_package_install": False,
            "upstream_test_or_build": False,
            "model_loading": False,
            "model_inference": False,
            "fine_tuning": False,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    if pa.__version__ != EXPECTED_PYARROW_VERSION:
        raise SystemExit(
            f"Expected pyarrow {EXPECTED_PYARROW_VERSION}; found {pa.__version__}."
        )
    if not args.input.is_file():
        raise SystemExit("Pinned Parquet file is missing.")
    file_bytes = args.input.stat().st_size
    if file_bytes != EXPECTED_PARQUET_BYTES:
        raise SystemExit(f"Parquet byte length mismatch: {file_bytes}.")
    actual_sha256 = sha256_file(args.input)
    if actual_sha256 != EXPECTED_PARQUET_SHA256:
        raise SystemExit("Pinned Parquet SHA-256 mismatch.")

    parquet = pq.ParquetFile(args.input)
    row_count = parquet.metadata.num_rows
    if row_count != EXPECTED_PARQUET_ROWS:
        raise SystemExit(f"Parquet row count mismatch: {row_count}.")
    table = parquet.read(columns=list(ROW_FIELDS))
    record = extract_environment_record(table, args.instance_id)
    output = build_output(record, actual_sha256, file_bytes, row_count)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": "PASS_METADATA_ONLY_EXTRACTION",
        "instance_id": args.instance_id,
        "repo": record["repo"],
        "environment_metadata_sha256": output["environment_metadata_sha256"],
        "upstream_test_or_build": False,
        "model_inference": False,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
