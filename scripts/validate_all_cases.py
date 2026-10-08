from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.validate_benchmark_case import validate


ROOT = Path(__file__).resolve().parents[1]


def validate_directory(directory: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(directory.glob("*.json")):
        try:
            case_errors = validate(path)
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

    errors = validate_directory(Path(args.pilot_dir))
    errors.extend(validate_directory(Path(args.benchmark_dir)))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    pilot_count = len(list(Path(args.pilot_dir).glob("*.json")))
    benchmark_count = len(list(Path(args.benchmark_dir).glob("*.json")))
    print(f"VALID RESEARCH CASE DATA: pilot={pilot_count}, benchmark={benchmark_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
