# Completion Gate and Final Report Plan — 23 October 2026

## Purpose and current truth

This is an execution contract for finishing the evidence-abstention research. It does not claim the study is complete or that the model improves reliability.

Verified current state:
- Accepted confirmatory cases: 0; independent source projects in accepted registry: 0.
- Formal registered-study model outputs: 0.
- Candidate model: Qwen/Qwen2.5-3B-Instruct, revision aa8e72537993ba99e69dfaafa59ed015b17504d1.
- Exact study runtime: not verified; calibration labels and frozen threshold: absent.
- Verifiable preregistration: not registered; inference permission: false.
- The prior 10-output Kaggle smoke is engineering-only and excluded because it used an exposed case, a protocol-deviating prompt and a different runtime.

## Gate A — Independently validated cases

Each case must have immutable source/buggy/fixed references, exact target test, raw test logs and SHA-256 values, recorded runtime, license/provenance, root-cause rationale, leakage/exposure review and evidence packets. The buggy target must fail because of the defect; the same target must pass on the fixed state. Setup/environment failures do not qualify.

Require two independent root-cause reviewers and a disjoint pair of evidence-sufficiency reviewers. Preserve individual ratings and adjudication history. Do not invent reviewer decisions. Confirmatory minimum: 60 accepted independent cases across at least 8 upstream projects; target 80. If the minimum is not reached, label the work exploratory/feasibility and do not relax the threshold after observing results.

## Gate B — Model/runtime and evidence decision

Run a generation-free model/tokenizer load preflight in the intended CUDA environment with the exact locked package versions. Record Python, PyTorch, Transformers, Accelerate, CUDA/GPU, model/tokenizer revisions, chat-template fingerprint and artifact hashes. The prior smoke runtime is not a substitute.

The packet auditor verifies structure, hashes and citation IDs only. Its semantic status `not_assessed` must not be interpreted as semantic support. Human E1/E2/E3 labels and gold root-cause labels must never enter runtime decision logic. Validate the operational decision layer against independently authored sufficient, partial, missing and contradictory evidence examples.

Use an independent calibration set, separate from the confirmatory sample. Choose and freeze thresholds before confirmatory outputs. Report Brier score/ECE only if calibration data support those metrics; otherwise do not claim calibrated probabilities.

## Gate C — Freeze, preregister, authorize

Before confirmatory generation, freeze and hash: case registry, all evidence packets, prompts, output schema, model/tokenizer revision, runtime lock, inference runner, generation settings, rubric, reviewer calibration, primary endpoint, exclusions and analysis script. Register the protocol at a publicly or independently verifiable registry and record the URI. Obtain explicit execution authorization. Passing CI does not authorize inference.

## Gate D — Execute and analyze

Only after A–C pass:
1. Generate one output per case × evidence level × policy (6 per case; 360 at N=60, 480 at N=80).
2. Preserve raw outputs, hashes, metadata and errors. No retries, JSON repair or outcome-informed replacement.
3. Use blinded independent human ratings for root-cause correctness and packet-level evidence support.
4. Primary endpoint: E3 unsupported definitive diagnosis, paired P0 vs P1, risk difference, exact two-sided McNemar test and confidence interval.
5. Report answer coverage and E1 unnecessary abstention alongside any reduction in unsupported diagnoses. More abstention alone is not success.
6. Report invalid outputs, all deviations, inter-rater agreement, case flow, project-clustering limitations and reproducibility details.

## Stop rules

- Any failed or unverified gate keeps formal inference disabled.
- Any case exposed during pipeline debugging is permanently excluded from confirmatory analysis, regardless of outcome.
- Investigate CI failures; do not weaken checks just to make CI green.
- If reviewers, runtime, preregistration or dataset cannot be obtained by the deadline, do not claim confirmatory efficacy. Submit an exploratory report only if competition rules permit.

## Final report structure

1. Abstract and research question.
2. Background and contribution.
3. Preregistered hypotheses and design.
4. Dataset provenance, inclusion/exclusion flow and case-review protocol.
5. Model/runtime, prompts, evidence packets and abstention policy.
6. Calibration and threshold selection with held-out separation.
7. Primary and secondary outcomes, uncertainty intervals and all failures.
8. Human-rating protocol, inter-rater agreement and adjudication.
9. Limitations: public-bug training contamination, source-project clustering, sample size, lexical disagreement, token-score interpretation, calibration uncertainty and external validity.
10. Reproducibility, artifact hashes, code/data availability and license statement.
11. Conclusion strictly limited to measured evidence.

## Current conclusion

Software scaffolding and automated tests exist, but the registered scientific experiment is not complete. Existing evidence does not establish that this method reduces hallucinations or provides calibrated uncertainty. The next legitimate steps are independent case adjudication and exact-runtime no-output preflight. Formal inference must remain disabled until all gates pass.
