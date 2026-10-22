# Completion Gate and Final Report Plan — 23 October 2026

## Purpose

This document defines what "complete" means for the evidence-abstention research project. It does not claim that the study is complete, that any case has been accepted, or that the model has demonstrated improved reliability.

## Current verified state

- Accepted confirmatory cases: 0.
- Independent upstream projects represented in the accepted registry: 0.
- Formal model outputs in the registered study: 0.
- Candidate model: `Qwen/Qwen2.5-3B-Instruct`, revision `aa8e72537993ba99e69dfaafa59ed015b17504d1`.
- Exact study runtime: not verified.
- Calibration dataset and frozen thresholds: not available.
- Verifiable preregistration: not registered.
- Inference permission: false.
- Existing 10-output Kaggle smoke: engineering-only, previously exposed case and protocol deviation; excluded from confirmatory evidence.

## Minimum completion gates

### Gate A — Dataset and case validation

For each proposed case, preserve immutable source revision, buggy/fixed revisions, exact test command, test logs and hashes, runtime fingerprint, license/provenance, root-cause evidence, and exposure/leakage review. The buggy revision must reproduce the target failure and the fixed revision must pass the same target test in the recorded compatible environment. Environment/setup errors do not count as reproduced bugs.

Require two independent root-cause reviewers and a disjoint pair of evidence-sufficiency reviewers per accepted case. Keep individual ratings and adjudication history. Do not infer or fabricate reviewer approval. Require at least 60 accepted independent cases from at least 8 upstream projects for confirmatory analysis; target 80. If this cannot be reached, label the study exploratory/feasibility and do not relax the threshold retrospectively.

### Gate B — Model, runtime, and decision mechanism

Run a model-generation-free load preflight in the intended CUDA environment using the exact pinned model/tokenizer revision and locked package versions. Record Python, PyTorch, Transformers, Accelerate, CUDA/GPU, tokenizer/chat-template fingerprint, model files and hashes. A smoke using a different runtime is not a substitute.

The structural packet auditor only checks packet integrity and citation IDs. Its `semantic_support_status=not_assessed` must not be treated as evidence that a claim is supported. Human evidence labels must never be passed to the runtime decision policy. Before confirmatory inference, the operational decision layer must be validated against independently authored examples for missing, contradictory, insufficient and sufficient evidence; no gold answerability labels may be used as runtime inputs.

Calibration observations must be independent of the confirmatory sample. Fit calibration and choose the abstention threshold on the calibration/validation split, report Brier score and ECE with limitations, then freeze the calibrator, threshold and hashes before confirmatory inference. If calibration data are inadequate, do not report calibrated probabilities; use only a clearly labeled uncalibrated abstention policy or postpone the confirmatory study.

### Gate C — Preregistration and authorization

Before generating confirmatory outputs, freeze and hash:
- case registry and all E1/E2/E3 evidence packets;
- prompt conditions and output schema;
- model/tokenizer revision and runtime lock;
- inference runner and generation parameters;
- human-rating rubric, adjudication rules and reviewer-calibration record;
- primary endpoint, exclusions, sample-size rule and analysis script.

Register the protocol at a public or otherwise independently verifiable registry and record the URI. Obtain explicit study execution authorization. Passing a CI check is not authorization to run inference.

### Gate D — Confirmatory execution and analysis

If and only if Gates A–C pass:
1. Execute one output per case × evidence level × policy (6 outputs/case; 480 outputs at N=80, 360 at N=60).
2. Store raw outputs unchanged, output hashes, run metadata and errors. No retries, JSON repair, or post-hoc case replacement.
3. Have blinded independent raters score answerability-independent evidence support, root-cause accuracy, abstention and missing-evidence usefulness.
4. Evaluate the predeclared primary endpoint: E3 unsupported definitive diagnosis, paired P0 vs P1, risk difference and two-sided exact McNemar test with confidence interval. Report all invalid outputs and prespecified sensitivity analyses.
5. Report E1 unnecessary abstention and answer coverage alongside unsupported-diagnosis reduction. More abstention alone is not success.
6. Include inter-rater agreement, case flow, project-cluster limitations, code/data availability, and all deviations.

## Stop rules

- Any failed or unverified gate keeps formal inference disabled.
- Any exposure to a case during pipeline debugging permanently excludes that case from the confirmatory sample, independent of outcome.
- A CI failure is investigated and documented; do not bypass it by weakening tests without a justified fix.
- If the required independent reviewers, runtime, preregistration, or dataset cannot be obtained by the deadline, submit an honestly labeled exploratory study only if allowed by the competition rules; do not claim confirmatory efficacy or finalist-level certainty.

## Final report outline

1. Abstract and research question.
2. Background and contribution.
3. Hypotheses and preregistered design.
4. Dataset construction, source provenance, inclusion/exclusion flow and case-review protocol.
5. Model, exact runtime, prompts, packet construction and abstention policy.
6. Calibration and threshold selection, including held-out separation.
7. Primary and secondary outcomes with confidence intervals and all failures.
8. Human rating protocol, inter-rater agreement and adjudication.
9. Threats to validity: public-bug training contamination, source-project clustering, small sample, lexical disagreement limitations, generation-score interpretation, calibration uncertainty and external validity.
10. Reproducibility, artifact hashes, code and ethical/licensing statement.
11. Conclusion limited to the measured evidence.

## Present conclusion

The software scaffold and some automated tests exist. The registered scientific experiment is **not complete**. Current evidence does not establish that the proposed method reduces hallucinations or improves calibrated uncertainty. The next legitimate completion work is independent case adjudication and the no-output exact-runtime preflight; confirmatory inference must remain disabled until all gates pass.
