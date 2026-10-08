from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_RUN_COUNT = 30
REQUIRED_FINAL_FILES = (
    Path("data/pilot/environment.json"),
    Path("data/pilot/pilot_evaluation.json"),
    Path("data/pilot/case_level_analysis.json"),
    Path("data/pilot/pilot_qa_report.json"),
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

    missing = [str(path) for path in REQUIRED_FINAL_FILES if not path.is_file()]
    if missing:
        raise RuntimeError(f"Required finalized pilot artifact(s) missing: {missing}")

    files = required + list(REQUIRED_FINAL_FILES)

    payload = {
        "version": "1.1",
        "finalization_gate": {
            "expected_run_record_count": EXPECTED_RUN_COUNT,
            "required_final_files": [str(path) for path in REQUIRED_FINAL_FILES],
            "status": "complete",
        },
        "files": [
            {
                "path": str(path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in files
        ],
    }
    payload["file_count"] = len(payload["files"])
    payload["run_record_count"] = len(required)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "pass",
        "run_record_count": len(required),
        "file_count": len(files),
        "output": str(output),
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
