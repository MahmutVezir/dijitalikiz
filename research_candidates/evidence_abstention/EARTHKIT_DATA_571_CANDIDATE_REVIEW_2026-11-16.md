# ecmwf/earthkit-data issue #571 — candidate review

**Cohort rank:** 4 of 96 primary candidates  
**Linked pull request:** https://github.com/ecmwf/earthkit-data/pull/592  
**Issue:** https://github.com/ecmwf/earthkit-data/issues/571  
**PR base:** `ef3b9c47048c7cc7dd200f86efda1a66f60e2a36`  
**PR head:** `8459c5e27704e849e7d6a4c3a9bbd78052a6cbd8`  
**Merge commit:** `1fdabaa46c3e8af46f026d07a15a1262b8a812a6`  
**Review status:** defect/patch alignment plausible; Stage 2 is BLOCKED pending exact dataset-row authentication and external GRIB fixture provenance, immutability, and license review. Not reproduced. Not an accepted case.

## 1. Reported defect and patch contract

Issue #571 reports that converting a GRIB source to xarray with a single variable can lose the `units` metadata, while a multi-variable conversion retains units. The report uses the `earthkit.data.from_source(..., "cds", ...)` path and compares the resulting xarray attributes.

PR #592 changes the `UniqueAttrBuilder` path. Before the fix, a unique metadata key could be collected as a global attribute, then removed from each variable's attributes by `adjust_attrs(drop_keys=global_attrs.keys())`. The builder also explicitly removed `units` from global attributes. The patch adds a `CFAttrs` lookup loaded from a new `cf_attrs.yaml`, removes keys that cannot be global under the declared CF attribute-use rules before variable attributes are adjusted, and therefore leaves `units` on the variable.

This source-level mechanism is consistent with the reported symptom. It is a static code analysis only; it is not an executed reproduction.

## 2. Pinned source identity and issue scope

- Repository: `ecmwf/earthkit-data`
- Issue #571 created: `2024-12-16T15:26:42Z`; closed: `2025-01-22T15:51:49Z`
- PR #592 created: `2025-01-22T14:40:06Z`; merged: `2025-01-22T14:52:37Z`
- PR base and head are recorded above.
- Changed files:
  - `src/earthkit/data/readers/grib/xarray.py`
  - `src/earthkit/data/utils/xarray/attrs.py`
  - `src/earthkit/data/utils/xarray/cf_attrs.yaml`
  - `src/earthkit/data/utils/xarray/engine.py`
  - `tests/xr_engine/test_xr_engine.py`

The source change is broader than the single visible failing attribute: it introduces a CF attribute catalogue and changes how unique/global attributes are classified. Stage 2 must show that the chosen target selector specifically detects the single-field units defect, rather than merely passing because unrelated behavior changed.

## 3. Regression test and fixture provenance blocker

The fixed PR adds/changes `test_xr_engine_single_field`. The test loads:

`earthkit_remote_test_data_file("test-data/xr_engine/level/pl.grib")`

The pinned PR source helper defines:

`_REMOTE_TEST_DATA_URL = "https://get.ecmwf.int/repository/test-data/earthkit-data/"`

and joins the supplied path to that root. Thus the test depends on an external GRIB file at:

`https://get.ecmwf.int/repository/test-data/earthkit-data/test-data/xr_engine/level/pl.grib`

The test then selects one field (`ds_ek[0]`) and asserts that the resulting variable has `standard_name`, `long_name`, and `units == "K"`.

This fixture is not stored in the source repository at the pinned test path, and the current candidate packet has not yet established:
1. an immutable fixture snapshot or content SHA-256;
2. the fixture's originating repository and provenance;
3. its applicable data license/terms and permission to retain or redistribute it in an evidence artifact;
4. that the same fixture bytes can be used for both the exact buggy base and fixed revision without remote mutation.

Do not download/execute upstream tests or include the fixture in an artifact until those checks are documented. A synthetic local fixture could be considered only if it preserves the exact test oracle and is independently shown to reproduce the defect; it must not silently replace the dataset's required test selector.

## 4. Source and dependency license screen

- Exact-base root `LICENSE` blob: `b43eff0798de10ffcd0bb7378f4d66bb27c02b70`; text is Apache License 2.0.
- Exact-base `pyproject.toml` blob: `9d4beb6eda92280614f326169deb8b351261f6e2`; project metadata declares Apache License 2.0.
- Exact-base `src/earthkit/data/utils/xarray/attrs.py` blob: `2515016fc87a65d0df0ea7361d3d8dc3fa9f759d`.
- Fixed `attrs.py` blob: `6762fd003bfa25692c32154461e390b966678493`.
- Fixed `cf_attrs.yaml` blob: `03767eb3bdca92b729c7ba546b12e7bdd829209d`.
- Exact-base direct runtime dependencies include `array-api-compat`, `cfgrib`, `dask`, `earthkit-meteo`, `eccodes`, `entrypoints`, `filelock`, `jinja2`, `jsonschema`, `lru-dict`, `markdown`, `multiurl`, `netcdf4`, `pandas`, `pdbufr`, `pyyaml`, `tqdm`, and `xarray`. The exact reproduction dependency subset is not yet frozen.

The new `cf_attrs.yaml` says it is based on CF Conventions Appendix A, but it contains no source version, source commit, attribution block, or license reference. The CF Conventions project currently states that its conventions document is dedicated to the public domain under CC0; however, the exact upstream specification revision and provenance used to create this particular YAML copy have not yet been identified. Do not treat the current project-level declaration as retrospective legal clearance for this copied file.

This review is not legal advice and does not grant blanket clearance for the full dependency tree, optional extras, GRIB data, external services, or redistribution.

## 5. Stage 2 decision

| Gate | Current evidence | Status |
|---|---|---|
| Issue/patch alignment | Issue symptom and source diff are consistent | Plausible, static only |
| Exact base/fix pins | PR API base/head commits recorded | Pass for source identity |
| Dataset row identity and selectors | Cohort scope audit links the row to PR #592; exact Parquet row, canonical row hash, and selectors not yet archived here | Open |
| Defect-specific test | `test_xr_engine_single_field` asserts variable `units == "K"` | Static test found |
| Fixture provenance and immutability | External ECMWF fixture; no frozen bytes/hash or terms record | BLOCKED |
| Changed-file source provenance | `cf_attrs.yaml` lacks pinned CF source revision and rights record | BLOCKED |
| Exact environment and dependencies | Full dependency metadata visible; minimal lock not produced | Open |
| Base-fail / fixed-pass logs and artifact | No candidate-specific reproduction run or raw artifact | NOT RUN |

**Stage 2 result:** BLOCKED — no source execution and no reproduction claim. Do not begin Stage 3 gold/tier adjudication until the test fixture, dataset selector, and source provenance gates are resolved and the same defect-specific test demonstrates buggy-base failure and fixed-revision pass.

## 6. Exposure, independence, and acceptance

- One case maximum for `ecmwf/earthkit-data`; any other candidate row from this repository is a replacement, not an independent case.
- The researcher has reviewed this issue and its patch during candidate screening; perfect blinding must not be claimed.
- Model-family release chronology alone cannot prove absence from the model's training data; exact training-data cutoff/provenance is not established.
- Related-defect clustering, repository lineage/fork checks, prior pipeline/debug exposure classification, and final case acceptance remain open.
- Accepted case count remains unchanged. Model loading and inference remain unauthorized.

## 7. Next bounded action

Resolve the external GRIB test-data origin, exact fixture bytes/hash, license/retention terms, and the historical source/version for the CF attribute catalogue. Then authenticate the exact Parquet row and selectors. Only after those gates pass may an isolated Stage 2 workflow be run on the exact buggy base and fixed revision.
