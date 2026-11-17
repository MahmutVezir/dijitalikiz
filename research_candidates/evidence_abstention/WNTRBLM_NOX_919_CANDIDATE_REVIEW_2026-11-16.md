# wntrblm/nox #919 — candidate review

**Cohort rank:** 6 of 96 primary candidates  
**Dataset instance:** wntrblm__nox-922  
**Issue:** https://github.com/wntrblm/nox/issues/919  
**Fix PR:** https://github.com/wntrblm/nox/pull/922  
**Review status:** issue/patch and root-license screen passed; two missing wheel-license metadata records now have exact upstream-source resolutions; the candidate-specific job has not started on the latest CI attempt (runner allocation failure, no steps/logs). Exact reproduction remains pending. Not an accepted case.

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
- Before any upstream test is executed, the workflow records distribution license metadata for every installed package and stops if a package has no license field or license classifier.
- `dependency-groups==1.3.0` has an exact-source MIT resolution: source commit `1c99d4a6e50504354ef501e5f8543a22830c788d`, LICENSE blob `b9723b85ed7adb32f8c2b4ee880c06ec3061da50`, and pyproject blob `db86f496d8dc41647df91b76d0b1319b9aa94974`.
- `attrs==24.3.0` has an exact-tag MIT resolution: source commit `598494a618410490cfbe0c896b7a544f6d23e0d9`, LICENSE blob `2bd6453d255e19b973f19b128596a8b6dd65b2c3`, and pyproject blob `0b598099fdd945dcb75f3145909a9b4a85a93972`. The pinned PyPI release metadata does not provide a usable license field/classifier, so the workflow now permits this exact source-verified fallback only for version 24.3.0.
- These two source records close the documentary ambiguity for those exact packages; they do **not** mean the complete installed package inventory or dependency licensing gate has passed. CI evidence and installed metadata for all remaining packages still require review.
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

## 6. Latest CI execution status

- Research branch commit containing the controlled `attrs==24.3.0` resolution: `801332f8a8a0e9a90695e9ba03c20dc07ebb9870`.
- Evidence Abstention Preflight run: `43896853159`, attempt 1 and targeted rerun attempt 2.
- Nox job attempt 1: `133402627435`; attempt 2: `133404336674`.
- Both Nox job records completed in approximately two seconds with `runner_id=0` and an empty `steps` array. The other candidate jobs in the same run also failed immediately without runner allocation or steps. The job-log endpoint returned `BlobNotFound`, and the run produced no artifacts.
- Therefore the attempt did not reach the dependency metadata step, dataset extraction, Nox source import, or either test suite. This is not evidence that the Nox source or reproducer failed. The exact CI failure cause remains unavailable from the current GitHub run data.

## 7. Current decision

Issue/patch alignment: strong candidate.  
Root source license: Apache-2.0.  
Exact-source license records: dependency-groups 1.3.0 and attrs 24.3.0 documented; remaining installed metadata inventory not verified.  
Dataset row and selectors: not yet authenticated in a completed workflow.  
Exact base-fail/fix-pass reproduction: not run; CI job did not start.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading and inference authorization: false.


## 8. 17 Kasım 2026 metodolojik düzeltme ve yeniden üretim durumu

The previous status sentence above saying that the candidate job had not started is historical and is superseded by this dated addendum.

- Actions run 44097375066 did execute the Nox job. The independent issue reproducer ran on the pinned buggy base before the dataset patch and produced the expected failure signature: `AssertionError: True is not false`. This is retained as independent-reproducer evidence only.
- The dataset selector portion of that run is **not admissible** for the base-fail/fixed-pass gate. The earlier workflow used shell word splitting for parameterized pytest node IDs and applied a full PR diff containing production changes to the buggy base before dataset testing. The old dataset result is therefore not used to reject or accept this candidate.
- The exact selector `tests/test__option_set.py::TestOptionSet::test_validation_options` was checked against the pinned buggy commit `97e0fad6a4036d610591a52e9ad0cfbe74a31af3` and fixed commit `5c4000550325fd1ad036716d9e600ef7411bed3d`. In both versions, `TestOptionSet` exists but has no `test_validation_options` method. The methods present in the inspected source include `test_namespace`, `test_namespace_values`, and `test_namespace_non_existent_options_with_values`. This is a dataset-row/selector-to-source mismatch, not an upstream bug failure. It will not be silently removed from the dataset record.
- The PR's exact source change is in `nox/virtualenv.py` and `tests/test_virtualenv.py`; the PR does not change `tests/test__option_set.py`. The mismatch therefore requires a documented row-level oracle disposition before acceptance.
- A shared selector runner now preserves each node ID as one argv element, validates that base-side failures are executed test failures rather than collection errors, and validates fixed-side passes. Its unit tests passed in the no-inference preflight of run [44103128787](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44103128787).
- In run 44103128787, the Nox candidate job was queued after no-inference preflight passed; no new Nox candidate test log/result was yet available when this addendum was written.

**Current decision:** retain Nox provisionally. Independent issue reproducer: positive buggy-base failure observed. Dataset FAIL_TO_PASS contract: unresolved due at least one exact selector that does not exist in either pinned source revision. Candidate acceptance remains **not accepted**; no selector is dropped or altered without an explicit provenance/oracle record.
