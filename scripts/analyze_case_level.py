from __future__ import annotations

import argparse
import json
import math
from math import comb
from pathlib import Path

CONDITIONS = ("standard", "ccdg")
SEEDS = (42, 43, 44, 45, 46)
MAJORITY_REQUIRED = 3
CI_Z = 1.959963984540054


def exact_mcnemar_pvalue(standard_only: int, ccdg_only: int) -> float:
    d = standard_only + ccdg_only
    if d == 0:
        return 1.0
    lower = sum(comb(d, k) for k in range(0, min(standard_only, ccdg_only) + 1))
    return min(1.0, 2.0 * lower / (2**d))


def wilson_interval(successes: int, n: int, z: float = CI_Z) -> tuple[float, float]:
    if n <= 0:
        raise ValueError("Wilson interval requires n > 0.")
    if not 0 <= successes <= n:
        raise ValueError("successes must be in [0, n].")
    phat = successes / n
    z2 = z * z
    denominator = 1.0 + z2 / n
    center = (phat + z2 / (2.0 * n)) / denominator
    margin = (
        z
        * math.sqrt((phat * (1.0 - phat) / n) + (z2 / (4.0 * n * n)))
        / denominator
    )
    return max(0.0, center - margin), min(1.0, center + margin)


def paired_risk_difference_ci(
    standard_only: int,
    ccdg_only: int,
    n: int,
) -> tuple[float, float]:
    """Newcombe-style paired risk-difference interval from discordant cells.

    The paired effect is p(CCDG pass, Standard fail) -
    p(Standard pass, CCDG fail). A conservative interval is formed by
    subtracting the Wilson lower/upper bounds of the two mutually
    exclusive discordant proportions.
    """
    ccdg_only_interval = wilson_interval(ccdg_only, n)
    standard_only_interval = wilson_interval(standard_only, n)
    return (
        ccdg_only_interval[0] - standard_only_interval[1],
        ccdg_only_interval[1] - standard_only_interval[0],
    )


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
    paired_effect = (ccdg_only - standard_only) / n
    ci_low, ci_high = paired_risk_difference_ci(standard_only, ccdg_only, n)

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
        "paired_effect_size": {
            "name": "paired_risk_difference",
            "definition": "P(CCDG correct, Standard incorrect) - P(Standard correct, CCDG incorrect)",
            "estimate": paired_effect,
            "95_ci": [ci_low, ci_high],
            "ci_method": "Newcombe-style interval using Wilson score intervals for the two discordant proportions",
        },
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
