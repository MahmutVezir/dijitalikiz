# GeoFileOps #649 — temporal exposure and dependency/license audit

**Date:** 21 November 2026  
**Candidate:** geofileops/geofileops issue #648 / PR #649  
**Purpose:** Bounded documentary audit of temporal exposure and the exact Stage 2 runtime artifact. This document is not legal advice, legal clearance, a blanket compatibility opinion, or final case acceptance.

## 1. Evidence base and artifact integrity

The audit is based on the independently verified Stage 2 artifact for workflow run `44916663456`, job `136883732286`, artifact `14711502949`.

- Artifact ZIP SHA-256: `b4b408170b3fcae7c305d060f0cc283fcf912e964403a9eb1015b1209e60553f`.
- Independent archive verification: outer SHA-256 matched the GitHub digest; ZIP CRC passed; 19 archive members; 18/18 entries in `SHA256SUMS.txt` passed.
- Frozen Conda explicit lock: `conda-explicit.txt`, 105 exact package URLs, SHA-256 `348678b8947ea677e184ed90fc20a92bc3b3fc353ec3f18b8220c8a5d6bccc79`.
- Python license metadata inventory: 14 distribution entries, SHA-256 `68f3a0c67a9fb1b5c36dc53f1ae5e5bbf0d9711dd3da705a1488b67b64c21a69`.
- Dataset-extraction utility inventory: PyArrow 19.0.1, Apache Software License, SHA-256 `18793a123ff7ff328b374cdc39e3cb61676e642364a9e9937a0a622891975bc5`.

The archive contains the exact lock and package metadata inventories, not the 105 Conda binary package archives themselves.

## 2. Temporal exposure — model identity correction and chronology

The current frozen pilot manifest is `data/pilot/pilot_manifest.json`. It identifies the active pilot model as:

- Model: `Qwen/Qwen2.5-3B-Instruct`
- Exact revision: `aa8e72537993ba99e69dfaafa59ed015b17504d1`
- Precision: FP16, loaded from the source BF16 checkpoint.

The older `Qwen/Qwen2.5-3B-Instruct-GPTQ-Int4` revision `68c4276063d1496cdf13d0b8e8221f899bfa77f7` is explicitly recorded in the manifest as the **previous** model configuration. It was replaced before any pilot inference record was written because the GPTQ loader reported newly initialized biases and generation failed with non-finite sampling probabilities. The manifest says no prior pilot inference records existed. The temporal assessment below therefore uses the active `Qwen2.5-3B-Instruct` revision, not the superseded GPTQ revision.

Hugging Face records the active revision `aa8e725...` as a 25 September 2024 commit, and its visible change is a README metadata line. The frozen candidate's issue and PR were created on 6 March 2025. Thus the issue/PR disclosure is later than the publicly pinned model revision by approximately 162 days.

**What this supports:** the specific March 2025 issue and PR text cannot have been part of the publicly released September 2024 model snapshot.

**What this does not support:** it does not prove the model's training-data cutoff, enumerate its pretraining sources, or rule out exposure to GeofileOps source code that existed before September 2024. No exact training-data cutoff or comprehensive source-corpus manifest has been established here.

Therefore temporal exposure is assessed as **reduced for issue/PR-specific leakage, but unresolved for pre-existing repository-source exposure**. Do not label the candidate contamination-free.

Sources:
- Frozen pilot manifest: `data/pilot/pilot_manifest.json` (the repository branch contains the exact model ID, revision and pre-inference replacement note).
- Hugging Face exact model revision and commit metadata: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/commit/aa8e72537993ba99e69dfaafa59ed015b17504d1
- Candidate issue: https://github.com/geofileops/geofileops/issues/648
- Candidate PR: https://github.com/geofileops/geofileops/pull/649

## 3. Dataset and model license context — separate scopes

The frozen SWE-rebench row records the upstream repository license as `BSD-3-Clause`; the upstream source `LICENSE.txt` is also BSD 3-Clause. The dataset card states that the dataset is CC-BY-4.0 and instructs users to respect each instance's source-repository license, which is supplied per row. These are distinct layers of provenance and should both remain visible.

The active Qwen model repository labels its license `qwen-research`. Its license text defines Non-Commercial as research or evaluation purposes and limits the grant to non-commercial purposes; it also specifies attribution/notice conditions for redistribution. This is a **study-wide model-use gate**, separate from the candidate's GeoFileOps source and runtime-dependency review. No inference is authorized by this document.

Sources:
- Dataset card: https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified
- Active model license at the exact pinned revision: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/aa8e72537993ba99e69dfaafa59ed015b17504d1/LICENSE

## 4. Runtime dependency inventory — partial findings only

The existing artifact inventories metadata for 14 Python distributions. Among them, `pygeoops 0.4.0` has a null `license` field even though its classifier says BSD; the artifact does not include a separately authenticated copy of that dependency's license text. PyPI displays BSD License/classifier metadata, but that listing itself labels the relevant project metadata unverified. This item still needs exact source/package-level confirmation.

The explicit Conda lock contains 105 packages, including the native geospatial stack and its transitive components. The existing artifact does **not** contain a per-package copyright/license/NOTICE inventory for all 105 entries. Preliminary package-source checks identify materially different license families, for example:

- GDAL 3.9.3: MIT metadata in conda-forge's GDAL feedstock.
- GEOS 3.13.1: LGPL-2.1-only in conda-forge's GEOS feedstock.
- `xz-gpl-tools 5.8.3` is present in the exact lock; the conda-forge recipe identifies the package as carrying `0BSD AND LGPL-2.1-or-later AND GPL-2.0-or-later`.
- `libtiff 4.7.2`: HPND metadata in the conda-forge package catalog.
- `libkml 1.3.0`: BSD-3-Clause metadata in the conda-forge package catalog.
- `xerces-c 3.2.5`: Apache-2.0 metadata in the conda-forge package catalog.

A further exact-build issue exists for `libspatialite 5.1.0`: the frozen explicit lock contains build `he17ca71_14`, while public package catalog entries show multiple GPL/LGPL build variants and the catalog overview presents MPL-1.1 metadata. The available records do not map the exact locked build to a specific license expression, so this report deliberately does not assign one.

Sources for these preliminary metadata checks:
- GDAL: https://github.com/conda-forge/gdal-feedstock
- GEOS: https://github.com/conda-forge/geos-feedstock
- XZ split packages: https://github.com/conda-forge/xz-feedstock
- LibTIFF: https://anaconda.org/conda-forge/libtiff
- LibKML: https://anaconda.org/conda-forge/libkml
- Xerces-C: https://anaconda.org/conda-forge/xerces-c
- libspatialite catalog/build variants: https://anaconda.org/conda-forge/libspatialite and https://anaconda.org/conda-forge/libspatialite/files
- pygeoops 0.4.0 PyPI metadata: https://pypi.org/project/pygeoops/0.4.0/

**Finding:** the root source and Python metadata inventories are partially documented, but the exact native/transitive dependency notice review is incomplete. It would be incorrect to mark all 105 package notices reviewed or to assert blanket license compatibility from the current artifact.

## 5. Scope boundary and remaining gates

This review does not authorize redistribution of the environment or binaries. The current Stage 2 artifact contains the textual explicit lock and evidence files, not the full binary Conda package set. Any later distribution that includes model materials, binaries, copied source or derived materials requires its own notice/permission review.

Still-open project gates:

1. **Project-lead temporal acknowledgement:** acknowledge that issue/PR-specific exposure is chronologically reduced, while prior repository-source exposure and exact model training-data cutoff remain unresolved.
2. **Dependency/native notice review:** resolve the exact locked package metadata and required notices for all 105 Conda packages, including the exact `libspatialite` build and the copyleft/license expressions present in the lock.
3. **Dataset-card and bounded-scope acknowledgement:** record the CC-BY-4.0 dataset attribution and BSD-3-Clause row/source context, and define the exact source, patch, selectors, environment and artifact materials used in the research scope. This is not legal clearance.
4. **Complete case record and fail-closed validation:** confirm all required hashes, decision links, exposure fields, source/license references and evidence-boundary fields are structurally complete.
5. **Separate final project-lead YES/NO acceptance:** do not infer acceptance from Stage 2 PASS or E3/E2/E1 approval.

Current disposition remains: Stage 2 technical PASS; strict mechanism gold and E3/E2/E1 tiers approved; prior pipeline/debug exposure none; temporal acknowledgement, full dependency/native notice review, bounded-scope acknowledgement, fail-closed case-record validation and final acceptance still open. No registry inclusion or inference authorization is asserted.

## 6. Project-lead acknowledgement — 21 November 2026

The project lead explicitly approved the bounded temporal-exposure assessment.

**Acknowledged conclusion:** issue #648 and PR #649 were created on 6 March 2025, approximately 162 days after the active frozen model revision dated 25 September 2024. Issue/PR-specific exposure is chronologically unlikely for that released revision. The model's exact training-data cutoff is not established, and exposure to pre-existing GeofileOps source code cannot be ruled out. The candidate is **not declared contamination-free**; the residual uncertainty must remain in the study record.

This acknowledgement closes the project-lead response gate for the bounded temporal assessment only. It does not prove a training cutoff, establish absence of contamination or memorization, or close the dependency/native notice review, bounded scope acknowledgement, case-record validation, or separate final acceptance.

The superseded GPTQ configuration is not treated as the active pilot checkpoint; the frozen manifest records that it was replaced before any pilot inference record was written.

**Updated status:** temporal-exposure acknowledgement received; full 105-package exact-build license/copyright/NOTICE review remains incomplete; pygeoops metadata requires source-level confirmation; bounded scope and dataset/source attribution acknowledgement remain open; complete case record and fail-closed validation remain open; final project-lead YES/NO acceptance remains open. No legal clearance, registry inclusion or inference authorization is asserted.

## 7. Exact-build Conda package inventory — completed 21 November 2026

The earlier partial Python-distribution-only inventory is superseded by an exact audit of every package archive in the frozen explicit lock.

### Reproduction and integrity

- GitHub Actions run: `44927884852`.
- Job: `136917880433`, conclusion: `success`.
- Workflow source commit: `75f653194a08939587157a863d59aab7aa30e9c2`.
- Source Stage 2 artifact: `14711502949`; SHA-256 `b4b408170b3fcae7c305d060f0cc283fcf912e964403a9eb1015b1209e60553f`.
- Frozen explicit lock SHA-256: `348678b8947ea677e184ed90fc20a92bc3b3fc353ec3f18b8220c8a5d6bccc79`.
- Exact locked package archives: **105/105 downloaded; 105/105 matched their frozen-lock MD5; 105/105 matched the package identity in `info/index.json`**.
- Conda `info/about.json` license metadata: **105/105 present; 0 missing**.
- `license_file` metadata present for 63 packages; `license_family` metadata present for 22 packages. Absence of these optional fields is not counted as a missing license expression.
- License/NOTICE files extracted: **253 files from 103 packages**. Two packages, `libsqlite 3.53.4 h0737f62_102` and `sqlite 3.53.4 h6e79ffa_102`, carry the `blessing` license expression and an upstream SQLite copyright URL in `about.json`, but no separate license/NOTICE file was present in either exact archive.
- Total package bytes downloaded: 140,794,604.
- Uploaded audit artifact: `14716462835`; SHA-256 `ff397b7a2afbed6ac524f570019f7e5211dfb49304d1f111a817233536a8ca49`.
- Independently downloaded artifact verification: outer SHA-256 matched GitHub; ZIP CRC passed; 257 members.
- `package-license-inventory.json`: 894,593 bytes; SHA-256 `333f433ed6c02647b19f21cf6cbeb12c15dd6ab82dde9da6ccb50aab523ffb0d`.
- `audit-summary.json`: 1,136 bytes; SHA-256 `34b5753bed2e52ee7c548c7ab2d33aa52dc45530b06021e05416668ccc66e276`.
- `source-conda-explicit.txt`: 12,152 bytes; SHA-256 matches the frozen lock above.
- Bundled `package-notices-and-inventory.zip`: 673,550 bytes; SHA-256 `bae502bc39363586cff1aa36d895d148a00ab60748787747e00c8c3bc72a6252`.

Artifact URL: https://github.com/MahmutVezir/dijitalikiz/actions/runs/44927884852/artifacts/14716462835

### Exact package license expressions

The Conda `info/about.json` fields in the exact binary package archives yielded the following license-expression counts (105 packages total):

| Package license expression | Package count |
|---|---:|
| MIT | 27 |
| BSD-3-Clause | 24 |
| Apache-2.0 | 7 |
| GPL-3.0-only WITH GCC-exception-3.1 | 7 |
| BSD-2-Clause | 4 |
| LGPL-2.1-only | 3 |
| Zlib | 3 |
| ISC | 2 |
| MPL-1.1 | 2 |
| LGPL-2.1-or-later | 2 |
| GPL-3.0-only | 2 |
| 0BSD | 2 |
| GPL-2.0-or-later | 2 |
| blessing | 2 |
| 0BSD AND LGPL-2.1-or-later AND GPL-2.0-or-later | 2 |
| Other single-package expressions | 14 |

The 14 single-package expressions are: `bzip2-1.0.6`, `MIT and PSF-2.0`, `curl`, `BSD-2-Clause OR GPL-2.0-or-later`, `IJG AND BSD-3-Clause AND Zlib`, `zlib-acknowledgement`, `HPND`, `X11 AND BSD-3-Clause`, `Python-2.0`, `BlueOak-1.0.0`, `TCL`, `PSF-2.0`, `LicenseRef-Public-Domain`, and `0BSD AND LGPL-2.1-or-later`.

### Material license/NOTICE review targets

The exact package records identify these notable license families and packages:

- **GCC runtime exception expressions:** `libgcc`, `libgcc-ng`, `libgfortran`, `libgfortran5`, `libgomp`, `libstdcxx`, and `libstdcxx-ng` carry `GPL-3.0-only WITH GCC-exception-3.1`.
- **GPL expressions without the GCC exception:** `ld_impl_linux-64` and `readline` carry `GPL-3.0-only`; `librttopo` and `lzo` carry `GPL-2.0-or-later`.
- **LGPL expressions:** `geos` and `libiconv` and `libnsl` carry `LGPL-2.1-only`; `keyutils` and `libxcrypt` carry `LGPL-2.1-or-later`.
- **Multi-license XZ expressions:** `xz` and `xz-gpl-tools` carry `0BSD AND LGPL-2.1-or-later AND GPL-2.0-or-later`; `xz-tools` carries `0BSD AND LGPL-2.1-or-later`.
- **MPL expressions:** `freexl` and the exact locked build `libspatialite 5.1.0 he17ca71_14` carry `MPL-1.1`.
- **Alternative licensing:** `libev` carries `BSD-2-Clause OR GPL-2.0-or-later`.

The exact Conda record for `pygeoops 0.4.0 pyhd8ed1ab_2` reports `BSD-3-Clause`, `license_family=BSD` and `license_file=LICENSE.txt`; its license file was extracted (SHA-256 `684f266645f9b1c7c9302202ac3f9d4eb9009627369e0151feb7793fd7bf2a3d`). This **supersedes** the preliminary Python-distribution metadata note above that its license field was null: the package-level Conda archive metadata and embedded license file are now present and authenticated.

The exact locked `libspatialite` build is also resolved at the **package metadata** level as `MPL-1.1`, with `COPYING` present in the package archive (SHA-256 `b81965482914858383484d7e63b5de1d0c4647fa7f527e78d4499e4a7b76aab5`). This supersedes the earlier statement that the exact build's license expression was not yet resolved.

### Interpretation and remaining limits

This is now a complete **exact locked package metadata and notice-file presence inventory**: all 105 package files were downloaded and checked against the frozen lock; all 105 contain a license expression; 253 local notice/license files were extracted from 103 packages.

It is **not** a compatibility analysis, legal opinion, proof that every dependency's obligations are satisfied, or legal clearance to redistribute binaries. The metadata expressions include GPL, LGPL and MPL families and must be assessed in the context of the actual use and distribution scope. The two SQLite packages do not carry separate notice files in their package archives; their `about.json` records point to the upstream SQLite copyright page: https://www.sqlite.org/copyright.html.

The original Stage 2 artifact contains logs, source/patch provenance and the explicit lock, not the downloaded 105 binary Conda packages. The new audit artifact contains the inventory and extracted license/notice materials, not those 105 package binaries.

### Updated status

- Exact-build license/NOTICE **inventory: complete**.
- Manual obligation-by-obligation compatibility and legal review: **not established by this audit**.
- Project-lead bounded dataset/source attribution and research-scope acknowledgement: **still required**.
- Complete schema-conformant case record and fail-closed validation: **still required**.
- Separate final project-lead YES/NO acceptance: **still required**.
- No accepted-registry insertion, legal clearance or model-inference authorization is asserted.
