# Project-lead bounded license-scope acknowledgement proposal — Dymos #1166

**Date:** 20 November 2026  
**Status:** PROPOSAL ONLY — project-lead acknowledgement is pending  
**Candidate:** OpenMDAO/dymos issue #1166 / fix PR #1165

## 1. Why this record exists

This is a factual inventory of the materials used and retained by the Dymos #1166 research workflow, followed by a proposed narrow project-scope acknowledgement. It is not a legal opinion, formal legal clearance, or a claim that every license question has been resolved.

The project lead must decide whether the described scope accurately reflects the intended educational research activity and the repository/artifact publication already undertaken. The assistant does not give the acknowledgement on the project lead's behalf.

## 2. Authenticated source and dataset identifiers

### Dymos source

- Repository: `OpenMDAO/dymos`
- Buggy base: `3efd1035c3bf62890034eb9e07de543f3d117867`
- Fixed PR head: `0ffc82225d6125dcb5c5b5acfb9be9fd712ef949`
- Root `LICENSE`: Apache-2.0; the exact pinned source file was captured in the Stage 2 evidence artifact.
- Upstream change set: six files; the complete PR patch SHA-256 is `651c7d79f67ea27405a29859c2367ca3392a833bdf5adca0876acd373ef833d4`.

### Dataset

- Dataset repository: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Exact revision used: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Exact-revision Hub commit page: https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified/commit/fb9aa226b2ce37c708ea7732e7b980abacdadb67
- The Hub page for that exact commit displays the dataset card license as CC-BY-4.0 and shows that the commit changes `README.md` and the train Parquet file.
- Selected row: `openmdao__dymos-1165`; its row-level `license` field is `Apache-2.0`. That field describes the upstream source repository for this row, not the dataset repository's overall license.
- The selected canonical row is 902 bytes; its `problem_statement` field is 517 characters. The whole dataset (6,272 rows) is not included in the evidence artifact.

The dataset card's CC-BY-4.0 terms and the row's upstream Dymos Apache-2.0 license are separate attribution/scope layers and must both be respected.

## 3. Materials currently retained in research/CI artifacts

The following are the actual artifact contents, not a hypothetical future plan:

1. Stage 2 dataset-selector evidence artifact `14341424466` (GitHub SHA-256 `8fc5e1de9ee8c7d4be45c29b48ba9b1a0e6c82194ecb9ce2b7f5757d4fd58051`): one canonical dataset row, the 517-character issue narrative, selector/test output, a test-only patch, the full upstream PR #1165 patch (24,143 bytes), the Dymos `LICENSE` text (10,760 bytes), project metadata, and dependency license inventories. Its ZIP CRC passed and all 18 internal SHA-256 entries passed.
2. Latest Dymos reproduction artifact `14650442090` (GitHub SHA-256 `9667f304d0a259ab3b1aedd19a5751bab9fc43a5d7544a21dc5f3b126b91ee00`): the full upstream PR patch (24,131 bytes), full captured buggy/fixed versions of `control_comp.py` and `misc.py`, the buggy-base `LICENSE`, project metadata, logs, runtime freeze, and hash manifest. ZIP CRC and 15/15 internal hashes passed.
3. The proposed E1 packet in the project repository includes a 517-character issue narrative and four small active source excerpts, the largest excerpt 1,316 characters, each pinned to the exact buggy-base commit/path/line range/hash.

These artifacts do **not** contain the complete Dymos repository or the complete 6,272-row dataset. The two CI artifacts do contain the full six-file upstream fix patch and two full source-file snapshots as described above. No NumPy/SciPy/PyArrow wheel or shared-library binary is included in these evidence ZIPs.

## 4. Reproduction environment and third-party notices

The Stage 2 run used CPython 3.11.9 and a 14-package test runtime. The inventory file SHA-256 is `6e8f21e813fd0332fa3a5c370f76a0a52653d49868348d4316cb0eb40d0c3c89`. The separate dataset extraction inventory SHA-256 is `ac40d99c0eeaa6654aa5197b320429c6efa6e720420692d146f4810798dfa068`.

Important runtime entries recorded in package metadata:

- NumPy 1.26.4 and SciPy 1.13.1: base package metadata identifies BSD-family terms. Their binary-distribution metadata also names bundled OpenBLAS and LAPACK notices (BSD-3-Clause / BSD-3-Clause-Attribution), GCC runtime library (GPL-3.0 with GCC Runtime Library Exception 3.1), and `libquadmath` (LGPL-2.1-or-later).
- Other test-runtime metadata: NetworkX 3.3 (BSD); packaging 24.2 (Apache/BSD classifiers); Requests 2.32.3 (Apache-2.0); certifi 2024.8.30 (MPL-2.0); charset-normalizer 3.4.0 (MIT); idna 3.10 (BSD); urllib3 2.2.3 (MIT); OpenMDAO 3.38.0 (Apache-2.0); pytest 8.3.3 (MIT); iniconfig 2.0.0 (MIT); pluggy 1.5.0 (MIT); Pygments 2.18.0 (BSD-2-Clause).
- PyArrow 19.0.1 (Apache Software License) was used in a separate extraction environment to read the selected Parquet row; it was not part of the 14-package Dymos test runtime.

The NumPy metadata also lists source-distribution/repository components (lapack-lite, Tempita, Dragon4, libdivide, Meson and spin). They are distinguished in the underlying metadata from the libraries explicitly listed in the installed binary-distribution sections; this reproduction used installed packages, not a source build. This record does not reclassify those source-only notices as installed wheel components.

The package records are metadata inventories, not formal legal conclusions. Binary notices are relevant even though the binaries themselves were not copied into the research artifacts.

## 5. Proposed bounded project-use scope for acknowledgement

The proposed acknowledgement would be limited to:

- educational/scientific research into one Dymos defect, using the pinned source revisions and one selected SWE-rebench row;
- execution of the pinned CPU test/reproducer environments, with dependencies installed into temporary CI environments;
- retaining and referencing the two identified CI evidence artifacts, including the full PR patch and the two source-file snapshots explicitly described above;
- retaining one selected dataset row and its issue narrative, and publishing short source excerpts with upstream repository, commit, path, line-range and hash attribution;
- keeping appropriate attribution and license notices with the research materials, including Dymos Apache-2.0, dataset CC-BY-4.0, the row-specific Dymos license, and the enumerated dependency notices where applicable.

## 6. Out of scope

This proposal does not cover or authorize:

- mirroring, hosting, or redistributing the complete SWE-rebench dataset;
- mirroring or redistributing the complete Dymos repository;
- distributing NumPy, SciPy, OpenBLAS, LAPACK, GCC runtime, libquadmath, or PyArrow binaries/wheels as research deliverables;
- unrelated Dymos issues or unrelated upstream packages;
- commercial product use or a general license grant beyond the specific educational research workflow described above;
- legal conclusions about whether any specific reuse, excerpt, or public artifact is permitted. No external legal review has been performed.

The repository and CI artifacts are accessible through the project's GitHub repository/PR workflow, so this proposal does not describe the materials as private-only.

## 7. Project-lead acknowledgement — pending

The proposed scope above is **not approved yet**. The project lead must explicitly accept or request a revision. This acknowledgement, if later approved, records the intended research scope and attribution/notice handling; it is not legal clearance.

Until the project lead responds:

- `project_lead_scope_acknowledgement = pending`;
- `accepted_as_legal_clearance = false`;
- Dymos final case acceptance remains `not_accepted`;
- model inference remains unauthorized.
