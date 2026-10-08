from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = {
    "case_id",
    "source",
    "source_url",
    "publication_date",
    "technology",
    "error_description",
    "evidence_urls",
}


def validate_candidate(payload: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(payload))
    if missing:
        errors.append(f"missing required fields: {missing}")

    if not isinstance(payload.get("case_id"), str) or not payload.get("case_id"):
        errors.append("case_id must be a non-empty string")
    if not isinstance(payload.get("source_url"), str) or not payload.get("source_url"):
        errors.append("source_url must be a non-empty string")
    if not isinstance(payload.get("evidence_urls"), list) or not payload.get("evidence_urls"):
        errors.append("evidence_urls must be a non-empty list")

    split = payload.get("split")
    if split not in {"candidates", "pilot", "confirmatory"}:
        errors.append("split must be candidates, pilot, or confirmatory")

    if payload.get("annotation_status") == "not_started" and split != "candidates":
        errors.append("unannotated cases may remain only in candidates split")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an intake candidate record.")
    parser.add_argument("path")
    args = parser.parse_args()

    path = Path(args.path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read candidate: {type(exc).__name__}: {exc}")
        return 1

    errors = validate_candidate(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"VALID CANDIDATE: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
