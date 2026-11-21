# Gammapy #5525 / issue #5524 — static scope and E3 sample-suitability review

**Date:** 21 November 2026  
**Candidate:** gammapy/gammapy issue #5524 / fix PR #5525  
**Cohort rank:** 54 of 96  
**Disposition:** **DIRECT NORMALIZATION DEFECT; ISSUE TITLE AND BODY ALREADY NAME MISSING NORMALIZATION; PR ALSO CONTAINS A SECOND INTEGRAL CORRECTION; HOLD OUT OF PRIMARY E3 SAMPLE PENDING PROJECT-LEAD DECISION; NO STAGE 2**

## 1. Frozen upstream identity

- Issue: https://github.com/gammapy/gammapy/issues/5524
- Fix PR: https://github.com/gammapy/gammapy/pull/5525
- Issue created: `2024-10-22T17:26:14Z`.
- PR created: `2024-10-24T14:11:19Z`.
- Exact PR base: `cff9ae2c54c38cc664967ff1cd2ef41457c2c6b8`.
- Exact PR head: `4b0318881c2b4a0d026033840792c6a76404c183`.
- Merge date: `2024-10-29T12:03:46Z`.
- Changed files: `gammapy/modeling/models/temporal.py`, `gammapy/modeling/models/tests/test_temporal.py`.

## 2. Issue-to-patch technical alignment

Issue #5524 says that `TemplatePhaseCurveTemporalModel` does not normalize its phase-curve template at initialization. It explains that the per-phase-bin `NORM` values can differ considerably from 1 and that simulated flux is consequently estimated incorrectly.

At the exact buggy base, `TemplatePhaseCurveTemporalModel.__init__` stores the supplied table unchanged (`self.table = table`). The class later constructs an interpolator from the `PHASE` and `NORM` columns; there is no normalization step during initialization.

At the exact PR head, initialization stores `self._normalise_table(table)`. That helper:
1. builds a linear `InterpolatedUnivariateSpline` over `PHASE` and `NORM`;
2. computes the interpolator's integral over phase interval [0, 1];
3. multiplies the table's `NORM` column by the reciprocal of that integral.

Tests are changed to expect the normalized shape and phase-average values. This is directly aligned with the issue's stated normalization defect.

## 3. E3 answerability risk

The issue title says the template “does not normalise the phasecurve template.” The issue body repeats that diagnosis, locates the behavior at initialization, names the `NORM` per-phase-bin values, and explains the consequence for flux estimation.

Therefore, the central defect is already stated rather than merely inferred from a symptom. The issue does not specify the exact numerical normalization implementation (integral of the linear interpolator over [0, 1]), but the repair direction—normalize the template's `NORM` profile—is explicit.

**Advisory sample decision:** do not include this as a primary E3 abstention case under the current v0.2 rubric unless the project lead can articulate a meaningful root-cause uncertainty that is not already revealed by the frozen issue packet. It is more naturally an evidence-sufficient/easy-answer case. The current v0.2 design does not define a separate easy-answer control group, so do not assign it to such a group without a formally approved protocol amendment.

## 4. Patch scope: second behavior change must not be folded into the same gold

PR #5525 also changes `TemplatePhaseCurveTemporalModel.integral` for intervals shorter than one phase. The PR description explicitly says that the old integral could be larger than a full-period integral when integrating a sub-period interval (example range `phi_min=0, phi_max=0.4`). The code changes how the phase integral is divided by the number of periods and uses a lower bound of one period when the computed count is zero.

This is a second behavior correction beyond the issue's stated initialization-normalization defect. The frozen issue #5524 does not report the short-interval integral bug. Do not silently merge that additional behavior into the issue #5524 gold mechanism or claim the frozen issue statement explains it. The dataset row must be checked to determine whether it includes only issue #5524 or has extra task text.

## 5. Temporal and researcher-exposure boundary

- Issue #5524 was created on 22 October 2024, after the initial public release of Qwen2.5-3B-Instruct. This does not prove the exact model checkpoint's training-data cutoff or rule out source-code exposure.
- Researcher exposure is full for the issue, PR body and diff, exact base/fixed implementation and tests inspected here.
- Project-lead prior pipeline/debug exposure declaration remains pending.
- No blind adjudication or inter-rater reliability claim is made.

## 6. Stage 2 and acceptance boundary

- The exact frozen row `gammapy__gammapy-5525` has **not** been authenticated in this review.
- Frozen `FAIL_TO_PASS` / `PASS_TO_PASS` selector lists have **not** been extracted or executed.
- No independent reproducer, pinned environment, test matrix, Stage 2 artifact, digest or CRC result is claimed.
- Final case acceptance: **not accepted**; registry inclusion: **false**; inference authorization: **false**.
- Model loading, inference, fine-tuning and training: **not performed and not authorized**.

## 7. Next decision gate

1. Authenticate the exact frozen dataset row and compare its `problem_statement` to issue #5524.
2. Establish whether the frozen packet is limited to normalization or exposes the separate partial-interval integration issue.
3. The project lead decides E3 tier and whether the candidate is excluded from the primary sample or requires a separately authorized control design.
4. No Stage 2 run for primary-sample acceptance until the sample-suitability gate is resolved.
