# Secondary model-training plan — evidence-conditioned abstention (v0.1 draft)

**Date:** 19 November 2026  
**Study:** TÜBİTAK 2204-A — Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Status:** Design proposal only. No model loading, inference, training, fine-tuning, adapter creation, or weight export is authorized by this document.

## 1. Purpose and scientific boundary

The project lead wants a trained model to be part of the broader research programme. That goal is recorded here, but training must test a falsifiable claim; it must not be used to make a preferred hypothesis appear true.

The primary v0.2 research question remains:

> On the same frozen language model and the same software-defect cases, does permitting abstention when the visible evidence does not distinguish plausible causes, compared with requiring a diagnosis, change the rate of unsupported definitive root-cause claims?

The primary P0/P1 comparison is a **fixed-base-model policy experiment**. It must not be replaced by a fine-tuned-versus-base comparison, because changing model weights at the same time as the abstention policy would confound the primary contrast.

The model-training study described here is a **separate, secondary experiment** with a separate research question:

> Does supervised fine-tuning on independently adjudicated evidence/decision examples improve evidence-conditioned selective diagnosis on previously unseen upstream projects, compared with the same frozen base model under the same abstention policy?

This secondary question can produce a positive, null, or adverse result. Training is not a prerequisite for the primary P0/P1 question and cannot be used to rescue an unfavourable primary result.

## 2. Hypotheses

- **H1 — primary policy hypothesis:** Under E3 (evidence insufficient to distinguish the predeclared alternatives), P1 reduces unsupported or contradicted definitive diagnoses relative to P0, while retaining useful diagnosis behaviour when evidence is sufficient.
- **H2 — secondary training hypothesis:** A supervised LoRA/adaptor model trained to condition its decision on visible evidence reduces unsupported/contradicted diagnoses on a project-disjoint holdout relative to the same base model under P1.
- **H3 — coverage guardrail:** Any reduction in unsupported diagnoses must not be explained merely by the trained model refusing everything. Diagnosis coverage and supported diagnosis accuracy on E1 must be reported separately; valid-abstention quality and missing-evidence usefulness must also be scored.

The project must report results that do not support H1/H2 as such. No success threshold may be selected after seeing held-out outputs.

## 3. Experimental arms

The primary experiment stays unchanged:

| Arm | Weights | Policy | Role |
|---|---|---|---|
| A | Frozen base model | P0: diagnosis required | Primary comparator |
| B | Same frozen base model | P1: evidence-aware abstention permitted | Primary treatment |

Only after the primary protocol is frozen and the training data gate is satisfied, add the separate secondary comparison:

| Arm | Weights | Policy | Role |
|---|---|---|---|
| C | Frozen base model | P1 | Secondary baseline |
| D | LoRA/adaptor fine-tuned from the exact same base revision | Same P1 | Secondary trained model |

If resources and the final preregistration support it, a 2×2 weight-status × policy design (base/LoRA × P0/P1) may be run. It must be explicitly preregistered as a separate factorial analysis; do not silently add it to the primary P0/P1 result.

## 4. Training-data requirements

Training examples must be created only from fully screened, independently accepted cases. Dataset candidate rows, technical reproduction passes, synthetic demonstrations, ChatGPT suggestions, and upstream patches are not automatically training labels.

For every training example, preserve:
- immutable case and project identity in a restricted split manifest;
- exact visible evidence packet bytes and SHA-256;
- the human-adjudicated evidence-support/answerability decision;
- the target output and its evidence references;
- provenance for every source item;
- a record of whether the case or reviewer had prior source/fix exposure.

Target behaviour:
- Diagnose only when the visible packet supports a sufficiently specific causal mechanism.
- When multiple materially different mechanisms remain plausible, abstain and identify the minimum additional evidence needed to discriminate them.
- Cite only evidence IDs present in the visible packet.
- Never receive the hidden gold, upstream fix, patch, fixed-side logs, hidden E-tier label, or held-out response as model-visible training input.

Do not derive a training target mechanically from the name E1/E2/E3. The target must be supported by the independently adjudicated visible-evidence assessment. Gold correctness and evidence support remain distinct labels.

## 5. Leakage-resistant split

The split unit is the upstream project, not an individual prompt or response. No repository, fork, mirror, project family, issue, patch, or case may appear across training, validation, and test splits.

Proposed secondary-study minimum:
- at least **80 fully accepted independent cases from 80 distinct upstream projects**;
- at least **60 cases in the training split**;
- at least **10 cases in validation**;
- at least **10 cases in the locked test split**;
- all splits frozen by upstream-project identity before training begins.

The existing inference gate is stricter than the current available evidence and separately requires at least 60 accepted cases across at least eight projects. This proposal does not lower that gate; it raises the proposed minimum for a credible trained-model holdout. If these thresholds are not reached, do not train for the research claim. Continue the base-model feasibility study and report the training study as not run.

Only training/validation projects may be used for adapter development, hyperparameter selection, prompt changes, early stopping, or threshold selection. The test split must remain unopened until the adapter, tokenizer, prompts, decoding settings, evaluator rubric, and analysis plan are frozen.

## 6. Model and training method

Candidate base model remains the exact immutable revision recorded in `MODEL_TRAINING_DECISION_2026-11-12.md` and `UNCERTAINTY_RUNTIME_LOCK.json`:

- Model: `Qwen/Qwen2.5-3B-Instruct`
- Revision: `aa8e72537993ba99e69dfaafa59ed015b17504d1`
- Tokenizer: same exact ID and revision
- Candidate runtime: Python 3.11.9, torch 2.2.1, transformers 4.43.2, accelerate 0.33.0, pending exact verification

Proposed training method: parameter-efficient LoRA adaptation, not full-model weight replacement. The exact target modules, rank, alpha, dropout, optimizer, learning rate, scheduler, batch size, gradient accumulation, sequence length, epochs, seeds, precision, quantization, checkpoint-selection rule, and stopping rule must be frozen before training. They are not chosen or tuned in this draft.

The base model must remain immutable. Preserve the base revision, tokenizer revision, training code commit, dependency lock, dataset split manifest, all training parameters, random seeds, adapter hashes, and full run logs.

The Qwen revision's recorded license identifier is `qwen-research`, not Apache-2.0. Exact license text, research-use scope, adapter/derivative terms, distribution limits, output terms, and TÜBİTAK/publication use require human review before downloading/loading/training. Metadata alone is not legal clearance. If the license cannot be approved, do not proceed with this candidate; choosing another model requires a new model decision, immutable revision, runtime lock, and preregistration amendment.

## 7. Outcomes and analysis

Primary secondary-study outcome:
- E3 unsupported/contradicted definitive diagnosis rate on the locked project-disjoint test set.

Required companion outcomes:
- valid abstention rate and quality;
- diagnosis coverage;
- fully supported, partially supported, unsupported, contradicted, and unscorable output categories;
- E1 supported diagnosis coverage and correctness;
- evidence-reference validity and schema validity;
- policy compliance;
- usefulness of missing-evidence requests;
- selective risk and risk–coverage curve;
- abstention behaviour by evidence condition;
- model size/runtime and training-resource record.

Partially supported and invalid/unscorable outputs remain separate categories; do not silently map them to success or failure. Correctness against hidden gold is scored separately from support by visible evidence.

Use case/project-clustered uncertainty intervals and paired comparisons where cases are evaluated under multiple arms. Repeated evidence tiers and generated responses are not independent cases. Report training-seed variation separately from project-sampling uncertainty. Do not claim general model self-awareness; the observable construct is evidence-conditioned decision behaviour.

## 8. Required gates before training

Training remains prohibited until every item below is independently documented:
1. The applicable no-inference/inference gate is closed according to its exact manifest and the project has explicitly authorized the relevant model operation.
2. At least 80 accepted independent cases and the proposed project-disjoint split exist; all acceptance records pass the fail-closed schema/registry validator.
3. The training labels have completed independent human adjudication; rater consent, role separation, exposure, calibration, and immutable score locks are complete.
4. Dataset, upstream source, changed files, dependencies, model, tokenizer, and any native/bundled components have completed license/provenance review.
5. No case or project overlaps across training, validation, and locked test; no patch, fix, hidden gold, answerability label, or test output leaks into model-visible inputs.
6. The model/runtime, LoRA configuration, prompt, output schema, generation parameters, training code, analysis plan, and split manifests are frozen and hash-recorded.
7. A separate training authorization is recorded after review of this plan and its prerequisites.

A successful CI test, Stage 2 reproduction, packet JSON/hash validation, or model-load smoke test does not itself satisfy these gates.

## 9. Current disposition — 19 November 2026

- Accepted cases: **0**.
- Model preflight: **not ready**; latest no-inference report records 14 blockers.
- Model revision/license: not cleared.
- Runtime: candidate, not independently verified.
- Training/validation/test splits: not created.
- Human labels and reviewer protocol: not frozen/complete.
- LoRA adapter: not created.
- Model loading, inference, fine-tuning, training: **not performed and not authorized**.

The next work is to complete candidate screening, Stage 3 human gold/alternative and evidence-tier adjudication, case acceptance, reviewer governance, and license/runtime review. Training may start only after the separate data and authorization gates above pass.
