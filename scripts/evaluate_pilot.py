from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from dijitalikiz.evaluation import evaluate_output
from dijitalikiz.models import DiagnosticOutput, ResearchCase

CASES = (
    "commons-math-defects4j-MATH-927",
    "commons-math-defects4j-MATH-950",
    "commons-math-defects4j-MATH-988",
)
CONDITIONS = ("standard", "ccdg")
SEEDS = (42, 43, 44, 45, 46)


def sha256_json(value: object) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_case(case_id: str) -> ResearchCase:
    path = Path("data/pilot", case_id + ".json")
    return ResearchCase.from_dict(json.loads(path.read_text(encoding="utf-8")))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-dir", default="data/pilot/runs")
    parser.add_argument("--output", default="data/pilot/pilot_evaluation.json")
    args = parser.parse_args()

    runs_dir = Path(args.runs_dir)
    records = []
    missing = []

    for case_id in CASES:
        case = load_case(case_id)
        for condition in CONDITIONS:
            for seed in SEEDS:
                path = runs_dir / f"{case_id}__{condition}__seed{seed}.json"
                if not path.exists():
                    missing.append(str(path))
                    continue
                record = json.loads(path.read_text(encoding="utf-8"))
                result = {
                    "case_id": case_id,
                    "condition": condition,
                    "seed": seed,
                    "parse_ok": record.get("parse_error") is None and record.get("parsed_output") is not None,
                    "parse_error": record.get("parse_error"),
                    "score": None,
                }
                if result["parse_ok"]:
                    output = DiagnosticOutput.from_dict(record["parsed_output"])
                    result["score"] = evaluate_output(output, case.ground_truth)
                records.append(result)

    by_condition = {}
    for condition in CONDITIONS:
        subset = [r for r in records if r["condition"] == condition]
        parse_ok = sum(r["parse_ok"] for r in subset)
        scored = [r for r in subset if r["score"] is not None]
        passed = sum(r["score"]["passed"] for r in scored)
        by_condition[condition] = {
            "n_expected": len(CASES) * len(SEEDS),
            "n_found": len(subset),
            "n_parse_ok": parse_ok,
            "parse_failure_rate": 1 - (parse_ok / len(subset)) if subset else None,
            "n_scored": len(scored),
            "n_passed": passed,
            "pass_rate": passed / len(scored) if scored else None,
        }

    # Detect identical parsed outputs across different seeds within each case/condition.
    duplicate_groups = []
    for case_id in CASES:
        for condition in CONDITIONS:
            subset = [
                r for r in records
                if r["case_id"] == case_id and r["condition"] == condition and r["parse_ok"]
            ]
            groups = {}
            for r in subset:
                key = sha256_json(next(
                    json.loads((runs_dir / f"{case_id}__{condition}__seed{r['seed']}.json").read_text(encoding="utf-8"))["parsed_output"]
                    for _ in [0]
                ))
                groups.setdefault(key, []).append(r["seed"])
            for output_hash, seeds in groups.items():
                if len(seeds) > 1:
                    duplicate_groups.append({
                        "case_id": case_id,
                        "condition": condition,
                        "output_sha256": output_hash,
                        "seeds": seeds,
                    })

    summary = {
        "status": "complete" if not missing else "incomplete",
        "expected_records": len(CASES) * len(CONDITIONS) * len(SEEDS),
        "found_records": len(records),
        "missing_files": missing,
        "by_condition": by_condition,
        "duplicate_output_groups": duplicate_groups,
        "records": records,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": summary["status"],
        "expected_records": summary["expected_records"],
        "found_records": summary["found_records"],
        "missing_files": len(missing),
        "by_condition": by_condition,
        "duplicate_output_groups": len(duplicate_groups),
        "output": str(output),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
