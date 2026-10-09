from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dijitalikiz.pilot_config import (
    expected_pilot_record_count,
    expected_pilot_run_filenames,
)


PILOT_ROOT = Path("data/pilot")
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a complete SHA-256 manifest for the frozen pilot artifact."
    )
    parser.add_argument("--runs-dir", default="data/pilot/runs")
    parser.add_argument("--output", default="data/pilot/artifact_manifest.json")
    args = parser.parse_args()

    runs_dir = Path(args.runs_dir)
    canonical_runs_dir = PILOT_ROOT / "runs"
    if runs_dir.resolve() != canonical_runs_dir.resolve():
        raise RuntimeError(
            f"Artifact runs must live in {canonical_runs_dir}; got {runs_dir}."
        )
    if not runs_dir.is_dir():
        raise RuntimeError(f"Pilot runs directory is missing: {runs_dir}")

    pilot_manifest_path = PILOT_ROOT / "pilot_manifest.json"
    try:
        pilot_manifest = json.loads(pilot_manifest_path.read_text(encoding="utf-8"))
        expected_count = expected_pilot_record_count(
            pilot_manifest, require_declared=True
        )
        expected_names = expected_pilot_run_filenames(
            pilot_manifest, require_declared=True
        )
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise RuntimeError(f"Frozen pilot manifest is invalid: {exc}") from exc

    actual_names = {path.name for path in runs_dir.iterdir()}
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        unexpected = sorted(actual_names - expected_names)
        raise RuntimeError(
            "Pilot artifact run-file set mismatch; "
            f"expected {expected_count} files, found {len(actual_names)}; "
            f"missing={missing}; unexpected={unexpected}."
        )

    case_paths = [
        PILOT_ROOT / f"{case_id}.json" for case_id in pilot_manifest["cases"]
    ]
    required_paths = [PILOT_ROOT / name for name in REQUIRED_FINAL_FILES]
    missing_paths = [
        str(path)
        for path in [*required_paths, *case_paths]
        if not path.is_file()
    ]
    if missing_paths:
        raise RuntimeError(
            f"Required frozen pilot artifact file(s) missing: {missing_paths}"
        )

    output = Path(args.output)
    output_resolved = output.resolve()
    all_files = sorted(
        path
        for path in PILOT_ROOT.rglob("*")
        if path.is_file() and path.resolve() != output_resolved
    )
    relative_files = [path.relative_to(PILOT_ROOT) for path in all_files]

    payload = {
        "version": "1.3",
        "root": "data/pilot",
        "finalization_gate": {
            "expected_run_record_count": expected_count,
            "required_final_files": sorted(REQUIRED_FINAL_FILES),
            "status": "complete",
        },
        "files": [
            {
                "path": relative_path.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path, relative_path in zip(all_files, relative_files)
        ],
    }
    payload["file_count"] = len(payload["files"])
    payload["run_record_count"] = expected_count

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "run_record_count": expected_count,
                "file_count": len(all_files),
                "root": "data/pilot",
                "output": str(output),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
