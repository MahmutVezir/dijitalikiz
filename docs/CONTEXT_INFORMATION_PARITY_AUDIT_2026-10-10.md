# Context Information Parity Audit and Study v2

**Date:** 2026-10-10  
**Status:** Methodological audit and future-study design; no new model inference performed.

## Executive finding

The frozen experiment's two context renderers are not information-matched as a pure representation comparison.

- The legacy Standard Context renderer includes Source, Technology, Error description, and I_base facts.
- The legacy CCDG Context renderer includes Source, Technology, dependency triples (including edge details), and I_base facts, but it omits the explicit Error description section.

As a result, the original two-condition comparison combines at least two changes: (1) adding an explicit dependency graph and (2) omitting the explicit error-description field from the context. The dependency graph may also make relationships more explicit than they are in the base facts. Therefore, the experiment cannot isolate the causal effect of graph structure alone.

This is a code-level design finding, not evidence that the observed model outputs are correct or incorrect. The 160 frozen records, original prompts, hashes, primary scoring rubric, statistical result, and archived report must remain unchanged. The original result is inconclusive for semantic root-cause diagnosis because the primary matcher produced a floor effect; this audit adds a further limitation on causal interpretation.

## Legacy behavior retained for reproducibility

The original functions in `dijitalikiz/context.py` have deliberately not been edited. Archived records and their prompt hashes were produced with those functions. Changing them in place would compromise the reproducibility of the frozen historical experiment.

The new, separately versioned implementation is `dijitalikiz/context_v2.py`. It is not wired into a new model run and does not overwrite old artifacts.

## Proposed three-condition follow-up

Use three conditions on the **same independently selected software-defect cases**:

| Condition | Information presented | Purpose |
|---|---|---|
| A. Standard baseline | Source, technology, error description, and I_base | Baseline without an explicit edge list |
| B. Dependency-enriched prose | All A information plus every CCDG edge expressed as a prose dependency fact | Measures the effect of making dependency facts explicit |
| C. CCDG triples | The exact same A information and the same edge endpoints, relation labels, and details as B, represented as graph triples | Tests whether graph structure adds value beyond explicit dependency information |

The primary comparison should be **C versus B**, because both include the same base facts and the same dependency edges; only their representation differs. The planned secondary comparisons are B versus A (adding explicit dependency facts) and C versus A (overall package effect). These comparisons and multiplicity handling must be predeclared before any new inference.

The v2 context renderers implement these three textual representations. They require tests plus a pre-run audit of rendered prompts, model-token counts, exact text hashes, and case-by-condition coverage before being used in any confirmatory run.

## Required gates before follow-up inference

1. **Score validation:** build a source-grounded calibration set and have two reviewers independently label it where possible. Resolve disagreements and freeze a primary root-cause correctness rule before generating confirmatory outputs. Synthetic matcher fixtures are software tests only, not scoring validation.
2. **Case quality and independence:** screen new, licensed, reproducible defects; document issue provenance, fixed revision, failing test, root-cause evidence, component boundaries, graph suitability, and contamination risk. Track unique defects separately from repeated model generations.
3. **Information parity:** ensure all three arms share identical source, technology, error description and I_base content; ensure B and C encode the same edge endpoints, relation labels and details. Compute and archive model-token lengths for every prompt.
4. **Protocol freeze:** record immutable model revision, runtime, generation parameters, prompts/renderers, case IDs, scoring rubric, repetitions, randomization policy, missing-output handling, statistical test, effect size, confidence interval, and sample-size rationale.
5. **Independent confirmatory sample:** do not tune prompts, labels, aliases, or scoring rules using the new confirmatory outputs.
6. **Reporting:** preserve the old experiment as a completed but inconclusive historical study. Report the new experiment as a distinct, versioned study; do not merge new scores into the frozen old summary.

## Hypotheses for the follow-up

- **Primary:** With the same underlying dependency facts available in both contexts, CCDG triples improve case-level root-cause correctness compared with dependency-enriched prose.
- **Secondary:** Explicitly supplying dependency facts improves root-cause correctness compared with the standard baseline.
- **Exploratory:** The size of any effect varies with graph complexity, case family, or model output stability.

No hypothesis is guaranteed to be supported. A null, negative, or inconclusive result must be reported accurately.

## Implementation added

- `dijitalikiz/context_v2.py`: independent v2 renderers; legacy renderers remain unchanged.
- `tests/test_context_v2.py`: checks common facts, edge-field parity between enriched prose and CCDG arms, intended baseline distinction, and ground-truth isolation.
- `tests/fixtures/scoring_matcher_characterization_v1.json` and `scripts/audit_scoring_matcher_characterization.py`: synthetic software-behavior checks for the legacy contiguous-alias matcher, explicitly not empirical model-evaluation data.

## Current state

The v2 design and test code are committed, but they must pass repository CI before being treated as validated. No v2 inference has run. No new human-adjudicated calibration set has been completed. The frozen confirmatory result remains unchanged.


## Additional answer-cue control — 2026-10-15

The first draft of `context_v2.py` rendered optional version-bound snapshot metadata inside every model context, including the exact regression-test name and observed code revision. Although shared across A/B/C, a test name can reveal the intended defect mechanism and can make cases artificially easy. The follow-up experiment does not need these provenance fields to compare the representation of dependency facts.

The v2 renderer has therefore been tightened: `software_twin_snapshot` remains available in the case record for source review and reproducibility, but none of its values are sent to the model in A, B or C. This does not edit the historical `context.py` renderer or alter frozen outputs. A regression test uses sentinel snapshot values and asserts that none appears in any rendered arm; the fail-closed parity audit also rejects leakage of any configured snapshot value.

This is a source-level risk control, **not yet a passing test result**. The current GitHub-hosted runner issue prevents a verified full repository test run; no new inference is authorized until tests, tokenizer audit, and all human/evidence gates pass.
