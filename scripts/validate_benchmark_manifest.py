from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from scripts.validate_benchmark_case import validate as validate_case
except ModuleNotFoundError:
    from validate_benchmark_case import validate as validate_case


def _number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


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

    root = root or Path(".")

    if status == "frozen":
        scoring = manifest.get("scoring_rubric")
        if not isinstance(scoring, dict):
            errors.append("a frozen benchmark requires a scoring_rubric with path and sha256")
        else:
            scoring_path_value = scoring.get("path")
            expected_rubric_sha = scoring.get("sha256")
            if not isinstance(scoring_path_value, str) or not scoring_path_value:
                errors.append("scoring_rubric.path must be a non-empty string")
            else:
                rubric_path = root / scoring_path_value
                if not rubric_path.is_file():
                    errors.append(f"missing scoring rubric: {rubric_path}")
                else:
                    try:
                        rubric_bytes = rubric_path.read_bytes()
                        actual_rubric_sha = hashlib.sha256(rubric_bytes).hexdigest()
                        if actual_rubric_sha != expected_rubric_sha:
                            errors.append("scoring rubric SHA-256 does not match manifest")
                        rubric = json.loads(rubric_bytes.decode("utf-8"))
                        if scoring.get("primary_endpoint") != rubric.get("primary_endpoint"):
                            errors.append("scoring rubric primary endpoint does not match manifest")
                        rubric_ids = [item.get("case_id") for item in rubric.get("cases", [])]
                        if rubric_ids != case_ids:
                            errors.append("scoring rubric case IDs/order must match manifest case_ids")
                        for item in rubric.get("cases", []):
                            aliases = item.get("root_cause_aliases")
                            if not isinstance(aliases, list) or not aliases or not all(
                                isinstance(alias, str) and alias.strip() for alias in aliases
                            ):
                                errors.append(
                                    f"{item.get('case_id', '<unknown>')}: root_cause_aliases must be non-empty strings"
                                )
                    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                        errors.append(f"cannot read scoring rubric: {type(exc).__name__}: {exc}")

        for case_id in case_ids:
            case_path = root / "data" / "benchmark" / "cases" / f"{case_id}.json"
            if not case_path.is_file():
                errors.append(f"missing benchmark case file: {case_path}")
            else:
                try:
                    case = json.loads(case_path.read_text(encoding="utf-8"))
                    required = {
                        "case_id", "source", "source_url", "publication_date",
                        "technology", "error_description", "i_base", "ccdg", "ground_truth",
                    }
                    missing = sorted(required - set(case))
                    if missing:
                        errors.append(f"{case_id} missing case fields: {missing}")
                    if case.get("case_id") != case_id:
                        errors.append(f"{case_id} file contains mismatched case_id")
                    if case.get("split") != "confirmatory":
                        errors.append(f"{case_id} must have split=confirmatory")
                    errors.extend(f"{case_id}: {e}" for e in validate_case(case_path))
                except (OSError, json.JSONDecodeError) as exc:
                    errors.append(f"cannot read {case_path}: {type(exc).__name__}: {exc}")

            assessment_path = root / "data" / "assessments" / f"{case_id}.json"
            if not assessment_path.is_file():
                errors.append(f"missing assessment file: {assessment_path}")
            else:
                try:
                    assessment = json.loads(assessment_path.read_text(encoding="utf-8"))
                    if assessment.get("eligible_for_main") is not True:
                        errors.append(f"{case_id} assessment is not marked eligible_for_main")
                    if assessment.get("contamination_risk") in {None, "unknown"}:
                        errors.append(f"{case_id} contamination risk is not resolved")
                except (OSError, json.JSONDecodeError) as exc:
                    errors.append(f"cannot read {assessment_path}: {type(exc).__name__}: {exc}")

        if manifest.get("contamination_audit_completed") is not True:
            errors.append("a frozen benchmark requires contamination_audit_completed=true")
        if not case_ids:
            errors.append("a frozen benchmark must contain at least one independent case")

        power = manifest.get("power_assumption")
        if not isinstance(power, dict):
            errors.append("a frozen benchmark requires power_assumption")
        else:
            required = {
                "p_standard_only", "p_ccdg_only", "target_power", "alpha",
                "required_case_count", "achieved_power",
            }
            missing = sorted(required - set(power))
            if missing:
                errors.append(f"power_assumption missing: {missing}")
            else:
                numeric = {
                    "p_standard_only", "p_ccdg_only", "target_power", "alpha", "achieved_power"
                }
                for key in numeric:
                    if not _number(power[key]):
                        errors.append(f"power_assumption.{key} must be numeric")
                if not isinstance(power["required_case_count"], int) or isinstance(
                    power["required_case_count"], bool
                ):
                    errors.append("power_assumption.required_case_count must be an integer")
                elif power["required_case_count"] < 2:
                    errors.append("power_assumption.required_case_count must be >= 2")

                if all(_number(power[key]) for key in numeric):
                    if power["p_standard_only"] < 0 or power["p_ccdg_only"] < 0:
                        errors.append("discordant probabilities must be non-negative")
                    if power["p_standard_only"] + power["p_ccdg_only"] > 1:
                        errors.append("discordant probabilities must sum to <= 1")
                    if not 0 < power["target_power"] <= 1:
                        errors.append("target_power must be in (0, 1]")
                    if not 0 < power["alpha"] < 1:
                        errors.append("alpha must be in (0, 1)")
                    if not 0 < power["achieved_power"] <= 1:
                        errors.append("achieved_power must be in (0, 1]")
                    if power["achieved_power"] + 1e-12 < power["target_power"]:
                        errors.append("achieved_power must be >= target_power")
                required_n = power.get("required_case_count")
                if isinstance(required_n, int) and len(case_ids) < required_n:
                    errors.append(
                        "confirmatory case count is below the predeclared required_case_count"
                    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the confirmatory benchmark manifest.")
    parser.add_argument("--manifest", default="data/benchmark/benchmark_manifest.json")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    root = (
        manifest_path.resolve().parents[2]
        if manifest_path.parts[-2:] == ("benchmark", "benchmark_manifest.json")
        else Path(".")
    )
    errors = validate_manifest(manifest, root)
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
