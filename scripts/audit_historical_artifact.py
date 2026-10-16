from __future__ import annotations

"""Fail-closed, no-inference audit for a previously archived confirmatory run."""

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

ARTIFACT_ROOT = "confirmatory-output/"
ARTIFACT_MANIFEST = ARTIFACT_ROOT + "artifact_manifest.json"
REQUIRED_FINAL_FILES = frozenset(
    {
        "environment.json",
        "confirmatory_evaluation.json",
        "case_level_analysis.json",
        "primary_analysis.json",
        "confirmatory_qa_report.json",
        "confirmatory_records.jsonl",
        "benchmark_manifest.json",
    }
)


class AuditFailure(ValueError):
    """Raised when the archive cannot be proven complete and byte-consistent."""


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(archive: zipfile.ZipFile, path: str) -> Any:
    try:
        return json.loads(archive.read(path).decode("utf-8"))
    except (KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuditFailure(f"cannot parse {path}: {type(exc).__name__}: {exc}") from exc


def audit_archive(
    archive_path: Path | str,
    *,
    expected_sha256: str,
    expected_run_record_count: int,
) -> dict[str, Any]:
    """Validate archive identity, every manifest-listed file, and the record set.

    expected_sha256 must come from a trusted, out-of-band pin (for the frozen
    historical artifact, the GitHub Actions artifact digest). The function never
    extracts files to the repository and never executes model code.
    """
    path = Path(archive_path)
    if not path.is_file():
        raise AuditFailure(f"archive does not exist or is not a file: {path}")
    if len(expected_sha256) != 64 or any(c not in "0123456789abcdef" for c in expected_sha256.lower()):
        raise AuditFailure("expected_sha256 must be a 64-character hexadecimal digest")
    if type(expected_run_record_count) is not int or expected_run_record_count < 1:
        raise AuditFailure("expected_run_record_count must be a positive integer")

    actual_archive_sha256 = _sha256_file(path)
    if actual_archive_sha256.lower() != expected_sha256.lower():
        raise AuditFailure(
            "archive SHA-256 mismatch: "
            f"expected={expected_sha256.lower()} actual={actual_archive_sha256}"
        )

    try:
        archive = zipfile.ZipFile(path, "r")
    except (OSError, zipfile.BadZipFile) as exc:
        raise AuditFailure(f"invalid ZIP archive: {type(exc).__name__}: {exc}") from exc

    with archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise AuditFailure("ZIP contains duplicate entry names")
        bad_member = archive.testzip()
        if bad_member is not None:
            raise AuditFailure(f"ZIP CRC/integrity check failed for entry: {bad_member}")
        if ARTIFACT_MANIFEST not in names:
            raise AuditFailure(f"missing pinned historical artifact manifest: {ARTIFACT_MANIFEST}")

        artifact_manifest = _read_json(archive, ARTIFACT_MANIFEST)
        if not isinstance(artifact_manifest, dict):
            raise AuditFailure("artifact_manifest.json must contain a JSON object")
        gate = artifact_manifest.get("finalization_gate")
        if not isinstance(gate, dict) or gate.get("status") != "complete":
            raise AuditFailure("archive finalization_gate is not complete")
        if gate.get("expected_run_record_count") != expected_run_record_count:
            raise AuditFailure(
                "manifest record-count contract mismatch: "
                f"expected={expected_run_record_count} "
                f"manifest={gate.get('expected_run_record_count')!r}"
            )
        required_final = gate.get("required_final_files")
        if not isinstance(required_final, list) or not REQUIRED_FINAL_FILES.issubset(set(required_final)):
            raise AuditFailure("finalization_gate omits one or more required final files")

        listed_files = artifact_manifest.get("files")
        if not isinstance(listed_files, list) or not listed_files:
            raise AuditFailure("artifact manifest files must be a non-empty list")

        errors: list[str] = []
        manifest_paths: set[str] = set()
        for item in listed_files:
            if not isinstance(item, dict):
                errors.append("artifact manifest contains a malformed file record")
                continue
            rel_path = item.get("path")
            expected_size = item.get("bytes")
            expected_file_sha = item.get("sha256")
            if not isinstance(rel_path, str) or not rel_path:
                errors.append("artifact manifest file path must be a non-empty string")
                continue
            posix_path = PurePosixPath(rel_path)
            if posix_path.is_absolute() or ".." in posix_path.parts or "\\" in rel_path:
                errors.append(f"unsafe artifact manifest path: {rel_path!r}")
                continue
            if rel_path in manifest_paths:
                errors.append(f"duplicate artifact manifest path: {rel_path}")
                continue
            manifest_paths.add(rel_path)
            if type(expected_size) is not int or expected_size < 0:
                errors.append(f"invalid byte count for {rel_path}")
            if not isinstance(expected_file_sha, str) or len(expected_file_sha) != 64:
                errors.append(f"invalid SHA-256 for {rel_path}")
                continue
            member_path = ARTIFACT_ROOT + rel_path
            if member_path not in names:
                errors.append(f"manifest-listed file is missing from ZIP: {member_path}")
                continue
            data = archive.read(member_path)
            actual_file_sha = _sha256_bytes(data)
            if type(expected_size) is int and len(data) != expected_size:
                errors.append(
                    f"byte-size mismatch for {rel_path}: expected={expected_size} actual={len(data)}"
                )
            if actual_file_sha.lower() != expected_file_sha.lower():
                errors.append(
                    f"SHA-256 mismatch for {rel_path}: "
                    f"expected={expected_file_sha.lower()} actual={actual_file_sha}"
                )

        missing_required = sorted(REQUIRED_FINAL_FILES - manifest_paths)
        if missing_required:
            errors.append(f"manifest omits required final files: {missing_required}")

        expected_root_members = {ARTIFACT_MANIFEST} | {ARTIFACT_ROOT + p for p in manifest_paths}
        actual_root_members = {n for n in names if n.startswith(ARTIFACT_ROOT) and not n.endswith("/")}
        unmanifested_root_members = sorted(actual_root_members - expected_root_members)
        if unmanifested_root_members:
            errors.append(f"unmanifested file(s) inside artifact root: {unmanifested_root_members}")
        if errors:
            raise AuditFailure("; ".join(errors))

        benchmark = _read_json(archive, ARTIFACT_ROOT + "benchmark_manifest.json")
        pilot = _read_json(archive, ARTIFACT_ROOT + "pilot_manifest.json")
        evaluation = _read_json(archive, ARTIFACT_ROOT + "confirmatory_evaluation.json")
        if not all(isinstance(obj, dict) for obj in (benchmark, pilot, evaluation)):
            raise AuditFailure("benchmark, pilot, and evaluation manifests must be JSON objects")
        if benchmark.get("status") != "frozen":
            raise AuditFailure("archived benchmark manifest is not frozen")
        case_ids = benchmark.get("case_ids")
        conditions = pilot.get("conditions")
        generation = pilot.get("generation")
        seeds = generation.get("seeds") if isinstance(generation, dict) else None
        if not isinstance(case_ids, list) or not case_ids or not all(isinstance(x, str) and x for x in case_ids):
            raise AuditFailure("benchmark manifest case_ids must be a non-empty list of strings")
        if len(case_ids) != len(set(case_ids)):
            raise AuditFailure("benchmark manifest case_ids are not unique")
        if not isinstance(conditions, list) or not conditions or not all(isinstance(x, str) and x for x in conditions):
            raise AuditFailure("pilot manifest conditions must be a non-empty list of strings")
        if len(conditions) != len(set(conditions)):
            raise AuditFailure("pilot manifest conditions are not unique")
        if not isinstance(seeds, list) or not seeds or any(type(seed) is not int for seed in seeds):
            raise AuditFailure("pilot manifest seeds must be a non-empty list of integers")
        if len(seeds) != len(set(seeds)):
            raise AuditFailure("pilot manifest seeds are not unique")

        computed_expected = len(case_ids) * len(conditions) * len(seeds)
        if computed_expected != expected_run_record_count:
            raise AuditFailure(
                "record-count contract does not match the manifest cross product: "
                f"cases={len(case_ids)} conditions={len(conditions)} seeds={len(seeds)} "
                f"product={computed_expected} expected={expected_run_record_count}"
            )
        if evaluation.get("status") != "complete":
            raise AuditFailure("confirmatory_evaluation.json is not marked complete")
        if evaluation.get("expected_records") != expected_run_record_count or evaluation.get("found_records") != expected_run_record_count:
            raise AuditFailure("confirmatory evaluation record counts do not match the pinned contract")
        if evaluation.get("missing_files") != []:
            raise AuditFailure("confirmatory evaluation reports missing files")

        records_path = ARTIFACT_ROOT + "confirmatory_records.jsonl"
        try:
            record_text = archive.read(records_path).decode("utf-8")
        except (KeyError, UnicodeDecodeError) as exc:
            raise AuditFailure(f"cannot read confirmatory JSONL: {type(exc).__name__}: {exc}") from exc
        lines = record_text.splitlines()
        if not lines or any(not line.strip() for line in lines):
            raise AuditFailure("confirmatory_records.jsonl is empty or contains blank lines")
        rows: list[dict[str, Any]] = []
        try:
            for line_number, line in enumerate(lines, start=1):
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise AuditFailure(f"record line {line_number} is not a JSON object")
                rows.append(row)
        except json.JSONDecodeError as exc:
            raise AuditFailure(f"invalid JSONL record: {exc}") from exc

        expected_keys = {
            (case_id, condition, seed)
            for case_id in case_ids
            for condition in conditions
            for seed in seeds
        }
        observed_keys: list[tuple[Any, Any, Any]] = []
        source_commits: set[str] = set()
        row_errors: list[str] = []
        for idx, row in enumerate(rows, start=1):
            key = (row.get("case_id"), row.get("condition"), row.get("seed"))
            observed_keys.append(key)
            if key not in expected_keys:
                row_errors.append(f"record {idx} has unexpected case/condition/seed identity: {key!r}")
            source_commit = row.get("source_commit")
            if not isinstance(source_commit, str) or not source_commit.strip():
                row_errors.append(f"record {idx} has missing source_commit")
            else:
                source_commits.add(source_commit)
            raw_output = row.get("raw_output")
            raw_hash = row.get("raw_output_sha256")
            if not isinstance(raw_output, str) or not isinstance(raw_hash, str):
                row_errors.append(f"record {idx} lacks string raw_output/raw_output_sha256")
            elif _sha256_bytes(raw_output.encode("utf-8")) != raw_hash:
                row_errors.append(f"record {idx} raw_output SHA-256 mismatch")

        duplicate_keys = sorted(
            (key for key in set(observed_keys) if observed_keys.count(key) > 1),
            key=lambda key: repr(key),
        )
        if duplicate_keys:
            row_errors.append(f"duplicate record identities: {duplicate_keys[:5]!r}")
        observed_set = set(observed_keys)
        missing_keys = expected_keys - observed_set
        if missing_keys:
            row_errors.append(f"missing expected record identities: {sorted(missing_keys, key=repr)[:5]!r}")
        if len(rows) != expected_run_record_count:
            row_errors.append(
                f"JSONL row-count mismatch: expected={expected_run_record_count} actual={len(rows)}"
            )
        if len(source_commits) != 1:
            row_errors.append(f"expected one source_commit across archived records, found {len(source_commits)}")

        by_condition = evaluation.get("by_condition")
        if not isinstance(by_condition, dict):
            row_errors.append("confirmatory evaluation by_condition must be an object")
        else:
            for condition in conditions:
                expected_condition_n = len(case_ids) * len(seeds)
                summary = by_condition.get(condition)
                if not isinstance(summary, dict):
                    row_errors.append(f"evaluation summary missing for condition {condition!r}")
                    continue
                if summary.get("n_expected") != expected_condition_n or summary.get("n_found") != expected_condition_n:
                    row_errors.append(f"evaluation counts do not match expected count for {condition!r}")
                actual_condition_n = sum(1 for row in rows if row.get("condition") == condition)
                if actual_condition_n != expected_condition_n:
                    row_errors.append(
                        f"JSONL rows for {condition!r}: expected={expected_condition_n} actual={actual_condition_n}"
                    )
        if row_errors:
            raise AuditFailure("; ".join(row_errors))

        return {
            "status": "pass",
            "archive": path.name,
            "archive_sha256": actual_archive_sha256,
            "zip_crc": "pass",
            "manifest_declared_files": len(manifest_paths),
            "files_checked": len(manifest_paths),
            "file_hash_or_size_mismatches": 0,
            "expected_run_records": expected_run_record_count,
            "found_run_records": len(rows),
            "unique_run_records": len(set(observed_keys)),
            "source_commits": sorted(source_commits),
            "conditions": {condition: sum(1 for row in rows if row.get("condition") == condition) for condition in conditions},
            "message": "Pinned historical archive verified; no extraction or model inference performed.",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, help="Path to the downloaded immutable artifact ZIP.")
    parser.add_argument("--expected-sha256", required=True, help="Trusted SHA-256 pin for the whole ZIP.")
    parser.add_argument("--expected-run-record-count", type=int, required=True)
    args = parser.parse_args()
    try:
        summary = audit_archive(
            args.archive,
            expected_sha256=args.expected_sha256,
            expected_run_record_count=args.expected_run_record_count,
        )
    except (AuditFailure, OSError) as exc:
        print(json.dumps({"status": "fail", "error": str(exc)}, indent=2, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
