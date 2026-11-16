# python-control issue #1144 — candidate review

**Cohort rank:** 35 of 96 primary candidates  
**Dataset instance:** python-control__python-control-1145 (exact row identity to be authenticated by the workflow)  
**Issue:** https://github.com/python-control/python-control/issues/1144  
**Fix PR:** https://github.com/python-control/python-control/pull/1145  
**Review status:** issue/patch and minimal environment screen passed; exact dataset selectors and source reproductions pending. Not an accepted case.

## 1. Defect contract

Issue #1144 demonstrates that nyquist_plot ignores the caller-supplied Matplotlib Axes and plots on the current/global axes instead. The reproduction creates a 2x2 figure and passes axes[1, 0], but the plot appears in the bottom-right subplot.

PR #1145 fixes the relevant plotting paths by using the explicitly supplied Axes object rather than pyplot's global state. It also addresses related axes-routing defects in Nichols and describing-function plots. The independent reproducer isolates the reported Nyquist behavior: set the current axes to axes[1, 1], pass axes[1, 0] to nyquist_plot, and require plotted lines only on axes[1, 0].

The PR changes five files and several related plotting routines. The dataset FAIL_TO_PASS selectors must be checked to confirm that each selector is within the explicit-axes defect family and not an unrelated behavior change.

## 2. Pinned source identity

- Repository: python-control/python-control
- Buggy base: dc7d71bd1a2d143f10fa8fe91d31292bdf8f5113
- Fixed PR head: 21f4912c8b12216534b8d5b07c243c66675a8b83
- Merge commit: 632391cae6d126ed5c632a01fe65be96dc28a344
- Issue #1144 created: 2025-04-16T16:21:23Z
- PR #1145 created: 2025-04-17T03:16:40Z
- Exact-base root LICENSE Git blob: fbfc42c670132862f4d6998add25451214023574
- Exact-base pyproject.toml Git blob: db70b8f48d989ce415255fb039aedaebd77fcc94
- Exact-base license declaration: BSD-3-Clause.
- Core runtime dependencies declared upstream: NumPy >=1.23, SciPy >=1.8, Matplotlib >=3.6.

## 3. Reproduction and dependency scope

The independent reproducer imports the exact source package and exercises nyquist_plot with an explicit Axes argument. The pinned environment includes the core NumPy/SciPy/Matplotlib runtime and pytest. It does not install optional slycot or cvxopt extras, use network services, or require external data fixtures.

The workflow records installed distribution license metadata before source tests. This is a narrow screen for the pinned core plotting environment, not blanket clearance for optional extras or redistribution.

## 4. Dataset selector requirement

The workflow authenticates the exact Parquet row python-control__python-control-1145, records its canonical row hash and FAIL_TO_PASS selectors, applies the exact PR diff to the buggy base, and runs every selector on both base and fixed revisions. Every base failure must be an explicit-axes assertion failure; every fixed selector must pass. Import/setup errors are not accepted as reproduction evidence.

## 5. Independence and exposure

- The frozen primary cohort contains one python-control/python-control candidate; this repository can contribute at most one accepted case.
- Issue and PR were created in April 2025, after the September 2024 public release of the pinned Qwen2.5-3B-Instruct family. This temporal ordering lowers the likelihood that the exact public issue/patch was present in the released weights, but does not prove the model's full training-data cutoff.
- The student researcher has reviewed the issue and PR during candidate screening; perfect blinding must not be claimed.
- Related issue-family and repository-lineage review remains required.

## 6. Current decision

Issue/patch alignment: strong.  
Independent Nyquist axes reproducer: prepared; workflow pending.  
Dataset FAIL_TO_PASS selectors: pending exact-row authentication and execution.  
Minimal dependency/license inventory: pending workflow evidence and human review.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading/inference authorization: false.
