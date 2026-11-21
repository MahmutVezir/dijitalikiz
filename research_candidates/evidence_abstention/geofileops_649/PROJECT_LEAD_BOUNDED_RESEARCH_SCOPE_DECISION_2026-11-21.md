# GeoFileOps #649 — project-lead bounded research-use and provenance scope decision

**Candidate:** geofileops/geofileops issue #648 / PR #649  
**Dataset instance:** `geofileops__geofileops-649`  
**Decision status:** **PENDING PROJECT-LEAD ACKNOWLEDGEMENT**  
**Decision date:** 21 November 2026

## 1. Purpose and decision boundary

This record proposes a narrowly defined scope for the exploratory research reproduction and documentary review of GeoFileOps #649. It is not legal advice, legal clearance, a blanket license compatibility opinion, redistribution authorization, or final case acceptance.

The exact 105-package Conda metadata and notice inventory is complete. The project lead is asked to acknowledge only the exact use and materials described below.

## 2. Exact bounded research scope proposed

### A. Upstream source and defect reproduction

- Upstream issue: https://github.com/geofileops/geofileops/issues/648
- Upstream PR: https://github.com/geofileops/geofileops/pull/649
- Exact buggy base: `f7f8a4cf49b1278f3e9e5f4157718de441a21b57`
- Exact fixed PR head: `ec1438fbf8527269cd1193647d05c8d7fdb83802`
- The five PR-changed paths only:
  - `CHANGELOG.md`
  - `geofileops/fileops.py`
  - `geofileops/util/_geoops_gpd.py`
  - `geofileops/util/_geoops_sql.py`
  - `tests/test_geofile.py`
- Stage 2 includes the single independent issue reproducer and its explicit-layer positive control, plus the 10 immutable dataset FAIL_TO_PASS selectors. No additional upstream test suite or optional integration is included in this scope.

### B. Frozen dataset row and attribution

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Instance ID: `geofileops__geopandas-3591` is a separate candidate; this scope applies only to `geofileops__geofileops-649`.
- GeoFileOps row canonical SHA-256: `2a85246a15d97ca6e73eb9a02f36022a05f80b8322c24a6522fbfee31fc7d1eb`.
- Dataset-card license metadata: CC-BY-4.0; row/source project license metadata: BSD-3-Clause.
- Attribution must retain PrimeIntellect as the dataset publisher and geofileops/geofileops as the upstream source project, with the frozen dataset revision and per-row source license stated separately.

### C. Exact reproduction environment

- GitHub Actions `ubuntu-24.04`, Linux `linux-64`, Python `3.11.9`.
- The committed `environment.yml` and the exact Conda explicit lock produced by the Stage 2 run.
- Frozen explicit-lock SHA-256: `348678b8947ea677e184ed90fc20a92bc3b3fc353ec3f18b8220c8a5d6bccc79`.
- The lock contains 105 exact Conda package archives. All 105 package archives were subsequently downloaded, matched the lock MD5 and internal `info/index.json` identity, and supplied an `info/about.json` license expression.
- Package metadata and notice inventory: workflow run `44927884852`, job `136917880433`, artifact `14716462835`, SHA-256 `ff397b7a2afbed6ac524f570019f7e5211dfb49304d1f111a817233536a8ca49`.
- Extracted notice/license files are retained in the audit artifact; the 105 package binaries are **not** included in the Stage 2 artifact, repository, or license-audit artifact.

### D. Research evidence artifacts

- Stage 2 workflow run: `44916663456`, job `136883732286`, artifact `14711502949`.
- Stage 2 artifact SHA-256: `b4b408170b3fcae7c305d060f0cc283fcf912e964403a9eb1015b1209e60553f`.
- The artifact contains the Stage 2 logs, the exact explicit lock, issue reproducer and positive-control logs, the 10-selector base/fixed logs, source/patch provenance hashes and relevant license files.
- The later package audit artifact contains package-level license metadata and the 253 extracted notice/license files from the exact locked package archives.

## 3. Explicit exclusions

This proposed acknowledgement does **not** cover or authorize:

- redistribution, publication, repackaging or mirroring of the 105 Conda binary package archives;
- distribution of a complete Conda environment or container image;
- additional versions, unpinned dependencies, other operating systems, architectures or Python versions;
- optional GeoFileOps integrations, adapters, extras or development-only components not present in the exact lock;
- additional upstream source files, issues, PRs, patches, tests or candidate cases beyond the exact set above;
- redistribution of the SWE-rebench dataset beyond its separate license and attribution conditions;
- model weight downloads, model loading, inference, fine-tuning or training;
- a general conclusion that every upstream dependency is compatible for every use or that all legal obligations have been satisfied.

Any material change to the source revisions, changed-file set, environment lock, package distribution, dataset revision or experiment scope requires a separate review.

## 4. Recorded license/NOTICE observations

The exact package archive metadata includes GPL, LGPL and MPL expressions as well as permissive expressions. The presence of those license families is recorded, not concealed or treated automatically as a violation. Two SQLite packages use the `blessing` expression and link to the SQLite copyright page but contain no separate license/NOTICE file in their exact package archives.

The inventory does not determine whether every license obligation is satisfied in every possible context. The project lead's acknowledgement below, if approved, is limited to this documented ephemeral CI research scope and the retained metadata/notice records; it is not professional legal review or clearance.

## 5. Proposed project-lead decision

Proposed decision language:

> YES — I acknowledge the exact bounded research-use and provenance scope in Sections 2–4 for GeoFileOps #649. This acknowledgement is limited to the pinned source revisions, the five listed changed paths, the frozen dataset row and revision, the exact 105-package Conda lock, the listed Stage 2 reproducer/selectors and the named evidence artifacts. It does not authorize redistribution of Conda binaries or a full environment, does not extend to other software versions or additional scope, and is not legal advice, legal clearance, a blanket license compatibility decision, or final case acceptance. The identified GPL/LGPL/MPL expressions and the two SQLite packages without separate local notice files remain disclosed in the research record.

**Project-lead decision:** PENDING  
**Decision timestamp (UTC):** pending  
**Decision record SHA-256 / URI:** pending

After this scope decision is recorded, the remaining steps are to assemble the complete schema-conformant case record, run the fail-closed structural validator, and obtain a separate final YES/NO acceptance decision. No accepted-registry insertion or model-inference authorization follows automatically from this acknowledgement.

## 6. Project-lead bounded research scope acknowledgement — 21 November 2026

**Decision: YES — APPROVED for the exact bounded exploratory research scope in Sections 2–4.**

The project lead explicitly approved use limited to the pinned buggy/fixed source revisions, the five listed changed files, the frozen dataset row and revision, the exact 105-package Conda lock, the ten frozen FAIL_TO_PASS selectors, the independent reproducer and the named evidence artifacts.

**Explicit exclusions remain binding:** no redistribution of the 105 Conda binary package archives or a complete environment; no unpinned versions, other OS/Python/runtime combinations, optional integrations, additional upstream files/tests/cases or broader experiments; no dataset redistribution beyond its own license and attribution conditions; no model-weight download, model loading, inference, fine-tuning or training.

This is a project-lead acknowledgement of a documentary, bounded research scope. It is not legal advice, legal clearance, a blanket compatibility opinion, proof that every legal obligation has been satisfied, or final case acceptance.

**Decision maker:** student project lead  
**Decision source:** explicit approval in ChatGPT conversation, 21 November 2026  
**Decision timestamp (UTC):** 2026-11-21 (time not independently captured; no fabricated time is recorded)  
**Scope-record content SHA-256:** to be recorded in the case acceptance artifact after file commit.

The remaining steps are a schema-conformant proposed case record, fail-closed validation, and a separate final YES/NO acceptance decision. No accepted-registry insertion or model-inference authorization follows automatically.