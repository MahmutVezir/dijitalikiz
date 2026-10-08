# Pilot Candidate Final Exclusion Report — 2026-10-08

## Final decision

Five Apache Commons Math candidates were reviewed against the frozen pilot criteria before real inference. Four are included; one is excluded.

| Case | Root cause / fix | Failing-test evidence | Component boundary | CCDG | Exposure risk | Decision |
|---|---|---|---|---|---|---|
| MATH-927 | Non-serializable BitsStreamGenerator broke distribution cloning; fixed by making it Serializable | RealDistributionAbstractTest.testDistributionClone | GammaDistribution → AbstractRealDistribution → random-generator hierarchy | strong | high | INCLUDE |
| MATH-950 | RESET_STATE could leave other EventState instances stale; fixed by advancing/resetting all event states | DormandPrince853IntegratorTest.testEventsScheduling | AbstractIntegrator ↔ EventState ↔ EventHandler | strong | medium | INCLUDE |
| MATH-938 | Localized 3D Line.revert precision defect | LineTest.testRevert | Single Line implementation | weak | high | EXCLUDE |
| MATH-949 | Shared BaseOptimizer iteration counter was not updated by concrete optimizers | Multiple optimizer iteration assertions, including AbstractLeastSquaresOptimizerAbstractTest.testGetIterations | BaseOptimizer + six concrete optimizer implementations | strong | high | INCLUDE |
| MATH-988 | SubLine.intersection did not handle a nullable Line.intersection result | SubLineTest.testIntersectionNotIntersecting; SubLineTest.testIntersectionParallel | SubLine.intersection ↔ Line.intersection ↔ remainingRegion | strong | high | INCLUDE |

## MATH-938 exclusion rationale

MATH-938 has valid provenance, root cause, fixed revision, and regression coverage, but the repair is confined to the 3D Line implementation. IC5 and IC6 therefore remain fail, so it is not a suitable cross-component CCDG case.

## MATH-949 decision reversal

MATH-949 is promoted from the earlier exclusion. The fix changes the shared BaseOptimizer iteration-counter contract and updates multiple concrete optimizer implementations, with regression assertions across multiple test classes. This establishes a meaningful cross-component dependency suitable for CCDG.

## Exposure-risk interpretation

High and medium labels are conservative public-exposure assessments. They do not establish that the frozen model was trained on, memorized, or otherwise contains a specific case.

## Frozen pilot size

4 cases × 2 conditions × 5 seeds = 40 inference records.

## Reproducibility

The full machine-readable decision record is data/pilot/final_candidate_review_2026-10-08.json.
