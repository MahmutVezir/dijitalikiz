# NumPyro #1916 — AI advisory semantic-tier review

**Date:** 20 November 2026  
**Role:** Advisory analysis only. This is not Panel A gold adjudication, not a Panel B rating, not a human decision, and not case acceptance.

## Scope

This note examines whether the E1/E2/E3 packets discriminate the candidate's plausible mechanisms. It uses pinned buggy-base source and public issue/PR context. The fix patch and fixed source are not added to model-visible evidence.

## Finding on the 19 November packet set

The original E1 included the issue narrative, traceback, MCMC.run key handoff, and EnsembleSampler.sample call to random.split. This gives a strong local execution trace but leaves an important alternative underdetermined: perhaps the ensemble sampler was intended to receive a batched key and should have vectorized its internal split.

The omitted buggy-base EnsembleSampler.init implementation changes that assessment. At lines 150–183, initialization requires a batch of chain keys to determine num_chains, then explicitly selects rng_key[0], splits that singleton key, and stores the resulting scalar key in EnsembleSamplerState. The later EnsembleSampler.sample method calls random.split(rng_key) on that state key. Thus the sampler's own normal initialization path stores a scalar key; the E1 handoff in MCMC.run replaces that scalar with a per-chain batch only when resuming from _warmup_state.

The public MCMC.warmup method documentation states that after warmup, run skips the warmup adaptation phase, and the method stores _warmup_state = _last_state. The reported warmup-then-run sequence is therefore a documented lifecycle, not by itself evidence of caller misuse.

## Proposed prospective packet amendment

A separate additive proposed packet set is prepared at:

- research_candidates/evidence_abstention/numpyro_1916/OPERATIONAL_EVIDENCE_PACKET_SET_PROPOSED_V0_2_2026-11-20.json
- research_candidates/evidence_abstention/numpyro_1916/EVIDENCE_PACKET_PROVENANCE_PROPOSED_V0_2_2026-11-20.json

The existing 19 November packet set remains unchanged and preserved. The proposed E1 adds one pinned buggy-base excerpt:

- Evidence ID: NP1916_BASE_ENSEMBLE_INIT_KEY_NORMALIZATION
- Source: numpyro/infer/ensemble.py, commit 07e4c9bc4524cc0a741ba8f8ad41339d34a0288d, lines 150–183
- Parent Git blob SHA-1: 64a2870ade0565cb6547cc92d97c11502e769bfd
- Excerpt SHA-256: 3792bc9a542c5a8896cb5f399ca4147c97fadbbe4e80b0e20bb542611a82ae07

E2 and E3 are unchanged. Proposed counts are E3=1, E2=2, E1=5. Proposed packet-set SHA-256: e1730956eb9cfc9015bb43c5725f49d3ebff9dfc3c564594060209bab5e5485d.

## Advisory mechanism assessment

The combined buggy-base code path supports this causal account: the documented warmup-resume lifecycle stores a sampler state whose ensemble key is scalar; MCMC.run splits a user-supplied scalar key into per-chain keys for vectorized execution but then overwrites the warmup state's scalar key with that batch; EnsembleSampler.sample later calls scalar-key random.split on the now-batched state field. The observed shape error is consistent with this mismatch.

The additional initializer excerpt materially weakens the alternative that the sampler's initialized state is designed to hold a batch key. The documented warmup lifecycle also weakens the caller-misuse alternative. The paired base-fail/fixed-pass result in the same pinned CPU dependency environment weighs against a general JAX-version incompatibility.

This remains AI advisory reasoning only. Under the superseding v0.2 adjudication route, the project lead makes the source-aware technical-gold and E1/E2/E3 decisions; ChatGPT is an advisory critic, not a human adjudicator. The two-human Panel B requirement applies later to blinded scoring of raw model responses, not to gold or evidence-tier construction. If a plausible alternative remains under E1, the project lead should reject or redesign E1 rather than force a tier.

## Role and acceptance boundaries

- The project lead has inspected the issue, patch, pinned source, and reproduction. The project lead may prepare and preserve packet bytes but cannot act as a blinded Panel B rater.
- Hasan has seen the E1/E2/E3 design proposal; under the approved protocol, Hasan is ineligible for blinded Panel B for this candidate. Any Panel A role would require a separately documented competence, consent, and independence check; none is presumed.
- No Panel B reviewer is currently appointed or exposure-cleared; no coded packet has been delivered or rated.
- The proposed packet set is not accepted. No model loading, inference, fine-tuning, or training is authorized.


## Superseding tier-by-tier advisory review — 20 November 2026

**Status:** AI advisory only; not a project-lead tier decision, not a human rating, and not case acceptance. The controlling definitions are those in `SWE_REBENCH_V2_PROTOCOL_V0_2_EXPLORATORY_DRAFT_2026-11-16.md`: E3 leaves all predeclared mechanisms possible; E2 eliminates at least one alternative while retaining at least two mechanisms; E1 leaves exactly one mechanism matching technical gold. Packet size is not the criterion.

### E3 — current proposal: provisionally adequate

E3 contains only the frozen issue narrative and reproducer code. It establishes the reported setting (AIES, 100 vectorized chains, a `warmup()` call followed by `run()`) but contains neither the traceback nor implementation internals. On the information actually visible in this packet, caller/API misuse, a sampler-state contract problem, and an internal warmup-resume handoff problem remain possible. No root-cause alternative is defensibly eliminated. This matches the E3 definition.

### E2 — pre-amendment gap (addressed by the approved packet amendment)

The current E2 adds the issue traceback. The traceback localizes the exception to `EnsembleSampler.sample -> random.split(rng_key)` and reports a key array with shape `(100, 2)`; JAX's error text says that this call accepts a single key and directs batching through `jax.vmap`. This is useful narrowing evidence and weighs against treating the event as an unexplained JAX failure on a scalar key.

However, the current E2 does not establish from the visible packet that the reporter's `warmup()` → `run()` sequence is a documented supported lifecycle, nor that passing a scalar key to `run()` for multiple chains is an allowed input. Consequently, the caller/API-misuse alternative is not cleanly eliminated. The trace also does not show whether the batched key was intentionally part of the ensemble sampler's state contract or was introduced by an internal state replacement. I would not record E2 as a fully established semantic tier in its current form.

### E1 — pre-amendment packet and the required API-contract evidence

The three existing pinned buggy-base source excerpts form a strong implementation chain:

1. `MCMC.run` splits a scalar key into a per-chain key array and, when `_warmup_state` exists, replaces the saved state's `rng_key` with that array.
2. `EnsembleSampler.init` accepts a batched key for vectorized chains, selects `rng_key[0]`, splits that scalar, and stores the resulting scalar key in `EnsembleSamplerState`.
3. `EnsembleSampler.sample` later calls `random.split(rng_key)` on the state field.

Together with the traceback, these excerpts support the approved gold mechanism: the warmup-resume handoff replaces the scalar sampler-state key with a per-chain batch, after which the sampler treats that field as a single key. The initializer excerpt materially resolves the alternative that the ordinary ensemble sampler state is designed to store a batch.

For a strict E1 decision, the pre-amendment packet needed to carry the pinned public API contract that the reported call sequence and scalar key are supported. Without that bridge, a reviewer could still argue caller misuse rather than the internal state transition.

### Minimal prospective amendment to the packet set

Add the following two immutable source excerpts from the exact buggy-base revision `07e4c9bc4524cc0a741ba8f8ad41339d34a0288d`, file `numpyro/infer/mcmc.py`, to **E2** (and therefore also to E1):

- Suggested ID `NP1916_BASE_MCMC_WARMUP_METHOD_CONTRACT`, lines 584–586: the `MCMC.warmup` docstring says that after this call `post_warmup_state` is set and `run()` skips the warmup adaptation phase.
- Suggested ID `NP1916_BASE_MCMC_RUN_KEY_CONTRACT`, lines 624–626: the `MCMC.run` docstring says that for multiple chains a batch may be supplied and that a key without the batch dimension is split into a batch of `num_chains` keys.

These are source-contract excerpts from the pinned buggy base, not current online documentation. They do not disclose the sampler's internal state transition. With these two items, E2 would eliminate the caller-misuse/unsupported-lifecycle alternative while leaving at least two materially distinct explanations open: (a) the MCMC warmup-resume handoff violates the sampler state's scalar-key invariant, or (b) the ensemble sampler's per-step state contract is intended to be batched and its split operation is the faulty layer. E1's three existing implementation excerpts then distinguish those explanations.

**Proposed counts after amendment:** E3=1, E2=4, E1=7. The project lead approved the packet-construction amendment on 20 November 2026. The amended E3=1, E2=4, E1=7 packet set passed structural/no-inference CI on branch-head commit `43b06b48b843bbca78cde608a96edce2344cca90` (run `44761690559`, 90 tests). This proves packet structure, nesting and hashes only; semantic sufficiency and final acceptance remain separate decisions.

### Advisory recommendation — not an approval

- E3: retain as proposed.
- E2: the two pinned API-contract excerpts are now included in E2; structural CI passed. The project lead's semantic-sufficiency decision remains separate.
- E1: the amended E1 inherits the two API-contract excerpts and adds the three implementation excerpts; this supports the approved warmup-state key-shape handoff mechanism. The project lead must still decide whether exactly one mechanism remains plausible.
- Do not add the fixed patch, fixed-source excerpts, fixed-pass logs, hidden gold statement, or tier labels to model-facing packets.
- Keep the project's source-aware decision and the later blinded raw-output scoring roles separate. No human Panel B ratings or independent adjudication are being claimed here.


## Branch-head verification — 20 November 2026

- Amended packet counts: E3=1, E2=4, E1=7.
- Packet-set SHA-256: `b53d655f38466f2aa5b164a3a96c13a630e4419986401e472f2ed4371ffd7edb`.
- Structural/no-inference preflight: run `44761690559`, job `136375587794`, commit `43b06b48b843bbca78cde608a96edce2344cca90` — success; 90 tests passed.
- Research Validation (No Inference): run `44761690466` — success.
- Independent NumPyro reproducer: run `44761690320`, job `136375585065` — success. The pinned buggy base produced the expected (100, 2) key-shape error; the exact fixed merge passed the same reproducer (1 passed in 3.89s). Artifact `14640974491`, GitHub digest `sha256:7717fe6ed53ae6752325cf954ea20285279ffff679403f7a5c2c9bf20216ac49`; this latest artifact was not locally downloaded and re-hashed.
- Readiness remains blocked with 13 global blockers, one accepted case (Dishka), and `ready_for_inference=false`. No model loading, inference, fine-tuning or training occurred.

These checks do not adjudicate semantic evidence sufficiency and do not accept NumPyro as a case.
