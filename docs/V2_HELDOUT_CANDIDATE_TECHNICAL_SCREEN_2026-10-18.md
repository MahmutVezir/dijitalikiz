# V2 held-out candidate technical screen — 18 October 2026

**Purpose:** Preserve the technical screening evidence for six new candidate leads. This is not an admission list, independent source adjudication, scorer calibration, or permission to run model inference.

**Canonical CI run:** https://github.com/MahmutVezir/dijitalikiz/actions/runs/39135614105  
**Screening type:** exact pre-fix/fixed-revision regression-test reproduction only; no LLM inference, training, GPU or Kaggle job.  
**Candidate admissions into V2:** **zero** as of this note. The V2 protocol manifest remains draft and inference-disabled.

| Candidate | Pre-fix SHA | Fixed SHA | Targeted regression | Technical result | Evidence artifact |
|---|---|---|---|---|---|
| Netty #17623 — negative DNS search-domain cache | `de7fa8997db278b83f56b22f89b691be58ae88ba` | `1addbf90c4fd35713c61e5c54ad4d21c14d7df1d` | `DnsNameResolverTest#testNegativelyCachedSearchDomainDoesNotShadowPositiveOne`; `...DoesNotShadowUncachedOne`; baseline control `...testNegativelyCachedBareHostnameStillShortcircuits` | **Red/green passed.** Defect-specific tests failed before and passed after; baseline control was required to pass at both revisions. | [artifact 12139437962](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39135614105/artifacts/12139437962) |
| Commons Compress #797 — LZ77 back-reference window bound | `4a17b64939b782a5e95c5aecfd583b631cb58522` | `cebee156fe66578b5142b4176e6c408a76d65c0c` | `AbstractLZ77CompressorInputStreamTest#testBackReferenceOffsetLargerThanWindowIsRejected` | **Red/green passed.** | [artifact 12139554127](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39135614105/artifacts/12139554127) |
| Commons Collections #724 — iterator removal leaves stale index | `3ff49116a265817f7546f72052e3d0478c159e62` | `651a6218910a906dc50415c145d63ba06c07a659` | `IndexedCollectionTest#testIteratorRemoveUpdatesIndex` | **Red/green passed.** | [artifact 12139891101](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39135614105/artifacts/12139891101) |
| Commons Collections #720 — synchronized collection forEach lock | `d58a5e3a1258877bd94ba79db9f8a5f90892624b` | `6ee9dd78c79f367dd8e3e1655e4664bcec960ad6` | `SynchronizedCollectionTest#testForEachHoldsLock` | **Red/green passed.** | [artifact 12139452931](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39135614105/artifacts/12139452931) |
| Commons Lang #1795 — mutable TimeZone leaking through formatter/parser cache | `d235f1e997523d7a3d9d1c63e9a1853c2ab728fd` | `117a9ea791b87af1b90413fa8290891ca3106cfd` | `FastDateFormatTest#testTimeZoneArgumentIsCopied`; `FastDateFormatTest#testTimeZoneGetterReturnsCopy`; `FastDateParserTest#testTimeZoneIsCopied` | **Red/green passed.** | [artifact 12139891280](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39135614105/artifacts/12139891280) |
| Netty #17764 — TLS 1.3 signature-algorithm key selection | `3eaff63caf06a582cc3df72422aa1124734b46c6` | `84c167ea85e0d7f5b40caec6cab859018f9490bd` | `PkiTestingTlsTest#connectWithEd25519`; `#connectWithEd25519AndRsa`; `#connectWithEd25519FailsWithoutCommonSignatureAlgorithm` | **Blocked.** The pre-fix run executed 7 tests with 0 failures, 0 errors and 0 skipped; it did not demonstrate the target regression. Source inspection explains the gap: the fixed revision's `ed25519Providers()` removes `SslProvider.OPENSSL` when `OpenSsl.isBoringSSL()` is false ([pinned test source](https://github.com/netty/netty/blob/84c167ea85e0d7f5b40caec6cab859018f9490bd/handler/src/test/java/io/netty/handler/ssl/PkiTestingTlsTest.java#L129-L136)), while the earlier `connectWithEd25519()` implementation hardcodes the JDK provider in the pre-fix test file. The workflow did not establish that a BoringSSL/OpenSSL-backed Ed25519 test executed against the pre-fix implementation. Do not call this a pass or a scientific disproof. Keep the case blocked until retained runtime evidence records `OpenSsl.isBoringSSL() == true`, shows that the targeted test invocation actually selected `SslProvider.OPENSSL` (rather than only running the JDK provider), and demonstrates a target-specific pre-fix failure followed by a fixed-revision pass under the same relevant test configuration. An environment label alone is not proof that the OpenSSL path executed. | [artifact 12138943916](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39135614105/artifacts/12138943916) |

## What remains before any candidate can be admitted

Each candidate still requires: upstream license and provenance review; duplicate/related-defect check against historical and calibration cases; source-level root-cause evidence from pinned revisions; a meaningful cross-component dependency path with evidence for every directed edge; contamination-risk assessment; two independent locked source reviews; and a separate adjudicator's evidence-based decision. The review records must be kept apart from model-facing prompts.

The five passing regression checks establish only that the named test differentiates the pinned revisions for the tested scenario. They do **not** establish that the defect is suitable for the graph-representation research question or that any dependency edge/gold diagnosis is correct. The seven earlier calibration candidates remain permanently excluded from the V2 confirmatory set.

Do not change `data/followup_v2/protocol_manifest.json` to frozen or enable inference merely because this screen passed. Populate the held-out case list only after independent review and adjudication have actually been completed and recorded.


## Preliminary repository license and NOTICE snapshot

The repository-level license and NOTICE files were fetched from both exact pinned revisions for each upstream project, not only from current default branches. All six candidates currently resolve to repositories carrying an Apache License 2.0 text at `LICENSE.txt`; this is a preliminary provenance observation, not a legal opinion or completed redistribution review.

| Upstream project | License file path / content blob SHA | NOTICE file content blob SHA | Pre-fix and fixed revisions checked |
|---|---|---|---|
| Netty | `LICENSE.txt` / `62589edd12a37dd28b6b6fed1e2d728ac9f05c8d` | `21367472ae93ec2e7e2fc2998589023498b0ef18` | `de7fa8997db278b83f56b22f89b691be58ae88ba` → `1addbf90c4fd35713c61e5c54ad4d21c14d7df1d`; TLS candidate `3eaff63caf06a582cc3df72422aa1124734b46c6` → `84c167ea85e0d7f5b40caec6cab859018f9490bd` |
| Commons Compress | `LICENSE.txt` / `b447376016c314574ee4d4b3d3ebd6eaf2972f07` | `1ea0233f17311a323af013e11b803d17a2c93019` | `4a17b64939b782a5e95c5aecfd583b631cb58522` → `cebee156fe66578b5142b4176e6c408a76d65c0c` |
| Commons Collections | `LICENSE.txt` / `ff9ad4530f5716304e042cbac72cecd7c40f0e0e` | `8c3e93e4e86beb91f07001380fbec5253e2f5010` | `3ff49116a265817f7546f72052e3d0478c159e62` → `651a6218910a906dc50415c145d63ba06c07a659`; `d58a5e3a1258877bd94ba79db9f8a5f90892624b` → `6ee9dd78c79f367dd8e3e1655e4664bcec960ad6` |
| Commons Lang | `LICENSE.txt` / `ff9ad4530f5716304e042cbac72cecd7c40f0e0e` | `246f39cc1d176c5995115d98b19ef45e35374731` | `d235f1e997523d7a3d9d1c63e9a1853c2ab728fd` → `117a9ea791b87af1b90413fa8290891ca3106cfd` |

### Limit of this check

The identical upstream license/NOTICE blobs across pinned revisions support that the repository-level notices were stable for these pins. Before a case can be admitted or any third-party source content is redistributed in a bundle, reviewers must still inspect relevant source-file headers, vendored/dependency notices, patch provenance and whether the intended research use/redistribution complies with upstream terms. The project should prefer minimal facts, hashes and upstream links over copying unnecessary upstream code or discussion text into public archives. This check does not resolve contamination risk or complete source/root-cause adjudication.
