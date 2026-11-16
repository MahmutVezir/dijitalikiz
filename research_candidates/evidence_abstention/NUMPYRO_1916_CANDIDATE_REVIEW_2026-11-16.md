# pyro-ppl/numpyro #1916 — candidate review

**Cohort rank:** 12 of 96 primary candidates  
**Dataset instance:** pyro-ppl__numpyro-1918  
**Issue:** https://github.com/pyro-ppl/numpyro/issues/1916  
**Fix PR:** https://github.com/pyro-ppl/numpyro/pull/1918  
**Review status:** strong static bug candidate; exact dataset reproduction pending. Not an accepted case.

## 1. Defect contract

Issue #1916 reports that calling MCMC.run after MCMC.warmup with the AIES ensemble kernel raises a JAX PRNG key shape error. The reported key has a batched shape (num_chains, 2), but the ensemble sampler calls random.split expecting a single key. The issue also reports the same failure with ESS.

PR #1918 changes the warmup-state handoff for ensemble kernels: it supplies the first key from the batched key array, while retaining the original behavior for non-ensemble kernels. The PR adds a test_warmup regression test parameterized over AIES and ESS with 10 vectorized chains.

The added upstream test directly exercises the reported warmup-then-run sequence and is therefore a stronger oracle than a test of an internal helper alone.

## 2. Pinned source identity

- Repository: pyro-ppl/numpyro
- Buggy base: 07e4c9bc4524cc0a741ba8f8ad41339d34a0288d
- PR head: d5367f16abee85a1d7788784c71eb908ecb12df7
- Fixed upstream merge revision used for reproduction: 5692d2da335945b756aeae02e3720b9b7f3efef2
- PR merge commit: 5692d2da335945b756aeae02e3720b9b7f3efef2
- Issue #1916 created: 2024-11-25T14:53:29Z
- PR #1918 created: 2024-11-28T00:54:29Z
- PR body explicitly says it fixes issue #1916.

## 3. Source and dependency license screen

- Exact-base setup.py declares Apache License 2.0 and the Apache Software License classifier.
- Both changed source/test files carry SPDX Apache-2.0 headers.
- The minimal test environment uses CPU JAX only; no GPU, external service, or downloaded model is required.
- Runtime/test dependencies and transitive dependencies are version-pinned. Before upstream source tests execute, the workflow records distribution license metadata for every installed package and stops if any package lacks both a license field and a license classifier.
- This is a narrow documentary screen, not legal advice or blanket clearance for optional extras or redistribution.

## 4. Test adequacy

The exact dataset FAIL_TO_PASS selectors are extracted from the pinned Parquet row. The workflow applies the diff from the exact buggy base to the upstream merge revision and runs those selectors, then runs the same selectors on that exact merge revision.

Required result: all selected tests fail on the base with the reported PRNG key shape failure and pass on the fixed revision. Collection errors, dependency failures, or unrelated failures do not count as a successful reproduction.

## 5. Independence and exposure

- The cohort contains one primary candidate for pyro-ppl/numpyro; this project can contribute at most one accepted case.
- Issue and PR dates are after the September 2024 public release of Qwen2.5-3B-Instruct. This reduces the likelihood that this exact public issue/patch was in the released weights but does not establish complete training-data provenance.
- The student researcher has reviewed the issue and patch during candidate screening. This exposure must be recorded; perfect blinding must not be claimed.
- Related issue-family, fork/lineage, and exact dataset provenance checks remain part of final acceptance.

## 6. Current decision

Issue/patch alignment: strong.  
Root source license: Apache-2.0.  
Dependency license inventory: pending workflow evidence and review.  
Exact base-fail/fix-pass reproduction: pending.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading and inference authorization: false.
