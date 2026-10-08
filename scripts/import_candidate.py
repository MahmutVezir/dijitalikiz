from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.validate_candidate import validate_candidate


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Import a candidate JSON into data/candidates.")
    parser.add_argument("source")
    parser.add_argument("--case-id", required=True)
    args = parser.parse_args()

    source = Path(args.source)
    payload = json.loads(source.read_text(encoding="utf-8"))
    payload["case_id"] = args.case_id
    errors = validate_candidate(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    destination = ROOT / "data" / "candidates" / f"{args.case_id}.json"
    if destination.exists():
        raise SystemExit(f"candidate already exists: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"IMPORTED: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
