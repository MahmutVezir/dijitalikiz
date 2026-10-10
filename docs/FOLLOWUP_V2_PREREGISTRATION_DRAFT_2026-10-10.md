# Follow-up Experiment v2 — Preregistration Draft

**Status: DRAFT — NO NEW MODEL INFERENCE AUTHORIZED.**

This document separates the proposed, information-matched follow-up from the historical two-condition experiment. It is a prospective protocol draft, not evidence that the hypothesis is true, not an official frozen preregistration, and not a replacement for the historic report.

## Why the new experiment is necessary

The historic literal-alias endpoint scored 0/80 for Standard and 0/80 for CCDG. This is a floor-effect result and cannot establish equivalence or absence of an effect. The historical context renderers also differ in information: legacy Standard includes the error-description field and legacy CCDG omits it while adding dependency edges. The old comparison therefore does not isolate graph representation alone. Keep every historic context, record, manifest and score unchanged.

## Design

Use three conditions over the exact same independently selected and adjudicated held-out defects:

| Arm | Context | Identified effect |
|---|---|---|
| A | Standard baseline: source, technology, error description, I_base, and version-bound source snapshot | Baseline |
| B | Same base facts plus each dependency edge as prose | Effect of explicitly exposing dependency facts (B vs A) |
| C | Same base facts and the same endpoints, relation labels, and details as B, encoded as directed CCDG triples | Added value of graph representation over matched prose (C vs B) |

The **single primary contrast is C versus B**. Secondary contrasts are B versus A and C versus A. Apply Holm correction across the two secondary tests. Do not add, remove, or reinterpret comparisons after viewing v2 outcomes.

## Outcome and blinded rating

Two independent reviewers, blinded to condition labels and any automated matcher result, label each generated answer as `correct`, `partially_correct`, `incorrect`, or `unscorable`. An independent adjudicator resolves disagreements against source-grounded case truth. Do not treat containing a gold phrase as sufficient evidence of correctness.

For each defect and condition, mark the case-condition as a binary pass if at least 3 of 5 outputs are adjudicated `correct`; all other labels, including `unscorable`, count as not-correct for this primary endpoint. The primary statistical unit is the independent defect case, not the individual generation. Compare paired C/B case-level outcomes with the exact two-sided McNemar test at alpha .05. Report the two discordant counts, paired difference and uncertainty interval; report secondary comparisons with Holm-adjusted p-values. Report null, adverse, and inconclusive outcomes accurately.

The calibration gate requires the scoring rubric to be tested on a separate source-grounded set. Before the follow-up is frozen, two raters must reach at least 0.80 exact agreement and Cohen's kappa at least 0.70 on the declared calibration set. If reliability misses either threshold or kappa is undefined, the gate stays blocked; do not relax thresholds after seeing outcomes. The calibration examples and the seven current calibration candidates are permanently excluded from v2 held-out case selection.

## Provisional sample size and workload

The current planning target is **61 independent defect cases × 3 conditions × 5 generations = 915 outputs**. The exact-McNemar sensitivity tool documents 80% power at two-sided alpha .05 under assumed prose-only discordance 0.05 and graph-only discordance 0.25. This is an assumption-based planning scenario, not an estimate from the old experiment, and does not prove that these probabilities are plausible. The final target and assumptions must be reviewed and frozen before any v2 confirmatory outputs exist. Do not use repeated generations as independent cases. If a defensible pool of enough cases cannot be assembled, record the limitation and lower expected precision; do not inflate the sample with weak or duplicate defects.

## Model and generation protocol

The draft proposes retaining the historical checkpoint `Qwen/Qwen2.5-3B-Instruct` at revision `aa8e72537993ba99e69dfaafa59ed015b17504d1`, FP16, non-quantized, with temperature 0.2, top-p 1.0, 256 maximum new tokens, and seeds 42–46. This keeps the model fixed so that context representation is the intended manipulated factor. It remains a proposal until the current runtime/loader/tokenizer compatibility check passes and the student researcher approves the freeze.

The three conditions must use identical system prompt, task prompt, model checkpoint, runtime, generation parameters, and shared base-context bytes. B and C must contain the same dependency endpoints, relation labels and details. Before inference, compute the model-tokenizer count for the *final chat-template-rendered sequence* for every case-condition and save SHA-256 hashes of the task prompt, system prompt, rendered context, rendered chat input and token ID sequence. Assert input tokens plus 256 generation-reserve tokens do not exceed the model context length of 32768. A whitespace-token estimate is not acceptable.

Pre-generate the case-condition-seed execution schedule, hash it, and freeze it before inference. Keep case IDs, source evidence and all ground-truth data out of prompt inputs. Archive every raw output, parsed output, parse failure, prompt/tokenizer hash, generation metadata and source commit. Do not silently retry/overwrite a record; declare retry/missingness handling before freeze.

## Case independence gate

A v2 held-out case must be a new defect, have a licensed reproducible repository source, an exact pre-fix commit and fixed commit, a pinned regression test that fails pre-fix and passes fixed, a single coherent root cause, an adjudicated multi-component dependency path suitable for CCDG, and an explicit contamination-risk assessment. Two independent reviewers must assess source revisions; a separate adjudicator resolves disagreements. Exclude all cases from the old pilot, old confirmatory benchmark, and scoring calibration. Each case requires a machine-readable assessment and source-revision evidence.

No current case IDs have been admitted to the v2 held-out pool. The current seven calibration candidates are **not eligible** for v2. Public defects can have unknown training-data exposure; document risk conservatively rather than claiming that a public case was or was not in training data.

## Freeze gates

The manifest at `data/followup_v2/protocol_manifest.json` must remain `status: draft` and `model_inference_permitted: false` until all of these are true and evidence hashes validate:

1. The separate scoring instrument calibration and human-rater reliability gate passes.
2. At least the planned number of new held-out cases have been source/revision reviewed, adjudicated, assessed and verified disjoint from all historical/calibration cases.
3. The exact model/runtime/tokenizer compatibility check passes.
4. Tokenizer-level prompts, context parity and per-input length hashes are archived; all prompts fit.
5. The randomized schedule, analysis script, missingness/retry handling, generation configuration, output schema, primary/secondary comparisons and sample-size rationale are reviewed and versioned.
6. The student researcher approves the freeze and the manifest captures the final source commit and SHA-256 fingerprints.

Do not change booleans to bypass missing real artifacts. The validator must verify evidence files and hashes, not merely trust status strings. This draft introduces no model inference and does not authorize either the old Kaggle runner or a new v2 runner.

## Prospective sample-size sensitivity audit (2026-10-10)

A separate design audit shows the proposed 61-case target has 80% power only under a relatively strong assumed imbalance in paired discordances (B-only pass 0.05; C-only pass 0.25). Under illustrative alternatives (0.05 vs 0.20) the power at 61 cases is 0.5904 and 92 cases are needed to reach 80%; under (0.05 vs 0.15) power at 61 cases is 0.3142 and 168 cases are needed. See [SAMPLE_SIZE_SENSITIVITY_AUDIT_2026-10-10.md](SAMPLE_SIZE_SENSITIVITY_AUDIT_2026-10-10.md).

These scenarios are assumptions, not model-derived estimates. Before the protocol is frozen, a qualified reviewer must assess the power calculation and justify the effect-size assumption; the sensitivity range must be declared before v2 confirmatory outputs exist. Do not reduce or increase the case count after observing v2 outcomes. If a defensible larger case pool is infeasible, report the expected precision honestly rather than adding weak or duplicated cases.

