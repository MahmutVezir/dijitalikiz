# SWE-rebench V2 — paired McNemar power sensitivity (v0.1 draft)

**Status:** hypothetical planning only. No confirmatory model outputs exist. These probabilities are not pilot estimates, observed rates, or claims about Qwen.

## Why this calculation exists

The primary endpoint is paired at the case level: for each E3 case, compare whether P0 and P1 produce an unsupported definitive diagnosis. The exact McNemar test uses only discordant pairs. Therefore, power depends on both the frequency and direction of discordance, not only on the marginal P0/P1 rates.

The case registry enforces one accepted case per independent upstream project. The calculation assumes independent case pairs. It does not correct for missing/unscorable pairs, multiplicity, protocol deviations, or any residual dependence between nominally distinct projects.

## Definitions

- `p_improved`: probability that P0 is unsafe and P1 is safe (P1 avoids an unsupported definitive diagnosis).
- `p_harmed`: probability that P0 is safe and P1 is unsafe.
- `p_concordant = 1 - p_improved - p_harmed`: all remaining paired outcomes.
- Two-sided exact conditional McNemar p-value: twice the smaller binomial tail among discordant pairs, capped at 1.
- Power: unconditional probability, under the specified multinomial paired-outcome probabilities, that the exact McNemar p-value is below 0.05.

## Hypothetical sensitivity scenarios

| Scenario | p_improved | p_harmed | Paired RD (P1 − P0 unsafe risk) | N=60 | N=80 |
|---|---:|---:|---:|---:|---:|
| Weaker | 0.20 | 0.12 | -0.08 | 0.138 | 0.181 |
| Moderate | 0.30 | 0.10 | -0.20 | 0.635 | 0.779 |
| Larger | 0.40 | 0.08 | -0.32 | 0.956 | 0.991 |

These scenarios are deliberately labeled assumptions. They are not derived from the dataset, earlier exposed cases, or model outputs. The moderate scenario still gives less than 80% power at N=80. The weaker scenario shows that a null or non-significant result at N=80 could be inconclusive under modest discordance.

## Interpretation and decision rule

1. N=60 is a minimum feasibility threshold, not a guarantee of adequate power.
2. N=80 is a target, not a guarantee of 80% power.
3. The final sample target and assumptions must be justified from external evidence or a defensible design rationale and frozen before confirmatory outcomes are observed.
4. If the available independent-project cohort cannot meet the justified sample target, report the study as feasibility/exploratory or revise the design prospectively; never relax eligibility after seeing outcomes.
5. Report discordant pair counts, complete-pair denominator, invalid/unscorable outputs, and the prespecified conservative sensitivity analysis alongside the primary test.

## Reproducibility

The exact enumeration is implemented in `implementation/swe_rebench_v2_power.py` and covered by `implementation/test_swe_rebench_v2_power.py`. It is a pure statistical planning utility. It does not load a dataset, access a model, or perform inference.
