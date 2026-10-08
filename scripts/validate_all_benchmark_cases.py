from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.validate_benchmark_case import validate as validate_case


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate every case named by the confirmatory benchmark manifest.")
    parser.add_argument("--manifest", default="data/benchmark/benchmark_manifest.json")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    root = manifest_path.resolve().parents[2]
    errors: list[str] = []

    for case_id in manifest.get("case_ids", []):
        case_path = root / "data" / "benchmark" / "cases" / f"{case_id}.json"
        assessment_path = root / "data" / "assessments" / f"{case_id}.json"
        if not case_path.is_file():
            errors.append(f"{case_id}: missing case file")
            continue
        errors.extend(f"{case_id}: {e}" for e in validate_case(case_path))
        try:
            case = json.loads(case_path.read_text(encoding="utf-8"))
            if case.get("case_id") != case_id:
                errors.append(f"{case_id}: case_id mismatch")
            if case.get("split") != "confirmatory":
                errors.append(f"{case_id}: split must be confirmatory")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{case_id}: unreadable case JSON: {type(exc).__name__}: {exc}")

        if not assessment_path.is_file():
            errors.append(f"{case_id}: missing assessment file")
            continue
        try:
            assessment = json.loads(assessment_path.read_text(encoding="utf-8"))
            if assessment.get("eligible_for_main") is not True:
                errors.append(f"{case_id}: eligible_for_main is not true")
            if assessment.get("contamination_risk") in (None, "unknown"):
                errors.append(f"{case_id}: contamination risk unresolved")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{case_id}: unreadable assessment JSON: {type(exc).__name__}: {exc}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"VALID CONFIRMATORY CASES: {len(manifest.get('case_ids', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
