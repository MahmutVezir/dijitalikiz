# mpmath #902 / issue #511 — temporal-exposure hold confirmation

**Date:** 21 November 2026  
**Candidate:** mpmath/mpmath issue #511 / fix PR #902  
**Cohort rank:** 40 of 96  
**Disposition:** **RETAINED AS PROVENANCE; HELD OUT OF PRIMARY EVALUATION SAMPLE; NO STAGE 2 EXECUTION**

## 1. Frozen screening decision

The frozen v0.2 exploratory manifest `research_candidates/evidence_abstention/SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json`, `candidate_review_records[12]`, identifies `mpmath__mpmath-902` as:

- `status = held_high_pre_release_temporal_exposure_risk`
- Issue: https://github.com/mpmath/mpmath/issues/511
- PR: https://github.com/mpmath/mpmath/pull/902
- Issue created: `2020-01-17T19:05:48Z`
- Hold reason: the exact public issue predates the public September 2024 release of the pinned Qwen2.5-3B-Instruct family by more than four years, so training-data exposure is plausible and cannot be ruled out.
- Case acceptance: not accepted; inference authorization: false.

This is a pre-existing frozen-sample exclusion, not a new technical judgment made from the patch. The later cohort scope audit calls it a provisional bug candidate on static technical grounds, but that does not override the more specific temporal hold in the exploratory manifest.

## 2. Technical screening performed in this continuation

The issue, PR and exact source changes were inspected at a static level only:
- Issue #511 reports that `laguerre(1, a, inf)` returns a finite value where the expected limit is negative infinity; the `fp` context raises `NoConvergence`.
- PR #902 (`Special case in ctx.hypsum for infinite z`) modifies `mpmath/ctx_fp.py`, `mpmath/ctx_mp.py` and `mpmath/tests/test_functions2.py`.
- The patch adds a polynomial terminating-series special case for infinite `z`, as well as denominator/pole handling and regression coverage.

These static observations are not an executed reproduction. No independent reproducer was added, no dataset row was extracted or authenticated, no source was built, and no Stage 2 test was run.

## 3. Decision boundary

- Do **not** initiate Stage 2 or include this candidate in the primary abstention evaluation sample under the existing frozen manifest.
- Do not treat the issue's age as proof that the exact report or source was in the model's training data; the correct statement is that exposure risk is high and cannot be ruled out.
- A primary-sample re-entry would require an explicit project-lead amendment to the frozen temporal-exposure rule and a documented rationale. It must not be inferred from the candidate's technical testability.
- The candidate may remain in provenance records or, only under a separate explicitly labelled engineering feasibility study, be considered as a non-primary illustrative control. It cannot count toward independent primary cases.
- Final acceptance: **not accepted**; registry inclusion: **false**; inference authorization: **false**.

## 4. Source references

- Frozen exploratory manifest: https://github.com/MahmutVezir/dijitalikiz/blob/621ca7acaedbfba6be6e5b81442a6059c73aea6b/research_candidates/evidence_abstention/SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json
- Cohort scope audit ranks 33–40: https://github.com/MahmutVezir/dijitalikiz/blob/621ca7acaedbfba6be6e5b81442a6059c73aea6b/research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_SCOPE_AUDIT_33_40_2026-11-12.md
- Qwen2.5 public announcement, 19 September 2024: https://qwenlm.github.io/blog/qwen2.5/
- Issue #511: https://github.com/mpmath/mpmath/issues/511
- Fix PR #902: https://github.com/mpmath/mpmath/pull/902