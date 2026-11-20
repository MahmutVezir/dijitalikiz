# Project-lead E1/E2/E3 semantic decision — NumPyro #1916

**Decision date:** 20 November 2026  
**Decision maker:** Student project lead  
**Adjudication route:** SWE-rebench V2 v0.2 exploratory; single source-aware project-lead human adjudicator  
**Technical gold record:** `PROJECT_LEAD_GOLD_DECISION_NUMPYRO_1916_2026-11-20.md`  
**Packet-set SHA-256:** `b53d655f38466f2aa5b164a3a96c13a630e4419986401e472f2ed4371ffd7edb`

## Decision

**APPROVED — E3, E2 and E1 as the proposed semantic evidence hierarchy for this exploratory candidate.**

The project lead's decision in the 20 November 2026 conversation was:

- **E3:** appropriate; multiple distinct root-cause mechanisms remain possible.
- **E2:** appropriate; the pinned API-contract excerpts exclude unsupported caller lifecycle/key usage, while at least two internal mechanisms remain possible.
- **E1:** the three implementation-code excerpts strongly support the approved technical-gold mechanism; the project lead authorized progression in the established work order.

The source-aware rationale below records why the amended E1 satisfies the single-surviving-mechanism criterion. ChatGPT supplied advisory criticism only; it is not a human rater or adjudicator.

## Candidate mechanisms

- `H1_CALLER_API_LIFECYCLE_OR_KEY_USAGE`: the reported `warmup()` then `run()` sequence or scalar key passed for multiple chains is unsupported caller usage.
- `H2_WARMUP_RESUME_STATE_KEY_SHAPE_HANDOFF`: the MCMC warmup-resume handoff replaces the scalar PRNG key in the saved ensemble sampler state with a per-chain key batch.
- `H3_ENSEMBLE_SAMPLE_BATCH_KEY_CONTRACT`: the ensemble sampler's per-step state is intended to carry a batch key, but `sample()` incorrectly calls scalar `random.split()` without batching.
- `H4_GENERAL_JAX_OR_RUNTIME_INCOMPATIBILITY`: the observed exception is primarily caused by a general JAX/runtime incompatibility rather than the NumPyro state transition.

## E3 — APPROVED

**Surviving mechanisms:** H1, H2, H3, H4.

E3 contains the issue narrative and reproducer code. It reports an error after a vectorized AIES `warmup()` followed by `run()`, but it does not include the traceback, API contract or internal state transitions. It therefore does not distinguish caller/API misuse, warmup-state handoff, sampler key-batching behavior or a runtime-level explanation.

## E2 — APPROVED

**Surviving mechanisms:** H2 and H3.

E2 adds the traceback and two immutable API-contract excerpts from buggy-base commit `07e4c9bc4524cc0a741ba8f8ad41339d34a0288d`, `numpyro/infer/mcmc.py`:

- Lines 584–586 document that `warmup()` establishes `post_warmup_state` and that `run()` skips the warmup adaptation phase after this call.
- Lines 624–626 document that a scalar key is valid for multi-chain execution and is split into a batch of `num_chains` keys when no batch dimension is supplied.

The traceback localizes the failure to `EnsembleSampler.sample()` calling `random.split(rng_key)` with a key array of shape `(100, 2)`. The supported public call sequence and valid scalar-key input eliminate H1. E2 still does not reveal whether the batch is incorrectly introduced by the warmup-resume handoff (H2) or whether the sampler's per-step key handling should itself support a batch (H3). The runtime alternative is weakened by the exact same-environment fixed-revision pass, but E2 does not expose the internal state invariant; H2 and H3 remain the material alternatives for tier counting.

## E1 — APPROVED

**Surviving mechanism:** H2 only.

E1 includes all E2 evidence and adds three exact buggy-base implementation excerpts:

1. `MCMC.run`, `numpyro/infer/mcmc.py`, lines 654–660: a scalar key is split into a per-chain batch; when a warmup state exists, the saved state's `rng_key` field is replaced with that batch.
2. `EnsembleSampler.init`, `numpyro/infer/ensemble.py`, lines 150–183: initialization selects `rng_key[0]`, splits that scalar key and stores the scalar sampler-state key in `EnsembleSamplerState`.
3. `EnsembleSampler.sample`, `numpyro/infer/ensemble.py`, lines 190–193: the per-step method reads the state key and calls scalar `random.split(rng_key)`.

The three excerpts identify both ends of the state contract. The initialized ensemble state stores a scalar key; the warmup-resume branch then replaces that field with a per-chain batch; the sampling method subsequently treats the field as scalar. H3 is inconsistent with the initializer's scalar state construction. H1 is already excluded by E2's API documentation. H4 does not explain the state-shape transition and is inconsistent with the same-runtime fixed-revision pass. H2 is therefore the only surviving mechanism matching the approved technical gold.

## Evidence and integrity references

- E3: `NP1916_ISSUE_NARRATIVE_CODE`
- E2 additions: `NP1916_ISSUE_TRACEBACK`, `NP1916_BASE_MCMC_WARMUP_METHOD_CONTRACT`, `NP1916_BASE_MCMC_RUN_KEY_CONTRACT`
- E1 additions: `NP1916_BASE_MCMC_RUN_HANDOFF`, `NP1916_BASE_ENSEMBLE_INIT_KEY_NORMALIZATION`, `NP1916_BASE_ENSEMBLE_SPLIT`
- Exact source commit: `07e4c9bc4524cc0a741ba8f8ad41339d34a0288d`
- Parent Git blob for `mcmc.py`: `dd3ec0c3a782c1e1530b138153d821392ee5bebd`
- Parent Git blob for `ensemble.py`: `64a2870ade0565cb6547cc92d97c11502e769bfd`
- Packet-set structural CI: run `44761690559`, 90 tests passed.
- Independent public-API reproducer: run `44761690320`; buggy base produced the expected `(100, 2)` key-shape failure and the exact fixed revision passed.

## Decision boundaries and remaining gates

This decision approves the candidate's source-aware semantic E1/E2/E3 hierarchy only. It does **not**:

- declare NumPyro a finally accepted case;
- approve the bounded documentary license scope;
- supply the missing factual `prior_pipeline_debug_exposure` declaration;
- claim a blinded independent Panel A or Panel B review;
- waive the later two-human scoring requirement for raw model-output evidence-support ratings; or
- authorize model loading, inference, fine-tuning or training.

The project lead's researcher-source exposure remains fully disclosed. The next case-specific gates are the factual prior pipeline/debug exposure declaration, the bounded documentary license-scope acknowledgement, the schema-conformant proposed case record, fail-closed registry validation, and a separate final project-lead YES/NO decision.
