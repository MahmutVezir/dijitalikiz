# First-eight case scope and PR-lineage audit

**Audit date:** 2026-11-12  
**Cohort:** First 8 rows of the pinned SWE-rebench V2 96-project primary cohort.  
**Purpose:** Determine whether each linked upstream change is a software-defect correction suitable for the stated root-cause research question.  
**Execution boundary:** GitHub issue/PR metadata and patch path review only. No upstream source checkout, test execution, model inference, or training.

## Executive finding

The eight cohort instance IDs map to GitHub pull requests whose target base commits match the cohort's pinned `base_commit` exactly: **8/8 exact matches**.

However, the first eight are not eight eligible software-bug cases:
- **4 provisional bug candidates:** Dishka, earthkit-data, Nox, dbt-databricks.
- **4 exclude from the strict bug-root-cause primary pool:** ANTA (test-only correction), python-tuf (issue classified as enhancement), python-bigquery (feature request), Cloud SQL Python Connector (feature request).

This is an important cohort-quality finding. The 96-row deterministic cohort is a metadata-selected pool, not a set of confirmed bugs. A case must pass this semantic case-type screen before technical reproduction.

## Case-by-case results

| # | Instance / repository | Linked PR and issue | Base-commit match | PR change scope | Issue classification | Decision |
|---:|---|---|---|---|---|---|
| 1 | `aristanetworks__anta-956` — [aristanetworks/anta](https://github.com/aristanetworks/anta) | [PR #956](https://github.com/aristanetworks/anta/pull/956), [issue #953](https://github.com/aristanetworks/anta/issues/953) | Exact | 2 files; 11 additions / 4 deletions; both paths are under test code (`anta/tests/cvx.py`, `tests/units/anta_tests/test_cvx.py`); no production implementation path changed | Issue reports a test/device `KeyError`; PR adjusts the test command revision | **Exclude from primary bug-root-cause pool:** test-suite correction rather than a production-code defect fix |
| 2 | `reagento__dishka-436` — [reagento/dishka](https://github.com/reagento/dishka) | [PR #436](https://github.com/reagento/dishka/pull/436), [issue #435](https://github.com/reagento/dishka/issues/435) | Exact | 5 files; 155 additions / 37 deletions; implementation in `src/dishka/registry_builder.py` plus four unit-test paths | Issue label `bug`; reproducible incorrect provider override with explicit expected/actual value | **Retain provisionally** |
| 3 | `theupdateframework__python-tuf-2808` — [theupdateframework/python-tuf](https://github.com/theupdateframework/python-tuf) | [PR #2808](https://github.com/theupdateframework/python-tuf/pull/2808), [issue #2807](https://github.com/theupdateframework/python-tuf/issues/2807) | Exact | 3 files; 9 additions / 13 deletions; updater implementation, a test file, and an example path | Issue labels `enhancement` and `client`; requests creating absent metadata/artifact directories | **Exclude from strict bug pool:** classified as enhancement; retain provenance only |
| 4 | `ecmwf__earthkit-data-592` — [ecmwf/earthkit-data](https://github.com/ecmwf/earthkit-data) | [PR #592](https://github.com/ecmwf/earthkit-data/pull/592), [issue #571](https://github.com/ecmwf/earthkit-data/issues/571) | Exact | 5 files; 261 additions / 12 deletions; production Python modules and xarray attribute mapping plus a regression-test path | Issue label `bug`; single-variable GRIB-to-xarray conversion loses units | **Retain provisionally** |
| 5 | `googleapis__python-bigquery-2140` — [googleapis/python-bigquery](https://github.com/googleapis/python-bigquery) | [PR #2140](https://github.com/googleapis/python-bigquery/pull/2140), [issue #1996](https://github.com/googleapis/python-bigquery/issues/1996) | Exact | 6 files; 36 additions / 0 deletions; public API/implementation additions and tests | Issue label `type: feature request`; requests exposing `total_bytes_processed` | **Exclude from strict bug pool:** feature addition |
| 6 | `wntrblm__nox-922` — [wntrblm/nox](https://github.com/wntrblm/nox) | [PR #922](https://github.com/wntrblm/nox/pull/922), [issue #919](https://github.com/wntrblm/nox/issues/919) | Exact | 2 files; 51 additions / 25 deletions; `nox/virtualenv.py` and `tests/test_virtualenv.py` | Issue label `bug`; pyenv shim for `uv` causes Nox environment creation failure | **Retain provisionally** |
| 7 | `googlecloudplatform__cloud-sql-python-connector-1221` — [GoogleCloudPlatform/cloud-sql-python-connector](https://github.com/GoogleCloudPlatform/cloud-sql-python-connector) | [PR #1221](https://github.com/GoogleCloudPlatform/cloud-sql-python-connector/pull/1221), [issue #1217](https://github.com/GoogleCloudPlatform/cloud-sql-python-connector/issues/1217) | Exact | 2 files; 29 additions / 1 deletion; connector implementation and unit tests | Issue label `type: feature request`; requests new environment-variable support | **Exclude from strict bug pool:** feature addition |
| 8 | `databricks__dbt-databricks-995` — [databricks/dbt-databricks](https://github.com/databricks/dbt-databricks) | [PR #995](https://github.com/databricks/dbt-databricks/pull/995), [issue #994](https://github.com/databricks/dbt-databricks/issues/994) | Exact | 3 files; 19 additions / 2 deletions; adapter implementation, regression-test path, changelog | Issue label `bug`; temporary tables persist because generated names contain illegal identifier characters | **Retain provisionally**; direct cleanup-path test adequacy remains to be checked |

## Static regression-test review notes

The following is a limited static review of the PR file lists and patch structure, not a test-result claim:

- **Dishka:** added parameterized override tests exercise provider/factory overrides across scopes. The issue includes a compact reproducer and expected result.
- **earthkit-data:** the regression test adds checks for xarray dataset/data-array attributes, matching the reported loss of unit metadata. Confirm exact test sensitivity during the later test-adequacy stage.
- **Nox:** the PR changes the virtualenv implementation and virtualenv unit tests. During later static review, verify that the tests explicitly model the failed pyenv-shim command-discovery path, rather than only testing ordinary version parsing.
- **dbt-databricks:** the added tests check generated temporary-table suffix properties. The reported defect concerns the actual identifier used during cleanup/drop. Confirm that the target FAIL_TO_PASS test covers that cleanup path; otherwise reject the case as not defect-sensitive.

No test has been run here. “Retain provisionally” is a queue decision only, not acceptance as a validated experiment case.

## Why the cohort needs this second screen

The deterministic sampler stratified on metadata such as language, license signal, and repository diversity. It did not prove that every PR is a defect correction. In the first eight, half are clearly outside the strict bug-root-cause definition (and one more is a test-only correction). Therefore:

1. Do not report the 96 primary rows as 96 bug cases.
2. Do not use feature/enhancement PRs as bug cases merely because they have test patches or a `FAIL_TO_PASS` entry.
3. Keep excluded rows in the immutable cohort/provenance record, but mark them ineligible for the primary bug cohort.
4. Preserve predeclared inclusion rules for all subsequent batches; do not change the rule based on whether an individual case looks easy to reproduce.

## Current gate decision

- Exact instance-to-PR/base-commit mapping: **8/8 verified**.
- Root-level license screen from the separate first-eight license audit: **8/8 Apache-2.0 text at the selected base commit**.
- Strict bug-type screen: **4/8 provisionally retained; 4/8 excluded**.
- Accepted independent cases: **0**.
- Accepted independent upstream projects: **0**.
- Source/test gate: **closed** until the full case-specific source/license review, test-adequacy screen, exact environment reproduction, and independent human review are complete.
- No upstream source or tests were executed; no model inference or training occurred.

**Next bounded task:** Apply this same PR/base-commit/issue-type screen to cohort rows 9–16. Carry forward the first-eight eligibility rule unchanged. Only after the entire candidate pool has been semantically screened should we begin exact-environment test reproduction for candidates whose source licenses are fully cleared.
