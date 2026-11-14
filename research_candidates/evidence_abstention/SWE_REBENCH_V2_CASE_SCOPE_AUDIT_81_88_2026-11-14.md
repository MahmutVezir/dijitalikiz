# SWE-rebench V2 — cohort rows 81–88: PR scope and exact-base license audit

**Audit date:** 14 November 2026  
**Cohort:** 12 November 2026 tarihli sabit 96-proje primary cohort'un 81–88. satırları.  
**Audit scope:** Cohort metadata, GitHub PR/issue açıklamaları, exact PR base SHA, changed-file listeleri ve exact-base root LICENSE/NOTICE kayıtları. Upstream checkout, package installation, target-test execution, human adjudication, model loading, inference veya training yapılmadı.

## 1. Reproducibility inputs

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Immutable Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Primary cohort CSV: `SWE_REBENCH_V2_COHORT_96_PRIMARY_2026-11-12.csv`
- Primary CSV SHA-256: `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`
- Cohort manifest SHA-256: `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`
- GitHub Actions cohort artifact: run [43257277504](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43257277504), artifact ID `13960884569`.
- Retrieved ZIP SHA-256: `d9d1fc04cb84233c021006f13205623ea9aa390caa6eb54ca4bc9d974e9a4c6c`; ZIP CRC check passed.
- Primary CSV: 17,409 bytes, 96 rows; hash matches manifest. Manifest: 2,711 bytes; hash matches the frozen artifact.

All eight upstream PR base SHAs match their corresponding pinned cohort `base_commit` (**8/8**). This validates lineage alignment only; it does not prove a defect, reproduce a failure, or accept a study case.

## 2. Candidate-by-candidate findings

| Rank / cohort ID | PR / linked issue | PR base SHA | Exact-base root license | Scope decision |
|---:|---|---|---|---|
| 81 — `diaoul__subliminal-1218` | [subliminal #1218](https://github.com/Diaoul/subliminal/pull/1218) / [#1164](https://github.com/Diaoul/subliminal/issues/1164), [#1059](https://github.com/Diaoul/subliminal/issues/1059) | Match — `8178b85aa0c50b5dd9f642b8e862264ace3dda1e` | `LICENSE`, MIT; blob `1eb8f684cfa2b45c219ddf10734bfc8b1f59480e` | Conditional — issue #1164 is a bug, but PR also addresses #1059 enhancement and performs a broad scan refactor |
| 82 — `astanin__python-tabulate-362` | [python-tabulate #362](https://github.com/astanin/python-tabulate/pull/362) / [#305](https://github.com/astanin/python-tabulate/issues/305) | Match — `537d7b03932263062d37a7e747f19a385709b9f7` | `LICENSE`, MIT-style permission text; blob `81241eca637574fb696620b54200d28a0ff53524` | Strong defect candidate |
| 83 — `pyjanitor-devs__pyjanitor-1451` | [pyjanitor #1451](https://github.com/pyjanitor-devs/pyjanitor/pull/1451) / [#1449](https://github.com/pyjanitor-devs/pyjanitor/issues/1449) | Match — `e87628596c12c57b5df1229550f8bb16032bd6f5` | `LICENSE`, MIT; blob `4694fc3c4839f4480533bbdcc9b4943c768b35bb` | Exclude — explicitly proposed alias convenience API |
| 84 — `copier-org__copier-1998` | [Copier #1998](https://github.com/copier-org/copier/pull/1998) / [#1995](https://github.com/copier-org/copier/issues/1995) | Match — `6eaa0d7e0959c81479b214eaf73aa55d14d0364d` | `LICENSE`, MIT; blob `1092fead68c67a68c03f3536f15bebe2ce996326` | Strong defect candidate |
| 85 — `frictionlessdata__frictionless-py-1729` | [frictionless-py #1729](https://github.com/frictionlessdata/frictionless-py/pull/1729) / [#1728](https://github.com/frictionlessdata/frictionless-py/issues/1728) | Match — `6b72909ee38403df7c0245f408f3881bfa56ad6f` | `LICENSE.md`, MIT; blob `826e5fbb033fba9784e78d9b392a3053ad2bf6b2` | Exclude — request to add a new configurable capability |
| 86 — `packit__packit-2556` | [Packit #2556](https://github.com/packit/packit/pull/2556) / [#2451](https://github.com/packit/packit/issues/2451) | Match — `01c46e8e676d776337c89e7f0268ead9bfde26c4` | `LICENSE`, MIT; blob `d0ca04ff16ce581eec154c2d3b17051c8c990d17` | Conditional defect candidate — verify exact expected `--config` long-option alias; patch exposes `--config-path` |
| 87 — `matthewwithanm__python-markdownify-202` | [markdownify #202](https://github.com/matthewwithanm/python-markdownify/pull/202) / [#201](https://github.com/matthewwithanm/python-markdownify/issues/201) | Match — `5122c973c1a0d4351e64f02e2782912afbada9ef` | `LICENSE`, MIT; blob `b899f0c3796900f8d3893a366229e6835aca73bd` | Strong defect candidate |
| 88 — `drivendataorg__cloudpathlib-474` | [cloudpathlib #474](https://github.com/drivendataorg/cloudpathlib/pull/474) / [#472](https://github.com/drivendataorg/cloudpathlib/issues/472) | Match — `68774bf42bb8c3856ed0fc16c13c9652e82fb2ad` | `LICENSE`, MIT; blob `e04f62c957afb213dab7b399c0155bde7a19fcbb` | Conditional — valid Python 3.13 import/API compatibility failure, but broad 17-file compatibility update |

Root `NOTICE` files were not found at the eight pinned base commits. This root-level screen does not rule out nested notices, file-specific licenses, bundled third-party code or fixture obligations.

### Rank 81 — subliminal: insufficient GuessIt data is hidden without debug

Issue #1164 reports that “Insufficient data to process the guess” is hidden unless `--debug` is enabled; ordinary verbose output only shows a generic “1 error”. PR #1218 adds a `GuessingError` subtype and prints a useful message in verbose mode. It also closes #1059, an enhancement request for more verbose GuessIt details, and refactors video/archive scanning across seven files (+176/−75).

**Decision:** conditional. The issue-specific behaviour is a real observability defect, but the PR combines it with a separate enhancement and a broad scan-path refactor. The changed tests cover video/core behaviour, but the PR does not add a direct CLI-level regression assertion for the exact non-debug verbose message. Promote only after isolating the #1164 CLI behaviour and reproducing its output on the exact base/fixed revisions.

### Rank 82 — python-tabulate: boolean-looking strings and None crash when wrapping cells

Issue #305 provides a concrete failure: a string cell such as `"True"` is parsed as a Boolean before the text wrapper receives it; a `None` cell also cannot be reconstructed by calling its type. PR #362 changes the wrapped-cell path to use `str(cell)` and adds a regression test containing `"True"` and `None`.

**Decision:** retain as a strong defect candidate. Technical reproduction must pin tabulate and verify both reported input classes. Also add a small guard test for numeric/custom-format cells so that the general conversion change does not silently alter existing formatting semantics.

### Rank 83 — pyjanitor: Series alias method

Issue #1449 proposes a new `Series.alias` method that accepts a scalar or callable to rename the Series. PR #1451 introduces the method, registration, documentation, changelog entry and tests.

**Decision:** exclude. This is a new convenience API request, not a failure of an existing documented contract.

### Rank 84 — Copier: UTF-8 YAML data file fails on non-UTF-8 system defaults

Issue #1995 shows UTF-8 YAML data failing on systems whose default text encoding is not UTF-8 (example: CP932 on Japanese Windows). PR #1998 changes `Path.open()` from text mode to binary mode before passing the stream to PyYAML, which detects UTF-8/UTF-16 encodings. It adds parametrized regression tests for UTF-8, UTF-8-SIG, UTF-16LE and UTF-16BE while monkeypatching the system default to CP932.

**Decision:** retain as a strong defect candidate. Reproduction should preserve the issue's non-UTF-8 default-encoding condition and demonstrate the exact base-fail/fixed-pass behaviour.

### Rank 85 — frictionless-py: configurable pass_row for field_update functions

Issue #1728 requests that the `field_update` step support a `pass_row` parameter for custom transformation functions, analogous to existing formula behaviour. PR #1729 adds a new Boolean step parameter, passes it into the transform operation, and adds a positive example.

**Decision:** exclude. The linked issue asks for new functionality; there is no reported regression or incorrect output under the prior contract.

### Rank 86 — Packit: validate-config ignores the selected config path

Issue #2451 reports that `packit validate-config` ignores the `-c/--config` option and always looks for a config in the current directory. PR #2556 adds a Click option declared as `-c` / `--config-path`, passes it to `PackitAPI.validate_package_config`, and adds functional/API tests.

**Decision:** conditional defect candidate. The root problem is a valid CLI bug, but the patch's long option is `--config-path`, whereas the issue describes `--config`. Before acceptance, decide whether the intended contract requires `--config` specifically, and verify that exact alias on both revisions. The `-c` short option appears in the patch; a test using only `-c` would not settle the long-option discrepancy.

### Rank 87 — python-markdownify: inline <br/> loses word separation

Issue #201 shows that `<br />` in inline contexts such as headings and table cells becomes an empty string, producing joined text such as `foobar`. PR #202 changes inline conversion from an empty string to a space and adds direct heading and table-cell assertions.

**Decision:** retain as a strong defect candidate. The minimal example and patch align closely; technical reproduction must preserve inline context and expected separator output.

### Rank 88 — cloudpathlib: Python 3.13 removes private pathlib imports

Issue #472 reports ImportErrors for `_PathParents`, `posixpath`, and `_make_selector` after Python 3.13 changed pathlib internals. PR #474 adds Python 3.13 to the support/test matrix and adapts import paths, glob handling, path APIs and client methods. It changes 17 files (+371/−67), including a substantial vendored glob implementation.

The PR's history explicitly links Python 3.13 support to issue #472. Issue #479 is a later follow-up about remaining glob semantic parity and is not the issue fixed by PR #474.

**Decision:** conditional. The import incompatibility is a concrete environment-specific failure, but the patch covers a broad set of pathlib APIs and a large vendored implementation. A technical dossier must isolate at least one deterministic import/API failure on Python 3.13 at the pinned base and its corresponding fixed behaviour without conflating it with the separate #479 follow-up.

## 3. Aggregate outcome

| Check | Outcome |
|---|---:|
| Cohort rows audited | 8 |
| PR base SHA matches pinned cohort base | **8/8** |
| Exact-base root LICENSE file located | **8/8** |
| Root NOTICE file present | **0/8** |
| Strong defect candidates | 3 (82, 84, 87) |
| Conditional defect candidates | 3 (81, 86, 88) |
| Feature/API requests excluded | 2 (83, 85) |
| Accepted confirmatory cases added | **0** |
| Upstream target tests executed | **0** |
| Human evidence adjudications | **0** |
| Model inference / training | **0 / 0** |

A root LICENSE file and absence of a root NOTICE file are not complete legal clearance. Nested notices, third-party code, test data, generated files and per-file licensing still require review before any source redistribution. Dataset-level CC BY 4.0 does not override upstream source licensing.

## 4. Related earlier blocker closed: cohort row 64 / OceanParcels repository transfer

The prior 57–64 audit marked row 64 provisional because the source repository URL `OceanParcels/Parcels` redirected and the exact-base license check was not complete. The repository has since transferred to `Parcels-code/Parcels`; the PR is accessible there.

- Cohort ID: `oceanparcels__parcels-1723`
- PR: [Parcels #1723](https://github.com/Parcels-code/Parcels/pull/1723)
- Linked issue: [#1722 — backward-in-time outputs not written at desired frequency](https://github.com/Parcels-code/Parcels/issues/1722)
- Cohort base commit and PR base SHA both equal `a1f76d2f7ca4b50de874e61b752ec8ccaf50283e`.
- Exact-base license: `LICENSE.md`, MIT; blob `ad992e728bfe484b4e761b455a2d2adce29a0a7f`.
- Root `NOTICE`: not found.
- PR changes `parcels/particleset.py`, `pyproject.toml`, `tests/test_particlefile.py`, and `tests/test_particlesets.py`. The core patch changes backward-time callback scheduling to `starttime + callbackdt * np.sign(dt)` and adds forward/backward output-frequency tests, including time-varying fields.

**Decision:** close the repository redirect/base/root-license metadata blocker. Row 64 remains a defect *candidate*, not an accepted confirmatory case; source provenance, exact fail/pass execution and human adjudication are still required.

## 5. Next bounded work

1. Continue static scope/PR-base audit with cohort rows 89–96.
2. Complete outstanding exact-base LICENSE/NOTICE and changed-file provenance review for rows 17–56.
3. Technical reproduction priority from this tranche: 82, 84 and 87 first; 81, 86 and 88 only after their scope/contract caveats are resolved.
4. Do not install upstream packages or run target tests until changed-file provenance and relevant license/NOTICE conditions are reviewed.
5. Keep all candidates outside `CASE_REGISTRY.json` until exact base-fail/fixed-pass evidence, blinded human evidence adjudication, evidence-tier decisions and global preregistration/sample gates are complete.

**Conclusion:** This tranche improves cohort triage and closes the row-64 redirect metadata gap. The confirmatory registry remains empty and model inference remains prohibited.
