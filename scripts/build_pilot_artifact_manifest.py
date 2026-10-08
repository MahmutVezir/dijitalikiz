from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_RUN_COUNT = 30
PILOT_ROOT = Path("data/pilot")
REQUIRED_FINAL_FILES = (
    Path("environment.json"),
    Path("pilot_evaluation.json"),
    Path("case_level_analysis.json"),
    Path("pilot_qa_report.json"),
    Path("pilot_records.jsonl"),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build immutable pilot artifact checksum manifest.")
    parser.add_argument("--runs-dir", default="data/pilot/runs")
    parser.add_argument("--output", default="data/pilot/artifact_manifest.json")
    args = parser.parse_args()

    runs_dir = Path(args.runs_dir)
    if not runs_dir.is_dir():
        raise RuntimeError(f"Pilot runs directory is missing: {runs_dir}")

    required = sorted(runs_dir.glob("*.json"))
    if len(required) != EXPECTED_RUN_COUNT:
        raise RuntimeError(
            f"Pilot artifact manifest requires exactly {EXPECTED_RUN_COUNT} run records; found {len(required)}."
        )

    missing = [str(PILOT_ROOT / path) for path in REQUIRED_FINAL_FILES if not path.is_file()]
    if missing:
        raise RuntimeError(f"Required finalized pilot artifact(s) missing: {missing}")

    files = required + [PILOT_ROOT / path for path in REQUIRED_FINAL_FILES]
    try:
        relative_files = [path.relative_to(PILOT_ROOT) for path in files]
    except ValueError as exc:
        raise RuntimeError("All pilot artifact paths must live below data/pilot.") from exc

    payload = {
        "version": "1.2",
        "root": "data/pilot",
        "finalization_gate": {
            "expected_run_record_count": EXPECTED_RUN_COUNT,
            "required_final_files": [str(path) for path in REQUIRED_FINAL_FILES],
            "status": "complete",
        },
        "files": [
            {
                "path": str(relative_path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path, relative_path in zip(files, relative_files)
        ],
    }
    payload["file_count"] = len(payload["files"])
    payload["run_record_count"] = len(required)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "run_record_count": len(required),
                "file_count": len(files),
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
