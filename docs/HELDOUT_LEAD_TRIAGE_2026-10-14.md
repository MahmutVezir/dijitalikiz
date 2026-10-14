# Additional held-out candidate triage — 2026-10-14

**Status: preliminary source/diff triage only. No case is admitted. No model inference is authorized.**

This note extends candidate discovery without changing the existing 12-lead technical-screening audit, the calibration-only seven-case pool, the frozen historical experiments, or `data/followup_v2/protocol_manifest.json`.

## Additional leads reviewed at the source-patch level

| Candidate | Provisional promise | Key test targets | Main quality question |
|---|---|---|---|
| [Netty #17623](https://github.com/netty/netty/pull/17623) | **Strong** — negative DNS cache entry must not suppress later search-domain resolution | `testNegativelyCachedSearchDomainDoesNotShadowPositiveOne`; `testNegativelyCachedSearchDomainDoesNotShadowUncachedOne`; `testNegativelyCachedBareHostnameStillShortCircuits` | Does the ground truth correctly separate negative caching, resolver cache probing, and the fallback search-domain ladder? |
| [Netty #17764](https://github.com/netty/netty/pull/17764) | **Strong** — TLS 1.3 server key selection must follow client signature algorithms for the chosen provider | `connectWithEd25519`; `connectWithEd25519AndRsa`; `connectWithEd25519FailsWithoutCommonSignatureAlgorithm` | Verify provider/JDK prerequisites and that the diagnosis captures negotiation semantics rather than test-certificate setup. |
| [Commons Collections #724](https://github.com/apache/commons-collections/pull/724) | **Strong** — iterator removal must keep an auxiliary MultiMap index consistent with the backing collection | `IndexedCollectionTest#testIteratorRemoveUpdatesIndex` | Is the collection/index dependency sufficiently cross-component, with a single coherent root cause? |
| [Commons Collections #720](https://github.com/apache/commons-collections/pull/720) | **Moderate** — inherited `forEach` must respect the synchronized decorator lock | `SynchronizedCollectionTest#testForEachHoldsLock` | May be too close to a synchronization-contract boundary; reviewers may exclude it from the primary pool. |
| [Commons Lang #1795](https://github.com/apache/commons-lang/pull/1795) | **Moderate** — mutable `TimeZone` reference leaks through cached date parser/formatter instances | `FastDateFormatTest#testTimeZoneArgumentIsCopied`; `FastDateFormatTest#testTimeZoneGetterReturnsCopy`; `FastDateParserTest#testTimeZoneIsCopied` | Avoid clustering this with other date/time defects and verify the cache–parser–formatter mechanism. |
| [Commons Compress #797](https://github.com/apache/commons-compress/pull/797) | **Moderate** — LZ77 back-reference offsets must not exceed the retained sliding-window size | `AbstractLZ77CompressorInputStreamTest#testBackReferenceOffsetLargerThanWindowIsRejected` | The test targets a shared decoder primitive; reviewers must establish a defensible caller/state path rather than a same-method boundary only. |

The machine-readable register `data/followup_v2/lead_triage_register_2026-10-14.json` records the proposed pre-fix/fixed revision pins, named tests, rationale, and open caveats. Pinning was tightened to use each merged fix commit's first parent as pre-fix and the merge commit as fixed revision; the original PR-head SHA remains separately recorded for provenance. In this triage, “strong/moderate” describes preliminary source-patch promise, **not** confirmed eligibility or independent ground truth.

## Why these are not yet benchmark cases

1. **Technical reproduction is not complete here.** Each lead must pass the repository's strict pre-fix-failure/fixed-pass workflow with the same regression-test patch hash on both revisions.
2. **No independent source review is recorded.** Two reviewers must independently assess exact source revisions, tests, one coherent root cause, affected components, and every proposed dependency edge; a separate adjudicator must resolve disagreements.
3. **The leads are not interchangeable independent units by default.** One shared defect spanning several protocols or decoder callers remains one case. Closely related defect families should not be over-represented.
4. **The frozen checkpoint is from 2024; these candidate fixes merged in 2026.** That makes exact exposure to these later fixed patches less plausible, but does not establish absence of training leakage: pre-fix code or related bug patterns may have been present. Risk must be described conservatively.
5. The seven scoring-calibration cases remain excluded from the held-out confirmatory set. These six leads are not added to `case_pool_manifest.json`, and no gate booleans are changed.

## Reserved and excluded alternatives

- [Commons Net #406](https://github.com/apache/commons-net/pull/406) is reserved because ambient-locale date parsing is closely related to the existing Lang #1800 lead.
- [Commons Compress #800](https://github.com/apache/commons-compress/pull/800) is reserved because it is in the same Pack200/unpack neighborhood as an existing #805 lead.
- [Commons Collections #719](https://github.com/apache/commons-collections/pull/719) is reserved to avoid over-representing collection-view/state-sync mechanisms while #694 and #724 are under review.
- [Commons Lang #1812](https://github.com/apache/commons-lang/pull/1812) is excluded from this primary triage because its PR explicitly discloses Claude Code assistance. This is a conservative case-selection rule, **not** a claim that the 2024 model was trained on that 2026 PR.
- [Commons Compress #806](https://github.com/apache/commons-compress/pull/806) is deferred because its apparent mechanism may be a single-component constructor boundary unless a broader dependency path is shown.

## Required next gates

- Run strict red/green tests for candidate leads and archive the hashes/artifacts.
- Complete independent source reviews and adjudication.
- Build a source-grounded scoring calibration set and meet the predeclared rater-reliability thresholds.
- Continue finding diverse new held-out defects; do not claim 61 eligible cases until adjudicated case records actually exist.
- Freeze the three-condition context-parity audit, tokenizer-length/hash audit, randomized schedule, analysis, and protocol before new inference.
- Keep all historical raw records and scores immutable.
