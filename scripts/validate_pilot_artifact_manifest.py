from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_RUN_COUNT = 30
REQUIRED_FINAL_FILES = {
    "environment.json",
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
    if gate.get("status") != "complete":
        errors.append("manifest finalization_gate.status must be complete")
    if gate.get("expected_run_record_count") != EXPECTED_RUN_COUNT:
        errors.append(
            f"manifest finalization_gate.expected_run_record_count must be {EXPECTED_RUN_COUNT}"
        )

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
        root = artifact_root.resolve()
        if root not in path.parents:
            errors.append(f"artifact path escapes artifact root: {rel}")
            continue

        if not path.is_file():
            errors.append(f"missing artifact file: {rel}")
            continue

        expected_bytes = entry.get("bytes")
        if not isinstance(expected_bytes, int) or expected_bytes < 0:
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

    run_entries = [
        rel for rel in seen
        if rel.startswith("runs/") and rel.endswith(".json")
    ]
    if len(run_entries) != EXPECTED_RUN_COUNT:
        errors.append(
            f"manifest must list exactly {EXPECTED_RUN_COUNT} run JSON files; found {len(run_entries)}"
        )

    if manifest.get("run_record_count") != EXPECTED_RUN_COUNT:
        errors.append(
            f"manifest run_record_count must be {EXPECTED_RUN_COUNT}, "
            f"got {manifest.get('run_record_count')!r}"
        )

    missing_final = sorted(REQUIRED_FINAL_FILES - seen)
    if missing_final:
        errors.append(
            "manifest missing required finalized files: " + ", ".join(missing_final)
        )

    gate_files = gate.get("required_final_files")
    if not isinstance(gate_files, list):
        errors.append("manifest finalization_gate.required_final_files must be a list")
    else:
        normalized = {str(Path(value)) for value in gate_files}
        if normalized != REQUIRED_FINAL_FILES:
            errors.append("manifest finalization_gate.required_final_files mismatch")

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
