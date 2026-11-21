# QuTiP #2646 — E3/E2/E1 evidence-elimination matrix

**Date:** 21 November 2026  
**Candidate:** qutip/qutip issue #2646 / fix PR #2694  
**Dataset row:** qutip__qutip-2694  
**Status:** SOURCE- AND STAGE2-ARTIFACT-AUDITED ADVISORY MATRIX; PRIORITY SCOPE MISMATCH RECORDED; NOT PROJECT-LEAD APPROVED; CASE NOT ACCEPTED

## 1. Purpose and conclusion

This matrix applies the strengthened tier criterion: E2 must eliminate at least one predeclared plausible alternative while leaving at least two plausible mechanisms unresolved.

**E2 satisfies the minimum elimination criterion under a narrow, explicit interpretation.** The original dataset issue is framed through QobjEvo construction. The exact Stage 2 independent reproducer and frozen selector instead call the public coefficient factory directly with an existing Coefficient and a replacement args mapping. That direct API reproduces the stale value outside QobjEvo. This eliminates the alternative that the failure is confined to QobjEvo's own constructor. At E2, the remaining possibilities include the Coefficient builder/dispatch path dropping the args mapping, the builder failing to invoke the supported replacement operation, or the replacement operation itself failing for this Coefficient subtype. E1 source code distinguishes the actual mechanism.

**Important scope qualification:** the verified reproducer is narrower than the original issue's QobjEvo scenario. The current three-test expansion adds a direct replace_arguments positive control and a QobjEvo integration test, but that expanded file was committed after the verified Stage 2 run and has no confirmed CI result yet. It is not counted as Stage 2 evidence.

**Prompt-quality issue:** the issue body writes `args={"g:2"}`, which is a Python set containing one string, not the intended dictionary `{"g": 2}`. The report describes a dictionary update, but the code example is malformed relative to that description. Keep the prompt byte-for-byte as the dataset row; do not silently repair it. This is a material E3 suitability caveat for project-lead review.

## 2. Frozen provenance and Stage 2 integrity

- Issue: https://github.com/qutip/qutip/issues/2646
- Fix PR: https://github.com/qutip/qutip/pull/2694
- Exact buggy base: `b821b1aa8c98a00f58014e7ec02cc9cbef701ce4`
- Exact fixed PR head: `61df3c7bccf474aba393940581ffbbeccf5da366`
- Merge commit: `08f5fdee245271d2cf26a729c6555348b5350fde`
- Issue created: `2025-03-05T18:35:23Z`
- PR and dataset-row timestamp: `2025-05-15T15:48:33Z`
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset instance: `qutip__qutip-2694`
- Canonical dataset-row SHA-256: `16ed66f7a865915697f5fbed540a56e3017ccfe460f3d5bc94d5918a63e9c1ee`
- Frozen selector: `qutip/tests/core/test_coefficient.py::test_coefficient_update_args`
- Stage 2 reproducer snapshot actually run: `test_issue_2646.py` blob `e395c9ef6fc14e28c522ce25a77cd460ddb4b0a4` (one test: `test_rewrapping_a_coefficient_updates_its_arguments`).
- Exact-base `qutip/core/coefficient.py` blob: `3d5698de11c00e0525382046318051d98e77ce39`
- Exact-base `qutip/core/cy/coefficient.pyx` blob: `119a0fae00b22faef115033969aae4a3a2e705d9`
- Exact-base `qutip/core/cy/qobjevo.pyx` blob: `849050fc201cdd0b02ff55f0541d814c68aa0b15`
- Fixed `qutip/core/coefficient.py` blob: `14315d49c760389d028fd0023cc382c973a08684`

Stage 2 workflow run/job/artifact: `44500943717 / 135481445830 / 14518471928`.

Artifact integrity independently rechecked on 21 November 2026:
- Artifact SHA-256: `ecbc4ff3f3640f15603020331bffb177d4a1c51282b66358c11a3a6078c673cc` — recomputed local ZIP digest matches GitHub's artifact digest.
- ZIP CRC: PASS.
- Internal `SHA256SUMS.txt`: 14/14 entries PASS.
- Archive contains 15 files, including raw base/fixed logs, canonical dataset row, source/patch digests, dependency inventory, and upstream license/build metadata.

Exact Stage 2 results:
- Independent direct coefficient API reproducer: base fails with `AssertionError: 1 != 2`; fixed revision passes (1 test).
- Frozen selector: exact buggy base fails with `assert 1 == 2`; exact fixed revision passes (1 selector).
- The dataset selector and independent reproducer test the same direct coefficient-rewrapping behavior. They are two evidence routes for one case, not two independent experiments.

## 3. Exact E3 packet and prompt scope

E3 is the exact `problem_statement` stored in the authenticated Parquet row, not the later issue comments, PR description, PR diff, or repository source.

The issue body says that a `QobjEvo` constructed from a `qt.coefficient` does not respond as expected to the `args` argument. It provides an example with a Coefficient created using `g=1`, then constructs a QobjEvo with what is described as an updated `g=2` mapping. The code literal is `args={"g:2"}`; that expression is a set containing the string `g:2`, not a dictionary mapping `g` to `2`.

The reporter asks whether this is a bug or incorrect usage. The issue narrative does not identify whether the failure comes from QobjEvo argument handling, the coefficient factory, a Coefficient builder, or the replacement operation.

**Leakage boundary:** public issue comments contain a maintainer's explicit statement that ignoring `args` is a bug and a later comment that directly identifies the `coefficient()` factory as failing to update arguments, with a minimal direct re-wrapping example. These comments were reviewed by the researcher and are recorded as researcher source exposure. They are not part of the frozen dataset `problem_statement` and must not be silently added to the E3 model-visible packet. The benchmark packet remains the authenticated dataset field only.

## 4. Predeclared alternatives

| ID | Alternative / mechanism | Distinguishing prediction |
|---|---|---|
| G1 | When `coefficient()` receives an existing `Coefficient`, its registered builder `_return` returns the original object and discards the new `args` mapping. | Exact-base source shows `Coefficient` mapped to `_return`, the factory passes `args` into the builder kwargs, and `_return` ignores those kwargs. |
| A1 | The defect is confined to QobjEvo's constructor or its argument parsing; direct use of `coefficient(existing_coefficient, args=...)` should work. | A direct coefficient-factory call outside QobjEvo would pass if this were the only faulty path. |
| A2 | The coefficient factory dispatches the existing Coefficient to the wrong builder or fails to forward the provided `args` mapping. | Source would show missing/incorrect kwargs forwarding or an incorrect builder selection. |
| A3 | `FunctionCoefficient.replace_arguments` itself fails to create a replacement with new values. | A direct call to `original.replace_arguments({"a": 2})` would return a stale value on the exact buggy base. |

These are competing explanations, not claims of equal prior probability.

## 5. E3 → E2 → E1 elimination matrix

| Evidence / alternative | E3 — issue text only | E2 — direct coefficient factory reproducer and frozen selector | E2 disposition | E1 — exact-base source chain |
|---|---|---|---|---|
| G1: `_return` discards supplied args | Possible but not source-located. | Direct re-wrapping produces the stale value `1` instead of requested `2`. | Remains live. | `Coefficient` is registered to `_return`; `_return` returns `base` without consuming `kwargs`. Confirmed. |
| A1: QobjEvo constructor alone drops args | Live from the issue example. | **Eliminated as the sole explanation:** the same stale-value behavior occurs in `coefficient(original, args={"a": 2})` without constructing a QobjEvo. | Eliminated. | QobjEvo's `_read_element` passes its `args` into `coefficient(op[1], args=args, ...)`; the failure occurs downstream in the coefficient factory. |
| A2: coefficient factory dispatch or kwargs forwarding is broken | Live. | Remains plausible; E2 does not show which builder is selected or how kwargs are delivered internally. | Remains live. | Factory code selects `coefficient_builders[type_]` and calls it with `**kwargs`, where `args` is present. The selected `_return` silently ignores it. |
| A3: FunctionCoefficient.replace_arguments is defective | Live. | Remains plausible; the verified Stage 2 run did not execute the later-added positive-control test. | Remains live. | The exact-base `FunctionCoefficient.replace_arguments` merges replacement kwargs into a copied argument mapping and constructs a new FunctionCoefficient. The problem is that this method is never invoked by the buggy `_return`. |

Surviving mechanism set:
- E3: `{G1, A1, A2, A3}`.
- E2: `{G1, A2, A3}`.
- E1: `{G1}`.

E2 eliminates A1 while retaining at least two plausible mechanisms, A2 and A3. Thus the minimum strengthened alternative-elimination criterion is met using only the historical, verified Stage 2 test.

## 6. E1 exact-base source chain

### QobjEvo argument handoff

Pinned source: https://github.com/qutip/qutip/blob/b821b1aa8c98a00f58014e7ec02cc9cbef701ce4/qutip/core/cy/qobjevo.pyx

- `QobjEvo.__init__`, lines 189–227, normalizes the incoming `args` through `_read_args`, then passes that mapping to each `_read_element` call.
- `_read_element`, lines 263–274, handles a `[Qobj, coefficient]` item by calling `coefficient(op[1], tlist=tlist, args=args, order=order, ...)`.

Therefore the QobjEvo path does pass its updated args mapping to the coefficient factory.

### Coefficient factory and builder selection

Pinned source: https://github.com/qutip/qutip/blob/b821b1aa8c98a00f58014e7ec02cc9cbef701ce4/qutip/core/coefficient.py

- Lines 43–44: buggy `_return(base, **kwargs)` immediately returns `base`.
- Lines 51–57: `coefficient_builders` maps `Coefficient` to `_return`.
- Lines 60 onward define the public `coefficient()` factory.
- Lines 176–186 prepare a kwargs mapping containing `args`, `args_ctypes`, `tlist`, `order`, and other construction options.
- Lines 188–190 iterate over registered builders, select the one matching `isinstance(base, type_)`, and call that builder with `**kwargs`.

For an existing `Coefficient`, the matching `_return` therefore receives `args` but ignores it. The same factory path explains the direct Stage 2 reproducer and the issue's QobjEvo failure.

### Replacement method distinguishes A3

Pinned source: https://github.com/qutip/qutip/blob/b821b1aa8c98a00f58014e7ec02cc9cbef701ce4/qutip/core/cy/coefficient.pyx

- Base `Coefficient.replace_arguments`, lines 89–107, returns `self` by default for coefficient types without argument support.
- `FunctionCoefficient.replace_arguments`, lines 231–260, merges the supplied replacement mapping into a new args dictionary and returns a new FunctionCoefficient with the updated mapping.

Thus A3 is not the cause for the FunctionCoefficient used in the reproducer. The defective `_return` fails to call the working replacement operation.

### Fixed-source validation only

The fixed PR changes `_return` to accept `args=None` and call `base.replace_arguments(args)` when supplied. Fixed source is hidden technical-gold evidence only; do not include it or the patch in model-visible E1 packets.

## 7. Expanded follow-up tests — not yet counted as verified

After the verified Stage 2 run, the reproducer was expanded to include three tests:

1. A positive control calling `original.replace_arguments({"a": 2})`, verifying the original remains `1` and the returned coefficient evaluates to `2`.
2. The direct `coefficient(original, args={"a": 2})` re-wrapping reproducer, asserting the original stays `1` and the new object evaluates to `2`.
3. A QobjEvo integration test comparing the original evolution (coefficient `t+1`) with an evolution built from the same coefficient but passed `args={"g": 2}` (expected coefficient `t+2`).

Expanded file blob: `63b63ee0bb40eb40410764ef1d647e6fbf3637cd` at commit `6ba3b84b7b8358519cff09827e7e3e4079809165`.

The main preflight workflow originally ran its QuTiP job only on `workflow_dispatch`; a scoped push condition was added at commit `18c5d82f1b7e7e5acd36514623b011bb381a14f1` to permit a targeted run when this reproducer or the workflow changes. No successful CI result for the expanded three-test suite has been verified in this review. Do not count those additional tests as passed.

## 8. E3 issue-quality and sample-suitability risk

The issue's code snippet contains `args={"g:2"}`. This is not the dictionary described in the prose; it is a set containing a string. The issue body therefore does not provide a clean, directly executable QobjEvo reproduction as published. The issue still describes a plausible observed behavior, and the authenticated dataset's frozen selector plus independent direct coefficient reproducer make the underlying coefficient-argument defect reproducible. However, the connection between the exact original prompt and the narrower verified selector must remain visible.

E3 ABSTAIN is a reasonable advisory proposal because the issue body does not reveal the coefficient builder or replacement path, and the sample contains an incorrect argument literal. However, the malformed snippet may make the task partly an API/syntax clarification rather than pure root-cause diagnosis. Project-lead review is required before this candidate enters the primary abstention sample.

## 9. Independence, exposure and temporal limits

- One issue (#2646), one fix PR (#2694), one dataset row, one selector and one upstream project. The candidate contributes at most one case.
- The direct reproducer and frozen selector exercise the same narrow coefficient-rewrapping behavior; they are not independent cases.
- Issue comments include a maintainer's minimal coefficient re-wrapping example and explicit diagnosis. Researcher exposure to issue comments, PR diff, exact source and Stage 2 artifacts is now full. No blind adjudication or inter-rater reliability claim is made.
- Project-lead prior pipeline/debug exposure declaration remains pending; it must be answered separately and cannot be inferred from declarations for other candidates.
- Issue #2646 was created on 5 March 2025 and PR #2694 on 15 May 2025. Both postdate Qwen2.5's public announcement on 19 September 2024 and the pinned model repository revision in September 2024. Issue/PR-specific text contamination is therefore less likely for the pinned checkpoint; pre-existing QuTiP source-code exposure remains unresolved.
- Root upstream license: BSD-3-Clause. The dataset row is also labeled BSD-3-Clause. The Stage 2 dependency inventory records Cython Apache-2.0; NumPy and SciPy BSD-family licenses; pytest/iniconfig/pluggy MIT; Pygments BSD-2-Clause; metadata gaps for packaging, setuptools and wheel beyond classifiers. NumPy's binary distribution includes OpenBLAS, LAPACK, GCC runtime components and other bundled notices. PyArrow 19.0.1 was used for dataset extraction with Apache Software License metadata.
- Dependency/package metadata and the root LICENSE are not a legal determination. Canonical package license texts, NumPy bundled/native notices, and exact dataset-card attribution remain open for human review.

## 10. Proposed tier and acceptance boundaries

- E3: ABSTAIN — advisory proposal; issue body alone does not show the source mechanism, but its malformed args literal creates a sample-quality caveat.
- E2: ABSTAIN — advisory proposal; direct coefficient re-wrapping reproducer eliminates a QobjEvo-only explanation while leaving builder-dispatch and replacement-method alternatives open.
- E1: ANSWER — advisory proposal; exact-base source proves `_return` silently discards args despite the factory forwarding them and FunctionCoefficient supporting replacement.
- Project-lead G1 and E3/E2/E1 approval: pending.
- Project-lead E3 sample-suitability decision on the malformed snippet / prompt-to-selector scope gap: pending.
- Project-lead prior pipeline/debug exposure declaration: pending.
- Project-lead temporal acknowledgement: pending.
- Human dependency/license/notice and bounded research-scope review: pending.
- Schema-conformant proposed case record and fail-closed validation: pending.
- Final case acceptance: **not accepted**; registry inclusion: **false**.
- Model loading, inference, fine-tuning and training: **not performed and not authorized**.