# SWE-rebench V2 — cohort rows 65–72: PR scope and exact-base license audit

**Audit date:** 14 November 2026  
**Cohort:** 12 November 2026 tarihli sabit 96-proje primary cohort'un 65–72. satırları.  
**Denetim sınırı:** Cohort metadata, GitHub PR/issue kayıtları, exact PR base SHA, değişen dosyalar ve exact-base root license dosyaları. Upstream checkout, paket kurulumu, target-test çalıştırma, insan adjudication, model yükleme, inference veya training yapılmadı.

## 1. Reproducibility inputs

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Immutable Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Primary cohort CSV: `SWE_REBENCH_V2_COHORT_96_PRIMARY_2026-11-12.csv`
- Primary CSV SHA-256: `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`
- Cohort manifest SHA-256: `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`
- GitHub Actions artifact: run [43257277504](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43257277504), artifact ID `13960884569`.
- Retrieved ZIP SHA-256: `d9d1fc04cb84233c021006f13205623ea9aa390caa6eb54ca4bc9d974e9a4c6c`; ZIP CRC check passed. CSV and cohort manifest hashes matched the expected values above.

For all eight rows, the upstream PR's reported base SHA matches the cohort row's pinned `base_commit` (**8/8**). This confirms lineage alignment; it does not demonstrate a defect, a valid reproducer, or case acceptance.

## 2. Candidate-by-candidate findings

| Rank / cohort ID | Upstream PR / issue | PR base SHA | Exact-base root license | Scope decision |
|---:|---|---|---|---|
| 65 — `mikedh__trimesh-2312` | [trimesh #2312](https://github.com/mikedh/trimesh/pull/2312) / [#2311](https://github.com/mikedh/trimesh/issues/2311) | Match — `6ed17ba4656b2f71ba45228e9a91fc1f8ae09f00` | `LICENSE.md`, MIT; blob `d0571124dc68ee63553001f17f043d19250159cc` | **Hold** — issue fix is present, but PR is a broad release/multi-change patch |
| 66 — `litestar-org__polyfactory-728` | [polyfactory #728](https://github.com/litestar-org/polyfactory/pull/728) / [#725](https://github.com/litestar-org/polyfactory/issues/725) | Match — `f270b0fb46f36b32db0a1c9f9d2cea25c59b8f22` | `LICENSE`, MIT; blob `4e58f77a5603d469b738db232743e40442dbc96d` | Defect candidate |
| 67 — `pyccel__pyccel-2038` | [Pyccel #2038](https://github.com/pyccel/pyccel/pull/2038) / [#2008](https://github.com/pyccel/pyccel/issues/2008) | Match — `9f7fb7c2d65c6da8b11135f83786b85c7833c06a` | `LICENSE`, MIT; blob `c0ab7b3df1a3bfa5e517814fb50ec5893b55586b` | Defect candidate |
| 68 — `pydap__pydap-481` | [pydap #481](https://github.com/pydap/pydap/pull/481) / [#480](https://github.com/pydap/pydap/issues/480) | Match — `6cdd01733fdbdbea34cf1f42b73d0f754e34e0ab` | `LICENSE`, MIT; blob `1d1d5dee4535556acf7a22fccba6c805735be59d` | **Exclude** — API naming/consistency migration, not a demonstrated defect |
| 69 — `python-attrs__attrs-1417` | [attrs #1417](https://github.com/python-attrs/attrs/pull/1417) / [#1416](https://github.com/python-attrs/attrs/issues/1416) | Match — `19943b775d40c018e844f2cb1728442f58112a3b` | `LICENSE`, MIT; blob `2bd6453d255e19b973f19b128596a8b6dd65b2c3` | **Conditional candidate** — PR test does not reproduce the full inherited-subclass issue example |
| 70 — `stingraysoftware__stingray-858` | [Stingray #858](https://github.com/StingraySoftware/stingray/pull/858) / [#857](https://github.com/StingraySoftware/stingray/issues/857) | Match — `137d17d9934705d01c50cf767f7f76415b970d44` | `LICENSE.rst`, MIT; blob `65e96d540a71f3f93ffd92c933d829fe9afa96e8` | Defect candidate |
| 71 — `softlayer__softlayer-python-2214` | [softlayer-python #2214](https://github.com/softlayer/softlayer-python/pull/2214) / [#2114](https://github.com/softlayer/softlayer-python/issues/2114) | Match — `8b3459767f1cd725f0358d50e677beb00f45b124` | `LICENSE`, MIT-style permission/disclaimer text; blob `e6da618307d35f88c314ca175e5fa9054970b2d4` | Defect candidate; preserve exact license text for legal review |
| 72 — `pypa__virtualenv-2907` | [virtualenv #2907](https://github.com/pypa/virtualenv/pull/2907) / [#2870](https://github.com/pypa/virtualenv/issues/2870) | Match — `07e61107546b5a867df4d4f9b633968621226e55` | `LICENSE`, MIT-style permissive text; blob `be9700d61a3a0e9f5c6a74f93d187f1805c7acbf` | Defect candidate |

### Rank 65 — trimesh: widget import failure, embedded in a broad release PR

Issue #2311 reports an `ImportError`: `geometry_hash` had been renamed to `_geometry_hash`, while `trimesh/viewer/widget.py` still imported the old name. PR #2312 directly updates that import and call site, so the reported issue has a matching patch.

However, the PR is titled “Release: Boolean Tests”, changes 12 files (+307/−277), and also changes boolean-engine selection, moves iteration utilities, adds XAML meter units, alters Docker/test dependency setup, and updates package metadata/versioning. The issue-specific fix is therefore embedded in a multi-topic release patch. No dedicated regression test for the widget import is added in the PR's changed tests.

**Decision:** retain the provenance record, but hold this row out of the clean confirmatory candidate pool. Reconsider only if the exact import failure can be isolated as a single-task dossier with a separately validated base/fixed reproducer.

### Rank 66 — polyfactory: unsupported Pydantic ForwardRef

Issue #725 reports that a Pydantic `JsonValue` annotation becomes `ForwardRef('JsonValue')` and raises `ParameterException: Unsupported type` in polyfactory 2.22.0, although the example worked in 2.21.0. PR #728 adds ForwardRef detection and explicit resolution; the Pydantic factory maps `JsonValue` to `str` for Pydantic v2+, and tests recursive/forward-reference handling.

**Decision:** retain as a defect candidate. Technical reproduction must pin the issue's Pydantic/polyfactory versions and run the issue's minimal example on the exact base and fixed revisions.

### Rank 67 — Pyccel: alias assignment semantics for mutable containers

Issue #2008 shows that after `b = a`, mutating `b` does not update `a` as Python list reference semantics require; generated C and Fortran differ from Python behavior. PR #2038 changes semantic alias handling, C/Fortran pointer/deallocation code, and adds list, set, and dictionary regression examples.

**Decision:** retain as a defect candidate. Reproduction must verify the same alias/mutation behavior separately for the supported code-generation targets; a compiler/setup failure is not a target defect.

### Rank 68 — pydap: DAP2/DAP4 dimension API consistency

Issue #480 describes different dimension attribute names on `BaseType` between DAP2 and DAP4 and proposes making the interfaces consistent. PR #481 renames the `BaseType` constructor/property from `dimensions` to `dims`, changes the default representation, and updates protocol/parser/response code and tests.

The issue does not document a failure or incorrect result under the existing DAP2 contract. The patch is primarily an API consistency migration, with compatibility implications for callers using `dimensions`.

**Decision:** exclude from the root-cause defect sample. Do not treat an API harmonization request as a confirmed bug merely because the linked PR is closed.

### Rank 69 — attrs: generator-valued field_transformer

Issue #1416 reports a TypeError when subclassing an attrs class after a generator-valued `field_transformer` is supplied. PR #1417 converts the transformer's result to a tuple before later processing and adds a generator regression test.

The code change is plausibly aligned with the root cause. However, the PR test checks a simple base class and does not recreate the issue's full inherited-subclass minimal example.

**Decision:** retain conditionally. Before promotion to technical reproduction, create a test dossier preserving the exact issue MCVE, including the subclass and constructor call; confirm the same failure/pass pair at the pinned revisions.

### Rank 70 — Stingray: one GTI yields duplicate outputs

Issue #857 reports that `FITSTimeseriesReader.apply_gti_lists()` returns two event lists for a single GTI input. PR #858 restructures the single-file and multi-GTI branches, normalizes GTI input with `np.asarray`, and adds parametrized tests for same/one/multiple GTI inputs, file-output mode, and empty entries.

**Decision:** retain as a defect candidate. Technical reproduction must demonstrate the one-GTI cardinality failure on the exact base and the expected single output after the patch.

### Rank 71 — softlayer-python: empty datacenter lookup causes TypeError

Issue #2114 shows the order command receiving an empty datacenter response; `location_dc` becomes `None`, then `location_dc.get('name')` raises a TypeError. PR #2214 guards the optional result before checking closed pods and adds a mocked empty-datacenter regression test that expects the command's proper `SoftLayerError`, rather than the accidental TypeError.

**Decision:** retain as a defect candidate. Technical reproduction must use the empty lookup response and verify the user-visible error path at both revisions. Keep the exact root permission text with the case dossier; metadata's MIT label alone is not a complete legal clearance.

### Rank 72 — virtualenv: missing absolute interpreter path blocks fallback

Issue #2870 documents that `virtualenv -p /missing/path -p python3.9 dest` raises `FileNotFoundError` instead of continuing to the second valid interpreter. PR #2907 changes the missing-path `OSError` handling to continue discovery and adds two tests: a missing absolute path followed by a valid interpreter succeeds, while a single missing absolute path still fails.

**Decision:** retain as a defect candidate. Technical reproduction must preserve both the fallback-success and no-valid-interpreter failure conditions.

## 3. Aggregate outcome and remaining gates

| Check | Outcome |
|---|---:|
| Rows audited | 8 |
| PR base SHA matches pinned cohort base | **8/8** |
| Exact-base root license file located | **8/8** |
| Clear defect candidates for next technical reproduction queue | 5 (66, 67, 70, 71, 72) |
| Conditional defect candidate | 1 (69) |
| Scope hold pending single-task isolation | 1 (65) |
| API consistency migration excluded from defect sample | 1 (68) |
| Root `NOTICE` files present | 0/8 |
| Accepted confirmatory cases added | **0** |
| Upstream target tests executed | **0** |
| Human root-cause/evidence adjudications | **0** |
| Model inference / training | **0 / 0** |

The absence of a root `NOTICE` file does not establish that no nested notices, third-party code, file-level licenses, fixtures, or attribution obligations exist. The root-license screen is not full legal clearance. Changed-file provenance, all nested license/notice paths, dataset permissions, and any required authorizations still need review before source reuse.

## 4. Next bounded work

1. Continue cohort scope/PR-base review with rows 73–80.
2. Complete exact-base license, NOTICE, and changed-file provenance review for rows 17–56; resolve row 64's repository redirect/base/license gap.
3. For rows 66, 67, 70, 71, and 72, prepare isolated reproducibility dossiers. Add row 69 only after its exact inherited-subclass MCVE is represented.
4. Do not run upstream target tests until the relevant license/provenance gate is complete.
5. Keep every candidate outside `CASE_REGISTRY.json` until buggy-fail/fixed-pass evidence, independent Panel A/Panel B review, evidence-tier adjudication, and all global preregistration/sample gates are complete.

**Conclusion:** This audit advances cohort triage only. The confirmatory registry remains empty and model inference remains prohibited.
