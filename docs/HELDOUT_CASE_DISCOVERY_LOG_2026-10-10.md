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
- Exact pinned revisions: pre-fix `324d9fbd091749a9c70aed4b038fd0b4a520b3cf`; fixed `c7f1a6d27707e8cd8cbed94f83e0c58d2c480614` (confirmed as a one-commit comparison).
- Relevant changed files: `src/main/java/org/apache/commons/lang3/time/FastDatePrinter.java`; `src/test/java/org/apache/commons/lang3/time/FastDateFormatTest.java`; `src/test/java/org/apache/commons/lang3/time/FastDatePrinterTest.java`.
- Regression test targets in the fixed change: `FastDateFormatTest#testEraRoundTripNonGregorianCalendar`; `FastDatePrinterTest#testEraMixedCalendarTypes`.
- Possible cross-component path to review: locale selection -> calendar implementation/era field -> printer era rendering -> parser round-trip.
- Risks/limitations: upstream PR discloses Claude Code assistance in defect discovery and patch/test drafting; public exposure is documented, model training exposure remains unknown. The exact pre-fix SHA is pinned, and the independent red/green run #38052846346 passed the named tests before/after the fix. This does not replace human source adjudication.
- Current decision: **promising lead; not eligible yet**. A reviewer must validate that the task requires cross-component dependency reasoning rather than only one local formatting fix.

### Lead HD-002 — Commons Lang TypeUtils/JDK WildcardType bound contract

- Source PR: https://github.com/apache/commons-lang/pull/1807
- Fix commit: https://github.com/apache/commons-lang/commit/43154e016ae213a0da5b727cd1aa18e6e0c56adb
- Problem described upstream: a custom unbounded WildcardType could expose an empty upper-bound array even though the Java reflection contract supplies `Object`; this caused equality to be asymmetric against the JDK's wildcard implementation and hash codes to disagree.
- Exact pinned revisions: pre-fix `25c4bfcd6d9dc3a7333088bfc3031b05cd93837e`; fixed `43154e016ae213a0da5b727cd1aa18e6e0c56adb` (confirmed as a one-commit comparison).
- Relevant changed files: `src/main/java/org/apache/commons/lang3/reflect/TypeUtils.java`; `src/test/java/org/apache/commons/lang3/reflect/TypeUtilsTest.java`.
- Regression test target: `TypeUtilsTest#testUnboundedWildcardType` (including equality/hash-code and implicit-bound assertions).
- Possible dependency path to review: custom `WildcardTypeImpl` construction -> `getUpperBounds` contract -> equality normalization -> hash-code consistency with JDK reflection values.
- Risks/limitations: upstream PR discloses Claude assistance; public exposure is documented but model training exposure is unknown. This may be too localized to `TypeUtils` and JDK interoperation to qualify as a strong cross-component case. The exact pre-fix SHA is pinned, and the independent red/green run #38052846346 passed the named test before/after the fix. This does not replace human source adjudication.
- Current decision: **moderate/uncertain lead; not eligible yet**. Use only if independent reviewers find the cross-component relation substantive.

### Lead HD-003 — Commons Collections ordered-map nextKey inconsistency

- Source PR: https://github.com/apache/commons-collections/pull/728
- Fix commit: https://github.com/apache/commons-collections/commit/04b30be69f4355f218d587703bc20b1a591c3e3c
- Problem described upstream: `AbstractSortedMapDecorator.nextKey` and `DualTreeBidiMap.nextKey` could skip a valid successor for an absent key or throw past the end instead of returning null; related decorators inherit behavior.
- Exact pinned revisions: pre-fix `a5248efd7f4f857f88770565414948e2d0524933`; fixed `04b30be69f4355f218d587703bc20b1a591c3e3c` (confirmed as a one-commit comparison).
- Relevant changed files: `src/main/java/org/apache/commons/collections4/map/AbstractSortedMapDecorator.java`; `src/main/java/org/apache/commons/collections4/bidimap/DualTreeBidiMap.java`; regression tests for `DualTreeBidiMap`, `FixedSizeSortedMap`, and `UnmodifiableSortedMap`.
- Regression test targets in the fixed change include `DualTreeBidiMapTest#testNextKeyAbsentKey`, `FixedSizeSortedMapTest#testNextKey`, and `UnmodifiableSortedMapTest#testNextKey`.
- Possible dependency path to review: `OrderedMap.nextKey` contract -> decorator traversal logic -> bidirectional sorted-map implementation and wrappers.
- Risks/limitations: the exact pre-fix SHA is pinned, and the independent red/green run #38052846346 passed the named tests before/after the fix. This does not replace human source adjudication. This may be one family of duplicated local implementation bugs rather than a sufficiently deep cross-component causal chain.
- Current decision: **possible lead; not eligible yet**.


### Lead HD-004 — Commons Net FTPS data-channel hostname verification

- Source PR: https://github.com/apache/commons-net/pull/404
- Exact revisions: pre-fix `faa4edd7e287a3db465a32efd9c2d5faa15757fe`; fix `a79729464f6e69b773171ff30e3d483cab7afd70` (one-commit comparison).
- Regression test: `FTPSClientTest#testHostnameVerifierUsedForDataConnection`; test fixture files pinned from the fixed revision: `AbstractFtpsTest.java` and `FTPSClientTest.java`.
- Defect summary: a configured TLS hostname verifier ran on the FTPS control connection but not on the data-channel TLS handshake. This can make data-channel identity checking inconsistent with the configured server-identity check.
- Candidate cross-component path: FTP command/listing flow -> data-connection socket creation -> TLS handshake -> configured `HostnameVerifier` -> acceptance/rejection of data-channel peer.
- Preliminary fit: **promising security/integration lead** because the defect crosses control/data connection flows and TLS identity verification. Public fix is known; model exposure remains unknown.
- Screening status: **red-green pass in run #38052846346**. Not eligible until exact-test red/green artifact and independent human source review/adjudication pass.

### Lead HD-005 — Commons Net FTP parser class initialization from untrusted SYST reply

- Source PR: https://github.com/apache/commons-net/pull/403
- Exact revisions: pre-fix `a3d19751891edb9f7cb8c11bc344eaf1683b2b32`; fix `6e38749760c0366aac1637c7dc15e4ccf76329c9` (one-commit comparison).
- Regression test: `DefaultFTPFileEntryParserFactoryTest#testNonParserClassIsNotInstantiated`; test file pinned from the fixed revision.
- Defect summary: the FTP server's `SYST` response could be treated as a fully qualified class name and loaded/initialized before the requested class was verified as an `FTPFileEntryParser`. A non-parser class's static initializer could run due to remote-controlled input.
- Candidate cross-component path: remote FTP `SYST` response -> parser auto-detection -> classloader lookup/initialization -> type-assignability guard -> constructor side effects.
- Preliminary fit: **strong candidate** for tracing untrusted-input flow across FTP protocol handling, parser dispatch and Java class-loading behavior. Public fix is known; model exposure remains unknown.
- Screening status: **pending on the six-lead red-green run**. Not eligible until exact-test red/green artifact and independent human source review/adjudication pass.

### Lead HD-006 — Commons Text StringMatcher overload loses buffer window start

- Source PR: https://github.com/apache/commons-text/pull/768
- Exact revisions: pre-fix `a6cbba814422a06a0366468b2346f52aaacf8f3d`; fix `81de4f7a7c7d3b13d89edd72d4c4b92aa33e6c81` (one-commit comparison).
- Regression tests in the fixed revision's new `StringMatcherTest.java`: `testIsMatchCharSequencePassesBufferStartThrough`, `testIsMatchCharSequenceStartDelegatesThroughTheCorrectedOverload`, `testIsMatchOverloadsAgreeOnTheSameWindow`, and `testStringSubstitutorHandsACustomMatcherTheRealBufferStart`.
- Defect summary: the `CharSequence` default overload forwarded `bufferEnd` into the `bufferStart` argument, which could prevent custom prefix matchers from matching a valid window. The issue was observable through `StringSubstitutor`.
- Candidate cross-component path: `StringSubstitutor` scanning -> `StringMatcher` overload dispatch -> `CharSequenceUtils` conversion -> buffer-window contract -> placeholder replacement outcome.
- Preliminary fit: **promising integration/API-contract lead**; public fix is known and the main change is small, so independent reviewers must decide whether the component boundary is sufficiently substantive for CCDG.
- Screening status: **pending on the six-lead red-green run**. Not eligible until exact-test red/green artifact and independent human source review/adjudication pass.


### Lead HD-007 — Commons Net CR/LF command injection across protocol senders

- Source PR: https://github.com/apache/commons-net/pull/400
- Exact revisions: pre-fix `2a3aa71b077ae9290d9c3b95f6ad23b0e0a357c2`; fix `a07b6c41b5c2369506e7d86c4808dc51317e1481` (one-commit comparison).
- Regression tests from the fixed revision: `FTPTest#testRejectCRLFInArgs`, `NNTPTest#testRejectCRLFInArgs`, `POP3Test#testRejectCRLFInArgs`, and `SMTPTest#testRejectCRLFInArgs`.
- Defect summary: protocol command senders concatenated caller-controlled command arguments into control-channel text without rejecting carriage-return/line-feed characters. A supplied argument could add an unintended second protocol command.
- Candidate cross-component path: application-provided command/argument -> FTP/NNTP/POP3/SMTP sender -> control-channel command assembly -> protocol parser interprets a second command.
- Preliminary fit: **promising shared-invariant lead across four protocol implementations**. The four protocol targets come from one shared change and should count as one independent defect case, not four. Independent reviewers must decide whether the common mechanism is coherent enough for CCDG.
- Screening status: **pending in the next red-green run**. Not eligible until every named test fails before the fix and passes after it, then independent source review and adjudication pass.

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
- Discovery leads in this note: **7**; HD-001 through HD-006 have completed red-green artifacts in run [#38052846346](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38052846346), while HD-007 is pending screening.
- Calibration-only cases remain permanently excluded from held-out confirmation.
- No new model inference was run or authorized.

## Automated screening added (2026-10-10)

The separate workflow [Held-out Lead Red-Green Screening](https://github.com/MahmutVezir/dijitalikiz/actions/workflows/heldout-lead-red-green.yml) now tests the named regression tests against each pinned pre-fix and fixed commit. It performs source-build tests only and does not load or query any LLM. The original screening run [#38052390809](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38052390809) passed the first three leads, and the expanded six-lead run [#38052846346](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38052846346) passed all six. Every named test executed and failed on the pinned pre-fix revision, then passed on the pinned fixed revision without failure/error/skip. The corresponding artifact ZIP digests and per-test red/green results are SHA-256 pinned in [discovery_screening_audit.json](../data/followup_v2/discovery_screening_audit.json).

The workflow and its inference-safety test are in the research branch. The separate [Research Validation (No Inference) run #38052846291](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38052846291) passed 161 tests and historical artifact checks. The red/green artifacts provide revision-bound reproduction evidence, but they still do not replace independent human source review/adjudication. The pre-fix failures include the expected era mismatch/parse failure (Lang #1800), a hashCode mismatch (Lang #1807), wrong-successor / `NoSuchElementException` behavior (Collections #728), data-channel hostname-verifier omission (Net #404), class-initialization-before-type-check (Net #403), and buffer-window forwarding mismatch (Text #768). Each named test passed after its respective fix.

The sample-size sensitivity calculation is also documented in [SAMPLE_SIZE_SENSITIVITY_AUDIT_2026-10-10.md](SAMPLE_SIZE_SENSITIVITY_AUDIT_2026-10-10.md). Its key implication is that the 61-case target only reaches about 80% power under the current strong assumed discordance imbalance; modest alternatives require a larger independent-case pool.

