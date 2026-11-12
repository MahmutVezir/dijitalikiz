# Model training decision — 12 November 2026

## Decision

**Do not start fine-tuning for the primary confirmatory study.** The current research question tests whether an evidence-aware abstention policy improves the reliability of a fixed model under insufficient evidence. The causal comparison is P0 versus P1 with the same immutable base model, tokenizer, decoding settings, and runtime.

Fine-tuning the base model before that comparison would change the model itself and confound the effect of the abstention policy. A trained model is not required to answer the primary research question.

## What currently exists

- Base model candidate: `Qwen/Qwen2.5-3B-Instruct`, revision `aa8e72537993ba99e69dfaafa59ed015b17504d1`.
- `qwen_uncertainty_adapter.py`: inference adapter only; no training loop or optimizer.
- `uncertainty_policy.py`: pure-Python policy/calibration logic; not a neural training script.
- `uncertainty_inference_gate.py`: read-only preflight that blocks model loading/generation until all gates pass.
- Current inference manifest: `inference_allowed=false`, 0 accepted case IDs, validation gate OPEN, preregistration draft, reviewer protocol not frozen, calibration incomplete, runtime not verified.
- V12 provides 100 metadata candidates, not accepted labeled cases.

## Primary experiment sequence

1. Freeze the exact base model/tokenizer revision and runtime.
2. Build and license-clear the case dataset.
3. Have independent, disjoint reviewer panels label root-cause correctness and evidence sufficiency without seeing model outputs or hidden labels.
4. Build E1/E2/E3 evidence packets without leaking the gold root cause, patch, or answerability label into the prompt.
5. Freeze P0 and P1 prompts/policies and the analysis plan before generation.
6. Run the same fixed model under both conditions.
7. Evaluate supported correctness, unsupported definitive diagnosis, abstention quality, coverage, selective risk, risk-coverage curves, and paired statistical comparisons.
8. Keep a project-disjoint holdout to test generalization.

## When fine-tuning could be justified

Fine-tuning may be a secondary experiment only after:
- at least 60 independently accepted cases (target 80) across at least eight projects;
- an independently labeled training/calibration set and a separate project-disjoint test set;
- a frozen preregistration and complete license review;
- documented prevention of train/test leakage and prompt/patch leakage;
- a distinct research question and a comparison against the frozen-base-model policy.

If using Qwen2.5-3B-Instruct under the Qwen Research License, any adapter must remain a Qwen derivative and comply with the exact license version. Do not use Qwen outputs to improve a different LLM. If a more permissive license is required, evaluate Qwen2.5-1.5B-Instruct (Apache-2.0) as a separate model choice and freeze a new revision/configuration.

## Current prohibition

Until the inference gate is explicitly and lawfully closed:
- do not load the model in a research run;
- do not generate confirmatory outputs;
- do not fine-tune or create adapter weights;
- do not treat V12 metadata candidates or the historical CCDG archive as training labels.
