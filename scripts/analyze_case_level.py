from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path

CONDITIONS = ("standard", "ccdg")
SEEDS = (42, 43, 44, 45, 46)
MAJORITY_REQUIRED = 3


def exact_mcnemar_pvalue(standard_only: int, ccdg_only: int) -> float:
    d = standard_only + ccdg_only
    if d == 0:
        return 1.0
    lower = sum(comb(d, k) for k in range(0, min(standard_only, ccdg_only) + 1))
    return min(1.0, 2.0 * lower / (2**d))


def load_evaluation(evaluation_path: Path, case_ids: list[str]) -> dict:
    payload = json.loads(evaluation_path.read_text(encoding="utf-8"))
    if payload.get("status") != "complete":
        raise ValueError("Pilot evaluation is incomplete; final case-level analysis is blocked.")
    if not case_ids:
        raise ValueError("At least one case is required for case-level analysis.")
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("case_ids must be unique; duplicate case IDs would overweight a case.")

    records = payload.get("records", [])
    outcomes = {}
    expected_seeds = set(SEEDS)
    for case_id in case_ids:
        outcomes[case_id] = {}
        for condition in CONDITIONS:
            subset = [
                r for r in records
                if r.get("case_id") == case_id and r.get("condition") == condition
            ]
            observed_seeds = [r.get("seed") for r in subset]
            if len(subset) != len(SEEDS) or set(observed_seeds) != expected_seeds:
                raise ValueError(
                    f"Expected exactly one scored run for each seed {SEEDS} for "
                    f"{case_id}/{condition}; observed seeds={observed_seeds}."
                )

            scores = []
            for record in subset:
                if record.get("score") is None:
                    raise ValueError(f"Missing score for {case_id}/{condition}/seed{record.get('seed')}.")
                passed = record["score"].get("passed")
                if not isinstance(passed, bool):
                    raise ValueError(
                        f"score.passed must be boolean for {case_id}/{condition}/seed{record.get('seed')}."
                    )
                scores.append(passed)

            outcomes[case_id][condition] = sum(scores) >= MAJORITY_REQUIRED
    return outcomes


def build_result(outcomes: dict, case_ids: list[str]) -> dict:
    if not case_ids:
        raise ValueError("At least one case is required for case-level analysis.")
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("case_ids must be unique; duplicate case IDs would overweight a case.")

    standard_only = sum(
        outcomes[c]["standard"] and not outcomes[c]["ccdg"] for c in case_ids
    )
    ccdg_only = sum(
        outcomes[c]["ccdg"] and not outcomes[c]["standard"] for c in case_ids
    )
    both_pass = sum(
        outcomes[c]["standard"] and outcomes[c]["ccdg"] for c in case_ids
    )
    both_fail = sum(
        not outcomes[c]["standard"] and not outcomes[c]["ccdg"] for c in case_ids
    )
    n = len(case_ids)
    standard_pass = sum(outcomes[c]["standard"] for c in case_ids)
    ccdg_pass = sum(outcomes[c]["ccdg"] for c in case_ids)
    return {
        "n_cases": n,
        "majority_rule": "at least 3 of 5 seeds",
        "contingency_table": {
            "standard_pass_ccdg_pass": both_pass,
            "standard_pass_ccdg_fail": standard_only,
            "standard_fail_ccdg_pass": ccdg_only,
            "standard_fail_ccdg_fail": both_fail,
        },
        "standard_accuracy": standard_pass / n,
        "ccdg_accuracy": ccdg_pass / n,
        "accuracy_difference_ccdg_minus_standard": (ccdg_pass - standard_pass) / n,
        "exact_two_sided_mcnemar_p": exact_mcnemar_pvalue(standard_only, ccdg_only),
        "case_outcomes": outcomes,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evaluation", required=True)
    parser.add_argument("--case-ids", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = build_result(
        load_evaluation(Path(args.evaluation), args.case_ids),
        args.case_ids,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
