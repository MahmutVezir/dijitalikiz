from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.validate_candidate import validate_candidate


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create and validate a new research candidate skeleton."
    )
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--publication-date", required=True)
    parser.add_argument("--technology", required=True)
    parser.add_argument("--error-description", required=True)
    parser.add_argument("--evidence-url", action="append", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    payload = {
        "case_id": args.case_id,
        "source": args.source,
        "source_url": args.source_url,
        "publication_date": args.publication_date,
        "technology": args.technology,
        "error_description": args.error_description,
        "evidence_urls": args.evidence_url,
        "split": "candidates",
        "annotation_status": "not_started",
        "provenance_verification_status": "unverified",
    }
    errors = validate_candidate(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    destination = Path(args.output) if args.output else (
        ROOT / "data" / "candidates" / f"{args.case_id}.json"
    )
    if destination.exists():
        raise SystemExit(f"candidate already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"CREATED CANDIDATE: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
