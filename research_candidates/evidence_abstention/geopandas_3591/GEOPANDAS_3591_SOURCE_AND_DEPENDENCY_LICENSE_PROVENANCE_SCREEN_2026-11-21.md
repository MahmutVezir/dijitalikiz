# GeoPandas #3591 — source, dataset and dependency license/provenance screen

**Date:** 21 November 2026  
**Scope:** Documentary source/license and artifact-provenance screen for the already completed GeoPandas #3591 Stage 2 reproduction  
**Disposition:** **No source-license conflict identified for the GeoPandas code used in the technical experiment; binary-wheel and public-comment redistribution questions remain open. This is not legal clearance.**

## 1. Boundary: what this screen did and did not change

This is a research-side audit note only. It does not alter:
- the frozen SWE-rebench dataset revision, row, problem statement, patch, test patch or selector;
- the E3/E2/E1 source-packet manifests or their approved tier decisions;
- the Stage 2 reproducer, dependency lock, executed workflow, test results or checksums;
- the exploratory registry, sample size, candidate ranking or inference gate.

No model was loaded and no inference, fine-tuning or training was performed. The GeoPandas candidate remains **HOLD** pending its separate final case-acceptance decision. Nothing in this note grants inference or redistribution permission.

## 2. Dataset license versus source-repository license

These are two separate layers and must not be conflated.

### Dataset layer

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Pinned revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Frozen instance: `geopandas__geopandas-3591`
- Canonical row SHA-256: `e543af0bbc5e779661c1b79c28849f67dee7c61157c000c6698b15ba1218e2`
- Problem-statement SHA-256: `c4aeb4909495887c065f1f7ae5ec0e321fb350e98ea789cde3f931cad597f12d`
- Dataset-wide license shown by its publisher: **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
- The dataset schema defines the per-row `license` field as the SPDX identifier for the underlying source repository, and the dataset description explicitly instructs users to respect each task repository's license.

Official dataset reference: https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified

### Source-repository layer

The exact row identifies `geopandas/geopandas` and declares `BSD-3-Clause`. I independently inspected the upstream source at both the exact buggy base and fixed PR commit:

| Item | Buggy base | Fixed PR commit |
|---|---|---|
| Commit | `c36eba059f6170715b63a9aa065817c64025d263` | `b3259ce23a37abd32650d7df098f3cdc8c4bb261` |
| Root license path | `LICENSE.txt` | `LICENSE.txt` |
| Root license Git blob SHA-1 | `028603be2080134aa4817ed691fec3f449ffa609` | `028603be2080134aa4817ed691fec3f449ffa609` |
| `pyproject.toml` Git blob SHA-1 | `7e423f8efebdcdf2f11e71ca9aff4ff31b3edf8a` | `7e423f8efebdcdf2f11e71ca9aff4ff31b3edf8a` |
| Project declaration | `license = { text = "BSD 3-Clause" }` | unchanged |

The base and fixed source therefore share the same root BSD-3-Clause license file and project license declaration. The PR's exact changed paths are:
1. `geopandas/geodataframe.py` — implementation change;
2. `geopandas/tests/test_geodataframe.py` — regression tests;
3. `CHANGELOG.md` — a four-line release note for the fix.

The source and test files do not carry separate file-level license headers in their leading lines; the repository-level license is the relevant source license identified by the exact upstream tree. The PR does not modify the license file or project license declaration.

**Finding:** the technical source patch is within a BSD-3-Clause project. Preserve the BSD copyright notice, conditions and disclaimer when distributing source or substantial source-derived material. The dataset's CC BY 4.0 attribution requirement is a separate requirement for the dataset material itself. Neither label replaces the other.

Upstream source references:
- Base license: https://github.com/geopandas/geopandas/blob/c36eba059f6170715b63a9aa065817c64025d263/LICENSE.txt
- Base project metadata: https://github.com/geopandas/geopandas/blob/c36eba059f6170715b63a9aa065817c64025d263/pyproject.toml
- Fixed license: https://github.com/geopandas/geopandas/blob/b3259ce23a37abd32650d7df098f3cdc8c4bb261/LICENSE.txt
- Fixed implementation: https://github.com/geopandas/geopandas/blob/b3259ce23a37abd32650d7df098f3cdc8c4bb261/geopandas/geodataframe.py
- Fixed regression tests: https://github.com/geopandas/geopandas/blob/b3259ce23a37abd32650d7df098f3cdc8c4bb261/geopandas/tests/test_geodataframe.py

## 3. Public issue/PR discussion snapshots

The frozen E3 evidence remains the authenticated dataset row/problem-statement identity only. Later source discussion is kept separate:
- E2 snapshot: `source_snapshots/E2_ISSUE_DISCUSSION_SOURCE_SNAPSHOT_V0_1.json`, current Git blob `575c1780e0ae48a50c43d5f0f595f7fa4cc3908b`; records three issue comments with author, permalink, timestamp and body hash.
- E1 snapshot: `source_snapshots/E1_PR_REVIEW_SUGGESTION_SOURCE_SNAPSHOT_V0_1.json`, current Git blob `149c70763e08de292002d5217e86e033ad291e50`; records the one PR review suggestion with author, permalink, timestamp and body hash.
- E3 reference: `source_snapshots/E3_FROZEN_ROW_AUDIT_REFERENCE_V0_1.json`, current Git blob `3f6af0d8ae8a708ae76bd65cbafa74bfe6013f39`; contains row/provenance hashes and explicitly says it is not the raw row payload.

The GitHub issue/PR bodies are user-contributed text. The snapshots record provenance, but they do not record an explicit open-source license granted by each commenter. The research repository is public and no project-wide license is declared for it by GitHub. Therefore:
- do not describe the comment snapshots as MIT/BSD/CC-licensed source code;
- keep the author, date and canonical upstream permalink with any necessary quotation;
- do not repackage the full comment bodies as generally redistributable source material without a separate rights review;
- do not rewrite the frozen E1/E2/E3 source packets as part of this audit.

Upstream permalinks:
- https://github.com/geopandas/geopandas/issues/3590#issuecomment-2943137874
- https://github.com/geopandas/geopandas/issues/3590#issuecomment-2944863844
- https://github.com/geopandas/geopandas/issues/3590#issuecomment-2945606056
- https://github.com/geopandas/geopandas/pull/3591#discussion_r2130293780

## 4. Exact Stage 2 environment observed

The successful GitHub Actions run used Ubuntu 22.04, CPython 3.11.9 and these exact locked distributions. The run log identifies the Linux x86-64 wheel tags for the five compiled packages listed below. The environment was not copied into the evidence ZIP as binaries.

| Distribution | Version | Declared/package license | Source/licensing note |
|---|---:|---|---|
| `geopandas` (editable exact upstream checkout) | 1.1.0 | BSD-3-Clause | Exact upstream `LICENSE.txt` and `pyproject.toml` checked above. |
| `certifi` | 2025.6.15 | MPL-2.0 | Exact source tag's `LICENSE` blob: `62b076cdee58ec8f34034141ba0befd9015b0c7e`; package includes a modified CA root bundle. |
| `iniconfig` | 2.1.0 | MIT | Exact source tag `v2.1.0`; `LICENSE` blob: `46f4b2846fd708ecb81b2d665434ce6379aa1101`. |
| `numpy` | 1.26.4 | BSD-3-Clause | Exact source tag `v1.26.4`; `LICENSE.txt` blob: `014d51c98dfaea666c7d7729333214843e258be4`. The exact tag's wheel build config selects OpenBLAS; wheel contents/hash were not retained. |
| `packaging` | 25.0 | Apache-2.0 OR BSD-2-Clause | Exact source tag `25.0`; `LICENSE.APACHE` blob `f433b1a53f5b830a205fd2df78e2b34974656c7b`; `LICENSE.BSD` blob `42ce7b75c92fb01a3f6ed17eea363f756b7da582`. |
| `pandas` | 2.2.3 | BSD-3-Clause | Exact source tag `v2.2.3`; `LICENSE` blob: `cdfa749dc34df3ff6664acd10a9b2e106ef19599`. |
| `pip` | 25.1.1 | MIT | Exact source tag `25.1.1`; `LICENSE.txt` blob: `8e7b65eaf628360e6f32f4140fcdd7ec7c2b7077`; its separately vendored modules were not inventoried here. |
| `pluggy` | 1.6.0 | MIT | Exact source tag `1.6.0`; `LICENSE` blob: `85f4dd63d2da8e31d7e84d5180f016fdfe315c2c`. |
| `Pygments` | 2.19.2 | BSD-2-Clause | Exact source tag `2.19.2`; `LICENSE` blob: `446a1a805c8a949579fb8a9799f2bec7777349dc`. |
| `pyogrio` | 0.11.0 | MIT | Exact source tag `v0.11.0`; `LICENSE` blob: `b5371fcf8083eba98e1dc444b911a459fd343285`. The Linux wheel contains GDAL 3.10.3 and associated native dependencies; see §5. |
| `pyproj` | 3.7.1 | MIT | Exact source tag `3.7.1`; `LICENSE` blob: `9e3de8f1130b96ac5b06d4ce75bb09794436ab60`. Its wheels contain PROJ 9.5.1; PROJ tag `9.5.1` `COPYING` blob: `d46f95cd6cccd0261593379658fd05c08f95bf49` (MIT-style license). |
| `pytest` | 8.3.5 | MIT | Exact source tag `8.3.5`; `LICENSE` blob: `c3f1657fce94589bd1ec7cead810639047f3d359`. |
| `python-dateutil` | 2.9.0.post0 | Apache-2.0 / BSD-3-Clause dual licensing | Exact source tag `2.9.0.post0`; `LICENSE` blob: `1e65815cf0b3132689485874a93034ede7206bf4`. The project documents the different terms applying to pre- and post-December 2017 contributions. |
| `pytz` | 2025.2 | MIT | Exact source tag `release_2025.2`; `LICENSE.txt` blob: `5f1c11289f6a54cb07ebdbf31d02e8e81b18b07f`. |
| `setuptools` | 80.9.0 | MIT | Exact source tag `v80.9.0`; `LICENSE` blob: `1bb5a44356f00884a71ceeefd24ded6caaba2418`; separately vendored modules were not inventoried here. |
| `shapely` | 2.1.1 | BSD-3-Clause | Exact source tag `2.1.1`; `LICENSE.txt` blob: `c2da06d68d2beb4b807017c876d03230051bc630`. The PyPI wheel bundles GEOS, which is LGPL-2.1; see §5. |
| `six` | 1.17.0 | MIT | Exact source tag `1.17.0`; `LICENSE` blob: `1cc22a5aa7679ebaa10934212f356823931bdc3e`. |
| `tzdata` | 2025.2 | Apache-2.0 | Exact source tag `2025.2`; `LICENSE` blob: `c2f84aeb06f7a520b7cf17bdd9c9c3854dc4c469`. |
| `wheel` | 0.45.1 | MIT | Exact source tag `0.45.1`; `LICENSE.txt` blob: `a31470f14c5978d5fcc3bc173b8399b6c9a6443f`. |

The 18 locked third-party distributions above are exactly the 18 entries in the captured `pinned-environment-freeze.txt`. GeoPandas itself was installed as an editable checkout at the exact fixed upstream commit and reported as version 1.1.0 in the runtime summary.

## 5. Native-library and wheel-level open items

The source/package license is not necessarily the only license that applies to a binary wheel.

### Shapely

- The experiment installed `shapely-2.1.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`.
- Shapely's 2.1.1 installation documentation says the PyPI binary wheel includes the GEOS version shipped at the time of release.
- The Shapely project identifies its own code as BSD-3-Clause and GEOS as LGPL-2.1.
- The experiment did not preserve the exact wheel bytes or record the bundled GEOS build/version. The Shapely Python-package license alone is therefore not a complete wheel-license inventory.

### Pyogrio / GDAL

- The experiment installed `pyogrio-0.11.0-cp311-cp311-manylinux_2_28_x86_64.whl`.
- Pyogrio's 0.11.0 release notes say its wheels include GDAL 3.10.3.
- GDAL's general source license is MIT-style, but its own license page warns that builds can incorporate dependencies with their own terms, including LGPL/GPL or proprietary components. Pyogrio's security policy names GEOS, PROJ and CURL among GDAL's third-party dependencies and says the set varies by build features and platform.
- PyPI publishes a SHA-256 for the corresponding CPython 3.11 manylinux_2_28 x86-64 wheel (`ec5666cc8bf97aef9993c998198f85fe209b8a9ad4737696d3d2ab573b3e9a5b`), but the workflow did not capture the wheel's local SHA-256. This published digest is not claimed to be a verified digest of the bytes installed on the runner.
- The exact GDAL subcomponent/notice set for this wheel was not extracted. This is an open item for any later binary redistribution, not a failure of the source reproduction.

### Pyproj / PROJ

- The experiment installed `pyproj-3.7.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`.
- Pyproj's 3.7.1 release notes state that its wheels contain PROJ 9.5.1; the exact PROJ source tag's `COPYING` file is MIT-style.
- The wheel bytes were not hash-pinned or separately archived. PROJ data/database and native wheel payload were not independently inventoried.

### NumPy

- The experiment installed `numpy-1.26.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`.
- The exact NumPy 1.26.4 source build configuration selects OpenBLAS for the wheel build. The published wheel has its own SHA-256 on PyPI, but the workflow did not save the local wheel bytes/hash or its embedded notice files.
- NumPy's current licensing documentation explains that PyPI wheels may include OpenBLAS and the GNU Fortran runtime with separate license terms; it also states that the bundled set varies by platform. This is a risk flag for binary redistribution, not a claim that the exact 1.26.4 wheel's complete payload was inspected here.

### Other packaging tools

The `pip` and `setuptools` source licenses were checked at their exact tags, but their wheel-internal vendored modules were not recursively inventoried. These are build/install tools in this experiment. Their binaries were not placed in the Stage 2 evidence artifact.

## 6. What was actually distributed in the evidence artifacts

Two artifacts must be distinguished.

### Stage 2 reproduction artifact

Latest repeat:
- Workflow run: [44936142633](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44936142633)
- Artifact ID: `14719339097`
- ZIP SHA-256: `eda44a04658c9250e4fa559c824a512ec4a91e7ff3f8595db0379db9c9ecd41e`

The Stage 2 ZIP contains logs, JSON result records, runtime/version information, source provenance, `requirements.lock` and `SHA256SUMS`. It contains **no installed package wheels, package source trees, GeoPandas source files, or license text bundles**. Its outer digest and ZIP CRC passed; all 17 internal SHA-256 entries passed.

### Frozen row extraction artifact

Earlier no-inference extraction:
- Workflow run: [44924570231](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44924570231)
- Artifact ID: `14715535728`
- ZIP SHA-256: `1abca7d09dfcbf4c4ba773ab87fb21225ec8f4208f44f2f7fbb19b613352459b`

Unlike the Stage 2 ZIP, this archive contains the frozen dataset row in JSON form, including the `problem_statement`, `patch` and `test_patch` fields. It is dataset-derived material (CC BY 4.0) and includes source-code patches identified by the row as BSD-3-Clause. The archive has a row audit manifest but does not include a separate GeoPandas BSD license text. The artifact is retained as a provenance record; for outward redistribution of the patch/test-patch material, include the appropriate dataset attribution and GeoPandas BSD notice/conditions. This note does not determine the legal status of the historical artifact or authorize new redistribution.

## 7. Reproducibility and supply-chain limitations

The dependency file is a **version lock, not a hash lock**:
- All installed Python distribution versions were pinned and `pip freeze --all` matched the version lock after excluding the editable GeoPandas checkout line.
- `pip check` reported no broken requirements.
- The workflow log exposes the exact wheel filenames/platform tags for the key binary packages.
- The workflow did not store each wheel's SHA-256, verify it against the corresponding PyPI digest, or preserve the wheel files. It is therefore environment-version reproducible, not proven byte-for-byte binary reproducible.

PyPI's own metadata documentation states that it displays publisher-provided license metadata and does not check that the declared license matches the actual contents. This screen therefore cross-checked exact source license files for the upstream repositories where available, while leaving the nested binary payload items above explicitly open.

## 8. Decision and next steps

**Current bounded finding**
1. GeoPandas source and test changes are covered by the same BSD-3-Clause repository license at the exact base and fixed commits. No license change was made by the PR.
2. The SWE-rebench dataset's CC BY 4.0 terms apply to the curated dataset material; the per-row BSD-3-Clause identifier separately points to the source repository license.
3. The Python package metadata/source-level screen found permissive licenses for most packages, plus MPL-2.0 for certifi and the expected Apache/BSD dual-licensed packages. The important extra binary components are GEOS under LGPL-2.1 and GDAL/PROJ/OpenBLAS-related native components whose complete wheel-level notice set has not been verified here.
4. The Stage 2 artifact itself does not redistribute these binaries. The separate row extraction artifact does include the data row and patch fields and needs attribution/notice care if it is republished outside the evidence archive.
5. The E1/E2 public-comment snapshots have strong provenance but no explicit commenter-granted license recorded. Keep them as linked, attributable research sources; do not repackage their full text as openly licensed material.

**Research decision:** this documentary screen does not alter the Stage 2 technical pass, the approved E3/E2/E1 decisions, or the scientific sample. GeoPandas stays **HOLD**. For the current internal reproduction, no dependency binaries are included in the Stage 2 artifact. Before distributing a container, wheel bundle, source bundle, or full row/patch archive with a paper, complete the native-wheel notice inventory and confirm the required dataset/source attributions and notices. This document is not legal advice or legal clearance.

## 9. Primary references

- Dataset README and CC BY 4.0 / per-row source-license distinction: https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified
- PyPI license metadata limitations: https://docs.pypi.org/project_metadata/
- Certifi 2025.6.15: https://pypi.org/project/certifi/2025.6.15/
- iniconfig 2.1.0: https://pypi.org/project/iniconfig/2.1.0/
- NumPy 1.26.4: https://pypi.org/project/numpy/1.26.4/
- packaging 25.0: https://pypi.org/project/packaging/25.0/
- pandas 2.2.3: https://pypi.org/project/pandas/2.2.3/
- pip 25.1.1: https://pypi.org/project/pip/25.1.1/
- pluggy 1.6.0: https://pypi.org/project/pluggy/1.6.0/
- Pygments 2.19.2: https://pypi.org/project/Pygments/2.19.2/
- pyogrio 0.11.0: https://pypi.org/project/pyogrio/0.11.0/
- GDAL license and dependency caveat: https://gdal.org/en/stable/license.html
- Pyogrio wheel and native dependency policy: https://github.com/geopandas/pyogrio/security/policy
- pyproj 3.7.1: https://pypi.org/project/pyproj/3.7.1/
- PROJ 9.5.1: https://github.com/OSGeo/PROJ/tree/9.5.1
- pytest 8.3.5: https://pypi.org/project/pytest/8.3.5/
- python-dateutil 2.9.0.post0: https://pypi.org/project/python-dateutil/2.9.0.post0/
- pytz 2025.2: https://pypi.org/project/pytz/2025.2/
- setuptools 80.9.0: https://pypi.org/project/setuptools/80.9.0/
- Shapely 2.1.1 and GEOS LGPL-2.1: https://pypi.org/project/shapely/2.1.1/
- Shapely 2.1.1 binary-wheel GEOS inclusion: https://shapely.readthedocs.io/en/2.1.1/installation.html
- six 1.17.0: https://pypi.org/project/six/1.17.0/
- tzdata 2025.2: https://pypi.org/project/tzdata/2025.2/
- wheel 0.45.1: https://pypi.org/project/wheel/0.45.1/
