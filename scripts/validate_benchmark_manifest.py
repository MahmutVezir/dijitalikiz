from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate_manifest(manifest: dict) -> list[str]:
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
    errors = validate_manifest(manifest)
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
