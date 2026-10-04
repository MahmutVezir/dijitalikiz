from __future__ import annotations

import argparse
import hashlib
import json
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
MAJORITY_REQUIRED = 3


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
                parse_ok = record.get("parse_error") is None and record.get("parsed_output") is not None
                result = {
                    "case_id": case_id,
                    "condition": condition,
                    "seed": seed,
                    "parse_ok": parse_ok,
                    "parse_error": record.get("parse_error"),
                    "score": None,
                }

                # Parse/schema failures are failed runs for the binary
                # complete-pass endpoint, preserving the frozen 3/5 rule.
                if parse_ok:
                    output = DiagnosticOutput.from_dict(record["parsed_output"])
                    result["score"] = evaluate_output(output, case.ground_truth)
                else:
                    result["score"] = {
                        "passed": False,
                        "component_match": False,
                        "entity_match": False,
                        "operation_match": False,
                        "root_cause_match": False,
                        "required_relations_match": False,
                    }

                records.append(result)

    by_condition = {}
    for condition in CONDITIONS:
        subset = [r for r in records if r["condition"] == condition]
        parse_ok = sum(r["parse_ok"] for r in subset)
        passed = sum(r["score"]["passed"] for r in subset if r["score"] is not None)
        by_condition[condition] = {
            "n_expected": len(CASES) * len(SEEDS),
            "n_found": len(subset),
            "n_parse_ok": parse_ok,
            "parse_failure_rate": 1 - (parse_ok / len(subset)) if subset else None,
            "n_scored": sum(r["score"] is not None for r in subset),
            "n_passed": passed,
            "pass_rate": passed / len(subset) if subset else None,
        }

    duplicate_groups = []
    for case_id in CASES:
        for condition in CONDITIONS:
            subset = [
                r for r in records
                if r["case_id"] == case_id and r["condition"] == condition and r["parse_ok"]
            ]
            groups = {}
            for r in subset:
                run_path = runs_dir / f"{case_id}__{condition}__seed{r['seed']}.json"
                parsed_output = json.loads(run_path.read_text(encoding="utf-8"))["parsed_output"]
                key = sha256_json(parsed_output)
                groups.setdefault(key, []).append(r["seed"])
            for output_hash, seeds in groups.items():
                if len(seeds) > 1:
                    duplicate_groups.append({
                        "case_id": case_id,
                        "condition": condition,
                        "output_sha256": output_hash,
                        "seeds": seeds,
                    })

    case_level = {}
    for condition in CONDITIONS:
        condition_cases = {}
        for case_id in CASES:
            subset = [r for r in records if r["case_id"] == case_id and r["condition"] == condition]
            if len(subset) != len(SEEDS):
                condition_cases[case_id] = {
                    "n_runs_found": len(subset),
                    "n_runs_expected": len(SEEDS),
                    "majority_pass": None,
                    "status": "missing_replication",
                }
            else:
                scores = [r["score"]["passed"] for r in subset]
                condition_cases[case_id] = {
                    "n_runs_found": len(scores),
                    "pass_count": sum(scores),
                    "majority_pass": sum(scores) >= MAJORITY_REQUIRED,
                    "status": "complete",
                }
        case_level[condition] = condition_cases

    summary = {
        "status": "complete" if not missing else "incomplete",
        "expected_records": len(CASES) * len(CONDITIONS) * len(SEEDS),
        "found_records": len(records),
        "missing_files": missing,
        "by_condition": by_condition,
        "case_level_majority_rule": "at least 3 of 5 seeds must pass; parse/schema failures count as failed runs",
        "case_level": case_level,
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
        "case_level": case_level,
        "duplicate_output_groups": len(duplicate_groups),
        "output": str(output),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
