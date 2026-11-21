# Project-lead Stage 2 execution authorization — GeoPandas #3591

**Decision date:** 21 November 2026  
**Approval captured:** 2026-11-21T21:20+03:00 (Europe/Istanbul)  
**Candidate:** geopandas/geopandas issue #3590 / PR #3591  
**Frozen cohort rank:** 52  
**Frozen dataset row:** `geopandas__geopandas-3591`

## Decision

**Project-lead decision: AUTHORIZE the bounded Stage 2 base/fix reproduction described below.**

The project lead explicitly accepted the proposed execution plan in the conversation on 21 November 2026. This authorizes execution of the narrow technical reproduction only.

## Frozen technical targets

- Base commit: `c36eba059f6170715b63a9aa065817c64025d263`
- Fixed commit: `b3259ce23a37abd32650d7df098f3cdc8c4bb261`
- Frozen FAIL_TO_PASS selector: `geopandas/tests/test_geodataframe.py::TestConstructor::test_geometry_nan_scalar`
- Input: `GeoDataFrame(data=[[np.nan, np.nan]], columns=["geometry", "something"], crs="EPSG:4326")`
- Expected base result: the exact CRS-without-geometry `ValueError`.
- Expected fixed result: construction succeeds; shape is (1, 2); active geometry is `geometry`; the geometry value is `None`; CRS is EPSG:4326.
- Fixed-revision regression check: run the exact frozen pytest selector on the fixed commit. The selector is not expected to exist on the buggy base because it was introduced by the fix PR; the same frozen input is therefore exercised on base by the independent reproducer.

## Execution controls

- Run only the exact base and fixed commits above.
- Use a pinned Python 3.11.9 environment with a fully version-pinned dependency lock.
- Authenticate source blobs and the exact base-to-fix changed-path set before running.
- Preserve raw reproducer and pytest logs, environment freeze, source provenance, and SHA-256 checksums in a workflow artifact.
- Do not alter either upstream commit or add a patch to the upstream checkout.
- No model loading, inference, fine-tuning, training, or candidate selection is permitted.
- No other candidate may be started by this authorization.

## Decision boundaries

This authorization is not a Stage 2 pass, not Stage 3 confirmation, not final case acceptance, not legal clearance, and not authorization for model inference. The candidate remains **HOLD** pending technical results and subsequent independent review.

## Execution status at authorization time

`authorized_not_yet_executed`. No Stage 2 result is claimed in this record.
