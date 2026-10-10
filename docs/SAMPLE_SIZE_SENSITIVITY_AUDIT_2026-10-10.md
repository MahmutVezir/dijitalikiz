# Prospective sample-size sensitivity audit — 2026-10-10

**Status: design audit only; no model outputs used.** This document does not change the draft protocol, does not imply that any effect size is likely, and does not authorize inference. Its purpose is to show how strongly the proposed 61-case target depends on assumed paired discordance probabilities.

## Primary contrast and exact calculation

The v2 primary contrast is C versus B: the same adjudicated dependency facts presented as CCDG triples versus prose. The primary outcome is one binary pass/fail per independent defect case and condition, derived from five outputs (at least three of five final human-adjudicated diagnoses must be correct). McNemar's exact two-sided test compares the paired case-level outcomes.

Define:
- `p_prose_only` = probability a case passes in B but fails in C.
- `p_graph_only` = probability a case fails in B but passes in C.

The present draft assumes 0.05 and 0.25, respectively, and reports 61 cases with power 0.8052 at two-sided alpha 0.05. These are not estimates from the historic experiment. The historical literal-alias endpoint had a floor effect and cannot estimate human-adjudicated B/C discordance.

I independently recalculated the exact conditional-binomial power using the same formulation documented in `scripts/power_mcnemar.py`: the discordant-pair count is binomial with probability `p_prose_only + p_graph_only`; conditional on discordance, the graph-only count is binomial with probability `p_graph_only / (p_prose_only + p_graph_only)`; rejection uses the exact two-sided binomial test at alpha 0.05.

## Sensitivity results

| Assumed B-only pass probability | Assumed C-only pass probability | Power at 61 cases | First case count reaching 80% power | Model outputs at that count (3 conditions × 5 repeats) |
|---:|---:|---:|---:|---:|
| 0.05 | 0.25 | 0.8052 | 61 | 915 |
| 0.05 | 0.20 | 0.5904 | 92 | 1,380 |
| 0.05 | 0.15 | 0.3142 | 168 | 2,520 |
| 0.10 | 0.30 | 0.6432 | 84 | 1,260 |
| 0.10 | 0.25 | 0.4322 | 129 | 1,935 |
| 0.10 | 0.20 | 0.2247 | 249 | 3,735 |

These are hypothetical design scenarios, not fitted estimates or predictions. They show that 61 cases is sufficient only under a strong assumed imbalance in discordant outcomes. Five repeated generations do not increase the independent case count; they define the case-condition majority outcome.

## Recommendation before preregistration freeze

1. Keep 61 as the current planning target only if the team explicitly accepts the strong-effect assumption and clearly labels it as a design scenario—not a demonstrated expectation.
2. Before any v2 confirmatory output exists, have a qualified reviewer inspect the power code and the assumed discordance probabilities. Consider a defensible effect range based on substantive reasoning or external pilot evidence that is independent of the v2 confirmation set.
3. Predeclare the sensitivity table or an equivalent range analysis in the preregistration. Do not choose a sample size after inspecting v2 model outcomes.
4. If a larger case count is infeasible, do not pad the set with weak, duplicated, single-component, or unadjudicated cases. Report the attainable precision and treat a null result as potentially inconclusive.
5. Record the feasibility trade-off before freeze: for this design, 92 cases means 1,380 outputs; 168 means 2,520; 249 means 3,735. These totals exclude human-rating effort and do not include calibration runs.

## Decision

**No change to the current draft manifest has been made.** The manifest remains `status: draft`, the held-out case pool has zero eligible cases, and `model_inference_permitted` remains false. This audit is a prerequisite for a reasoned freeze discussion, not permission to run the model.