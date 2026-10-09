from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REQUIRED_ARTIFACTS = {
    "environment.json",
    "confirmatory_evaluation.json",
    "case_level_analysis.json",
    "primary_analysis.json",
    "confirmatory_qa_report.json",
    "confirmatory_records.jsonl",
    "benchmark_manifest.json",
    "pilot_manifest.json",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify the complete confirmatory artifact and reject unmanifested files."
    )
    parser.add_argument("--artifact-root", default="data/benchmark")
    parser.add_argument("--manifest", default="data/benchmark/artifact_manifest.json")
    args = parser.parse_args()

    root = Path(args.artifact_root).resolve()
    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        raise RuntimeError("Artifact manifest must contain a non-empty files list.")
    if manifest.get("file_count") != len(entries):
        raise RuntimeError("Artifact manifest file_count does not match the files list.")
    if manifest.get("finalization_gate", {}).get("status") != "complete":
        raise RuntimeError("Confirmatory finalization gate is not marked complete.")

    declared_paths = [entry.get("path") for entry in entries]
    if not all(isinstance(path, str) and path for path in declared_paths):
        raise RuntimeError("Artifact manifest contains an empty or invalid path.")
    if len(declared_paths) != len(set(declared_paths)):
        raise RuntimeError("Artifact manifest contains duplicate paths.")

    declared_set: set[str] = set()
    for entry in entries:
        relative = Path(entry["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimeError(f"Unsafe path in artifact manifest: {entry['path']!r}")
        path = (root / relative).resolve()
        if root != path and root not in path.parents:
            raise RuntimeError(f"Artifact path escapes artifact root: {entry['path']!r}")
        if path == manifest_path:
            raise RuntimeError("The artifact manifest must not hash itself.")
        if not path.is_file():
            raise RuntimeError(f"Missing artifact: {path}")
        if not isinstance(entry.get("bytes"), int) or path.stat().st_size != entry["bytes"]:
            raise RuntimeError(f"Size mismatch: {path}")
        expected_sha = entry.get("sha256")
        if not isinstance(expected_sha, str) or len(expected_sha) != 64:
            raise RuntimeError(f"Invalid SHA-256 declaration: {entry['path']}")
        if sha256_file(path) != expected_sha:
            raise RuntimeError(f"Checksum mismatch: {path}")
        declared_set.add(relative.as_posix())

    actual_set = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.resolve() != manifest_path
    }
    missing = sorted(actual_set - declared_set)
    absent = sorted(declared_set - actual_set)
    if missing or absent:
        raise RuntimeError(
            f"Artifact file inventory mismatch; unmanifested={missing}, missing={absent}"
        )

    missing_required = sorted(REQUIRED_ARTIFACTS - actual_set)
    if missing_required:
        raise RuntimeError(f"Missing required confirmatory artifacts: {missing_required}")

    benchmark_manifest = json.loads(
        (root / "benchmark_manifest.json").read_text(encoding="utf-8")
    )
    if benchmark_manifest.get("status") != "frozen":
        raise RuntimeError("Delivered benchmark manifest is not frozen.")
    case_ids = benchmark_manifest.get("case_ids", [])
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise RuntimeError("Delivered benchmark case IDs are empty or duplicated.")

    pilot_manifest = json.loads(
        (root / "pilot_manifest.json").read_text(encoding="utf-8")
    )
    conditions = pilot_manifest.get("conditions", [])
    seeds = pilot_manifest.get("generation", {}).get("seeds", [])
    if not conditions or len(conditions) != len(set(conditions)):
        raise RuntimeError("Pilot/confirmatory condition list is invalid.")
    if not seeds or len(seeds) != len(set(seeds)):
        raise RuntimeError("Pilot/confirmatory seed list is invalid.")

    expected_names = {
        f"{case_id}__{condition}__seed{seed}.json"
        for case_id in case_ids
        for condition in conditions
        for seed in seeds
    }
    runs = root / "runs"
    actual_runs = {path.name for path in runs.glob("*.json") if path.is_file()}
    if actual_runs != expected_names:
        raise RuntimeError(
            "Delivered run set differs from the frozen design; "
            f"missing={sorted(expected_names - actual_runs)}, "
            f"unexpected={sorted(actual_runs - expected_names)}"
        )
    expected_count = len(expected_names)
    if manifest.get("run_record_count") != expected_count:
        raise RuntimeError(
            f"Manifest run_record_count {manifest.get('run_record_count')} != {expected_count}"
        )
    if manifest.get("finalization_gate", {}).get("expected_run_record_count") != expected_count:
        raise RuntimeError("Finalization-gate run count disagrees with the frozen design.")

    jsonl = root / "confirmatory_records.jsonl"
    with jsonl.open("r", encoding="utf-8") as stream:
        lines = [line for line in stream if line.strip()]
    if len(lines) != expected_count:
        raise RuntimeError(
            f"Confirmatory JSONL record count {len(lines)} != {expected_count}"
        )
    for line_number, line in enumerate(lines, start=1):
        try:
            json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Invalid JSONL record on line {line_number}: {exc}"
            ) from exc

    print(
        json.dumps(
            {
                "status": "pass",
                "run_record_count": len(actual_runs),
                "file_count": len(entries),
                "required_artifacts": len(REQUIRED_ARTIFACTS),
                "unmanifested_files": 0,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
