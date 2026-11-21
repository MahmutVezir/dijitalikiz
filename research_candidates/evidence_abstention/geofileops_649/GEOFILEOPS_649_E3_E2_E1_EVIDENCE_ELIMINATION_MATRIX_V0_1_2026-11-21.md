# GeofileOps #649 / issue #648 — E3/E2/E1 evidence-elimination matrix

**Date:** 21 November 2026  
**Candidate:** geofileops/geofileops issue #648 / PR #649  
**Dataset instance:** `geofileops__geofileops-649`  
**Status:** TECHNICAL GOLD SOURCE-AUDITED; TIER LABEL DEPENDS ON PREDECLARED DIAGNOSTIC GRANULARITY; PROJECT-LEAD APPROVAL AND FINAL ACCEPTANCE PENDING

## 1. Candidate contract and gold mechanism

Issue #648 reports that the default `dst_layer` used by `copy_layer` and `append_to` is not the destination filename stem, despite the documented API contract. PR #649 changes the behavior so that when `dst_layer is None`, the destination layer name is derived from `get_default_layer(dst)`.

**G1 — `MISSING_NONE_TO_DESTINATION_STEM_FALLBACK`.** The default destination-layer fallback is not applied when `dst_layer=None` reaches the copy/append path. The existing helper `get_default_layer(path)` already returns `Path(path).stem`; the buggy base simply does not invoke that helper at the necessary entry/helper points. GDAL therefore receives a missing destination layer name and chooses a layer name derived from the source or its own driver behavior, rather than the destination file stem.

PR #649 adds the fallback in three places: `append_to`, `_append_to_nolock`, and `copy_layer`. The repeated guard protects both public paths and direct/internal callers.

## 2. Frozen E3 packet and diagnostic-granularity problem

The authenticated dataset `problem_statement` reads:

> BUG: in copy_layer and append_to the default dst_layer is not the stem of the filename

It then says the documentation states that it should work this way, that the inconsistency is confusing, and that the change may be non-backwards-compatible.

The packet explicitly names:
- both affected public APIs: `copy_layer` and `append_to`;
- the parameter: `dst_layer`;
- the erroneous default behavior: it is not the filename stem;
- the expected contract: the destination filename stem is the default layer name.

It does **not** include a minimal code reproducer, exact output layer names, source code, a stack trace, or the point in the call chain where the `None` value is not normalized.

That creates two legitimate grading granularities:

1. **API-contract diagnosis:** “When `dst_layer` is omitted, the destination layer should default to `Path(dst).stem`; the current behavior violates that contract.” This is effectively disclosed by the E3 title/body. Under this target, E3 is answerable.
2. **Implementation-mechanism diagnosis:** “The buggy code passes `dst_layer=None` through the public/helper paths instead of calling the existing `get_default_layer(dst)` fallback.” This requires source-level evidence and is not proven by the E3 packet alone. Under this stricter target, E3 should abstain.

Project lead must decide which granularity the preregistered gold rubric intends. Do not choose the E3 label after observing model answers.

## 3. Predeclared alternatives

| ID | Alternative / mechanism | Distinguishing evidence |
|---|---|---|
| G1 | The `None` destination-layer fallback is not applied in the copy/append call chain; the existing `get_default_layer(dst)` helper is skipped. | Exact-base source has no `dst_layer is None` fallback in `copy_layer`, `append_to`, or `_append_to_nolock`; the fixed revision adds the fallback. |
| A1 | Only `copy_layer` is defective; `append_to` already derives the destination stem correctly. | An `append_to` case with omitted `dst_layer` should fail if A1 is false. |
| A2 | Only `append_to` is defective; `copy_layer` already derives the destination stem correctly. | `copy_layer` cases with omitted `dst_layer` should fail if A2 is false. |
| A3 | The shared `get_default_layer()` helper computes the wrong filename component or mishandles extensions. | Source inspection of the helper and direct behavior for ordinary and compressed destination paths distinguishes this. |
| A4 | A single GDAL driver or input-format interaction causes the observed mismatch, rather than a shared default-parameter path. | Cross-format selectors and a simple independent GeoPackage reproducer distinguish a narrow driver/input-specific defect from a shared fallback defect. |

These alternatives are not assigned equal prior probabilities.

## 4. E3 → E2 → E1 evidence-elimination matrix

| Evidence / alternative | E3 — frozen problem statement only | E2 — independent reproducer + authenticated frozen selectors | E2 disposition | E1 — exact-base source chain |
|---|---|---|---|---|
| G1: missing `None` fallback | Names the wrong default for `dst_layer` in both public APIs, but not the code location or omitted operation. | Independent `copy_layer` reproducer returns `source_layer` rather than `destination_result`; 10 frozen selectors fail on base and pass fixed. | Remains live. | Base does not call `get_default_layer(dst)` in `copy_layer`, `append_to`, or `_append_to_nolock`; fixed revision adds these guards. |
| A1: only `copy_layer` is defective | Both APIs are named, but no separate example establishes either path. | The frozen `append_to` selector `test_append_different_columns[.csv]` also fails on base and passes fixed. | Eliminated as the sole explanation. | `append_to` and `_append_to_nolock` both receive the unresolved `dst_layer` in base; fixed resolves it. |
| A2: only `append_to` is defective | Both APIs are named, but no independent path evidence. | Nine frozen `copy_layer` selectors fail on base and pass fixed; independent copy reproducer repeats the mismatch. | Eliminated as the sole explanation. | `copy_layer` passes `dst_layer` unchanged to `_append_to_nolock` in base; fixed resolves it before the call. |
| A3: `get_default_layer()` computes the wrong stem | Not distinguishable from a missing call to the helper. | E2 does not directly inspect helper implementation; `.gpkg` and `.gpkg.zip` paths behave consistently with the intended filename stem after the fix. | Remains plausible until E1. | Exact-base helper returns `Path(path).stem` at `geofileops/fileops.py:508`; the helper itself is correct. |
| A4: single format/input driver issue | Not distinguishable from the issue text alone. | Selectors span GeoPackage, shapefile and CSV inputs; GeoPackage and compressed GeoPackage outputs; plus the append-to-CSV path. Independent GPKG reproducer also fails. | Narrow driver/input-specific explanations are eliminated; a general GDAL interpretation of missing layer remains possible until E1. | Missing fallback is explicit in source at the shared/public call paths; fixed behavior is not a one-driver special case. |

Surviving mechanisms under the strict source-mechanism target:
- E3: `{G1, A3, A4}` plus uncertainty over which public path fails where.
- E2: `{G1, A3, A4}`. E2 eliminates A1 and A2 and narrows A4 from a single-format explanation, while at least two causal alternatives remain.
- E1: `{G1}`.

Therefore, under a strict implementation-mechanism rubric, the proposed tiers are **E3 ABSTAIN / E2 ABSTAIN / E1 ANSWER** and E2 meets the strengthened alternative-elimination criterion.

Under an API-contract rubric, E3 may already be ANSWER because the exact incorrect default and intended value are written in the title. This candidate is not eligible for primary abstention sampling until project lead resolves this rubric ambiguity.

## 5. Exact E1 source chain

### Existing helper is correct

Buggy-base source blob `9edeb1c1bf7eb7d0f35b246611b27bad33fdcc7e` in `geofileops/fileops.py` defines `get_default_layer` at lines 497–508 and returns `Path(path).stem` at line 508.

### Buggy base does not apply the fallback

- `copy_layer` begins at line 2622. It converts `src` and `dst` to `Path`, validates source and overwrite behavior, then calls `_append_to_nolock` with `dst_layer` unchanged (around lines 2744–2756). No `if dst_layer is None` branch exists in the function.
- `append_to` begins at line 2295. It converts paths and enters the lock/append loop, then forwards `dst_layer` unchanged to `_append_to_nolock` around lines 2432–2458.
- `_append_to_nolock` begins at line 2474. After normalizing `columns`, it immediately prepares GDAL options; no `dst_layer` default is applied before the operation proceeds.

### Fixed PR applies the fallback at all three relevant boundaries

Fixed-source blob `29738ee57088279b7bf7c656b34721dbc8d78f7b`:
- `append_to`: lines 2419–2420 set `dst_layer = get_default_layer(dst)` when `None`.
- `_append_to_nolock`: lines 2502–2503 apply the same fallback, covering direct/internal calls.
- `copy_layer`: lines 2750–2751 apply the fallback before passing the destination layer to `_append_to_nolock`.

The exact code chain distinguishes G1 from A3 and A4: the helper already returns the required `Path(dst).stem`; the missing step is applying it when `dst_layer` is omitted.

## 6. Stage 2 behavioral evidence

Stage 2 and archive verification are recorded in:

`GEOFILEOPS_649_STAGE2_REPRODUCTION_AND_ARTIFACT_AUDIT_2026-11-21.md`

Key results: independent `copy_layer` default reproducer fails on base; explicit `dst_layer` positive control passes on base; the two reproducer tests pass on fixed; all 10 frozen selectors fail on base and pass fixed. The artifact is independently verified (outer SHA-256 match, clean CRC, 18/18 inner hashes).

Selectors are multiple observations for one issue and one upstream repository, not independent cases.

## 7. Researcher exposure, issue family and temporal limits

- One issue (#648), one fix PR (#649), one dataset row, one upstream project. Maximum contribution: one case.
- Targeted repository searches for `dst_layer`/`stem`, `default layer` and `get_default_layer` surfaced only issue #648; this is a targeted search, not an exhaustive repository history proof.
- Issue comments retrieved: none. Researcher exposure is full for issue body, PR diff, exact base/fixed source, test suite, Stage 2 logs and artifact. No blind adjudication or inter-rater reliability claim is made.
- Project-lead prior pipeline/debug exposure declaration remains pending; declarations for other candidates are not transferable.
- Issue/PR date is 6 March 2025. This postdates Qwen2.5's public September 2024 announcement and the pinned model repository revision in September 2024. Issue/PR-specific exposure is less likely by chronology; pre-existing GeofileOps source exposure and the exact checkpoint training-data cutoff remain unresolved.

## 8. Advisory disposition and open gates

- Gold proposal: `MISSING_NONE_TO_DESTINATION_STEM_FALLBACK`.
- Strict source-mechanism tiers: E3 ABSTAIN / E2 ABSTAIN / E1 ANSWER.
- API-contract tier alternative: E3 may be ANSWER because the issue itself states the default `dst_layer` is not the filename stem.
- Project lead must freeze the diagnostic granularity before using this candidate as a primary abstention case.
- Project-lead gold/tier approval: pending.
- Project-lead prior pipeline/debug exposure declaration: pending.
- Temporal-exposure acknowledgement: pending.
- Human review of root BSD-3-Clause, environment dependencies/native notices, dataset-card attribution and scope: pending; no legal clearance claim.
- Bounded research-scope acknowledgement, schema-conformant case record and fail-closed validation: pending.
- Separate final project-lead YES/NO acceptance: pending.
- Final case acceptance: **not accepted**; registry inclusion: **false**; inference authorization: **false**.
- No model weights were loaded; no inference, fine-tuning or training occurred.