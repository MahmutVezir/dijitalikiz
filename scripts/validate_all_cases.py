from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.validate_benchmark_case import validate


ROOT = Path(__file__).resolve().parents[1]

# These JSON files live in data/pilot for execution bookkeeping and are not ResearchCase records.
PILOT_CONTROL_FILES = {
    "pilot_manifest.json",
    "environment.json",
    "pilot_evaluation.json",
    "case_level_analysis.json",
    "pilot_qa_report.json",
    "artifact_manifest.json",
}


def validate_directory(directory: Path, expected_split: str | None = None) -> list[str]:
    errors: list[str] = []
    for path in sorted(directory.glob("*.json")):
        if directory.name == "pilot" and path.name in PILOT_CONTROL_FILES:
            continue
        try:
            case_errors = validate(path)
            if expected_split is not None:
                payload = json.loads(path.read_text(encoding="utf-8"))
                if payload.get("split") != expected_split:
                    case_errors.append(
                        f"split must be {expected_split!r}, got {payload.get('split')!r}"
                    )
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
            errors.append(f"{path}: {type(exc).__name__}: {exc}")
            continue
        errors.extend(f"{path}: {error}" for error in case_errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate all frozen-format research case records.")
    parser.add_argument("--pilot-dir", default=str(ROOT / "data" / "pilot"))
    parser.add_argument("--benchmark-dir", default=str(ROOT / "data" / "benchmark" / "cases"))
    args = parser.parse_args()

    pilot_dir = Path(args.pilot_dir)
    benchmark_dir = Path(args.benchmark_dir)

    errors = validate_directory(pilot_dir, expected_split="pilot")
    errors.extend(validate_directory(benchmark_dir, expected_split="confirmatory"))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    pilot_count = sum(
        1 for path in pilot_dir.glob("*.json") if path.name not in PILOT_CONTROL_FILES
    )
    benchmark_count = len(list(benchmark_dir.glob("*.json")))
    print(f"VALID RESEARCH CASE DATA: pilot={pilot_count}, benchmark={benchmark_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
