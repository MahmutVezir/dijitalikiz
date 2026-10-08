from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate_manifest(manifest: dict, root: Path | None = None) -> list[str]:
    errors: list[str] = []
    status = manifest.get("status")
    if status not in {"draft", "frozen"}:
        errors.append("status must be 'draft' or 'frozen'")

    case_ids = manifest.get("case_ids", [])
    pilot_case_ids = set(manifest.get("pilot_case_ids", []))
    if not isinstance(case_ids, list) or not all(isinstance(x, str) and x for x in case_ids):
        errors.append("case_ids must be a list of non-empty strings")
        case_ids = []

    if len(case_ids) != len(set(case_ids)):
        errors.append("case_ids must be unique")

    overlap = sorted(set(case_ids) & pilot_case_ids)
    if overlap:
        errors.append(f"confirmatory cases overlap pilot cases: {overlap}")

    if root is None:
        root = Path(".")

    if status == "frozen":
        for case_id in case_ids:
            case_path = root / "data" / "benchmark" / "cases" / f"{case_id}.json"
            if not case_path.is_file():
                errors.append(f"missing benchmark case file: {case_path}")
            else:
                try:
                    case = json.loads(case_path.read_text(encoding="utf-8"))
                    required_case_fields = {"case_id", "source", "source_url", "publication_date", "technology", "error_description", "i_base", "ccdg", "ground_truth"}
                    missing_case_fields = sorted(required_case_fields - set(case))
                    if missing_case_fields:
                        errors.append(f"{case_id} missing case fields: {missing_case_fields}")
                    if case.get("case_id") != case_id:
                        errors.append(f"{case_id} file contains mismatched case_id")
                except (OSError, json.JSONDecodeError) as exc:
                    errors.append(f"cannot read {case_path}: {type(exc).__name__}: {exc}")

            assessment_path = root / "data" / "assessments" / f"{case_id}.json"
            if not assessment_path.is_file():
                errors.append(f"missing assessment file: {assessment_path}")
            else:
                try:
                    assessment = json.loads(assessment_path.read_text(encoding="utf-8"))
                    if assessment.get("eligible_for_pilot") is not True:
                        errors.append(f"{case_id} assessment is not marked eligible")
                    if assessment.get("contamination_risk") in {None, "unknown"}:
                        errors.append(f"{case_id} contamination risk is not resolved")
                except (OSError, json.JSONDecodeError) as exc:
                    errors.append(f"cannot read {assessment_path}: {type(exc).__name__}: {exc}")

        if manifest.get("contamination_audit_completed") is not True:
            errors.append("a frozen benchmark requires contamination_audit_completed=true")

    power = manifest.get("power_assumption")
    if status == "frozen":
        if not case_ids:
            errors.append("a frozen benchmark must contain at least one independent case")
        if not isinstance(power, dict):
            errors.append("a frozen benchmark requires power_assumption")
        else:
            required = {"p_standard_only", "p_ccdg_only", "target_power", "alpha"}
            missing = sorted(required - set(power))
            if missing:
                errors.append(f"power_assumption missing: {missing}")
            else:
                values = {key: power[key] for key in required}
                for key, value in values.items():
                    if not isinstance(value, (int, float)):
                        errors.append(f"power_assumption.{key} must be numeric")
                if not errors:
                    if values["p_standard_only"] < 0 or values["p_ccdg_only"] < 0:
                        errors.append("discordant probabilities must be non-negative")
                    if values["p_standard_only"] + values["p_ccdg_only"] > 1:
                        errors.append("discordant probabilities must sum to <= 1")
                    if not 0 < values["target_power"] <= 1:
                        errors.append("target_power must be in (0, 1]")
                    if not 0 < values["alpha"] < 1:
                        errors.append("alpha must be in (0, 1)")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the confirmatory benchmark manifest.")
    parser.add_argument("--manifest", default="data/benchmark/benchmark_manifest.json")
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    errors = validate_manifest(manifest, Path(args.manifest).resolve().parents[2] if Path(args.manifest).parts[-2:] == ("benchmark", "benchmark_manifest.json") else Path("."))
    if errors:
        print(json.dumps({"status": "fail", "errors": errors}, indent=2, ensure_ascii=False))
        return 1

    print(json.dumps({
        "status": "pass",
        "benchmark_status": manifest.get("status"),
        "case_count": len(manifest.get("case_ids", [])),
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
