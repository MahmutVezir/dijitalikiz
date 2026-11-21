# qutip/qutip issue #2646 — candidate review

**Cohort rank:** 39 of 96 primary candidates  
**Dataset instance:** qutip__qutip-2694 (exact row identity to be authenticated by the workflow)  
**Issue:** https://github.com/qutip/qutip/issues/2646  
**Fix PR:** https://github.com/qutip/qutip/pull/2694  
**Review status (updated 21 Nov 2026):** Stage 2 exact source build, one-test independent reproducer, exact dataset row and frozen selector base-fail/fixed-pass verified; latest artifact independently downloaded and checked. Stage 3 source-aware matrix and advisory gold/tier proposal prepared. Prompt/selector scope review, prior exposure declaration, human license review and final acceptance remain open. Not an accepted case.

## 1. Defect contract

Issue #2646 reports that constructing a QobjEvo from an existing QuTiP Coefficient with an updated args mapping does not change the arguments used for evaluation. Important prompt-quality caveat: the example as published includes `args={"g:2"}`, which is a set containing one string, not the intended dictionary `{"g": 2}`. Do not silently correct the model-visible prompt.

PR #2694 changes the internal _return helper to apply replace_arguments(args) when a new args mapping is supplied. It also changes mutable default dictionaries to None and normalizes None to empty mappings. The PR adds a focused regression test: coefficient(coeff1, args={"a": 2}) must evaluate to 2.

The historical Stage 2 independent reproducer uses the public `coefficient(existing_coefficient, args={...})` API directly and checks the updated argument value. It does not construct QobjEvo. The frozen selector exercises the same narrower API path; preserve this issue-to-selector/reproducer scope discrepancy.

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

The workflow records installed distribution license metadata before building or executing upstream source. The inventory includes Cython 3.0.11 (Apache-2.0), NumPy 2.1.3 and SciPy 1.14.1 (BSD-family licenses), pytest/iniconfig/pluggy (MIT), Pygments (BSD-2-Clause), metadata gaps for packaging 24.2, setuptools 75.6.0 and wheel 0.45.1 beyond license classifiers, and PyArrow 19.0.1 for dataset extraction (Apache Software License). NumPy's binary distribution also declares bundled OpenBLAS, LAPACK and GCC runtime components with their own license notices. Canonical package license texts and bundled/native notices require human review. This is not blanket clearance for optional QuTiP extras or redistribution.

## 4. Dataset selector requirement

The workflow authenticated the exact Parquet row `qutip__qutip-2694`, canonical row SHA-256 `16ed66f7a865915697f5fbed540a56e3017ccfe460f3d5bc94d5918a63e9c1ee`, and one FAIL_TO_PASS selector: `qutip/tests/core/test_coefficient.py::test_coefficient_update_args`. The selector fails on the exact buggy base with value 1 instead of 2 and passes on the exact fixed revision. Build/collection errors are not counted as reproduction.

## 5. Independence, researcher exposure and temporal provenance

- The frozen primary cohort contains one qutip/qutip candidate; this repository can contribute at most one accepted case.
- Targeted issue-family searches found no exact duplicate candidate. This is not an exhaustive repository-wide historical issue audit.
- Public issue comments include a maintainer statement that ignoring args is a bug and a later comment that directly identifies `coefficient()` as failing to update args, with a minimal re-wrapping example. These comments are not part of the frozen dataset problem_statement, but were reviewed by the researcher.
- Researcher source exposure is now **full** for the issue comments, PR diff/review comments, exact base/fixed source, reproducer and Stage 2 artifacts. Perfect blinding must not be claimed.
- Project-lead prior pipeline/debug exposure declaration remains pending; it must not be inferred from other candidates.
- Issue/PR chronology postdates Qwen2.5's public release in September 2024. A separate temporal screen records the bounded conclusion and its limitations.

## 6. Current Stage 3 decision

- Proposed gold: `COEFFICIENT_BUILDER_PASSTHROUGH_DISCARDS_UPDATED_ARGS`.
- Advisory tiers: E3 ABSTAIN; E2 ABSTAIN; E1 ANSWER.
- E2 eliminates a QobjEvo-only explanation because the direct public coefficient factory reproduces the stale value outside QobjEvo; builder dispatch/kwargs handling and replacement-method explanations remain until E1.
- E1 source shows QobjEvo forwards args to `coefficient()`, the factory passes args in kwargs and dispatches an existing Coefficient to `_return`, and buggy `_return` simply returns the original object. `FunctionCoefficient.replace_arguments` is implemented to return a new coefficient with the merged args.
- Stage 2 historical single-test snapshot passed base-fail/fixed-pass. A later three-test expansion was committed but its CI result is not yet verified.
- Prompt/selector scope gap: original QobjEvo snippet is malformed (`args={"g:2"}`); the verified reproducer and frozen selector test the direct coefficient factory. Project-lead sample-suitability review is required.
- Gold/tier approval, prior exposure declaration, temporal acknowledgement, canonical dependency/license notices and bounded scope acknowledgement: pending.
- Final case acceptance: **not accepted**. Registry inclusion: false. Model loading/inference authorization: false.

## 7. Latest independently audited Stage 2 repeat — 2026-11-19

- Workflow: [run 44500943717](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44500943717)
- Job: `135481445830` — successful
- Artifact: [qutip-issue-2646-reproduction](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44500943717/artifacts/14518471928)
- Artifact SHA-256: `ecbc4ff3f3640f15603020331bffb177d4a1c51282b66358c11a3a6078c673cc`
- Independent local audit: ZIP CRC passed; all 14 entries in `SHA256SUMS.txt` verified.
- Dataset row: `qutip__qutip-2694`
- Canonical dataset-row SHA-256: `16ed66f7a865915697f5fbed540a56e3017ccfe460f3d5bc94d5918a63e9c1ee`
- Frozen buggy base: `b821b1aa8c98a00f58014e7ec02cc9cbef701ce4`
- Fixed revision: `61df3c7bccf474aba393940581ffbbeccf5da366`
- Exact `FAIL_TO_PASS` selector: `qutip/tests/core/test_coefficient.py::test_coefficient_update_args`
- Selector result: 1/1 expected failure on buggy base; 1/1 pass on fixed revision.
- Independent reproducer: failure on buggy base (`AssertionError: 1 != 2)); pass on fixed revision.
- Exact upstream `LICENSE.txt`: BSD 3-Clause. Dependency license inventory retained in the artifact; this is not a substitute for human license review.

### Scope caveat

The issue's report demonstrates the stale-argument behavior through `QobjEvo`; the independent reproducer and frozen selector exercise the underlying public coefficient-argument update behavior more narrowly. The base/fix contrast is reproducible, but the Stage 3 gold record must explicitly preserve this difference rather than imply the reproducer is a verbatim replay of the complete issue example.

### Decision after repeat

Stage 2 technical reproduction: **passed**. Stage 3 gold mechanism/alternative adjudication, independent E1/E2/E3 semantic review, training-exposure assessment, human license review and final case acceptance: **not completed**. Model loading, inference and fine-tuning remain unauthorized.
