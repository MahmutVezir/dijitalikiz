# Confirmatory Analysis Plan

## Primary question

Does explicit Cross-Component Dependency Graph (CCDG) representation improve root-cause diagnosis accuracy compared with Standard context when all other experimental inputs are held constant?

## Primary endpoint

The primary endpoint is **case-level complete diagnostic correctness**.

A run is correct only when all frozen evaluation checks pass:

- diagnosed component
- affected entity
- operation evidence
- root-cause class
- required dependency relations

Each software case is tested under both Standard and CCDG.

### Replication aggregation

Five seeds are repeated measurements of the same case-condition pair; they are **not five independent software cases**.

For the primary binary endpoint, a condition is classified as case-level correct when at least **3 of 5** seeds pass the frozen evaluator. This majority rule is fixed before the main benchmark.

A case therefore contributes exactly one paired binary observation:

- Standard: correct / incorrect
- CCDG: correct / incorrect

## Primary statistical test

Use an exact two-sided McNemar test on paired case-level outcomes.

- Null hypothesis: Standard and CCDG have equal marginal correctness.
- Alternative hypothesis: their marginal correctness differs.
- Alpha: 0.05.
- Unit of inference: independent software case.

The direction of interest is CCDG improvement, but the primary test remains two-sided.

## Secondary endpoints

Report, separately by condition:

1. mean run-level complete-pass rate across the five seeds;
2. component accuracy;
3. affected-entity accuracy;
4. operation evidence accuracy;
5. root-cause accuracy;
6. required-relation accuracy;
7. parse failure rate;
8. within-case seed agreement / output duplication.

Secondary analyses are descriptive unless an inferential procedure is explicitly specified before the main benchmark.

## Missing data

A parse failure is not silently converted into a correct answer. It is recorded as a failed evaluable run for the complete-pass endpoint and reported separately.

If a seed file is missing, the case-condition pair is not silently assigned a majority outcome. The primary analysis must either complete the missing replication or mark that pair missing and document the deviation.

## Pilot handling

Pilot cases are used to validate the protocol and estimate execution feasibility. They are not automatically included in the confirmatory benchmark.

If pilot cases are retained in the final dataset, their inclusion/exclusion rule must be declared before inspecting the final benchmark outcome.

## Power analysis

The main sample size is selected before the confirmatory benchmark using an explicit assumption about:

- P(Standard fails, CCDG passes)
- P(Standard passes, CCDG fails)

The repository's exact McNemar power utility is used for this calculation. No probability is selected retrospectively to obtain a desired sample size.

## Contamination

The selected model/checkpoint, prompt, and benchmark cases require an explicit contamination-risk audit before the main benchmark. Unknown contamination status is not equivalent to low risk.

The audit must document the search method, date, scope, and decision for each case/model combination.
