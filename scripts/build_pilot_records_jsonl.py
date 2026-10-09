from __future__ import annotations

import argparse
import json
from pathlib import Path

from dijitalikiz.pilot_config import (
    expected_pilot_record_count,
    expected_pilot_run_filenames,
)


MANIFEST = Path("data/pilot/pilot_manifest.json")


def build(
    runs_dir: Path,
    output: Path,
    manifest_path: Path = MANIFEST,
) -> int:
    if not runs_dir.is_dir():
        raise RuntimeError(f"Pilot runs directory is missing: {runs_dir}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected_count = expected_pilot_record_count(manifest, require_declared=True)
        expected_names = expected_pilot_run_filenames(manifest, require_declared=True)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise RuntimeError(f"Frozen pilot manifest is invalid: {exc}") from exc

    actual_names = {path.name for path in runs_dir.iterdir()}
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        unexpected = sorted(actual_names - expected_names)
        raise RuntimeError(
            "Frozen pilot run-file set mismatch; "
            f"expected {expected_count} files, found {len(actual_names)}; "
            f"missing={missing}; unexpected={unexpected}."
        )

    records = [
        json.loads((runs_dir / name).read_text(encoding="utf-8"))
        for name in sorted(expected_names)
    ]
    if len(records) != expected_count:
        raise RuntimeError(
            f"Frozen pilot JSONL export requires {expected_count} records; found {len(records)}."
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(
                json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
            )
    return len(records)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export the frozen pilot run records to deterministic JSONL."
    )
    parser.add_argument("--runs-dir", default="data/pilot/runs")
    parser.add_argument("--output", default="data/pilot/pilot_records.jsonl")
    parser.add_argument("--manifest", default=str(MANIFEST))
    args = parser.parse_args()

    count = build(Path(args.runs_dir), Path(args.output), Path(args.manifest))
    print(f"EXPORTED PILOT JSONL: {count} records -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
