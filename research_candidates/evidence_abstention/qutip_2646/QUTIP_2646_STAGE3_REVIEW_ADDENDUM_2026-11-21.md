# QuTiP #2646 — Stage 3 review addendum

**Date:** 21 November 2026  
**Candidate:** qutip/qutip issue #2646 / fix PR #2694  
**Dataset instance:** qutip__qutip-2694  
**Disposition:** Stage 2 technical evidence and archive integrity passed for the historical one-test reproducer; source-aware E3/E2/E1 matrix, issue-family/exposure record and temporal chronology review prepared; project-lead decisions and final acceptance pending.

## 1. Stage 2 technical and artifact status

- Buggy base: `b821b1aa8c98a00f58014e7ec02cc9cbef701ce4`.
- Fixed PR head: `61df3c7bccf474aba393940581ffbbeccf5da366`.
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`.
- Canonical row: `qutip__qutip-2694`.
- Canonical dataset-row SHA-256: `16ed66f7a865915697f5fbed540a56e3017ccfe460f3d5bc94d5918a63e9c1ee`.
- Frozen selector: `qutip/tests/core/test_coefficient.py::test_coefficient_update_args`.
- Workflow run/job/artifact: `44500943717 / 135481445830 / 14518471928`.
- Artifact SHA-256: `ecbc4ff3f3640f15603020331bffb177d4a1c51282b66358c11a3a6078c673cc`.
- Artifact independently downloaded and checked: recomputed outer SHA-256 matches GitHub; ZIP CRC PASS; internal SHA256SUMS 14/14 PASS.

The exact historical Stage 2 reproducer snapshot contained one test: `coefficient(original, args={"a": 2})` must evaluate to 2. It failed on the exact buggy base with `AssertionError: 1 != 2`, and the identical reproducer passed on the exact fixed revision (1 test). The frozen selector showed the same 1-versus-2 failure on base and passed on fixed.

**Scope caveat:** that historical independent reproducer does not construct QobjEvo. It tests the direct public coefficient factory route underlying the issue. The full issue example as published also contains `args={"g:2"}`, a set literal rather than the intended dictionary. The discrepancy is documented in the candidate review and E3/E2/E1 matrix.

## 2. Expanded follow-up reproducer — not yet verified

The reproducer was later expanded to three tests:
- positive control for direct `original.replace_arguments({"a": 2})`;
- direct `coefficient(original, args={"a": 2})` re-wrapping behavior;
- QobjEvo integration, comparing the original and updated embedded coefficient arguments.

Expanded file blob: `63b63ee0bb40eb40410764ef1d647e6fbf3637cd` at commit `6ba3b84b7b8358519cff09827e7e3e4079809165`.

The main preflight workflow's QuTiP job was previously restricted to workflow_dispatch. A narrow push condition for the QuTiP reproducer/workflow path was added at commit `18c5d82f1b7e7e5acd36514623b011bb381a14f1`. No CI artifact or successful workflow result for the expanded three-test suite has been verified as part of this addendum. Do not claim the positive control or QobjEvo integration test has passed on base/fixed until a matching run and logs are inspected.

## 3. Source-aware Stage 3 result

- Proposed gold G1: the `Coefficient` builder `_return` returns the original object and discards a supplied `args` mapping.
- Evidence matrix: `QUTIP_2646_E3_E2_E1_EVIDENCE_ELIMINATION_MATRIX_V0_1_2026-11-21.md`.
- Gold/tier proposal: `QUTIP_2646_SOURCE_AWARE_GOLD_AND_EVIDENCE_TIERS_PROPOSAL_V0_1_2026-11-21.md`.
- E2 direct coefficient-factory reproduction eliminates a QobjEvo-only explanation and retains builder dispatch/kwargs handling and replacement implementation alternatives.
- E1 source confirms QobjEvo passes `args` to `coefficient()`, the factory forwards `args` in builder kwargs, `Coefficient` is mapped to `_return`, and the buggy `_return` returns `base` without using kwargs. FunctionCoefficient has a working `replace_arguments` override. The exact source path selects G1.

## 4. E3 prompt and issue-comment exposure

The authenticated dataset problem_statement is the model-visible E3 packet. It has a malformed `args={"g:2"}` expression, which is a set rather than a dictionary. Preserve the exact prompt and ask the project lead whether this is a sufficient scope/quality caveat for the primary sample.

Public issue comments later state that ignoring args is a bug and identify `coefficient()` as the function that fails to update arguments. These comments are not included in the dataset problem_statement and must not be added to E3. The researcher reviewed them, so researcher source exposure is full.

## 5. Temporal exposure

Separate record: `QUTIP_2646_TEMPORAL_EXPOSURE_REVIEW_2026-11-21.md`.

Qwen2.5 was publicly announced on 19 September 2024. QuTiP issue #2646 was filed on 5 March 2025 and PR #2694 on 15 May 2025. This lowers the likelihood of issue/PR-specific exposure in the pinned checkpoint but does not establish the full training-data cutoff or absence of earlier QuTiP source code.

## 6. Independence, licenses and remaining gates

- One issue, one fix PR, one frozen selector and one upstream project. The independent reproducer and selector are not separate cases.
- Targeted issue-family search found no exact second candidate; repository-wide issue-family review is not exhaustive.
- Project-lead prior pipeline/debug exposure declaration: pending.
- Project-lead G1 and E3/E2/E1 decision: pending.
- Project-lead review of malformed issue example and the QobjEvo-to-direct-coefficient scope discrepancy: pending.
- Project-lead temporal-exposure acknowledgement: pending.
- Root upstream license is BSD-3-Clause. The pinned environment inventory includes Cython (Apache-2.0), NumPy and SciPy (BSD-family), packaging (Apache/BSD classifiers but empty license text field), setuptools/wheel (MIT classifiers but empty license text fields), pytest/iniconfig/pluggy (MIT), Pygments (BSD-2-Clause), and PyArrow 19.0.1 for dataset extraction (Apache Software License). NumPy's binary distribution includes bundled OpenBLAS, LAPACK and GCC runtime components with additional license notices. Canonical license/notice review is still required.
- Exact dataset-card provenance, dependency/native notices, bounded documentary scope acknowledgement: pending.
- Schema-conformant case record and fail-closed validator: pending.
- Separate final project-lead YES/NO case acceptance: pending.
- Final acceptance: not accepted; registry inclusion false.
- Model loading, inference, fine-tuning and training: not performed and not authorized.