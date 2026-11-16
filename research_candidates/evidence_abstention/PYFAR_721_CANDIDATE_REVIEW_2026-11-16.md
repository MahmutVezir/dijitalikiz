# pyfar/pyfar #721 — candidate review

**Cohort rank:** 90 of 96 primary candidates  
**Dataset instance:** pyfar__pyfar-722  
**Issue:** https://github.com/pyfar/pyfar/issues/721  
**Fix PR:** https://github.com/pyfar/pyfar/pull/722  
**Review status:** strong numerical bug candidate; exact dataset reproduction pending. Not an accepted case.

## 1. Defect contract

Issue #721 reports that energy normalization does not achieve its requested target. The issue provides a numerical counterexample: an input with energy 20 normalized to target energy 1 yields energy 0.05 instead of 1.

PR #722 corrects the scaling for energy and power normalization by applying the square-root relationship between amplitude and energy/power. It adds parameterized checks over multiple target values and channel-handling modes for energy, power, and RMS.

The issue has a quantitative, independently checkable expected result. A correct numerical guess is not the criterion; the test must show that the output's measured energy/power equals the requested target within the specified tolerance.

## 2. Pinned source identity

- Repository: pyfar/pyfar
- Buggy base: 648dda4c60c5a6f74acf335f7808c590c9d23929
- Fixed commit: a4d72d380bb8ddb0950d334eb1b0793ee6d86e0e
- Issue #721 created: 2024-11-11
- PR #722 created: 2024-11-15
- Exact-base setup.py declares MIT license and MIT license classifier.
- Exact-base runtime dependencies: numpy, scipy, matplotlib, sofar, urllib3, deepdiff, soundfile.

## 3. Test and dependency scope

- The regression test uses generated in-memory signals; no external audio fixture or remote service is required.
- pyfar's top-level package imports its DSP, plotting, sampling, and I/O modules, so the test environment includes the project's declared runtime dependencies rather than only numpy/scipy.
- The pinned environment also includes the required transitive dependencies for matplotlib, soundfile, h5py, deepdiff, and pytest.
- The workflow records distribution license metadata before importing pyfar source and stops if any package lacks both a license field and a license classifier.
- The exact dataset FAIL_TO_PASS selectors are extracted from the pinned Parquet row.
- This is a narrow documentary screen, not legal advice or blanket clearance for optional extras or redistribution.

## 4. Test adequacy

The workflow applies the exact PR diff to the exact buggy base, runs the dataset FAIL_TO_PASS selectors, then runs the same selectors on the exact fixed revision.

Required result: the base fails the energy/power target assertion, and the fixed revision passes. Collection errors, dependency failures, or unrelated failures do not count as reproduction.

## 5. Independence and exposure

- The cohort contains one primary candidate for pyfar; this project can contribute at most one accepted case.
- The issue and PR were created after the September 2024 public release of Qwen2.5-3B-Instruct. This reduces the likelihood that this exact issue/patch was in the released weights but does not establish complete training-data provenance.
- The student researcher has reviewed the issue and patch during candidate screening. This exposure must be recorded; perfect blinding must not be claimed.
- Related issue-family and fork/lineage checks remain part of final acceptance.

## 6. Current decision

Issue/patch alignment: strong numerical contract.  
Root source license: MIT.  
Dependency license inventory: pending workflow evidence and review.  
Exact base-fail/fix-pass reproduction: pending.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading and inference authorization: false.
