"""Exact paired-McNemar power sensitivity; planning only, never model execution."""
from __future__ import annotations

import math


def exact_mcnemar_pvalue(improved: int, harmed: int) -> float:
    """Two-sided exact conditional McNemar p-value for discordant pairs.

    improved: P0 unsafe and P1 safe.
    harmed: P0 safe and P1 unsafe.
    """
    if type(improved) is not int or type(harmed) is not int:
        raise TypeError("discordant counts must be integers")
    if improved < 0 or harmed < 0:
        raise ValueError("discordant counts must be non-negative")
    discordant = improved + harmed
    if discordant == 0:
        return 1.0
    tail = sum(math.comb(discordant, k) for k in range(min(improved, harmed) + 1))
    return min(1.0, 2.0 * tail / (2 ** discordant))


def exact_paired_mcnemar_power(
    n: int,
    p_improved: float,
    p_harmed: float,
    alpha: float = 0.05,
) -> float:
    """Unconditional power by enumerating the paired multinomial outcomes.

    This assumes independent case pairs and fixed discordance probabilities.
    It is a sensitivity calculator, not an effect estimate or a sample-size
    guarantee. It does not account for missing pairs or multiplicity.
    """
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    for name, value in (("p_improved", p_improved), ("p_harmed", p_harmed), ("alpha", alpha)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(name + " must be finite")
    if p_improved < 0 or p_harmed < 0 or p_improved + p_harmed > 1:
        raise ValueError("discordance probabilities must be non-negative and sum to at most 1")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be strictly between 0 and 1")

    p_concordant = 1.0 - p_improved - p_harmed
    power = 0.0
    for improved in range(n + 1):
        for harmed in range(n - improved + 1):
            if exact_mcnemar_pvalue(improved, harmed) < alpha:
                concordant = n - improved - harmed
                probability = (
                    math.comb(n, improved)
                    * math.comb(n - improved, harmed)
                    * (p_improved ** improved)
                    * (p_harmed ** harmed)
                    * (p_concordant ** concordant)
                )
                power += probability
    return min(1.0, power)
