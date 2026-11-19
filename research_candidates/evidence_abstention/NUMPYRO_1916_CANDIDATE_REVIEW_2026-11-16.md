# pyro-ppl/numpyro #1916 — candidate review

**Cohort rank:** 12 of 96 primary candidates  
**Dataset instance:** `pyro-ppl__numpyro-1918`  
**Issue:** https://github.com/pyro-ppl/numpyro/issues/1916  
**Fix PR:** https://github.com/pyro-ppl/numpyro/pull/1918  
**Review status:** provisional technical candidate. The 18 November 2026 branch-head repeat now confirms the exact dataset selectors fail on the pinned buggy base and pass on the pinned upstream merge revision. Stage 3 human adjudication, exposure/independence and license-scope review remain open. The case is **not accepted**.

## 1. Defect contract

Issue #1916 reports that calling `MCMC.run` after `MCMC.warmup` with an AIES ensemble kernel raises a JAX PRNG-key shape error in vectorized multi-chain execution. The reporter also states that ESS exhibits the same error.

PR #1918 changes the warmup-state handoff for ensemble kernels: when `_warmup_state` exists, it supplies the first key from the batched key array; non-ensemble kernels retain the prior behavior. The PR adds a `test_warmup` regression test parameterized over AIES and ESS with 10 vectorized chains.

## 2. Pinned source and dataset identity

- Upstream repository: `pyro-ppl/numpyro`
- Buggy base: `07e4c9bc4524cc0a741ba8f8ad41339d34a0288d`
- PR head: `d5367f16abee85a1d7788784c71eb908ecb12df7`
- Fixed upstream merge revision: `5692d2da335945b756aeae02e3720b9b7f3efef2`
- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Exact row: `pyro-ppl__numpyro-1918`
- Canonical row SHA-256: `d0dfd87ddd0598ebf368352385419aad6e2d571d2ac83dad04fe57612a7b9646`
- Row metadata: `pyro-ppl/numpyro`, base SHA above, `2024-11-28 00:54:29`, Python, Apache-2.0
- Frozen selectors:
  - `test/infer/test_ensemble_mcmc.py::test_warmup[AIES]`
  - `test/infer/test_ensemble_mcmc.py::test_warmup[ESS]`

The dataset row was authenticated in the run and stored in the artifact. The two selectors are test variants within one upstream project; they are not two independent cases.

## 2A. Exact source-code cross-check

The upstream files were fetched independently at the pinned revisions and compared around the failing path:

- Buggy-base `numpyro/infer/mcmc.py`, Git blob SHA-1 `dd3ec0c3a782c1e1530b138153d821392ee5bebd`: lines 654–660 split a scalar key into per-chain keys, then pass the resulting array unchanged into `_warmup_state`.
- Buggy-base `numpyro/infer/ensemble.py`, Git blob SHA-1 `64a2870ade0565cb6547cc92d97c11502e769bfd`: lines 190–193 unpack the state and call `random.split(rng_key)`.
- Fixed `numpyro/infer/mcmc.py`, Git blob SHA-1 `7dd596bca382c4f6517e93458c5806c690cddb59`: lines 661–664 use `rng_key[0]` only for ensemble kernels and preserve the full key array for non-ensemble kernels.
- Fixed regression test file, Git blob SHA-1 `bda377b993ef198960eddc0b27b9e217978d20a3`: lines 101–115 add the AIES/ESS vectorized warmup-then-run test.

The source-level difference matches the observed runtime trace. These anchors support the proposed mechanism but do not replace Stage 3 human adjudication.

## 3. Latest exact Stage 2 reproduction — 18 November 2026

Latest branch-head workflow: https://github.com/MahmutVezir/dijitalikiz/actions/runs/44338919763

- Workflow run: `44338919763`
- Job: `134923384282` (`numpyro-issue-1916-reproduction`)
- Job conclusion: **success**
- Artifact ID: `14441559416`
- Artifact: `numpyro-issue-1916-reproduction`
- Artifact ZIP SHA-256: `b90d9c22614e277c3888cca9d7d62b97dfc51523bf9d145e20083e9a6c5ff360`
- Independent local verification: outer SHA-256 matched the GitHub artifact digest; ZIP CRC passed; all 15 payload-file hashes in `SHA256SUMS.txt` passed.

Observed selector results, using the same pinned CPU environment and the same two test selectors:

| Revision | AIES selector | ESS selector | Contract |
|---|---:|---:|---|
| Buggy base `07e4c9b...` | Executed and failed with the reported PRNG-key shape error | Executed and failed with the reported PRNG-key shape error | 2/2 expected failures |
| Fixed merge `5692d2d...` | Passed | Passed | 2/2 passes |

The failing path reaches `numpyro/infer/ensemble.py` in `EnsembleSampler.sample`, where `random.split(rng_key)` receives a traced key array with shape `(10, 2)`; JAX requires one key at this call site. The fixed run passes both selectors (one pass per selector). The reporter's original example uses 100 chains; the pinned regression selectors exercise 10 chains.

Relevant artifact hashes:
- Full upstream PR patch: `d05cbdbc3b934c55ace104d7d031c9987d61db5e1abba815104eab8004af5512`
- Dataset-only test patch applied to the buggy base: `03df1473e0a8ebcdba4f5981b2f8dfeef57484088a66c495bcc903204dbb51e4`
- Buggy-base test log: `0c4e0e335b80877185ab2b54ec527add0bd1e1b9c733511c4f71aa09e4ba20c1`
- Fixed-revision test log: `e268b6d982d0d335970c28310727c3e822e7e1684a076db2f2b854b9b186901b`
- Dependency lock file SHA-256: `8a160de15a15792632268e9840879fe262b98413ac1c5fe7bcf4253631f6bbb5`
- Dependency-license inventory artifact SHA-256: `20b6109dae0af95a6c4917cadca00c958e5aa9cc02f11c536854c78305d7eaba`

This closes the previous review's statement that the corrected workflow had not run. The 18 November repeat is the current evidence; the historical failed attempt against the fork-only PR-head SHA remains recorded as workflow history, not as the current result.

## 4. Source and dependency license screen

- The exact-base NumPyro source declares Apache License 2.0; both changed source/test files carry SPDX Apache-2.0 headers.
- The reproduction uses a CPU-only pinned environment. No GPU, external service or downloaded model is required.
- The lock explicitly pins 17 runtime/test packages and their transitive requirements. The workflow recorded license text/classifier metadata for all 17 before executing upstream source tests; the metadata-presence gate passed.
- The captured NumPy 1.26.4 metadata identifies its binary distribution's bundled OpenBLAS (BSD-3-Clause), LAPACK (BSD-3-Clause-Attribution) and GCC runtime library/libgfortran (GPL-3.0-with-GCC-exception). This merits a scope/notice check; it does not by itself establish a license conflict or determine what must be redistributed in the final project artifact.
- Metadata presence is not legal clearance. The inventory does not replace review of bundled components, notices, redistribution scope or competition-use conditions.
- Project-lead acknowledgement of the narrow dependency/license scope remains open. This is not legal advice or blanket approval for optional extras or redistribution.

## 5. Proposed technical mechanism and alternatives

A separate Stage 3 proposal is recorded in `NUMPYRO_1916_GOLD_AND_EVIDENCE_TIERS_DRAFT_2026-11-18.md`. In brief, the leading mechanism is a mismatch between the batched per-chain PRNG key carried through the warmup-state path and the singleton key expected by `EnsembleSampler.sample`. The upstream fix's conditional selection of `rng_key[0]` for ensemble kernels is consistent with that mechanism.

The mechanism, alternative hypotheses, and the proposed E1/E2/E3 evidence subsets are **drafts for project-lead adjudication**. The fix patch and fixed-revision pass records are reserved for hidden adjudication evidence and are not proposed as model-visible packet items, to avoid leaking the correction. The three-tier set is not yet operationalized or validated.

## 6. Independence, exposure and acceptance

- The cohort contains one primary candidate for `pyro-ppl/numpyro`; the project can contribute at most one accepted case.
- The student project lead has reviewed the issue, PR, source patch and reproduction results during candidate screening. This exposure is disclosed; perfect blinding is not claimed.
- Rater B's case-specific exposure/independence screen and participation status have not been confirmed. Rater B is for blinded model-output scoring only, not technical-gold or E1/E2/E3 adjudication.
- Fork/lineage, issue-family duplication and the final candidate-specific exposure decision remain open.
- The public issue/PR dates are after the September 2024 release of Qwen2.5-3B-Instruct. This timing reduces one narrow exposure concern but does not establish complete training-data provenance.

Current disposition:
- Static issue/patch alignment: strong.
- Exact dataset row and selectors: authenticated.
- Stage 2 exact base-fail/fixed-pass: passed, repeated on the 18 November branch head.
- Source/dependency documentary metadata: recorded; human license-scope sign-off pending.
- Technical gold and at least two alternatives: proposed, not adjudicated.
- E1/E2/E3 semantics and packet hashes: proposed, not frozen or validated as a packet set.
- Independence/exposure review: open.
- Stage 3 adjudication: not complete.
- Final case acceptance: **not accepted**.
- Model loading, inference and fine-tuning authorization: **false**.


## Stage 3 packet construction addendum — 19 November 2026

The project lead reports approval by himself and Hasan to proceed with the E1/E2/E3 design logic, conditional on preserving the scientific safeguards. This is not semantic tier adjudication or case acceptance.

Two real-case files were added:
- `numpyro_1916/OPERATIONAL_EVIDENCE_PACKET_SET_V0_1_2026-11-19.json`
- `numpyro_1916/EVIDENCE_PACKET_PROVENANCE_V0_1_2026-11-19.json`

Packet-set SHA-256: `7156e7c0bebf694946495b638f8dd21fbe45b7fbafde2607e6cc11e8b4f9bdfc`.

The exact issue-row excerpts were reconstructed from the immutable dataset row and checked against the recorded UTF-8 byte ranges and SHA-256 values: narrative/reproducer bytes [0,836), traceback bytes [838,5775). The two buggy-base source excerpts were fetched at commit `07e4c9bc4524cc0a741ba8f8ad41339d34a0288d` and their excerpt hashes match the proposal: `mcmc.py` lines 654–660 and `ensemble.py` lines 190–193. The inner packets contain 1, 2 and 4 items for E3, E2 and E1 respectively; repeated items are byte-identical and the evidence ID sets are strictly nested.

A real-packet regression test was added to `implementation/test_evidence_level_packet_set.py`, calling the existing `validate_packet_set` with the externally pinned packet-set SHA. Its CI result has not yet been observed, so the existing operational validator is **not yet reported as passed on this real packet**. The manifest construction and SHA-256 computations were performed; CI confirmation remains pending.

Semantic adequacy remains open. In particular, the E1 source excerpts expose both the MCMC key-array handoff and the ensemble sampler's scalar `random.split` call, but an independent panel must decide whether this truly eliminates the sampler-contract alternative. The project lead's design approval cannot substitute for Panel B's blinded mechanism ratings. No fix patch, fixed-pass log, gold label, or E-level label is included in the model-facing inner packets. The outer packet set is for preparation/validation only.

Current disposition: Stage 2 passed; Stage 3 packet construction complete; structural CI validation pending; semantic adjudication pending; exposure/independence and human license-scope review open; final case acceptance remains `not_accepted`; inference remains unauthorized.
