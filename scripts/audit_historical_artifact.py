from __future__ import annotations

"""Fail-closed, no-inference audit for a previously archived confirmatory run."""

import argparse
import hashlib
import json
import math
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.models import ResearchCase

ARTIFACT_ROOT = "confirmatory-output/"
ARTIFACT_MANIFEST = ARTIFACT_ROOT + "artifact_manifest.json"
PINNED_SOURCE_COMMIT = "e1e083f5400432b98143bdb35ff2c5b435ea8f6e"
PINNED_MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"
PINNED_MODEL_REVISION = "aa8e72537993ba99e69dfaafa59ed015b17504d1"
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
REQUIRED_ARCHIVE_FILES = REQUIRED_FINAL_FILES | frozenset(
    {"pilot_manifest.json", "PROMPT_TEMPLATE.txt", "SYSTEM_PROMPT.txt"}
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


def _read_json(archive: zipfile.ZipFile, member: str) -> Any:
    try:
        return json.loads(archive.read(member).decode("utf-8"))
    except (KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuditFailure(f"cannot parse {member}: {type(exc).__name__}: {exc}") from exc


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _require_numeric_match(record: dict[str, Any], key: str, expected: object, row_number: int, errors: list[str]) -> None:
    observed = record.get(key)
    if not _is_number(expected) or not _is_number(observed) or float(observed) != float(expected):
        errors.append(f"record {row_number} {key} mismatch: expected={expected!r} actual={observed!r}")


def audit_archive(
    archive_path: Path | str,
    *,
    expected_sha256: str,
    expected_run_record_count: int,
) -> dict[str, Any]:
    """Verify the exact ZIP, all manifest files, frozen settings and record identities.

    The expected ZIP digest and source commit are fixed out-of-band pins for the
    2026-10-09 historical confirmatory artifact. The archive is read in place;
    files are not extracted or rewritten and no model code is executed.
    """
    path = Path(archive_path)
    if not path.is_file():
        raise AuditFailure(f"archive does not exist or is not a file: {path}")
    if len(expected_sha256) != 64 or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256):
        raise AuditFailure("expected_sha256 must be a 64-character hexadecimal digest")
    if type(expected_run_record_count) is not int or expected_run_record_count < 1:
        raise AuditFailure("expected_run_record_count must be a positive integer")

    actual_archive_sha256 = _sha256_file(path)
    if actual_archive_sha256.lower() != expected_sha256.lower():
        raise AuditFailure(f"archive SHA-256 mismatch: expected={expected_sha256.lower()} actual={actual_archive_sha256}")

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
            raise AuditFailure(f"missing historical artifact manifest: {ARTIFACT_MANIFEST}")

        artifact_manifest = _read_json(archive, ARTIFACT_MANIFEST)
        if not isinstance(artifact_manifest, dict):
            raise AuditFailure("artifact_manifest.json must contain a JSON object")
        gate = artifact_manifest.get("finalization_gate")
        if not isinstance(gate, dict) or gate.get("status") != "complete":
            raise AuditFailure("archive finalization_gate is not complete")
        if gate.get("expected_run_record_count") != expected_run_record_count:
            raise AuditFailure(f"manifest expected record count mismatch: {gate.get('expected_run_record_count')!r}")
        if artifact_manifest.get("run_record_count") != expected_run_record_count:
            raise AuditFailure(f"artifact manifest run_record_count mismatch: {artifact_manifest.get('run_record_count')!r}")
        required_final = gate.get("required_final_files")
        if not isinstance(required_final, list) or not all(isinstance(item, str) for item in required_final) or not REQUIRED_FINAL_FILES.issubset(set(required_final)):
            raise AuditFailure("finalization_gate omits one or more required final files")

        listed_files = artifact_manifest.get("files")
        if not isinstance(listed_files, list) or not listed_files:
            raise AuditFailure("artifact manifest files must be a non-empty list")
        if artifact_manifest.get("file_count") != len(listed_files):
            raise AuditFailure(f"artifact manifest file_count mismatch: declared={artifact_manifest.get('file_count')!r} actual={len(listed_files)}")

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
            safe_path = PurePosixPath(rel_path)
            if safe_path.is_absolute() or ".." in safe_path.parts or "\\" in rel_path:
                errors.append(f"unsafe artifact manifest path: {rel_path!r}")
                continue
            if rel_path in manifest_paths:
                errors.append(f"duplicate artifact manifest path: {rel_path}")
                continue
            manifest_paths.add(rel_path)
            if type(expected_size) is not int or expected_size < 0:
                errors.append(f"invalid byte count for {rel_path}")
            if not isinstance(expected_file_sha, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_file_sha):
                errors.append(f"invalid SHA-256 for {rel_path}")
                continue
            member_path = ARTIFACT_ROOT + rel_path
            if member_path not in names:
                errors.append(f"manifest-listed file is missing from ZIP: {member_path}")
                continue
            data = archive.read(member_path)
            actual_file_sha = _sha256_bytes(data)
            if type(expected_size) is int and len(data) != expected_size:
                errors.append(f"byte-size mismatch for {rel_path}: expected={expected_size} actual={len(data)}")
            if actual_file_sha.lower() != expected_file_sha.lower():
                errors.append(f"SHA-256 mismatch for {rel_path}: expected={expected_file_sha.lower()} actual={actual_file_sha}")
        missing_required = sorted(REQUIRED_ARCHIVE_FILES - manifest_paths)
        if missing_required:
            errors.append(f"manifest omits required archive files: {missing_required}")
        expected_root_members = {ARTIFACT_MANIFEST} | {ARTIFACT_ROOT + rel for rel in manifest_paths}
        actual_root_members = {name for name in names if name.startswith(ARTIFACT_ROOT) and not name.endswith("/")}
        unmanifested = sorted(actual_root_members - expected_root_members)
        if unmanifested:
            errors.append(f"unmanifested file(s) inside artifact root: {unmanifested}")
        if errors:
            raise AuditFailure("; ".join(errors))

        benchmark = _read_json(archive, ARTIFACT_ROOT + "benchmark_manifest.json")
        pilot = _read_json(archive, ARTIFACT_ROOT + "pilot_manifest.json")
        evaluation = _read_json(archive, ARTIFACT_ROOT + "confirmatory_evaluation.json")
        if not all(isinstance(obj, dict) for obj in (benchmark, pilot, evaluation)):
            raise AuditFailure("benchmark, pilot and evaluation manifests must be JSON objects")
        if benchmark.get("status") != "frozen":
            raise AuditFailure("archived benchmark manifest is not frozen")
        case_ids = benchmark.get("case_ids")
        conditions = pilot.get("conditions")
        generation = pilot.get("generation")
        seeds = generation.get("seeds") if isinstance(generation, dict) else None
        model = pilot.get("model")
        prompt_info = pilot.get("prompt")
        system_info = pilot.get("system_prompt")
        if not isinstance(case_ids, list) or not case_ids or not all(isinstance(x, str) and x for x in case_ids):
            raise AuditFailure("benchmark manifest case_ids must be a non-empty list of strings")
        if len(case_ids) != len(set(case_ids)):
            raise AuditFailure("benchmark manifest case_ids are not unique")
        if not isinstance(conditions, list) or conditions != ["standard", "ccdg"]:
            raise AuditFailure("pilot manifest conditions must be the frozen ['standard', 'ccdg'] list")
        if not isinstance(seeds, list) or not seeds or any(type(seed) is not int for seed in seeds):
            raise AuditFailure("pilot manifest seeds must be a non-empty list of integers")
        if len(seeds) != len(set(seeds)):
            raise AuditFailure("pilot manifest seeds are not unique")
        if seeds != [42, 43, 44, 45, 46]:
            raise AuditFailure(f"pilot seeds do not match frozen historical seeds: {seeds!r}")
        if not isinstance(model, dict) or model.get("model_id") != PINNED_MODEL_ID or model.get("revision") != PINNED_MODEL_REVISION:
            raise AuditFailure("archived pilot model ID/revision do not match the frozen historical model")
        if model.get("precision") != "float16" or model.get("quantization") != "none":
            raise AuditFailure("archived pilot model precision/quantization do not match the frozen profile")
        if not isinstance(generation, dict) or generation.get("do_sample") is not True:
            raise AuditFailure("archived pilot generation must set do_sample=true")
        if not _is_number(generation.get("temperature")) or float(generation["temperature"]) != 0.2:
            raise AuditFailure("archived pilot temperature does not match frozen value 0.2")
        if not _is_number(generation.get("top_p")) or float(generation["top_p"]) != 1.0:
            raise AuditFailure("archived pilot top_p does not match frozen value 1.0")
        if type(generation.get("max_new_tokens")) is not int or generation["max_new_tokens"] != 256:
            raise AuditFailure("archived pilot max_new_tokens does not match frozen value 256")
        if not isinstance(prompt_info, dict) or not isinstance(system_info, dict):
            raise AuditFailure("pilot prompt/system_prompt manifest entries must be objects")

        computed_expected = len(case_ids) * len(conditions) * len(seeds)
        if computed_expected != expected_run_record_count:
            raise AuditFailure(f"record-count contract mismatch: {len(case_ids)} cases x {len(conditions)} conditions x {len(seeds)} seeds = {computed_expected}, expected {expected_run_record_count}")
        if evaluation.get("status") != "complete":
            raise AuditFailure("confirmatory_evaluation.json is not marked complete")
        if evaluation.get("expected_records") != expected_run_record_count or evaluation.get("found_records") != expected_run_record_count:
            raise AuditFailure("confirmatory evaluation record counts do not match pinned contract")
        if evaluation.get("missing_files") != []:
            raise AuditFailure("confirmatory evaluation reports missing files")
        evaluation_conditions = evaluation.get("by_condition")
        if not isinstance(evaluation_conditions, dict):
            raise AuditFailure("confirmatory evaluation by_condition must be an object")

        prompt_text = archive.read(ARTIFACT_ROOT + "PROMPT_TEMPLATE.txt").decode("utf-8")
        system_text = archive.read(ARTIFACT_ROOT + "SYSTEM_PROMPT.txt").decode("utf-8")
        if _sha256_bytes(prompt_text.encode("utf-8")) != prompt_info.get("sha256"):
            raise AuditFailure("PROMPT_TEMPLATE.txt SHA-256 does not match pilot manifest")
        if _sha256_bytes(system_text.encode("utf-8")) != system_info.get("sha256"):
            raise AuditFailure("SYSTEM_PROMPT.txt SHA-256 does not match pilot manifest")

        prompt_hashes: dict[tuple[str, str], tuple[str, str]] = {}
        for case_id in case_ids:
            case_payload = _read_json(archive, ARTIFACT_ROOT + "cases/" + case_id + ".json")
            if not isinstance(case_payload, dict):
                raise AuditFailure(f"archived case {case_id} must be a JSON object")
            case = ResearchCase.from_dict(case_payload)
            if case.case_id != case_id:
                raise AuditFailure(f"archived case file ID mismatch for {case_id}: {case.case_id!r}")
            for condition in conditions:
                context = render_standard_context(case) if condition == "standard" else render_ccdg_context(case)
                prompt_hashes[(case_id, condition)] = (
                    _sha256_bytes((prompt_text + "\n\n" + context).encode("utf-8")),
                    _sha256_bytes(context.encode("utf-8")),
                )

        try:
            record_text = archive.read(ARTIFACT_ROOT + "confirmatory_records.jsonl").decode("utf-8")
        except (KeyError, UnicodeDecodeError) as exc:
            raise AuditFailure(f"cannot read confirmatory JSONL: {type(exc).__name__}: {exc}") from exc
        lines = record_text.splitlines()
        if not lines or any(not line.strip() for line in lines):
            raise AuditFailure("confirmatory_records.jsonl is empty or contains blank lines")
        rows: list[dict[str, Any]] = []
        try:
            for index, line in enumerate(lines, start=1):
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise AuditFailure(f"record line {index} is not a JSON object")
                rows.append(row)
        except json.JSONDecodeError as exc:
            raise AuditFailure(f"invalid JSONL record: {exc}") from exc

        expected_keys = {(case_id, condition, seed) for case_id in case_ids for condition in conditions for seed in seeds}
        observed_keys: list[tuple[str, str, int]] = []
        source_commits: set[str] = set()
        row_errors: list[str] = []
        for index, row in enumerate(rows, start=1):
            case_id, condition, seed = row.get("case_id"), row.get("condition"), row.get("seed")
            if not isinstance(case_id, str) or not isinstance(condition, str) or type(seed) is not int:
                row_errors.append(f"record {index} has malformed case/condition/seed identity")
            else:
                key = (case_id, condition, seed)
                observed_keys.append(key)
                if key not in expected_keys:
                    row_errors.append(f"record {index} has unexpected case/condition/seed identity: {key!r}")
            source_commit = row.get("source_commit")
            if source_commit != PINNED_SOURCE_COMMIT:
                row_errors.append(f"record {index} source_commit mismatch: expected={PINNED_SOURCE_COMMIT} actual={source_commit!r}")
            if isinstance(source_commit, str) and source_commit:
                source_commits.add(source_commit)
            if isinstance(case_id, str) and isinstance(condition, str) and (case_id, condition) in prompt_hashes:
                expected_prompt_sha, expected_context_sha = prompt_hashes[(case_id, condition)]
                if row.get("prompt_sha256") != expected_prompt_sha:
                    row_errors.append(f"record {index} prompt_sha256 mismatch for {case_id}/{condition}")
                if row.get("context_sha256") != expected_context_sha:
                    row_errors.append(f"record {index} context_sha256 mismatch for {case_id}/{condition}")
            if row.get("system_prompt_sha256") != system_info.get("sha256"):
                row_errors.append(f"record {index} system_prompt_sha256 mismatch")
            if row.get("model_id") != model.get("model_id"):
                row_errors.append(f"record {index} model_id mismatch")
            if row.get("model_revision") != model.get("revision"):
                row_errors.append(f"record {index} model_revision mismatch")
            if row.get("model_dtype") != model.get("precision"):
                row_errors.append(f"record {index} model_dtype mismatch")
            if row.get("quantization") != model.get("quantization"):
                row_errors.append(f"record {index} quantization mismatch")
            _require_numeric_match(row, "temperature", generation.get("temperature"), index, row_errors)
            _require_numeric_match(row, "top_p", generation.get("top_p"), index, row_errors)
            if type(row.get("max_new_tokens")) is not int or row.get("max_new_tokens") != generation.get("max_new_tokens"):
                row_errors.append(f"record {index} max_new_tokens mismatch: expected={generation.get('max_new_tokens')!r} actual={row.get('max_new_tokens')!r}")
            raw_output, raw_hash = row.get("raw_output"), row.get("raw_output_sha256")
            if not isinstance(raw_output, str) or not isinstance(raw_hash, str):
                row_errors.append(f"record {index} lacks string raw_output/raw_output_sha256")
            elif _sha256_bytes(raw_output.encode("utf-8")) != raw_hash:
                row_errors.append(f"record {index} raw_output SHA-256 mismatch")

        counts = Counter(observed_keys)
        duplicates = sorted((key for key, count in counts.items() if count > 1), key=repr)
        if duplicates:
            row_errors.append(f"duplicate record identities: {duplicates[:5]!r}")
        missing_keys = expected_keys - set(observed_keys)
        if missing_keys:
            row_errors.append(f"missing expected record identities: {sorted(missing_keys, key=repr)[:5]!r}")
        if len(rows) != expected_run_record_count:
            row_errors.append(f"JSONL row-count mismatch: expected={expected_run_record_count} actual={len(rows)}")
        if source_commits != {PINNED_SOURCE_COMMIT}:
            row_errors.append(f"source_commit set does not match the pinned source commit: {sorted(source_commits)}")
        for condition in conditions:
            expected_condition_n = len(case_ids) * len(seeds)
            summary = evaluation_conditions.get(condition)
            if not isinstance(summary, dict):
                row_errors.append(f"evaluation summary missing for condition {condition!r}")
                continue
            if summary.get("n_expected") != expected_condition_n or summary.get("n_found") != expected_condition_n:
                row_errors.append(f"evaluation counts mismatch for condition {condition!r}")
            observed_condition_n = sum(1 for row in rows if row.get("condition") == condition)
            if observed_condition_n != expected_condition_n:
                row_errors.append(f"JSONL condition count mismatch for {condition!r}: expected={expected_condition_n} actual={observed_condition_n}")
        if row_errors:
            raise AuditFailure("; ".join(row_errors))

        return {
            "status": "pass",
            "archive": path.name,
            "archive_bytes": path.stat().st_size,
            "archive_sha256": actual_archive_sha256,
            "zip_crc": "pass",
            "manifest_declared_files": len(manifest_paths),
            "files_checked": len(manifest_paths),
            "file_hash_or_size_mismatches": 0,
            "expected_run_records": expected_run_record_count,
            "found_run_records": len(rows),
            "unique_run_records": len(set(observed_keys)),
            "source_commits": sorted(source_commits),
            "model_id": model["model_id"],
            "model_revision": model["revision"],
            "model_dtype": model["precision"],
            "quantization": model["quantization"],
            "generation": {
                "do_sample": generation["do_sample"],
                "temperature": generation["temperature"],
                "top_p": generation["top_p"],
                "max_new_tokens": generation["max_new_tokens"],
                "seeds": seeds,
            },
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
