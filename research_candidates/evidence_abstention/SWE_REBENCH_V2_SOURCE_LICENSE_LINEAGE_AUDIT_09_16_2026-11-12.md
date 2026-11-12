# SWE-rebench V2 source license and repository-lineage audit: cohort rows 9–16

**Audit date:** 2026-11-12  
**Scope:** Primary cohort rows 9–16, using the exact pinned base commit from the 96-project cohort.  
**Method:** GitHub repository metadata, recursive Git trees, exact-commit root LICENSE/NOTICE files, and repository-transfer lineage.  
**Execution boundary:** No upstream source checkout, test execution, model inference, or training.

## Executive result

- All eight repositories resolve at their pinned base commits.
- Each recursive Git tree returned `truncated=false`.
- All eight exact-commit root license files identify Apache License 2.0.
- All eight current repository metadata records report `fork=false` and `archived=false`.
- Additional project-level notices were found for D-Wave (duplicate documentation license material) and EODAG (third-party software license inventory and test-fixture data provenance).
- FastMCP's dataset identity `jlowin/fastmcp` now resolves to the transferred/renamed `PrefectHQ/fastmcp` repository; the exact pinned PR base SHA still matches the cohort commit. It is not marked as a fork.
- The root-license screen is **8/8 pass**, but this is not case-level legal clearance. The actual changed files, their headers, dependencies, fixture provenance, and preservation of notices still need to be checked before reuse.

## Pinned license evidence

The IDs below are GitHub Git blob object IDs (SHA-1), not SHA-256 checksums. Each file URL pins the selected immutable cohort base commit.

| # | Repository / cohort instance | Pinned base commit | Exact root license | Git blob SHA-1 | GitHub lineage metadata |
|---:|---|---|---|---|---|
| 9 | [getmoto/moto](https://github.com/getmoto/moto) — `getmoto__moto-8296` | `bf49e22f41be7444dc20e05dfa5dd13f25672eba` | [LICENSE](https://github.com/getmoto/moto/blob/bf49e22f41be7444dc20e05dfa5dd13f25672eba/LICENSE) — Apache-2.0 | `90a85e7149454f173dd595bdeb884340cc01e6f6` | `fork=false`; `archived=false` |
| 10 | [dwavesystems/dwave-system](https://github.com/dwavesystems/dwave-system) — `dwavesystems__dwave-system-554` | `1bb84c6e73513c66f31dc4bee06aeab6b9e6743d` | [LICENSE](https://github.com/dwavesystems/dwave-system/blob/1bb84c6e73513c66f31dc4bee06aeab6b9e6743d/LICENSE) — Apache-2.0 | `661333e8305241693ea37bad4da2144287fd83cc` | `fork=false`; `archived=false` |
| 11 | [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp) — cohort alias `jlowin__fastmcp-164` | `059c0889fdf16b7dfa53e84f08034c3ac914e4a6` | [LICENSE](https://github.com/PrefectHQ/fastmcp/blob/059c0889fdf16b7dfa53e84f08034c3ac914e4a6/LICENSE) — Apache-2.0 | `f49a4e16e68b128803cc2dcea614603632b04eac` | `fork=false`; `archived=false`; repository transferred/renamed |
| 12 | [pyro-ppl/numpyro](https://github.com/pyro-ppl/numpyro) — `pyro-ppl__numpyro-1918` | `07e4c9bc4524cc0a741ba8f8ad41339d34a0288d` | [LICENSE.md](https://github.com/pyro-ppl/numpyro/blob/07e4c9bc4524cc0a741ba8f8ad41339d34a0288d/LICENSE.md) — Apache-2.0 | `d645695673349e3947e8e5ae42332d0ac3164cd7` | `fork=false`; `archived=false` |
| 13 | [dpkp/kafka-python](https://github.com/dpkp/kafka-python) — `dpkp__kafka-python-2544` | `1bd6573b30ddf896b6110be227906c67d1ee5205` | [LICENSE](https://github.com/dpkp/kafka-python/blob/1bd6573b30ddf896b6110be227906c67d1ee5205/LICENSE) — Apache-2.0 | `412a2b630bac63250b65e8e14e20451759a0d8ed` | `fork=false`; `archived=false` |
| 14 | [PennyLaneAI/pennylane](https://github.com/PennyLaneAI/pennylane) — `PennyLaneAI__pennylane-6738` | `8d33455821351e8aba8631173e5adc87847c59d5` | [LICENSE](https://github.com/PennyLaneAI/pennylane/blob/8d33455821351e8aba8631173e5adc87847c59d5/LICENSE) — Apache-2.0 | `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `fork=false`; `archived=false` |
| 15 | [OpenMDAO/dymos](https://github.com/OpenMDAO/dymos) — `openmdao__dymos-1165` | `3efd1035c3bf62890034eb9e07de543f3d117867` | [LICENSE](https://github.com/OpenMDAO/dymos/blob/3efd1035c3bf62890034eb9e07de543f3d117867/LICENSE) — Apache-2.0 | `55da29e11b1fb2465936598779085f1cbcdf2908` | `fork=false`; `archived=false` |
| 16 | [CS-SI/eodag](https://github.com/CS-SI/eodag) — `CS-SI__eodag-1536` | `b7cc06e19025e5bbf14e28a0975f1749e21e9be3` | [LICENSE](https://github.com/CS-SI/eodag/blob/b7cc06e19025e5bbf14e28a0975f1749e21e9be3/LICENSE) — Apache-2.0 | `1a9893b43e8e6d46ff5cda60ab6562850b7f78ff` | `fork=false`; `archived=false` |

## Additional license and notice material

### D-Wave System
The pinned tree contains:
- root `LICENSE` (Apache-2.0);
- `docs/LICENSE`, also Apache-2.0 (blob `ea5b60640b01f74e295037aa8a6b7d4ea278a739`);
- `docs/license.rst`, which includes `docs/LICENSE` (blob `71e7788c912861094084be9007a1c40f7d9e70bd`).

The documentation license is a duplicate/reference, not a different license. No other root/nested files matching the audit's LICENSE/NOTICE/COPYING filename patterns were found in the complete pinned tree.

### Kafka Python
The pinned tree contains:
- root `LICENSE` (Apache-2.0);
- `docs/license.rst`, which explicitly points to Apache License v2.0 and the root license (blob `f419915bdc3a3f171131f5ab83195481390e759a`).

This is consistent documentation, not a second license regime.

### EODAG
The pinned tree contains root `LICENSE` (Apache-2.0), root `NOTICE`, and `tests/resources/NOTICE`.

- Root `NOTICE` (blob `9f763bc3c2f90854b8209ce60e23c8fc03c6ec7e`) records third-party components under Apache-2.0, MIT, BSD-2-Clause, BSD-3-Clause, and Python Software Foundation licenses. It also identifies a modified Django `slugify` function as BSD-3-Clause.
- `tests/resources/NOTICE` (blob `9a89f4ad6a39bb16c03fa6b6a2b149f050cc259d`) attributes several test-resource files to external catalogues and data providers, and notes a modified Sentinel product sample with a link to its legal notice.
- The selected PR #1536 changes `eodag/config.py`, `eodag/resources/user_conf_template.yml`, and `tests/units/test_core.py`; it does not change the listed external fixture files. Nevertheless, if any such fixtures are copied into our evidence packets or redistributed, their data/catalogue terms need a separate check.
- The PR patch also adds `StacListAssets` to a config branch in `eodag/config.py`, in addition to correcting the `geodes_s3` key. This is a potentially separate change-scope element; preserve it in the case dossier and have the reviewers decide whether the benchmark task still has one unambiguous target root cause.

### FastMCP repository transfer
The benchmark alias `jlowin/fastmcp` currently resolves to `PrefectHQ/fastmcp`. The cohort base commit `059c0889fdf16b7dfa53e84f08034c3ac914e4a6` is the exact base SHA reported by PR #164 in the transferred repository. The pinned root LICENSE at that SHA is Apache-2.0. GitHub currently reports the repository as `fork=false`, `archived=false`. Record both names in provenance; do not silently rewrite the original dataset row.

## Audit method

1. Used the exact `base_commit` values for cohort rows 9–16.
2. Queried each current upstream repository record for fork/archive/owner/license metadata.
3. Retrieved each exact commit's recursive Git tree. All eight trees were complete (`truncated=false`).
4. Fetched the root license text by the immutable base commit and recorded the Git blob SHA.
5. Inspected additional matching license/notice paths and checked D-Wave/Kafka documentation license files and EODAG's two NOTICE files.
6. No source checkout, test, build, package install, model inference, or training was performed.

## Decision

- Exact root license screen: **8/8 Apache-2.0**.
- Fork/archive screen: **8/8 not forks; 8/8 not archived**.
- Additional notice handling: D-Wave and Kafka documentation license references recorded; EODAG third-party and test-data notices require preservation/relevance review.
- Case-level reuse clearance: **not granted by this screen**.
- Upstream source/test gate: **still closed** until affected-file and dependency/license scope is checked and the candidate's test is shown to be defect-sensitive.
- No accepted cases are added by this document.

This is a technical license/provenance screen, not legal advice or complete clearance for redistribution.
