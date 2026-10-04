from __future__ import annotations

import argparse
import math


def binom_pmf(n: int, k: int, p: float) -> float:
    if p <= 0:
        return 1.0 if k == 0 else 0.0
    if p >= 1:
        return 1.0 if k == n else 0.0
    return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))


def exact_mcnemar_power(
    n: int,
    p_standard_only: float,
    p_ccdg_only: float,
    alpha: float = 0.05,
) -> float:
    """Approximate two-sided McNemar power by exact binomial conditioning.

    p_standard_only = P(Standard fails, CCDG passes)
    p_ccdg_only = P(Standard passes, CCDG fails)

    Conditional on a discordant pair, B ~ Binomial(D, q), where
    q = p_standard_only / (p_standard_only + p_ccdg_only).
    The discordant-pair count D ~ Binomial(n, p_standard_only+p_ccdg_only).

    The rejection rule uses the standard exact two-sided binomial test.
    """
    d_prob = p_standard_only + p_ccdg_only
    if not (0 < d_prob <= 1):
        return 0.0

    q = p_standard_only / d_prob
    power = 0.0

    for d in range(1, n + 1):
        pd = binom_pmf(n, d, d_prob)
        rejection = 0.0

        for b in range(d + 1):
            pb = binom_pmf(d, b, q)
            # Exact two-sided binomial p-value under H0 q=0.5.
            tail_lo = sum(binom_pmf(d, j, 0.5) for j in range(0, b + 1))
            tail_hi = sum(binom_pmf(d, j, 0.5) for j in range(b, d + 1))
            p_value = min(1.0, 2.0 * min(tail_lo, tail_hi))
            if p_value <= alpha:
                rejection += pb

        power += pd * rejection

    return power


def required_n(
    p_standard_only: float,
    p_ccdg_only: float,
    target_power: float = 0.80,
    alpha: float = 0.05,
    max_n: int = 1000,
) -> int | None:
    for n in range(2, max_n + 1):
        if exact_mcnemar_power(
            n,
            p_standard_only,
            p_ccdg_only,
            alpha=alpha,
        ) >= target_power:
            return n
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exact McNemar power calculation for paired Standard-vs-CCDG case outcomes."
    )
    parser.add_argument("--p-standard-only", type=float, required=True)
    parser.add_argument("--p-ccdg-only", type=float, required=True)
    parser.add_argument("--target-power", type=float, default=0.80)
    parser.add_argument("--alpha", type=float, default=0.05)
    args = parser.parse_args()

    if args.p_standard_only < 0 or args.p_ccdg_only < 0:
        raise SystemExit("Discordant probabilities must be non-negative.")
    if args.p_standard_only + args.p_ccdg_only > 1:
        raise SystemExit("Discordant probabilities must sum to <= 1.")

    n = required_n(
        args.p_standard_only,
        args.p_ccdg_only,
        target_power=args.target_power,
        alpha=args.alpha,
    )
    if n is None:
        print("No sample size found within the search limit.")
        return

    power = exact_mcnemar_power(
        n,
        args.p_standard_only,
        args.p_ccdg_only,
        alpha=args.alpha,
    )
    print(f"required_case_count={n}")
    print(f"achieved_power={power:.4f}")
    print(f"alpha={args.alpha:.4f}")
    print("Primary unit: independent software case paired across Standard and CCDG.")


if __name__ == "__main__":
    main()
