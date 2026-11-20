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

This remains AI advisory reasoning. E1 must not be marked semantically sufficient until two independent blinded Panel B reviewers assess coded packets without source/fix exposure, then a separate adjudicator resolves any disagreement against independently prepared Panel A gold. If a plausible alternative remains, E1 must be rejected or redesigned prospectively.

## Role and acceptance boundaries

- The project lead has inspected the issue, patch, pinned source, and reproduction. The project lead may prepare and preserve packet bytes but cannot act as a blinded Panel B rater.
- Hasan has seen the E1/E2/E3 design proposal; under the approved protocol, Hasan is ineligible for blinded Panel B for this candidate. Any Panel A role would require a separately documented competence, consent, and independence check; none is presumed.
- No Panel B reviewer is currently appointed or exposure-cleared; no coded packet has been delivered or rated.
- The proposed packet set is not accepted. No model loading, inference, fine-tuning, or training is authorized.
