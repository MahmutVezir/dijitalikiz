"""Paired E1 answer-coverage guardrail; analysis only, no model execution."""
from __future__ import annotations

import random
from collections.abc import Sequence
from typing import Any

DEFAULT_MARGIN = 0.10
DEFAULT_BOOTSTRAP_REPLICATES = 20_000
DEFAULT_SEED = 20_261_115


def analyze_e1_coverage(
    p0_covered: Sequence[bool],
    p1_covered: Sequence[bool],
    *,
    margin: float = DEFAULT_MARGIN,
    replicates: int = DEFAULT_BOOTSTRAP_REPLICATES,
    seed: int = DEFAULT_SEED,
) -> dict[str, Any]:
    """Analyze paired binary coverage using case-level percentile bootstrap.

    Inputs contain one interpretable P0/P1 pair per independently accepted E1
    case. Invalid outputs must be excluded from this complete-pair input and
    reported separately; callers must not silently recode invalidity as
    abstention. Bootstrap resampling preserves each case's paired outcomes.
    """
    if len(p0_covered) != len(p1_covered):
        raise ValueError("P0 and P1 must contain the same number of paired cases")
    n = len(p0_covered)
    if n < 2:
        raise ValueError("at least two complete paired cases are required")
    for name, values in (("P0", p0_covered), ("P1", p1_covered)):
        if any(type(value) is not bool for value in values):
            raise TypeError(name + " coverage values must be booleans")
    if isinstance(margin, bool) or not isinstance(margin, (int, float)) or not 0 < margin < 1:
        raise ValueError("margin must be strictly between 0 and 1")
    if type(replicates) is not int or replicates < 1000:
        raise ValueError("replicates must be an integer >= 1000")
    if type(seed) is not int:
        raise TypeError("seed must be an integer")

    differences = [int(p1) - int(p0) for p0, p1 in zip(p0_covered, p1_covered)]
    both = sum(p0 and p1 for p0, p1 in zip(p0_covered, p1_covered))
    p0_only = sum(p0 and not p1 for p0, p1 in zip(p0_covered, p1_covered))
    p1_only = sum(p1 and not p0 for p0, p1 in zip(p0_covered, p1_covered))
    neither = sum(not p0 and not p1 for p0, p1 in zip(p0_covered, p1_covered))
    estimate = sum(differences) / n

    rng = random.Random(seed)
    boot = []
    for _ in range(replicates):
        sample_sum = sum(differences[rng.randrange(n)] for _ in range(n))
        boot.append(sample_sum / n)
    boot.sort()
    # Nearest-rank 5th percentile: rank = ceil(0.05 * B), one-based.
    lower_index = max(0, (replicates + 19) // 20 - 1)
    lower = boot[lower_index]

    return {
        "n_complete_pairs": n,
        "p0_coverage": sum(p0_covered) / n,
        "p1_coverage": sum(p1_covered) / n,
        "delta_p1_minus_p0": estimate,
        "paired_counts": {
            "both_covered": both,
            "p0_only_covered": p0_only,
            "p1_only_covered": p1_only,
            "neither_covered": neither,
        },
        "one_sided_95_percent_lower_bound": lower,
        "non_inferiority_margin": -float(margin),
        "non_inferiority_demonstrated": lower > -float(margin),
        "bootstrap": {
            "method": "paired_case_level_percentile",
            "replicates": replicates,
            "seed": seed,
            "lower_quantile": 0.05,
            "quantile_rule": "nearest_rank",
        },
        "interpretation": "pass" if lower > -float(margin) else "non_inferiority_not_demonstrated",
    }
