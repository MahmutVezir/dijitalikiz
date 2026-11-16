# wntrblm/nox #919 — candidate review

**Cohort rank:** 6 of 96 primary candidates  
**Dataset instance:** wntrblm__nox-922  
**Issue:** https://github.com/wntrblm/nox/issues/919  
**Fix PR:** https://github.com/wntrblm/nox/pull/922  
**Review status:** static issue/patch and root-license screen passed; exact reproduction pending. Not an accepted case.

## 1. Defect contract

Issue #919 reports that a pyenv shim named uv can be present on PATH even when it cannot launch the actual uv executable. Nox's old discovery path treats the PATH hit as proof that uv is available. A later Nox command then invokes the broken shim and fails with exit code 127.

PR #922 changes find_uv to query the candidate executable's version before classifying it as available. A failed version command produces version 0.0 and the PATH shim is rejected. The change is limited to nox/virtualenv.py and tests/test_virtualenv.py.

The independent issue reproducer creates a local executable named uv that emits the pyenv-style error and exits 127. It checks the public HAS_UV discovery result in a fresh interpreter process. Expected: the buggy base reports True; the fixed revision reports False.

## 2. Pinned source identity

- Repository: wntrblm/nox
- Buggy base: 97e0fad6a4036d610591a52e9ad0cfbe74a31af3
- Fixed PR head: 5c4000550325fd1ad036716d9e600ef7411bed3d
- PR merge commit: c62875562eb5140431ef874ff66179ad7947c4d0
- Issue #919 created: 2025-01-29T22:52:33Z
- PR #922 created: 2025-01-31T20:53:30Z
- PR #922 explicitly says it fixes issue #919.

## 3. Source and dependency license screen

- Exact-base root LICENSE is Apache-2.0.
- Exact-base pyproject.toml declares Apache-2.0.
- The changed files are covered by the repository license; no external fixture or third-party source file is required for the independent reproducer.
- The test environment uses the Nox runtime dependencies declared in the exact-base pyproject plus pytest and their pinned transitive dependencies. The lock is isolated from the upstream source and installed with --no-deps.
- Before any upstream test is executed, the workflow records distribution license metadata for every installed package and stops if a package has no license field or license classifier. The resulting inventory must be reviewed before treating the license gate as cleared.
- No optional uv package is installed. A local fake pyenv shim is used to reproduce the failure.
- This is a narrow documentary screen, not legal advice or blanket clearance for optional extras, redistribution, or later experiments.

## 4. Test adequacy

The upstream PR changes the test_find_uv cases to include version-command success and failure paths. The dataset FAIL_TO_PASS selectors are extracted from the pinned Parquet row, rather than manually guessed.

The independent reproducer separately checks the actual issue behavior: a PATH-visible uv shim exits 127, and Nox must not set HAS_UV to True. Both the upstream dataset selectors and the independent reproducer must fail on the exact buggy base and pass on the exact fixed revision. Collection errors are not accepted as defect-specific failures.

## 5. Independence and exposure

- The cohort contains one primary candidate for wntrblm/nox; this project can contribute at most one accepted case.
- The issue and PR were created after the pinned Qwen2.5-3B-Instruct public release in September 2024. This reduces the likelihood that this exact public issue/patch was in the released weights, but does not prove full training-data provenance.
- The student researcher has reviewed the issue and patch during candidate screening. This exposure must be recorded; perfect blinding must not be claimed.
- Related issue-family and fork/lineage checks remain to be recorded before final case acceptance.

## 6. Current decision

Issue/patch alignment: strong candidate.  
Root source license: Apache-2.0.  
Dependency license inventory: pending workflow evidence and review.  
Exact base-fail/fix-pass reproduction: pending.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading and inference authorization: false.
