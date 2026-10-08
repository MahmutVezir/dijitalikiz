from __future__ import annotations

import argparse
import json
from pathlib import Path


EXPECTED_RUN_COUNT = 30


def build(runs_dir: Path, output: Path) -> int:
    if not runs_dir.is_dir():
        raise RuntimeError(f"Pilot runs directory is missing: {runs_dir}")

    records = []
    for path in sorted(runs_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        records.append(payload)

    if len(records) != EXPECTED_RUN_COUNT:
        raise RuntimeError(
            f"Frozen pilot JSONL export requires exactly {EXPECTED_RUN_COUNT} run records; "
            f"found {len(records)}."
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    return len(records)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export the 30 frozen pilot run records to deterministic JSONL.")
    parser.add_argument("--runs-dir", default="data/pilot/runs")
    parser.add_argument("--output", default="data/pilot/pilot_records.jsonl")
    args = parser.parse_args()

    count = build(Path(args.runs_dir), Path(args.output))
    print(f"EXPORTED PILOT JSONL: {count} records -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
