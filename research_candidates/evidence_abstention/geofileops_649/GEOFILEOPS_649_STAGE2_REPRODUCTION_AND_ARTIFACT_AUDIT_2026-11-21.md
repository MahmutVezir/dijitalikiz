# GeofileOps #649 / issue #648 — Stage 2 reproduction and artifact audit

**Date:** 21 November 2026  
**Candidate:** geofileops/geofileops issue #648 / PR #649  
**Dataset instance:** `geofileops__geofileops-649`  
**Status:** STAGE 2 EXACT-BASE / FIXED-REVISION REPRODUCTION PASSED; ARTIFACT INDEPENDENTLY VERIFIED; STAGE 3 / ACCEPTANCE PENDING

## 1. Frozen upstream and dataset provenance

- Issue: https://github.com/geofileops/geofileops/issues/648
- Fix PR: https://github.com/geofileops/geofileops/pull/649
- Issue created: `2025-03-06T14:07:54Z`.
- PR created: `2025-03-06T15:39:28Z`.
- Exact buggy base: `f7f8a4cf49b1278f3e9e5f4157718de441a21b57`.
- Exact fixed PR head: `ec1438fbf8527269cd1193647d05c8d7fdb83802`.
- Merge commit: `d475d6d2ec5719c7f00d1e441e1cdbe0765087b7`.
- Exact buggy-base source blobs: `geofileops/fileops.py` `9edeb1c1bf7eb7d0f35b246611b27bad33fdcc7e`; `tests/test_geofile.py` `52047a77a384dc2f469029c50be4775f5ee1eae4`; `LICENSE.txt` `ecf40d7a30bd534ebd781bca089abd3168bc13a1`.
- Exact fixed source blobs: `geofileops/fileops.py` `29738ee57088279b7bf7c656b34721dbc8d78f7b`; `tests/test_geofile.py` `64cd2ab90f37c9f53672388ce0b0ee4112a2104f`.
- SWE-rebench dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`.
- Whole Parquet file SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`.
- Canonical row: `geofileops__geofileops-649`; repository `geofileops/geofileops`; `base_commit` equals the exact buggy base; `created_at` `2025-03-06 15:39:28`; row license `BSD-3-Clause`.
- Canonical row SHA-256: `2a85246a15d97ca6e73eb9a02f36022a05f80b8322c24a6522fbfee31fc7d1eb`.

## 2. Frozen FAIL_TO_PASS selectors

The authenticated row contains **10 selectors**. They represent one candidate, not 10 independent cases:

1. `tests/test_geofile.py::test_append_different_columns[.csv]`
2. `tests/test_geofile.py::test_copy_layer[polygon-parcel-.gpkg-.gpkg-None]`
3. `tests/test_geofile.py::test_copy_layer[polygon-parcel-.gpkg-.gpkg-XYZ]`
4. `tests/test_geofile.py::test_copy_layer[polygon-parcel-.shp-.gpkg-None]`
5. `tests/test_geofile.py::test_copy_layer[polygon-parcel-.shp-.gpkg-XYZ]`
6. `tests/test_geofile.py::test_copy_layer[polygon-parcel-.csv-.gpkg-None]`
7. `tests/test_geofile.py::test_copy_layer[polygon-parcel-.csv-.gpkg-XYZ]`
8. `tests/test_geofile.py::test_copy_layer[curvepolygon-.gpkg-.gpkg-None]`
9. `tests/test_geofile.py::test_copy_layer[polygon-parcel-.gpkg-.gpkg.zip-None]`
10. `tests/test_geofile.py::test_copy_layer_layer[None]`

The selector set covers both public operations named by the issue (`copy_layer` and `append_to`), several source formats, a compressed GeoPackage target, and the default `dst_layer=None` behavior.

## 3. Reproduction environment and provenance

- Runtime: Python `3.11.9` on `linux-64`.
- The environment was created from `research_candidates/evidence_abstention/reproduction/geofileops_issue_648/environment.yml` using `setup-micromamba`.
- The exact resolved Conda package set was captured in `conda-explicit.txt` in the artifact. The environment file constrains the supported dependency ranges, while this explicit export records the actual resolution used for this run; it is not claimed to be a pre-existing historical lock from the original PR CI.
- Python distribution license metadata and PyArrow dataset-extraction license metadata are captured in the artifact. Metadata for packages that do not expose Python distribution metadata is recorded as unavailable rather than inferred.
- Root source license: BSD 3-Clause. Dataset row license: BSD-3-Clause. This is provenance evidence, not legal clearance for every transitive/native dependency or redistribution.

Source provenance hashes are recorded in `source-provenance-sha256.txt` for upstream `LICENSE.txt`, `setup.py`, `pyproject.toml`, the full PR patch and the frozen dataset-test patch.

## 4. Independent reproducer results

The independent reproducer is `research_candidates/evidence_abstention/reproduction/geofileops_issue_648/test_issue_648.py`.

- `test_copy_layer_default_destination_layer_uses_destination_stem`: **fails on the exact buggy base**, observing `source_layer` rather than `destination_result` for a destination file named `destination_result.gpkg`.
- `test_copy_layer_explicit_destination_layer_is_preserved`: **passes on the exact buggy base**, confirming that an explicitly supplied `dst_layer` is honored.
- The same two tests: **2 passed on the exact fixed PR head**.

These tests establish the behavior independently of the frozen test module and distinguish default handling from explicit-layer handling.

## 5. Frozen selector results

- Exact buggy base: **10/10 selectors failed**.
- Exact fixed revision: **10/10 selectors passed**.

Failure modes on the base:
- The nine `copy_layer` selectors report that the output layer name remains the source layer/source stem (for example `parcels` or `polygon-parcel_31370_None`) rather than the destination file stem.
- The `append_to` CSV selector reports a GDAL CSV layer creation error while creating/updating `dst.csv`; on the exact fixed revision the same selector passes. This is consistent with the missing destination-layer fallback: the CSV destination is not given its intended `dst` layer name.

The CSV failure was not discarded as an unrelated environment failure: it is part of the frozen `append_to` selector, occurs on the exact buggy source, and changes to a passing test on the exact fixed source under the captured runtime. The other nine selectors independently show direct layer-name mismatches.

## 6. Workflow and artifact

- Workflow run: `44916663456` — https://github.com/MahmutVezir/dijitalikiz/actions/runs/44916663456
- GeofileOps job: `136883732286`.
- Artifact ID: `14711502949` — https://github.com/MahmutVezir/dijitalikiz/actions/runs/44916663456/artifacts/14711502949
- Artifact SHA-256 recorded by GitHub: `b4b408170b3fcae7c305d060f0cc283fcf912e964403a9eb1015b1209e60553f`.

Independent artifact verification:
- Downloaded archive SHA-256 recomputed locally: matches GitHub's digest exactly.
- ZIP CRC: PASS (`ZipFile.testzip()` returned `None`).
- Archive members: 19.
- `SHA256SUMS.txt`: 18 internal entries, **18/18 passed**.

## 7. Stage 2 disposition

**Stage 2 technical reproduction: PASS.** The exact upstream base builds, independent default-layer reproducer fails as expected, explicit-layer positive control passes, the frozen Parquet row is authenticated, all 10 selectors fail on base, and the same 10 selectors pass on the exact fixed revision. The independent reproducer also passes both tests on fixed.

Stage 2 success does not by itself accept the candidate for the primary abstention sample. E3/E2/E1 adjudication, source-exposure declaration, temporal acknowledgement, human license/notice review, bounded scope acknowledgement, schema validation and separate final acceptance remain open.

No model was loaded; no inference, fine-tuning or training was performed.