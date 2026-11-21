# music21 #1736 / issue #1735 — static scope and E3 sample-suitability review

**Date:** 21 November 2026  
**Candidate:** cuthbertLab/music21 issue #1735 / fix PR #1736  
**Cohort rank:** 51 of 96  
**Disposition:** **STRONG TECHNICAL ISSUE/PR ALIGNMENT; ISSUE TEXT ALREADY DISCLOSES THE TYPE-LOSS ROOT CAUSE; POSSIBLE MIXED PATCH SCOPE; HOLD BEFORE STAGE 2**

## 1. Frozen upstream identity

- Issue: https://github.com/cuthbertLab/music21/issues/1735
- Fix PR: https://github.com/cuthbertLab/music21/pull/1736
- Issue created: `2024-10-27T13:43:42Z`.
- PR created: `2024-10-28T03:20:50Z`.
- Exact PR base: `e05fc53dfef7b2c9ac974c0cacb8b85e9c4d4605`.
- Exact PR head: `80eda7cd2b043c5ee3f48fd0630b2811af313da7`.
- Merge commit: `91e3521173251e3f56706423067d722e5e3e52ad`.
- PR changed 6 files: `.pylintrc`, `music21/base.py`, `music21/figuredBass/resolution.py`, `music21/stream/base.py`, `music21/stream/tests.py`, and `music21/test/testLint.py`.

The PR description is brief: “Fixes #1735” and “Adds tests.”

## 2. Issue-level symptom and source/patch alignment

Issue #1735 reports that this call fails:

```python
from music21 import stream, note
stream.Measure([note.Note(quarterLength=8)]).splitByQuarterLengths([4, 4])
```

Observed exception:

```text
AttributeError: 'tuple' object has no attribute 'spannerList'
```

The issue body itself says that the `st` variable inside `splitAtQuarterLength` is a `_SplitTuple`, but when returned to `splitByQuarterLengths` it becomes an ordinary tuple. This is a direct statement of the type-preservation failure, not merely a symptom description.

The PR's main causal change is in `music21/stream/base.py`: the Stream override of `splitAtQuarterLength` now returns `base._SplitTuple([sLeft, sRight])` in both the early-return and normal-return paths, rather than returning a plain two-item tuple. It also adds the corresponding return annotation.

The related `music21/base.py` implementation uses the `_SplitTuple` contract and reads `st.spannerList` while aggregating spanners across splits. The PR adds a regression test in `music21/stream/tests.py` that exercises `Measure.splitByQuarterLengths`, verifies the returned object is `_SplitTuple`, and checks the partitioned measures and note durations.

At this level, issue symptom, likely root cause, and principal fix align strongly.

## 3. E3 answerability risk

The issue body discloses all of the key causal elements:
- the failing public call and arguments;
- the exact exception and missing attribute;
- the internal type name `_SplitTuple`;
- the fact that the object is a specialized tuple before return;
- the loss of the specialized type on the path back to `splitByQuarterLengths`.

A model reading that issue text can already infer that the Stream override must preserve the specialized tuple subtype on its return path. The likely repair direction is therefore highly exposed at issue-text level.

**Advisory sample decision:** this candidate is not a defensible primary E3 abstention case unless the exact frozen dataset `problem_statement` is materially less diagnostic than the upstream issue body, or the preregistered scoring rubric demands a different, genuinely unresolved causal distinction. Until the frozen row is authenticated, treat E3 suitability as a strong risk rather than a final semantic tier decision.

## 4. Patch-scope / gold-patch caveat

The PR also changes `music21/figuredBass/resolution.py` by adding truthiness checks to pitch-comparison lambdas, and updates lint configuration and documentation. Those changes do not obviously follow from the Stream `_SplitTuple` issue as written.

The patch additionally changes `_SplitTuple.__eq__` and `__hash__` semantics so that associated spanner lists affect equality/hash behavior. That may be a consequence of treating this object as a meaningful tuple subtype, but its exact necessity for the reported `spannerList` AttributeError should be separately established.

These observations do not invalidate the main fix. They do mean that the PR patch should not be treated as one perfectly scoped change without checking the frozen dataset row, FAIL_TO_PASS selectors, and the role of each changed file. No claim is made that the unrelated-looking changes are independently defective.

## 5. Temporal and researcher-exposure boundary

- The issue was filed on 27 October 2024, after the public Qwen2.5 announcement on 19 September 2024 and the initial public upload of the pinned Qwen2.5-3B-Instruct checkpoint. This reduces the likelihood that the exact issue/PR text was in the released checkpoint's pre-release training data; it does not establish the exact training-data cutoff.
- Researcher exposure is now full for the issue, PR description/diff, exact base/fixed revisions and tests inspected in this static review.
- Project-lead prior pipeline/debug exposure declaration remains pending.
- No blind adjudication or inter-rater reliability claim is made.

## 6. Stage 2 / acceptance boundary

- Exact frozen SWE-rebench row and its `problem_statement` have **not** yet been authenticated.
- Frozen `FAIL_TO_PASS` and `PASS_TO_PASS` selectors have **not** been run on the exact base and fixed revisions.
- No independent reproducer, Stage 2 environment, artifact, digest or CRC result is claimed.
- Final case acceptance: **not accepted**; registry inclusion: **false**; inference authorization: **false**.
- No model has been loaded; no inference, fine-tuning or training has been performed.

## 7. Next decision gate

1. Authenticate the exact frozen row for `music21__music21-1736`, including the full problem statement, all frozen selectors, base commit and timestamp.
2. Compare the complete frozen test patch/selector scope with the issue-specific Stream regression. In particular, account for `figuredBass/resolution.py` changes rather than silently treating them as part of the Stream defect.
3. The project lead decides whether this should be excluded from the primary abstention sample due to high E3 answerability, or whether an independently justified and separately preregistered control use is appropriate.
4. Do not start primary-sample Stage 2 until the sample-suitability and scope gate has been decided. A technical reproduction pass alone would not settle E3 eligibility or final case acceptance.


## 8. Project-lead conditional exclusion amendment — 21 November 2026

**CONDITIONAL EXCLUSION APPROVED, pending exact frozen-row authentication.** The project lead approved excluding music21 #1736 from the current primary abstention sample if the exact frozen SWE-rebench row confirms that E3 includes the same explanation already visible in upstream issue #1735: `_SplitTuple` becomes an ordinary tuple on return to `splitByQuarterLengths`, leading to the `spannerList` AttributeError.

The exact frozen row, problem statement, base commit and selectors have not yet been independently authenticated and hashed. Therefore this record is a conditional project-lead decision, not a completed primary-sample exclusion. If the frozen packet confirms the same disclosure, formalize exclusion and do not run Stage 2. If it materially differs, return to project-lead E3 adjudication before any Stage 2 run. Do not assign this candidate to a control group. No case acceptance or inference is authorized.

The project lead has not supplied a prior pipeline/debug exposure declaration for this candidate.

Decision record: `PROJECT_LEAD_RANK49_52_STAGE2_STAGE3_DECISIONS_2026-11-21.md`.


## 9. Exact frozen-row authentication and conditional-exclusion resolution — 21 November 2026

The exact pinned dataset row is now authenticated by the no-inference workflow run 44924570231, job 136907864713, artifact 14715535728.

- Dataset: PrimeIntellect/SWE-rebench-V2-Filtered-Verified, revision fb9aa226b2ce37c708ea7732e7b980abacdadb67.
- Whole Parquet SHA-256: 7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9; 226,272,977 bytes; 6,272 rows.
- Exact discovered row ID: cuthbertlab__music21-1736; repository cuthbertLab/music21; base e05fc53dfef7b2c9ac974c0cacb8b85e9c4d4605.
- Dataset created_at: 2024-10-28 03:20:50; dataset license metadata: BSD-3-Clause.
- Canonical row SHA-256: 7bdd5e62281c92e750afb6e34066a28ff429b2bc45e9cc31a0ada13307522db3.
- Frozen problem_statement SHA-256: 06eac6d4bb2e84cb1ecbdb67507954a2e8eb5b531bb19d4a82005ba70f471432.
- Frozen FAIL_TO_PASS count: 1; selector: music21/stream/tests.py::Test::testSplitByQuarterLengths.

The authenticated E3 packet contains the same explicit causal disclosure as upstream issue #1735: the st value is a _SplitTuple inside splitAtQuarterLength, but is an ordinary tuple when returned to splitByQuarterLengths, causing spannerList access to raise AttributeError. The project-lead-approved condition is therefore **satisfied**.

**Final primary-sample disposition: EXCLUDED.** Do not run Stage 2 for this row. Do not assign it to a control group. This does not imply that the upstream patch is technically ineffective.

Patch-scope confirmation from the authenticated frozen row:
- The target stream correction is in music21/stream/base.py, with supporting music21/base.py tuple semantics and a single frozen regression selector.
- The full PR patch also includes separate truthiness changes in music21/figuredBass/resolution.py, in addition to lint/config/documentation changes. Preserve this mixed-scope caveat; do not fold the figured-bass behavior into the issue-specific gold.
- Frozen test patch SHA-256: 847ea373fba70f0e07cebb7b8a9ae8b9d9b163a961d07a7441a579d0f1d65b99.
- Full PR patch SHA-256: 180edff926152a2a62781ad458de19d7f04b389760e2c0563808f3bf2a97976f.

Artifact integrity:
- Artifact URL: https://github.com/MahmutVezir/dijitalikiz/actions/runs/44924570231/artifacts/14715535728
- GitHub artifact SHA-256: 1abca7d09dfcbf4c4ba773ab87fb21225ec8f4208f44f2f7fbb19b613352459b.
- Independently downloaded ZIP SHA-256: identical; ZIP CRC passed; all 6 internal SHA256SUMS entries passed.
- The workflow used only the pinned Parquet metadata/row extraction; no upstream source checkout, package installation, upstream test/build, model loading, inference, fine-tuning or training.

The project-lead prior pipeline/debug exposure declaration for music21 remains undeclared; this does not change the E3-based primary-sample exclusion.
