# Confirmatory Power Planning

Updated: 2026-10-08

## Principle

The confirmatory sample size must be selected before confirmatory inference and must not be changed in response to pilot results.

Primary analysis: exact two-sided McNemar test, alpha = 0.05.

The quantities below are planning scenarios for the probability of discordant pairs:

- (p_{S}): Standard-only correct/CCDG incorrect or equivalently the Standard-side discordant direction defined by the analysis plan.
- (p_{C}): CCDG-only discordant direction.

These scenarios are not observed project results.

## Exact conditional-power scenarios

| p_standard_only | p_ccdg_only | Required independent cases | Exact power |
|---:|---:|---:|---:|
| 0.30 | 0.05 | 45 | 0.8044 |
| 0.25 | 0.05 | 61 | 0.8052 |
| 0.20 | 0.05 | 92 | 0.8014 |
| 0.30 | 0.10 | 84 | 0.8030 |
| 0.35 | 0.05 | 36 | 0.8131 |
| 0.40 | 0.05 | 29 | 0.8062 |
| 0.50 | 0.05 | 21 | 0.8108 |
| 0.45 | 0.05 | 25 | 0.8202 |
| 0.50 | 0.10 | 30 | 0.8085 |
| 0.55 | 0.05 | 18 | 0.8028 |
| 0.60 | 0.05 | 16 | 0.8070 |
| 0.40 | 0.02 | 22 | 0.8135 |
| 0.30 | 0.02 | 32 | 0.8180 |

## Current planning implication

The candidate pool now contains 16 additional provisional candidates that are not pilot cases. A 16-case confirmatory design is therefore mechanically possible under the (0.60/0.05) scenario, but this scenario is **not yet selected as the scientific assumption**.

Before freezing the benchmark, the project must record:

1. the scientific rationale for the chosen discordant-pair probabilities;
2. the chosen target power and alpha;
3. the resulting required case count;
4. the achieved exact power for that integer case count.

The validator rejects a frozen manifest when the case count is below the declared requirement or achieved power is below target.

## No retrospective power selection

Pilot inference outcomes must not be used to choose the most favorable row in this table. The final row must be selected from the study design rationale and documented before confirmatory model inference.
