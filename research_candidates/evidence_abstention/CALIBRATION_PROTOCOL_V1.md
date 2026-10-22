# Calibration protocol — evidence-abstention study v1

**Status: draft. Calibration data is empty; no confidence probability or threshold is currently valid.**

## Target label

A diagnosis is positive only when it is adjudicated correct and supported by the exact evidence packet shown to the model. A correct guess without packet support is a negative outcome. Abstention quality is scored separately. Invalid or unscorable outputs must not be silently labeled correct.

Labels come from the independent blinded review process in `RATER_RUBRIC_AND_ADJUDICATION_V1.md`. Preserve independent ratings and the adjudicated label.

## Separation

- Calibration and confirmatory cases must be disjoint at the underlying defect/root-cause level.
- No confirmatory output may be used to fit the calibrator or revise thresholds.
- Hidden E1/E2/E3 labels must not enter runtime model inputs or decision logic.
- Freeze calibration data, output hashes, adjudication records, model/tokenizer revision, prompt/schema hashes and scoring implementation before confirmatory inference.
- Five sampled responses are not five independent labeled examples. Candidate zero remains the predeclared decision output.

## Current mapping

The current score combines available uncertainty signals: mean normalized generated-token entropy, lexical disagreement across sampled answers, one minus independently assessed claim-support coverage, and self-check conflict. This is an engineering score, not a probability or a pure epistemic-uncertainty estimate.

The current calibrator uses five equal-width bins with Laplace smoothing and at least eight labeled observations per bin. Underpopulated bins yield no probability and must force abstention. Do not merge bins or change their count after observing confirmatory outcomes.

## Required gates

1. Calibration data is non-empty, provenance-checked, adjudicated and disjoint from confirmatory cases.
2. Each row has a unique record ID, uncertainty score in [0,1], binary adjudicated label, raw-output hash, packet hash, model/runtime fingerprints and review references.
3. Report bin counts and underpopulated bins. Those bins remain fail-closed.
4. Report Brier score and ECE on held-out calibration/validation observations with sample counts and bin definitions. Training-only metrics are not evidence of generalization.
5. Freeze minimum confidence and maximum uncertainty thresholds using calibration/validation data before confirmatory inference. Record the selection objective and the costs of unsupported diagnoses versus unnecessary abstentions.
6. Keep the inference gate closed if held-out calibration or independent runtime claim-support/contradiction signals are missing.

## Separate unresolved dependency: runtime evidence checker

Calibration maps a score to observed reliability; it does not create semantic evidence-support signals. The live decision path still needs an independently specified and validated way to assess claim support, explicit contradictions and self-check conflict without using gold E1/E2/E3 labels. The structural packet validator does not supply these semantic signals. Until a candidate checker is validated on disjoint data and frozen, the system must not assert calibrated confidence or proceed to confirmatory inference.

## Deviations

Any change to bin count, minimum observations, target definition, threshold objective, calibration split or signal calculation requires a new protocol version before confirmatory inference. Never select changes based on confirmatory results.
