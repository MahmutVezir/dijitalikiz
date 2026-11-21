# GeoPandas #3591 — license and provenance audit

**Audit date:** 2026-11-21  
**Scope:** Existing frozen E1/E2/E3 packets, frozen dataset row provenance, pinned Stage 2 environment and uploaded Stage 2 evidence archives.  
**Purpose:** Identify attribution, license and reproducibility boundaries. This is a research-governance audit, not legal advice or a legal clearance.

## 1. Executive disposition

**Disposition: HOLD — limited research use is documented; publication/redistribution clearance is not established.**

The Stage 2 execution archive contains logs, result summaries, environment versions, source commit identifiers and a requirements lock. It does not contain GeoPandas source files, dependency wheels, dependency source distributions, or copies of dependency license texts. Therefore, the Stage 2 archive itself does not appear to redistribute those software packages.

However, a separate frozen-row audit artifact contains the complete canonical dataset row, including `patch` and `test_patch` diffs, plus the issue problem statement. The dataset repository declares CC BY 4.0, while the row's source-repository license field says BSD-3-Clause. The original GeoPandas repository is independently marked BSD 3-Clause. The dataset-level declaration must not be treated as replacing or extinguishing the upstream source-code license or third-party authors' rights in issue/PR text.

The E1/E2 snapshots also retain verbatim GitHub issue/PR comment bodies. The inspected snapshots do not contain an explicit license grant for those user-authored comments. Keep the evidence provenance, but do not publish the full comment text as though it were covered by the GeoPandas BSD license or automatically cleared by the dataset card.

No finding in this audit changes the technical Stage 2 result. No finding authorizes model inference or final case acceptance.

## 2. Dataset and frozen-row provenance

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Frozen dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset Hub card declares: **CC BY 4.0**
- Dataset URL: https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified/tree/fb9aa226b2ce37c708ea7732e7b980abacdadb67
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Frozen row: `geopandas__geopandas-3591`
- Canonical row SHA-256: `e543af0bbc5e779661c3b1b79c28849f67dee7c61157c000c6698b15ba1218e2`
- Frozen problem statement SHA-256: `c4aeb4909495887c065f1f7ae5ec0e321fb350e98ea789cde3f931cad597f12d`
- Dataset row's `license` field: `BSD-3-Clause` (source-project metadata; not the same field as the Hub repository's CC BY 4.0 declaration).

### Row-audit artifact content

- Artifact ID: `14715535728`
- Artifact SHA-256: `1abca7d09dfcbf4c4ba773ab87fb21225ec8f4208f44f2f7fbb19b613352459b`
- ZIP CRC and all six internal file hashes were previously verified.
- The ZIP contains the complete canonical GeoPandas row. Its fields include `problem_statement`, `patch`, and `test_patch`; it is not merely a row hash or metadata-only reference.
- It also contains a second candidate row (music21), so it is a multi-row audit bundle, not a GeoPandas-only publication packet.

**Implication:** The row-audit artifact is useful as a restricted provenance/evidence artifact, but it should not be treated as automatically cleared for republication. Before external publication, include dataset attribution and review the upstream BSD-3 conditions for the embedded code diffs, as well as the rights status of the issue text. Do not claim that CC BY 4.0 alone resolves every upstream component.

## 3. GeoPandas source license

At both pinned revisions:
- Buggy base: `c36eba059f6170715b63a9aa065817c64025d263`
- Fixed PR head: `b3259ce23a37abd32650d7df098f3cdc8c4bb261`

The repository contains `LICENSE.txt`, and `pyproject.toml` declares `BSD 3-Clause`. The license file has the same Git blob at both revisions:

- `LICENSE.txt` blob SHA-1: `028603be2080134aa4817ed691fec3f449ffa609`
- `pyproject.toml` blob SHA-1: `7e423f8efebdcdf2f11e71ca9aff4ff31b3edf8a`

Pinned source links:
- [Base LICENSE.txt](https://github.com/geopandas/geopandas/blob/c36eba059f6170715b63a9aa065817c64025d263/LICENSE.txt)
- [Fixed LICENSE.txt](https://github.com/geopandas/geopandas/blob/b3259ce23a37abd32650d7df098f3cdc8c4bb261/LICENSE.txt)
- [Base pyproject.toml](https://github.com/geopandas/geopandas/blob/c36eba059f6170715b63a9aa065817c64025d263/pyproject.toml)

BSD 3-Clause requires retention of the copyright notice, conditions and disclaimer for source redistributions, and reproduction of them for binary redistributions. It also contains a non-endorsement condition. The Stage 2 archive contains only the project identity, commit references, logs and result metadata—not GeoPandas source code or binaries—so this audit found no GeoPandas source/binary redistribution inside that Stage 2 ZIP.

The row-audit ZIP does contain patch/test-patch diffs from the GeoPandas repository. Treat that artifact separately from the Stage 2 execution ZIP; do not omit the BSD notice/conditions/disclaimer if redistributing the code diffs in a form that constitutes source redistribution. This report does not decide the legal characterization of a dataset patch field.

## 4. GitHub issue and PR discussion snapshots

The E2 snapshot `E2_ISSUE_DISCUSSION_SOURCE_SNAPSHOT_V0_1.json` stores verbatim bodies of three issue comments:
- `2943137874` — maintainer's explanation of `np.nan` as a float;
- `2944863844` — reporter's follow-up observations;
- `2945606056` — maintainer's geometry-sanitization comment.

The E1 snapshot `E1_PR_REVIEW_SUGGESTION_SOURCE_SNAPSHOT_V0_1.json` stores the exact PR review suggestion `2130293780`, including the proposed predicate.

These are GitHub user-generated comments, not GeoPandas source files. The inspected snapshots record authors, timestamps, upstream URLs and body hashes, but do not record an explicit content-license grant. The repository's BSD license must not be assumed to cover these comments.

**Handling recommendation:** retain URLs, authors, timestamps, hashes and concise factual paraphrases for auditability. For a public report, quote only the minimum text necessary for analysis, attribute the speaker and link the original discussion. Obtain permission or a jurisdiction-specific legal review before reproducing full comment bodies or presenting them as separately licensed content. Do not delete or rewrite the frozen tier evidence silently; any future redacted/public derivative must be versioned separately and must preserve the original hashes and audit trail.

## 5. Stage 2 execution archive

Second verified repeat:
- Workflow run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/44936142633
- Artifact ID: `14719339097`
- Artifact SHA-256: `eda44a04658c9250e4fa559c824a512ec4a91e7ff3f8595db0379db9c9ecd41e`
- ZIP CRC: pass
- Internal SHA-256 checks: 17/17 pass

The archive contains 18 entries: result/log files, source-provenance metadata, runner metadata, `requirements.lock`, environment freeze and `SHA256SUMS`. It contains no GeoPandas source file, no upstream issue/PR snapshot, no dependency wheel or source distribution, and no dependency license/NOTICE files.

Thus, based on the inspected archive contents, the Stage 2 artifact is an execution-evidence bundle rather than a software redistribution bundle.

## 6. Pinned dependency inventory and reproducibility limitation

The lock contains 18 pinned distributions:

| Distribution | Version |
|---|---:|
| certifi | 2025.6.15 |
| iniconfig | 2.1.0 |
| numpy | 1.26.4 |
| packaging | 25.0 |
| pandas | 2.2.3 |
| pip | 25.1.1 |
| pluggy | 1.6.0 |
| Pygments | 2.19.2 |
| pyogrio | 0.11.0 |
| pyproj | 3.7.1 |
| pytest | 8.3.5 |
| python-dateutil | 2.9.0.post0 |
| pytz | 2025.2 |
| setuptools | 80.9.0 |
| shapely | 2.1.1 |
| six | 1.17.0 |
| tzdata | 2025.2 |
| wheel | 0.45.1 |

The lock records package names and versions but has no per-distribution SHA-256 hashes and no SPDX license identifiers. The uploaded Stage 2 archive likewise does not contain wheel hashes, package license texts, an SPDX SBOM, or a complete third-party NOTICE bundle. Therefore:

- Exact package versions were pinned and the observed freeze matched the lock.
- This is **not** a byte-for-byte package-artifact lock.
- This audit does **not** certify the license of every pinned distribution or of bundled native components (for example, native geospatial libraries carried by platform wheels).
- No dependency package files were found inside the Stage 2 artifact; the environment was installed for execution and the artifact retains only the inventory/metadata.

A future reproducibility enhancement may add per-wheel hashes and a generated SPDX SBOM/third-party license inventory in a separately versioned audit. Do not retroactively describe the existing Stage 2 run as hash-locked at the package-artifact level.

## 7. Final audit table

| Area | Finding | Status |
|---|---|---|
| Dataset repository license | Hub card declares CC BY 4.0; pinned revision recorded | Identified; attribution required |
| Frozen row source license field | BSD-3-Clause | Identified; do not conflate with dataset license |
| GeoPandas source repository | BSD 3-Clause at base and fix revisions | Identified; notice retention needed for source redistribution |
| Row-audit ZIP | Contains full row, problem statement, patch and test_patch | Redistribution status requires separate review |
| E1/E2 GitHub comments | Verbatim comment bodies captured; explicit license grant not found in inspected snapshots | Rights status unresolved |
| Stage 2 ZIP | Logs/metadata/lock only; no source or package binaries | No software package redistribution detected in this archive |
| Dependency license inventory | Versions pinned, license texts/SPDX IDs absent | Incomplete |
| Dependency artifact integrity | Version lock only; no wheel hashes | Reproducibility limitation |
| Model inference / training | Not performed | Unchanged |
| Final case acceptance | Not decided | HOLD |

## 8. Decision and next gate

1. Keep GeoPandas #3591 in **HOLD**. The technical Stage 2 result remains passed; this audit does not change it.
2. Do not alter the frozen E1/E2/E3 semantic packet contents or their hashes as part of this audit.
3. Do not add the candidate to the accepted registry yet.
4. Before external publication, create a separately versioned public-facing derivative that uses attribution, links and paraphrase rather than wholesale reproduction of comments/patch payloads; include the relevant BSD notice if source diffs are redistributed.
5. If the study later distributes its execution environment, generate a hash-locked requirements file and an SPDX SBOM/third-party license notice inventory for the exact platform artifacts, including bundled native components.
6. Only after the documentary/publication scope is resolved should the project lead make a separate final case-acceptance decision.

**No model was loaded; no inference, fine-tuning or training was performed.**
