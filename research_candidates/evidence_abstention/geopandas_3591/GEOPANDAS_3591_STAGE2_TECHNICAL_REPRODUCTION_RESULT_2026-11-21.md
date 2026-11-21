# GeoPandas #3591 — Stage 2 technical reproduction result

**Result:** `PASSED — technical base/fix reproduction`  
**Run completed:** 2026-11-21T18:29:30Z  
**Local time:** 2026-11-21 21:29:30 Europe/Istanbul  
**Frozen cohort rank:** 52  
**Dataset instance:** `geopandas__geopandas-3591`  
**Project lead authorization:** `PROJECT_LEAD_STAGE2_EXECUTION_AUTHORIZATION_2026-11-21.md`

## 1. Scope and pinned upstream revisions

- Repository: `geopandas/geopandas`
- Issue / PR: [#3590](https://github.com/geopandas/geopandas/issues/3590) / [#3591](https://github.com/geopandas/geopandas/pull/3591)
- Buggy base: `c36eba059f6170715b63a9aa065817c64025d263`
- Fixed revision: `b3259ce23a37abd32650d7df098f3cdc8c4bb261`
- Frozen selector: `geopandas/tests/test_geodataframe.py::TestConstructor::test_geometry_nan_scalar`
- Frozen row SHA-256: `e543af0bbc5e779661c3b1b79c28849f67dee7c61157c000c6698b15ba1218e2`
- Frozen problem-statement SHA-256: `c4aeb4909495887c065f1f7ae5ec0e321fb350e98ea789cde3f931cad597f12d`

The upstream base-to-fix comparison authenticated exactly three changed paths:
1. `CHANGELOG.md` — four-line release note for GeoPandas 1.1.1, explicitly referencing fix #3591; not runtime or test code.
2. `geopandas/geodataframe.py` — source fix.
3. `geopandas/tests/test_geodataframe.py` — regression tests.

Source identities:
- Base constructor blob: `1a607cbb5baea0c3ddc50b03042734c44b7945da`
- Fixed constructor blob: `243d98759878754975e1b8b1732cfb503dd1bf0a`
- Fixed test file blob: `61eac57b37d9b0550a8b7d97f603a03d82725d28`
- Base CHANGELOG blob: `f3cc885587583b6badcf8cb67e9303d3ac2aae04`
- Fixed CHANGELOG blob: `56554d4f7a07cddd51abaf9170dfa08462e9f1ac`
- Base-to-fix patch SHA-256: `45073898f1fb0ec51ec7e8b7e17fffb2dfb6be1c9510cdfc35c23ed574990640`

## 2. Environment

- Runner: Ubuntu 22.04 / GitHub-hosted runner, Linux x86_64
- Python: `3.11.9`
- NumPy: `1.26.4`
- pandas: `2.2.3`
- Shapely: `2.1.1`
- pyproj: `3.7.1`
- pyogrio: `0.11.0`
- pytest: `8.3.5`
- pip: `25.1.1`
- setuptools: `80.9.0`
- wheel: `0.45.1`

The full environment was installed from `reproduction/geopandas_3591/requirements.lock`. The observed `pip freeze --all` exactly matched the lock after excluding only the editable GeoPandas checkout line. `pip check` reported: `No broken requirements found.`

## 3. Reproduction results

The exact frozen constructor input was used on both revisions:

```python
GeoDataFrame(
    data=[[np.nan, np.nan]],
    columns=["geometry", "something"],
    crs="EPSG:4326",
)
```

### Buggy base

- Commit: `c36eba059f6170715b63a9aa065817c64025d263`
- Independent reproducer: **PASS — expected defect reproduced**
- Observed exception: `ValueError`
- Exact message begins: `Assigning CRS to a GeoDataFrame without a geometry column is not supported.`

The frozen pytest selector was not run on base because that selector was added by the fix PR and is not present in the buggy revision. The base-side test therefore used the same frozen input in the independent reproducer rather than silently substituting or editing an upstream test.

### Fixed revision

- Commit: `b3259ce23a37abd32650d7df098f3cdc8c4bb261`
- Independent reproducer: **PASS — expected fixed behavior observed**
- Resulting shape: `(1, 2)`
- Active geometry: `geometry`
- Geometry value: `None`
- CRS: `EPSG:4326`
- Exact frozen pytest selector: **1 passed in 0.16s**

This is a technical base-fail / fixed-pass reproduction for the frozen input and the fixed-revision regression selector.

## 4. GitHub Actions run and evidence integrity

- Workflow run: [44935740419](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44935740419)
- Job: `136941838630` — `geopandas-3591-stage2`
- Run conclusion: `success`
- Research branch head used: `73d35f7f6e94337ba24c99568a582a1fdcfa8ea6`
- Artifact: [geopandas-3591-stage2-44935740419.zip](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44935740419/artifacts/14719727030)
- Artifact ID: `14719727030`
- Artifact size: `6816 bytes`
- Artifact SHA-256: `bc807d9c1bdec02e72c61783d9f3e8a5640574fd620fd0da5de2ec4468a1894e`

The artifact was downloaded independently after upload:
- Local outer SHA-256 matched the GitHub artifact digest.
- ZIP CRC check: **PASS**.
- Archive members: **18**.
- Internal `SHA256SUMS` entries: **17/17 PASS**.

The artifact contains sanitized execution outputs, pinned-environment details, source provenance, raw reproducer logs, the fixed pytest log and the SHA-256 index. Upstream source files, full test fixture contents, and the frozen dataset row/problem statement were not copied into the artifact.

## 5. Execution attempts and corrections

The following runs stopped before completing technical tests; none is counted as a Stage 2 result:

| Run | Failure point | Resolution |
|---|---|---|
| `44935393890` | Source change-set check initially omitted the release-note path. | Authenticated the exact base/fixed CHANGELOG blob identities and included the release-note-only path. |
| `44935451603` | Same change-set mismatch. | Same exact source-scope correction. |
| `44935659230` | Editable install used the upstream clone's default branch instead of the pinned base checkout; after correcting checkout, freeze comparison exposed package-name casing. | Install from the exact base commit and canonicalize the Pygments distribution name. |

The successful run above passed all source, environment, base reproduction, fixed reproduction, pytest, evidence-index and upload steps.

## 6. Disposition and boundaries

- Stage 2 technical reproduction: **PASSED**.
- Approved gold mechanism remains: `G1_NONEMPTY_ALL_NULL_FLOAT_GEOMETRY_SKIPS_AUTO_COERCION`.
- Approved semantic tiers remain: **E3 ABSTAIN / E2 ABSTAIN / E1 ANSWER**.
- Candidate status remains: **HOLD** pending separate final case-acceptance and remaining documentary/license-scope review.
- Final case acceptance: **not decided / not accepted**.
- v0.2 accepted-case registry: unchanged.
- Model loading: **not performed**.
- Model inference: **not performed**.
- Fine-tuning or training: **not performed**.

This report records technical reproducibility only. It is not final case acceptance, legal clearance, a blinded adjudication, inter-rater reliability evidence, or authorization for model inference.
