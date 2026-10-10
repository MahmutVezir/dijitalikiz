# Held-out case discovery log — 2026-10-10

**Status: preliminary discovery leads only.** This document is not a held-out case manifest, not an admission decision, not source adjudication, and not permission to run model inference. The v2 protocol remains draft with an empty held-out case pool. No lead below may be used until the exact pre-fix revision is pinned, a targeted regression is independently reproduced red/green, source evidence is captured, and two independent reviewers plus a separate adjudicator approve the case.

## Selection rules

- Keep the 16 historical confirmatory cases, historical pilot cases, and all seven scoring-calibration candidates out of the held-out set.
- Prefer recent and diverse repositories/defect mechanisms where possible; still mark training-data exposure unknown unless supported by evidence.
- Require a coherent cross-component mechanism, immutable pre-fix and fixed revisions, a named regression test that fails before the fix and passes after it, provenance/license evidence, and one source-grounded assessment per case.
- A closed PR, passing project-wide build, or plausible bug description is a lead—not a substitute for pinned red/green reproduction and independent adjudication.

## Preliminary shortlist

### Lead HD-001 — Commons Lang FastDatePrinter locale-calendar era mismatch

- Source PR: https://github.com/apache/commons-lang/pull/1800
- Fix commit: https://github.com/apache/commons-lang/commit/c7f1a6d27707e8cd8cbed94f83e0c58d2c480614
- Problem described upstream: FastDatePrinter sourced era names from a Gregorian two-entry symbol table even when the printer used Thai Buddhist or Japanese Imperial calendars; formatting could produce the wrong era or throw for an era index beyond the Gregorian table, while the parser obtained era names from the calendar.
- Relevant changed files: `src/main/java/org/apache/commons/lang3/time/FastDatePrinter.java`; `src/test/java/org/apache/commons/lang3/time/FastDateFormatTest.java`; `src/test/java/org/apache/commons/lang3/time/FastDatePrinterTest.java`.
- Regression test targets in the fixed change: `FastDateFormatTest#testEraRoundTripNonGregorianCalendar`; `FastDatePrinterTest#testEraMixedCalendarTypes`.
- Possible cross-component path to review: locale selection -> calendar implementation/era field -> printer era rendering -> parser round-trip.
- Risks/limitations: upstream PR discloses Claude Code assistance in defect discovery and patch/test drafting; public exposure is documented, model training exposure remains unknown. Exact pre-fix SHA and a new independent red/green artifact have not been pinned in this project's intake record.
- Current decision: **promising lead; not eligible yet**. A reviewer must validate that the task requires cross-component dependency reasoning rather than only one local formatting fix.

### Lead HD-002 — Commons Lang TypeUtils/JDK WildcardType bound contract

- Source PR: https://github.com/apache/commons-lang/pull/1807
- Fix commit: https://github.com/apache/commons-lang/commit/43154e016ae213a0da5b727cd1aa18e6e0c56adb
- Problem described upstream: a custom unbounded WildcardType could expose an empty upper-bound array even though the Java reflection contract supplies `Object`; this caused equality to be asymmetric against the JDK's wildcard implementation and hash codes to disagree.
- Relevant changed files: `src/main/java/org/apache/commons/lang3/reflect/TypeUtils.java`; `src/test/java/org/apache/commons/lang3/reflect/TypeUtilsTest.java`.
- Regression test target: `TypeUtilsTest#testUnboundedWildcardType` (including equality/hash-code and implicit-bound assertions).
- Possible dependency path to review: custom `WildcardTypeImpl` construction -> `getUpperBounds` contract -> equality normalization -> hash-code consistency with JDK reflection values.
- Risks/limitations: upstream PR discloses Claude assistance; public exposure is documented but model training exposure is unknown. This may be too localized to `TypeUtils` and JDK interoperation to qualify as a strong cross-component case. Exact pre-fix SHA and independent red/green artifact are not yet pinned in this project's intake record.
- Current decision: **moderate/uncertain lead; not eligible yet**. Use only if independent reviewers find the cross-component relation substantive.

### Lead HD-003 — Commons Collections ordered-map nextKey inconsistency

- Source PR: https://github.com/apache/commons-collections/pull/728
- Fix commit: https://github.com/apache/commons-collections/commit/04b30be69f4355f218d587703bc20b1a591c3e3c
- Problem described upstream: `AbstractSortedMapDecorator.nextKey` and `DualTreeBidiMap.nextKey` could skip a valid successor for an absent key or throw past the end instead of returning null; related decorators inherit behavior.
- Relevant changed files: `src/main/java/org/apache/commons/collections4/map/AbstractSortedMapDecorator.java`; `src/main/java/org/apache/commons/collections4/bidimap/DualTreeBidiMap.java`; regression tests for `DualTreeBidiMap`, `FixedSizeSortedMap`, and `UnmodifiableSortedMap`.
- Regression test targets in the fixed change include `DualTreeBidiMapTest#testNextKeyAbsentKey`, `FixedSizeSortedMapTest#testNextKey`, and `UnmodifiableSortedMapTest#testNextKey`.
- Possible dependency path to review: `OrderedMap.nextKey` contract -> decorator traversal logic -> bidirectional sorted-map implementation and wrappers.
- Risks/limitations: exact pre-fix SHA and an independent red/green reproduction artifact are not yet pinned in this project's intake record. This may be one family of duplicated local implementation bugs rather than a sufficiently deep cross-component causal chain.
- Current decision: **possible lead; not eligible yet**.

## Screened but not admitted

- Commons Lang PR #1799 (`stripAccents` Hangul recomposition): https://github.com/apache/commons-lang/pull/1799. The available description and diff point mainly to one string-normalization method and its unit test. Keep out of the primary cross-component pool unless reviewers identify a stronger justified component boundary; otherwise it may serve only as a calibration/control lead if permitted by that separate protocol.
- Commons Compress PR #813 (empty-input LZ4 output): https://github.com/apache/commons-compress/pull/813. The PR was open in the observed snapshot, so it is not admitted as a fixed, stable defect case. Revisit only after a fixed commit is merged or otherwise made immutable and the pre-fix/fixed test is reproduced.
- Commons Compress PR #814 (UNIX hardlink extraction): https://github.com/apache/commons-compress/pull/814. This is an in-progress feature change, not an accepted fixed-defect case; exclude from the present pool.

## Required next actions for every lead

1. Resolve and record an exact pre-fix commit SHA and exact fixed commit SHA; do not infer a SHA from PR date or branch name.
2. Confirm license and immutable source/revision links.
3. Run the named regression test separately on each pinned revision; archive logs and hashes and confirm fail-before/pass-after.
4. Create the source-linked case record and draft CCDG edges; have two independent reviewers assess root cause, edges, one-defect coherence, contamination and suitability.
5. Have a separate adjudicator resolve disagreements and record an evidence-bound decision.
6. Keep all these leads out of `data/followup_v2/cases/` and the held-out manifest until all evidence is complete. Do not count them toward the 61-case target yet.

## Current count

- Held-out eligible cases: **0**.
- Discovery leads in this note: **3** (none eligible).
- Calibration-only cases remain permanently excluded from held-out confirmation.
- No new model inference was run or authorized.