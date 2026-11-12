# SWE-rebench V2: first-eight source license and lineage audit

**Audit date:** 2026-11-12  
**Scope:** First 8 primary rows in the deterministic 96-project cohort. Metadata and repository-tree review only.  
**No upstream source checkout, test execution, model inference, or model training was performed.**

## Decision summary

- All 8 selected base commits resolve in GitHub and contain a repository-root license file.
- Each pinned root license file is an Apache License 2.0 text. The pinned file was fetched by immutable commit SHA, not from the current default branch.
- All 8 repositories report `fork=false` in GitHub repository metadata. The recursive trees are complete (`truncated=false`); no additional root/nested license or notice files matching the audit filename patterns were found beyond those listed below.
- This is **not final case-level legal clearance**. The license of every file actually used in a case, issue/PR text, vendored code, and relevant third-party components still needs review before source extraction or tests.
- `googleapis/python-bigquery` is currently marked archived by GitHub. This is a feasibility/maintenance flag, not an automatic legal disqualification.
- `googleapis/python-bigquery` and `GoogleCloudPlatform/cloud-sql-python-connector` are distinct repositories and neither is marked as a fork, but both are Google-associated projects. For conservative independence accounting, treat them as one organizational family until the project-level independence rule is finalized.
- The known BugsInPy exposure-exclusion set checked for this cohort was `keras-team/keras`, `pandas-dev/pandas`, `scrapy/scrapy`, and `tornadoweb/tornado`. None of the first eight repositories matches those names. This does **not** establish zero model pretraining or prior-publication exposure.

## Pinned repository audit

The SHA values below are GitHub Git blob object IDs (SHA-1 identifiers), **not SHA-256 checksums**. They identify the exact text object returned for the specified commit.

| # | Repository / instance | Selected base commit | Root license file at that commit | Git blob SHA-1 | Lineage / status |
|---:|---|---|---|---|---|
| 1 | [aristanetworks/anta](https://github.com/aristanetworks/anta) — `aristanetworks__anta-956` | `0efdd1cb598ff94f28241e2a2c244fff5dadf2d1` | [LICENSE](https://github.com/aristanetworks/anta/blob/0efdd1cb598ff94f28241e2a2c244fff5dadf2d1/LICENSE) — Apache-2.0 | `2e9460e9fcf5049efd3522ba58ab1ecb0aab8c6a` | `fork=false`; root `NOTICE` exists |
| 2 | [reagento/dishka](https://github.com/reagento/dishka) — `reagento__dishka-436` | `8718d5af93f9e48bc2506c64827663fdccc5ad89` | [LICENSE](https://github.com/reagento/dishka/blob/8718d5af93f9e48bc2506c64827663fdccc5ad89/LICENSE) — Apache-2.0 | `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `fork=false` |
| 3 | [theupdateframework/python-tuf](https://github.com/theupdateframework/python-tuf) — `theupdateframework__python-tuf-2808` | `8df9f0fd121fa6b9f4ca838570911001738f0dcf` | [LICENSE](https://github.com/theupdateframework/python-tuf/blob/8df9f0fd121fa6b9f4ca838570911001738f0dcf/LICENSE) — Apache-2.0 | `91e18a62b67551a4d427e2eaee0d33dcab94e141` | `fork=false`; separate [LICENSE-MIT](https://github.com/theupdateframework/python-tuf/blob/8df9f0fd121fa6b9f4ca838570911001738f0dcf/LICENSE-MIT) also exists (blob `096d0b9e2279c4cda1860dd65cfd547529626e20`); scope must be determined |
| 4 | [ecmwf/earthkit-data](https://github.com/ecmwf/earthkit-data) — `ecmwf__earthkit-data-592` | `ef3b9c47048c7cc7dd200f86efda1a66f60e2a36` | [LICENSE](https://github.com/ecmwf/earthkit-data/blob/ef3b9c47048c7cc7dd200f86efda1a66f60e2a36/LICENSE) — Apache-2.0 | `b43eff0798de10ffcd0bb7378f4d66bb27c02b70` | `fork=false`; `docs/licence.rst` repeats Apache-2.0 and states ECMWF does not waive its privileges and immunities |
| 5 | [googleapis/python-bigquery](https://github.com/googleapis/python-bigquery) — `googleapis__python-bigquery-2140` | `f8572dd86595361bae82c3232b2c0d159690a7b7` | [LICENSE](https://github.com/googleapis/python-bigquery/blob/f8572dd86595361bae82c3232b2c0d159690a7b7/LICENSE) — Apache-2.0 | `d645695673349e3947e8e5ae42332d0ac3164cd7` | `fork=false`; currently `archived=true` |
| 6 | [wntrblm/nox](https://github.com/wntrblm/nox) — `wntrblm__nox-922` | `97e0fad6a4036d610591a52e9ad0cfbe74a31af3` | [LICENSE](https://github.com/wntrblm/nox/blob/97e0fad6a4036d610591a52e9ad0cfbe74a31af3/LICENSE) — Apache-2.0 | `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `fork=false` |
| 7 | [GoogleCloudPlatform/cloud-sql-python-connector](https://github.com/GoogleCloudPlatform/cloud-sql-python-connector) — `googlecloudplatform__cloud-sql-python-connector-1221` | `dde235b0207b861e2a262964f35e7141885384ed` | [LICENSE](https://github.com/GoogleCloudPlatform/cloud-sql-python-connector/blob/dde235b0207b861e2a262964f35e7141885384ed/LICENSE) — Apache-2.0 | `d645695673349e3947e8e5ae42332d0ac3164cd7` | `fork=false`; Google-associated family with row 5 |
| 8 | [databricks/dbt-databricks](https://github.com/databricks/dbt-databricks) — `databricks__dbt-databricks-995` | `9e89d6ba3c6f894131df86fdd42ec93e9e71a3ad` | [License.md](https://github.com/databricks/dbt-databricks/blob/9e89d6ba3c6f894131df86fdd42ec93e9e71a3ad/License.md) — Apache-2.0 | `8dada3edaf50dbc082c9a125058f25def75e625a` | `fork=false` |

### Additional notices and license material found in the pinned trees

- **ANTA:** root `NOTICE` (blob `fbbee8d43b202fc64a8db51d90ed09c91dea2dd9`) identifies `aio-eapi` as included software and says it is also Apache-2.0. The project also has `.github/license-short.txt` (blob `787e7ab9da40ec46f67b8326f810510420907260`).
- **python-tuf:** in addition to the root Apache-2.0 `LICENSE`, a separate MIT license file exists. The files or subcomponents to which it applies must be mapped before using a specific case.
- **earthkit-data:** `docs/licence.rst` (blob `2ca0073db586c688ed9a08fe7b6d46843da37314`) repeats Apache-2.0 and includes an ECMWF privileges-and-immunities reservation. This does not itself establish a prohibition on research use; retain it as a legal-review note.

## Method and limits

1. Read the primary-cohort CSV and selected exact `base_commit` values.
2. Queried the GitHub repository API for `fork`, `parent`, `source`, and current `archived` metadata.
3. Queried each immutable commit's recursive Git tree. All eight trees returned `truncated=false`; license/notice filename matches are recorded above.
4. Fetched each root license file by the exact base commit. The file contents begin with “Apache License” and identify Version 2.0. The returned Git blob IDs are recorded above.
5. Compared repository names against the already-known BugsInPy overlap exclusions.

**Not done:** no upstream files were downloaded for execution; no patch/test content was inspected; no affected-file header audit; no dependency/SBOM audit; no third-party copyright clearance; no model-facing prompt material was assembled; no tests, inference, or training.

## Gate decision

- **Root-license screen:** 8/8 pass at the pinned repository root.
- **Lineage screen:** 8/8 report non-fork; Google-associated rows 5 and 7 are grouped conservatively for organization-level clustering.
- **Exposure screen:** no name overlap with the four known BugsInPy exclusion repositories; broader training-data exposure remains unknown.
- **Source/test gate:** **still closed**. Do not clone source for reproduction or run upstream tests until the next review maps case-specific files and patch paths to their applicable licenses, preserves all notices, and checks third-party components.
- **Candidate 5 (python-bigquery):** retain provisionally but flag current archived status for technical-feasibility review.
- **Candidate 3 (python-tuf):** retain provisionally but map the Apache/MIT split.
- **Candidate 4 (earthkit-data):** retain provisionally with the ECMWF reservation noted for legal review.

This is a reproducible technical screening note, not legal advice or a claim of complete reuse clearance.
