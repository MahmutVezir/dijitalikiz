from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dijitalikiz.pilot_config import (
    expected_pilot_record_count,
    expected_pilot_run_filenames,
)


REQUIRED_FINAL_FILES = {
    "pilot_manifest.json",
    "PROMPT_TEMPLATE.txt",
    "SYSTEM_PROMPT.txt",
    "environment.json",
    "model_load_preflight.json",
    "pilot_evaluation.json",
    "case_level_analysis.json",
    "pilot_qa_report.json",
    "pilot_records.jsonl",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative_path(value: str) -> Path | None:
    candidate = Path(value)
    if candidate.is_absolute() or any(part == ".." for part in candidate.parts):
        return None
    return candidate


def validate(artifact_root: Path, manifest_path: Path) -> list[str]:
    errors: list[str] = []
    artifact_root = artifact_root.resolve()
    manifest_path = manifest_path.resolve()

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"manifest unreadable: {type(exc).__name__}: {exc}"]

    if manifest.get("root") != "data/pilot":
        errors.append("manifest root must be data/pilot")

    gate = manifest.get("finalization_gate")
    if not isinstance(gate, dict):
        errors.append("manifest finalization_gate must be an object")
        gate = {}

    pilot_config = None
    expected_count = None
    expected_run_entries: set[str] = set()
    try:
        pilot_config = json.loads(
            (artifact_root / "pilot_manifest.json").read_text(encoding="utf-8")
        )
        expected_count = expected_pilot_record_count(
            pilot_config, require_declared=True
        )
        expected_run_entries = {
            f"runs/{name}"
            for name in expected_pilot_run_filenames(
                pilot_config, require_declared=True
            )
        }
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        errors.append(
            "frozen pilot configuration unreadable or invalid: "
            f"{type(exc).__name__}: {exc}"
        )

    if expected_count is not None:
        if gate.get("expected_run_record_count") != expected_count:
            errors.append(
                "manifest finalization_gate.expected_run_record_count mismatch: "
                f"expected {expected_count}, got {gate.get('expected_run_record_count')!r}"
            )
    if gate.get("status") != "complete":
        errors.append("manifest finalization_gate.status must be complete")

    entries = manifest.get("files", [])
    if not isinstance(entries, list):
        return errors + ["manifest files must be a list"]

    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("manifest contains a non-object file entry")
            continue

        rel = entry.get("path")
        if not isinstance(rel, str) or not rel:
            errors.append("manifest contains an invalid file path entry")
            continue
        if rel in seen:
            errors.append(f"duplicate manifest path: {rel}")
            continue
        seen.add(rel)

        safe_rel = _safe_relative_path(rel)
        if safe_rel is None:
            errors.append(f"unsafe manifest path: {rel}")
            continue

        path = (artifact_root / safe_rel).resolve()
        if artifact_root not in path.parents:
            errors.append(f"artifact path escapes artifact root: {rel}")
            continue
        if not path.is_file():
            errors.append(f"missing artifact file: {rel}")
            continue

        expected_bytes = entry.get("bytes")
        if type(expected_bytes) is not int or expected_bytes < 0:
            errors.append(f"invalid byte count: {rel}")
        elif path.stat().st_size != expected_bytes:
            errors.append(f"byte-size mismatch: {rel}")

        expected_sha = entry.get("sha256")
        if not isinstance(expected_sha, str) or len(expected_sha) != 64:
            errors.append(f"invalid sha256: {rel}")
        elif sha256_file(path) != expected_sha:
            errors.append(f"sha256 mismatch: {rel}")

    if manifest.get("file_count") != len(entries):
        errors.append(
            f"manifest file_count mismatch: {manifest.get('file_count')!r} != {len(entries)}"
        )

    if expected_count is not None:
        if manifest.get("run_record_count") != expected_count:
            errors.append(
                "manifest run_record_count mismatch: "
                f"expected {expected_count}, got {manifest.get('run_record_count')!r}"
            )

        actual_run_entries = {
            rel for rel in seen
            if rel.startswith("runs/") and rel.endswith(".json")
        }
        if actual_run_entries != expected_run_entries:
            missing_runs = sorted(expected_run_entries - actual_run_entries)
            unexpected_runs = sorted(actual_run_entries - expected_run_entries)
            errors.append(
                "run record path set mismatch; "
                f"missing={missing_runs}; unexpected={unexpected_runs}"
            )

    required_case_files = (
        {f"{case_id}.json" for case_id in pilot_config["cases"]}
        if pilot_config is not None
        else set()
    )
    missing_required = sorted((REQUIRED_FINAL_FILES | required_case_files) - seen)
    if missing_required:
        errors.append(
            "manifest missing required frozen inputs/artifacts: "
            + ", ".join(missing_required)
        )

    gate_files = gate.get("required_final_files")
    if not isinstance(gate_files, list):
        errors.append("manifest finalization_gate.required_final_files must be a list")
    else:
        normalized = {str(Path(value)) for value in gate_files}
        if normalized != REQUIRED_FINAL_FILES:
            errors.append("manifest finalization_gate.required_final_files mismatch")

    actual_files = {
        path.relative_to(artifact_root).as_posix()
        for path in artifact_root.rglob("*")
        if path.is_file() and path.resolve() != manifest_path
    }
    unlisted_files = sorted(actual_files - seen)
    if unlisted_files:
        errors.append("unlisted artifact file(s): " + ", ".join(unlisted_files))
    listed_missing_files = sorted(seen - actual_files)
    if listed_missing_files:
        errors.append(
            "manifest lists file(s) absent from artifact root: "
            + ", ".join(listed_missing_files)
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify a completed frozen pilot artifact against its SHA-256 manifest."
    )
    parser.add_argument("--artifact-root", default="data/pilot")
    parser.add_argument("--manifest", default="data/pilot/artifact_manifest.json")
    args = parser.parse_args()

    errors = validate(Path(args.artifact_root), Path(args.manifest))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"VALID PILOT ARTIFACT: {args.artifact_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
