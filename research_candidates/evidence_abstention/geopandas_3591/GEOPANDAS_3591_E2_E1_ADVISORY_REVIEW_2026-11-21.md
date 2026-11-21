> **Project-lead decision recorded (21 November 2026): APPROVED.** The gold mechanism G1 and alternatives are approved; E3 = ABSTAIN, E2 = ABSTAIN, E1 = ANSWER. The AI advisory analysis below is superseded as a proposal by the binding project-lead decision at [the decision record](./PROJECT_LEAD_GOLD_AND_EVIDENCE_TIERS_DECISION_GEOPANDAS_3591_2026-11-21.md). The packet manifests are frozen, but Stage 2 remains unrun and requires a separate explicit approval. Candidate disposition remains HOLD.

# GeoPandas #3591 — E2/E1 advisory review

**Date:** 21 November 2026  
**Frozen cohort rank:** 52  
**Candidate:** geopandas/geopandas issue #3590 / PR #3591  
**Dataset row:** `geopandas__geopandas-3591`  
**Review status:** AI advisory proposal only; project-lead E2/E1 decisions pending  
**Execution boundary:** no Stage 2, no upstream tests/build, no model loading or inference

## 1. Existing project-lead decisions preserved

The project lead has already decided:

- E3 = **ABSTAIN** for the frozen problem statement.
- Candidate disposition = **HOLD**.
- Prior pipeline/debug exposure = `none`.
- E2 and E1 are separate decisions; neither is implied by the E3 decision.
- No Stage 2, final case acceptance, registry inclusion or model inference is authorized by the E3 decision.

This review does not alter those decisions. The project lead's current instruction, “tamamdır devam et” (21 November 2026), is treated only as authorization to prepare this bounded E2/E1 advisory analysis. It is not recorded as approval of the proposed gold mechanism or tiers.

## 2. Authenticated identity and frozen E3 boundary

- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`.
- Whole Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`.
- Canonical row SHA-256: `e543af0bbc5e779661c3b1b79c28849f67dee7c61157c000c6698b15ba1218e2`.
- Frozen problem-statement SHA-256: `c4aeb4909495887c065f1f7ae5ec0e321fb350e98ea789cde3f931cad597f12d`.
- Exact base: `c36eba059f6170715b63a9aa065817c64025d263`.
- Exact fix: `b3259ce23a37abd32650d7df098f3cdc8c4bb261`.
- Frozen FAIL_TO_PASS selector: `geopandas/tests/test_geodataframe.py::TestConstructor::test_geometry_nan_scalar`.

The frozen E3 statement consists of the issue body: a one-row DataFrame with a `geometry` column containing `np.nan` and a CRS; a CRS/geometry-column error in GeoPandas 1.1.0; a working explicit `geometry="geometry"` workaround; and a non-failing comparison with a valid Point in the same geometry column. It does not show the constructor's internal dtype eligibility predicate or source call chain.

The exact row was authenticated by no-inference workflow run 44924570231, job 136907864713, artifact 14715535728. The artifact SHA-256 is `1abca7d09dfcbf4c4ba773ab87fb21225ec8f4208f44f2f7fbb19b613352459b`; its ZIP CRC and all six internal hashes passed. No selector was run.

## 3. Proposed technical gold mechanism

**Proposed gold ID:** `G1_NONEMPTY_ALL_NULL_FLOAT_GEOMETRY_SKIPS_AUTO_COERCION`

**Proposed gold statement:** When `geometry=None` and the input has a single-level column named `geometry`, the buggy `GeoDataFrame.__init__` only routes that column through `_ensure_geometry` when its dtype is `geometry`, `object`, or the frame is empty with float dtype. A non-empty all-`np.nan` geometry column has float dtype, so it misses the coercion condition; the constructor leaves `geometry` unset and the later CRS guard raises the observed error. The fix adds a condition for a non-empty geometry column whose values are all missing, causing the column to be coerced and installed as the active geometry.

This is a source-level implementation mechanism, not merely the API-contract statement “the constructor should accept the input.”

## 4. Predeclared candidate mechanisms for tier analysis

These alternatives are provisional and require project-lead approval or correction before packet freezing.

| ID | Candidate mechanism | Distinguishing evidence |
|---|---|---|
| G1 | The implicit constructor's dtype eligibility predicate omits non-empty all-null float geometry columns. | Exact base/fixed constructor branch and added all-null predicate. |
| A1 | The failure is caused by a pandas/data-construction shape or column-alignment path for the one-row list input, rather than the GeoPandas dtype eligibility condition. | A longer all-null column with the same named columns would falsify a one-row-only explanation. |
| A2 | The CRS/active-geometry state transition is the primary defect: the geometry column is not registered as active before the CRS guard, independently of the dtype eligibility predicate. | Exact constructor control flow should show whether the CRS guard is only a downstream consequence of the failed auto-coercion branch. |

A1 is a deliberately narrow, testable alternative, not a claim that pandas itself is defective. A2 is a competing explanation of the error path, not a claim that changing the CRS guard alone is a safe fix. If the project lead judges either alternative insufficiently plausible or not distinct from G1, do not force a three-mechanism design; mark the candidate unclassifiable for the three-tier protocol or revise the alternatives before any model output exists.

## 5. Candidate E2 evidence additions

The following are candidate E2 additions, not yet a frozen packet. None is an independent reproduction log.

1. Issue comment by the maintainer, 5 June 2025 07:55:20 UTC: notes that `np.nan` is technically a float rather than a geometry object or `None`, and provides an explicit `geometry=[np.nan]` example.  
   Source: https://github.com/geopandas/geopandas/issues/3590#issuecomment-2943137874

2. Issue comment by the reporter, 5 June 2025 14:48:48 UTC: reports the same old-version behavior for a 10-row all-`np.nan` geometry column and for a mixture of `np.nan`, `None` and `pd.NA`. This is a reporter-authored follow-up observation, not a separately authenticated test log.  
   Source: https://github.com/geopandas/geopandas/issues/3590#issuecomment-2944863844

3. Maintainer follow-up, 5 June 2025 18:26:21 UTC: states that the project's geometry sanitization already handles these missing values elsewhere and that this constructor path need not disallow them.  
   Source: https://github.com/geopandas/geopandas/issues/3590#issuecomment-2945606056

4. The fixed PR's added regression tests at `geopandas/tests/test_geodataframe.py`, lines 1516–1540, cover the one-row scalar case and mixed null types; they assert active geometry, null semantics and CRS when pyproj is available. The tests are fixed-revision test code, not proof that the frozen selector was executed on the buggy base.  
   Pinned source: https://github.com/geopandas/geopandas/blob/b3259ce23a37abd32650d7df098f3cdc8c4bb261/geopandas/tests/test_geodataframe.py#L1516-L1540  
   Git blob SHA-1: `61eac57b37d9b0550a8b7d97f603a03d82725d28`

**Advisory E2 result: ABSTAIN.** These additions narrow the case: they make a one-row-only explanation less tenable and clarify the null/dtype behavior. They still do not expose the exact implicit constructor predicate or prove whether the failure is the dtype eligibility check versus a separate active-geometry/CRS state-transition mechanism. At least G1 and A2 remain plausible under the implementation-mechanism target. The comments and fixed tests do not justify an E2 ANSWER.

## 6. Candidate E1 additions

E1 would add the exact source-level evidence, kept out of E2:

- Buggy base `geopandas/geodataframe.py`, `GeoDataFrame.__init__`, lines 208–242: the implicit geometry conversion conditions and the later `geometry is None and crs` error guard. Git blob SHA-1: `1a607cbb5baea0c3ddc50b03042734c44b7945da`.  
  Pinned source: https://github.com/geopandas/geopandas/blob/c36eba059f6170715b63a9aa065817c64025d263/geopandas/geodataframe.py#L208-L247

- Buggy base `geopandas/array.py`, `from_shapely`, lines 153–190: the conversion path recognises missing values and appends `None`; this argues against a fundamental inability to normalize `np.nan`. Git blob SHA-1: `131a248229fcffeeab1a8217f9a9b398bae5c5df`.  
  Pinned source: https://github.com/geopandas/geopandas/blob/c36eba059f6170715b63a9aa065817c64025d263/geopandas/array.py#L153-L190

- Fixed PR head `geopandas/geodataframe.py`, line 215: adds `((not self.empty) and self["geometry"].isna().all())` to the implicit coercion predicate. Git blob SHA-1: `243d98759878754975e1b8b1732cfb503dd1bf0a`.  
  Pinned source: https://github.com/geopandas/geopandas/blob/b3259ce23a37abd32650d7df098f3cdc8c4bb261/geopandas/geodataframe.py#L208-L226

- PR review suggestion at 5 June 2025 20:43:12 UTC gives the exact all-null predicate; this belongs only in E1 because it directly discloses the patch mechanism.  
  Source: https://github.com/geopandas/geopandas/pull/3591#discussion_r2130293780

**Advisory E1 result: ANSWER.** The source shows that the all-null float column is excluded by the buggy implicit-coercion condition, while `from_shapely` can normalize missing values once called. The fixed change adds precisely the missing non-empty/all-missing condition; the later CRS guard is reached only because automatic geometry coercion did not occur. This leaves G1 as the sole surviving mechanism under the proposed alternatives.

## 7. Proposed tier summary — not approved

| Tier | Proposed result | Surviving mechanisms |
|---|---|---|
| E3 | ABSTAIN — already approved by the project lead | G1, A1, A2 |
| E2 | ABSTAIN — advisory recommendation only | G1, A2 |
| E1 | ANSWER — advisory recommendation only | G1 |

E2 and E1 are not project-lead decisions yet. No nested packet has been frozen and no SHA-256 packet manifests have been issued. Any alternative-mechanism changes must happen before packet freezing and before model output is seen.

## 8. Limits and next gate

- Researcher source exposure is full for the issue, comments, PR diff, exact base/fixed source and tests. No blinded researcher adjudication or inter-rater reliability claim is made.
- The issue comments are supplemental E2 candidates, not part of the frozen E3 problem statement.
- The fixed PR tests have not been claimed as executed here. The frozen FAIL_TO_PASS selector has not been run on either revision.
- No Stage 2 reproducer, environment lock, raw execution log or Stage 2 artifact exists for this candidate.
- No legal/licensing clearance or redistribution permission is asserted.
- No model has been loaded; no inference, fine-tuning or training was performed or authorized.
- Candidate remains HOLD; no registry inclusion or final acceptance.

**Requested project-lead gate:** review the proposed gold/alternatives and separately approve or revise E2 and E1. Only after that decision is recorded may the evidence packets be frozen. Stage 2 remains a distinct later gate and is not authorized by this advisory note.
