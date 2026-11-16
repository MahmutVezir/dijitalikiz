# qutip/qutip issue #2646 — candidate review

**Cohort rank:** 39 of 96 primary candidates  
**Dataset instance:** qutip__qutip-2694 (exact row identity to be authenticated by the workflow)  
**Issue:** https://github.com/qutip/qutip/issues/2646  
**Fix PR:** https://github.com/qutip/qutip/pull/2694  
**Review status:** issue/patch alignment and root-license screen passed; exact source build and dataset reproduction pending. Not an accepted case.

## 1. Defect contract

Issue #2646 reports that wrapping an existing QuTiP Coefficient with a new args dictionary does not update the arguments used when evaluating that coefficient. The example creates a coefficient with a=1, then constructs a second coefficient from it with a=2, but evaluation still uses the original argument.

PR #2694 changes the internal _return helper to apply replace_arguments(args) when a new args mapping is supplied. It also changes mutable default dictionaries to None and normalizes None to empty mappings. The PR adds a focused regression test: coefficient(coeff1, args={"a": 2}) must evaluate to 2.

The independent reproducer uses the same public coefficient API and checks the updated argument value. It does not depend on QobjEvo construction or external data.

## 2. Pinned source identity

- Repository: qutip/qutip
- Buggy base: b821b1aa8c98a00f58014e7ec02cc9cbef701ce4
- Fixed PR head: 61df3c7bccf474aba393940581ffbbeccf5da366
- Issue #2646 created: 2025-03-05T18:35:23Z
- PR #2694 created: 2025-05-15T15:48:33Z
- Exact-base LICENSE.txt Git blob: bb2d6131bb8f4820a2e29714fb4ce1792e0215b6
- Exact-base pyproject.toml Git blob: 888bbb161e1d432e23c22725a9497bcc132c096b
- Exact-base setup.cfg Git blob: 382021a63c177b81ac9ea5c743dc5f6907086eac
- Exact-base license: BSD 3-Clause.

## 3. Reproduction and dependency scope

QuTiP uses compiled Cython extensions. The workflow pins Cython, NumPy, SciPy, setuptools, wheel, packaging, and pytest, then builds the exact upstream source in editable mode. The source build is required; testing against a separately installed QuTiP release would not authenticate the candidate.

The workflow records installed distribution license metadata before building or executing upstream source. No GPU, external service, or private fixture is required. This is a narrow screen for the pinned build/test environment, not blanket legal clearance for optional QuTiP extras or redistribution.

## 4. Dataset selector requirement

The workflow authenticates the exact Parquet row qutip__qutip-2694, records its canonical row hash and FAIL_TO_PASS selectors, applies the exact PR diff to the buggy base, and runs every selector on both base and fixed revisions. Every base failure must identify the stale coefficient argument; every fixed selector must pass. Build or collection errors do not count as reproduction.

## 5. Independence and exposure

- The frozen primary cohort contains one qutip/qutip candidate; this repository can contribute at most one accepted case.
- Issue and PR were created in March/May 2025, after the September 2024 public release of the pinned Qwen2.5-3B-Instruct family. This temporal ordering lowers the likelihood that the exact public issue/patch was present in the released weights, but does not prove the model's full training-data cutoff.
- The student researcher has reviewed the issue and PR during candidate screening; perfect blinding must not be claimed.
- Related issue-family and repository-lineage review remains required.

## 6. Current decision

Issue/patch alignment: strong.  
Independent coefficient reproducer: prepared; source build/workflow pending.  
Dataset FAIL_TO_PASS selectors: pending exact-row authentication and execution.  
Build dependency/license inventory: pending workflow evidence and human review.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading/inference authorization: false.
