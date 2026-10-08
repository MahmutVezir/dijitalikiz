from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


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
    required = sorted(runs_dir.glob("*.json"))
    fixed = [
        Path("data/pilot/environment.json"),
        Path("data/pilot/pilot_evaluation.json"),
        Path("data/pilot/case_level_analysis.json"),
    ]
    files = required + [path for path in fixed if path.is_file()]

    if not fixed[-1].is_file():
        raise RuntimeError("Case-level analysis is missing; artifact manifest cannot be finalized.")

    payload = {
        "version": "1.0",
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
