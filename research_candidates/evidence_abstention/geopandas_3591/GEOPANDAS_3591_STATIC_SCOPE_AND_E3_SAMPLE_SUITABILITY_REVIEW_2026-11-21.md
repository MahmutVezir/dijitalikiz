# GeoPandas #3591 / issue #3590 — static scope and E3 sample-suitability review

**Date:** 21 November 2026  
**Candidate:** geopandas/geopandas issue #3590 / fix PR #3591  
**Cohort rank:** 52 of 96  
**Disposition:** **STRONG ISSUE/PATCH ALIGNMENT; DIRECT ALL-NULL GEOMETRY EDGE CASE; MODERATE-TO-HIGH E3 ANSWERABILITY RISK; HOLD BEFORE STAGE 2**

## 1. Frozen upstream identity

- Issue: https://github.com/geopandas/geopandas/issues/3590
- Fix PR: https://github.com/geopandas/geopandas/pull/3591
- Issue created: `2025-06-05T00:05:04Z`.
- PR created: `2025-06-05T07:55:40Z`.
- Exact PR base: `c36eba059f6170715b63a9aa065817c64025d263`.
- Exact PR head: `b3259ce23a37abd32650d7df098f3cdc8c4bb261`.
- Merge commit: `b3259ce23a37abd32650d7df098f3cdc8c4bb261`.
- Changed files: `CHANGELOG.md`, `geopandas/geodataframe.py`, `geopandas/tests/test_geodataframe.py`.

## 2. Issue symptom and exact implementation change

Issue #3590 reports a regression from GeoPandas 1.0.1 to 1.1.0. In 1.0.1, a GeoDataFrame created with a column named `geometry` whose only value is `np.nan` silently converts that value to `None` and accepts the supplied CRS. In 1.1.0, the constructor rejects the same input with:

```text
ValueError: Assigning CRS to a GeoDataFrame without a geometry column is not supported.
```

The issue gives a one-row, two-column example and contrasts it with a geometry column containing both `np.nan` and a valid `Point`, which still works. It also says that supplying `geometry="geometry"` explicitly makes the failing example work.

At the exact buggy base, `geopandas/geodataframe.py` only attempts automatic geometry coercion when the inferred geometry dtype is `geometry`, `object`, or the empty-frame special case with `float` dtype. A non-empty all-`np.nan` column has float dtype, so it misses all three conditions and is not passed through `_ensure_geometry`. The constructor then proceeds without having recognized a geometry column, and CRS assignment fails.

At the exact PR head, the constructor adds:

```python
or ((not self.empty) and self["geometry"].isna().all())
```

This explicitly includes non-empty all-null geometry columns in the coercion path. The regression tests cover the one-row `np.nan` case and a longer mixed-null sequence containing `np.nan`, `None`, and `pd.NA`; they assert the active geometry column, null conversion/semantics, and CRS when pyproj is available.

Issue, source-level failure path, implementation change and added tests align directly. No unrelated source file or second bug is introduced by the three-file PR scope.

## 3. E3 answerability and information separation

### Frozen issue body

The issue body already provides:
- the precise constructor input with `columns=["geometry", "something"]`;
- the supplied CRS;
- the old-version behavior (the NaN is treated as missing geometry);
- the new-version exception and its full CRS/geometry-column message;
- a working workaround using `geometry="geometry"`;
- a contrast case with a valid Point present in the same geometry column, which does not fail.

These clues strongly narrow the failure to automatic geometry-column recognition when the geometry column contains no actual geometry objects and consists only of missing values. The likely repair is to recognise an all-missing geometry column and still send it through geometry coercion. The issue does not name the constructor's dtype gate or the exact `isna().all()` condition, so the final E3 sufficiency classification is not asserted here; it requires the project lead's source-aware judgment.

### Later issue comments — not part of the frozen issue body

The researcher also inspected two follow-up comments:
- A maintainer says `np.nan` is technically a float, not a geometry object or `None`, and acknowledges that the reported case should probably work.
- The reporter clarifies that longer columns where `np.nan` is the only unique value and mixed null types (`np.nan`, `None`, `pd.NA`) should also work.

These comments strengthen the causal interpretation and expose the all-null-type generalization, but they must not be silently inserted into the frozen E3 packet if the dataset `problem_statement` contains only the issue body. Researcher exposure to these comments is disclosed separately.

**Advisory sample-suitability recommendation:** hold the candidate out of Stage 2 until the exact frozen row is authenticated and the project lead decides the E3 tier. The issue body is unusually concrete and the implementation repair is a narrow all-null predicate; this creates a moderate-to-high easy-answer risk. However, unlike cases where the issue literally states the missing code path, it does not expose the internal dtype conditional. Do not automatically exclude it solely from this preliminary review.

## 4. Temporal and researcher-exposure boundary

- Issue #3590 was created on 5 June 2025, after the public September 2024 release and initial upload of the pinned Qwen2.5-3B-Instruct checkpoint. This reduces the likelihood of exact issue/PR-specific training exposure, but does not prove the checkpoint's actual training-data cutoff or rule out exposure to pre-existing GeoPandas source.
- Researcher exposure is full for the issue, comments, PR diff, and exact base/fixed source reviewed here.
- Prior pipeline/debug exposure declaration from the project lead remains pending.
- No blinded adjudication or inter-rater reliability claim is made.

## 5. Stage 2 and acceptance boundary

- The exact frozen SWE-rebench row `geopandas__geopandas-3591` has **not** yet been authenticated.
- The frozen `FAIL_TO_PASS` and `PASS_TO_PASS` selectors have **not** been extracted or run on the exact base and fixed revisions.
- No independent reproducer, pinned environment, Stage 2 artifact, digest or CRC result is claimed.
- No model has been loaded and no inference, fine-tuning or training has been performed.
- Final case acceptance: **not accepted**; registry inclusion: **false**; inference authorization: **false**.

## 6. Next decision gate

1. Authenticate the exact frozen dataset row, `problem_statement`, selector lists, base commit and row hash.
2. Confirm whether the frozen E3 packet is exactly the issue body or includes additional comments/metadata; keep later comments out unless the frozen source actually includes them.
3. The project lead decides whether E3 still leaves the root cause unresolved enough for the primary abstention sample.
4. Only after that scope/suitability decision may Stage 2 reproduction begin. A technical base-fail/fixed-pass result alone would not grant final case acceptance.


## 7. Project-lead hold and exposure amendment — 21 November 2026

The project lead confirmed candidate-specific `prior_pipeline_debug_exposure=none`. The candidate remains **held**: this declaration is not an E3 tier decision, Stage 2 authorization, final acceptance or model-inference authorization.

The next gates remain exact frozen-row and selector authentication, confirmation of the frozen E3 packet boundary, and project-lead semantic E3 suitability adjudication. Until those pass, do not run Stage 2 or include the candidate in the primary sample.

Decision record: `PROJECT_LEAD_RANK49_52_STAGE2_STAGE3_DECISIONS_2026-11-21.md`.
