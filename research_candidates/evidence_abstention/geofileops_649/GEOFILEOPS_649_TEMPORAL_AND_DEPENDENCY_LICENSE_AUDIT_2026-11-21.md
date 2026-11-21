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
