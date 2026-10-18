# Public Archive Provenance Inventory

**Audit date:** 2026-10-18  
**Audited revision:** `8d65597ae82dab3852bc5c5e1a43747d31528b2d`  
**Scope:** Tracked ZIP archives and the distinction between source-code licensing and rights to redistribute issue text, artifacts, and derived research records.

## Finding

The repository tree at the audited revision contains two ZIP archives at its root. The repository tree does not contain a root-level `LICENSE` or `COPYING` file. This inventory is a conservative release gate; it is **not** a legal conclusion that either archive infringes copyright or cannot be used for research.

| Tracked archive | Git blob SHA | Size in Git tree | Content / redistribution status |
|---|---|---:|---|
| `RSC-Bench-pilot-v1.0-stage4-gated.zip` | `f7ffd3a6ad44eb5b15a421bd052375f23924d34c` | 89,753 bytes | Member-by-member licensing/provenance inventory not established by this tree audit; public redistribution status unresolved. |
| `rsc-bench-v0.1.zip` | `6ebd3e43f6ff59ef5cc41bc328921acb43e10988` | 38,288 bytes | Member-by-member licensing/provenance inventory not established by this tree audit; public redistribution status unresolved. |

The ZIP contents were not extracted or legally reviewed as part of this audit. Do not infer that the source-code licenses for the upstream projects automatically cover GitHub issue/PR discussion, test fixtures, model outputs, derived records, or an entire bundled archive.

## Required release checks

Before redistributing either archive or using its contents in a public submission bundle:

1. Extract each archive into an isolated temporary directory; record archive SHA-256, ZIP CRC/integrity, complete member paths, file sizes, and per-file SHA-256.
2. Identify every upstream project and exact revision represented by the files. Record the applicable source-code license and required copyright/NOTICE text for each project.
3. Classify member content separately: source code, tests, issue/PR text, logs, model prompts/outputs, derived labels/graphs, metadata, and generated reports.
4. For issue/PR text and other non-code content, identify an explicit license or other documented permission. Do not treat the repository's code license, public accessibility, or a successful test as permission to redistribute every type of content.
5. Check whether each member is necessary for the research result. Prefer a minimal evidence manifest and links to upstream sources over bundling unnecessary third-party text.
6. Record exclusions and their reasons. If permission remains unresolved, keep the affected content out of public redistribution packages; do not delete or rewrite the frozen historical record solely to make the audit pass.
7. Have the project owner or an appropriately qualified adviser review the resulting inventory before publication or submission.

## Research integrity constraints

- Preserve the frozen pilot and confirmatory outputs, their manifests, and historical hashes unchanged.
- Keep source-code license, content redistribution rights, model-output rights, data provenance, and contamination risk as separate questions.
- Public issue/PR text can prime a blind reviewer. Reviewers should inspect pinned source revisions and named tests before opening public issue discussions or existing reproduction logs.
- Do not claim that a candidate is eligible for the future held-out set based only on a passing red/green test. Independent source review and separate adjudication remain required.
- This inventory does not authorize model inference, Kaggle/GPU execution, or changes to protocol readiness.

## Current disposition

**Status: pending content-level inventory and rights review.** No archive was removed, rewritten, or republished by this audit. No legal permission or infringement conclusion is asserted.
