# Follow-up Sample-Size Sensitivity — 2026-10-10

**Status:** Planning sensitivity analysis only. This does not freeze the future sample size and is not based on observed successes from the frozen experiment.

## Primary contrast

For the proposed three-condition design, the primary contrast is CCDG triples versus dependency-enriched prose with the same underlying facts. The independent unit is a software defect case. Repeated model generations are aggregated to one binary case-level result per condition before the paired comparison.

The repository utility `scripts/power_mcnemar.py` calculates exact two-sided McNemar power using assumed paired discordance probabilities:
- (p_{prose-only}): probability the prose condition passes and CCDG fails;
- (p_{graph-only}): probability CCDG passes and prose fails.

The completed legacy experiment had zero case-level passes under its frozen literal-alias endpoint in both conditions. It therefore cannot estimate these future semantic-outcome discordance probabilities. The figures below are assumptions for sensitivity analysis, not estimates from the old experiment.

## Exact McNemar sensitivity scenarios

Target power = 0.80; two-sided alpha = 0.05 for the single predeclared primary comparison.

| Assumed prose-only probability | Assumed graph-only probability | Required independent cases | Achieved power (approx.) |
|---:|---:|---:|---:|
| 0.10 | 0.20 | 249 | 0.8014 |
| 0.05 | 0.25 | 61 | 0.8052 |
| 0.05 | 0.35 | 36 | 0.8131 |
| 0.05 | 0.40 | 29 | 0.8062 |
| 0.05 | 0.60 | 16 | 0.8070 |

These scenarios show that a modest paired effect can require many independent cases. A small sample is adequately powered only under a very large assumed directional difference. Repeated generations do not substitute for additional distinct defects.

## Operational implication

With 5 generations per condition and 3 conditions, a 61-case study would require 915 model outputs, before accounting for retries or technical failures. A 36-case study would require 540 outputs. These are workload calculations, not recommendations to choose a convenient sample size.

## Freeze decision rule

Do not choose the future sample size to obtain a desired result. First complete the scoring calibration, estimate plausible paired effect scenarios without looking at the new confirmatory outcomes, then commit:
- one primary contrast and its alpha;
- the case-level aggregation rule;
- the discordance assumptions and power method;
- the planned number of independent cases;
- secondary-comparison multiplicity handling;
- missing-output and exclusion rules.

If the available candidate pool cannot support the justified target, report that constraint and its effect on precision rather than treating repeated generations as independent cases or claiming confirmatory power that was not achieved.
