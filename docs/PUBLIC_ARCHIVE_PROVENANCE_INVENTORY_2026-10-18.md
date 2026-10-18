# Public Archive Provenance Inventory

**Audit date:** 2026-10-18  
**Audited repository revision:** `8d65597ae82dab3852bc5c5e1a43747d31528b2d`  
**Scope:** Two ZIP archives tracked at repository root; archive structure, integrity, embedded source references, and the distinction between source-code licensing and rights to redistribute issue text, artifacts, and derived research records.

## Findings

The repository tree at the audited revision contains two ZIP archives at its root and no root-level `LICENSE` or `COPYING` file. Both ZIPs passed their built-in CRC check when inspected from the available repository snapshot. Neither ZIP contains a file named `LICENSE`, `LICENCE`, `COPYING`, or `NOTICE` (case-insensitive exact-name scan).

This is a conservative release gate; it is **not** a legal conclusion that either archive infringes copyright or cannot be used for research.

| Tracked archive | Git blob SHA | Git tree size | Extracted archive SHA-256 | Files | CRC check | Rights status |
|---|---|---:|---|---:|---|---|
| `RSC-Bench-pilot-v1.0-stage4-gated.zip` | `f7ffd3a6ad44eb5b15a421bd052375f23924d34c` | 89,753 bytes | `2efdd7cbcb0c2b14b399a0788cddf5f2afb90efb78da6b91931f8f550c6ed259` | 79 | Pass | Member-level license/provenance review still required |
| `rsc-bench-v0.1.zip` | `6ebd3e43f6ff59ef5cc41bc328921acb43e10988` | 38,288 bytes | `bd6e31303f8afb64534a287b9839d0377825f0c67551bd4da97aaf8a7a06fdd0` | 65 | Pass | Member-level license/provenance review still required |

The ZIP member counts exclude directory entries. Archive SHA-256 values are computed over the exact nested ZIP bytes recovered from the available repository snapshot; Git blob SHA values are separate identifiers and are not SHA-256 checksums.

## Content-level observations

### `RSC-Bench-pilot-v1.0-stage4-gated.zip`

- Contains the RSC-Bench pilot repository, including experiment code, prompt templates, schemas, source notes, pilot cases, ground-truth labels, and CCDG records.
- Contains four public Supabase technical-source references in the pilot data: Supabase issue #35459, Supabase issue #47835, Supabase discussion #40671, and Supabase Storage issue #1109.
- Contains 25 cache/compiled files under `__pycache__` or `.pytest_cache`; these are not needed as canonical source evidence and should be excluded from any newly prepared release package.
- No exact-name license/notice file was found inside the archive.

### `rsc-bench-v0.1.zip`

- Contains an earlier pilot scaffold, including a synthetic fixture marked with `example.invalid`, schemas, prompts, code, and tests.
- Contains 20 cache/compiled files under `__pycache__` or `.pytest_cache`; these should be excluded from any newly prepared release package.
- No exact-name license/notice file was found inside the archive.
- Its contents overlap substantially with the later pilot scaffold; the precise intended archival role and whether it must remain a public downloadable bundle should be documented by the project owner. Do not silently replace or delete this historical file.

## Licensing and redistribution interpretation

Do not infer that upstream source-code licenses automatically cover GitHub issue/PR discussion, test fixtures, model outputs, derived labels/graphs, or an entire bundled archive. Public accessibility and successful red/green tests are not, by themselves, evidence of permission to redistribute all content types.

The audit confirms embedded source URLs and file inventory; it does not independently verify the current license/terms of every upstream project, issue, discussion, or third-party file. No infringement finding is made.

## Required release checks

Before redistributing either archive or using its contents in a public submission bundle:

1. Identify every upstream project and exact revision represented by each source/test file. Record applicable code licenses and required copyright/NOTICE text.
2. Classify each member separately: original project code, copied source/test content, issue/PR text, logs, model prompts/outputs, derived labels/graphs, metadata, and generated reports.
3. For issue/PR text and other non-code content, identify an explicit license or documented permission. If permission remains unresolved, do not include that content in a new public bundle.
4. Check whether each member is necessary. Prefer a minimal provenance manifest and links to upstream sources over bundling unnecessary third-party content or caches.
5. Record exclusions and reasons. Preserve frozen historical artifacts and hashes; do not rewrite the historic result just to make this audit pass.
6. Have the project owner or an appropriately qualified adviser review the inventory before publication or submission.

## Research integrity constraints

- Preserve frozen pilot and confirmatory outputs, their manifests, and historical hashes unchanged.
- Keep source-code license, content redistribution rights, model-output rights, data provenance, and contamination risk as separate questions.
- Public issue/PR text can prime a blind reviewer. Reviewers should inspect pinned source revisions and named tests before opening public issue discussions or existing reproduction logs.
- A passing red/green test does not establish that a candidate's root cause or every CCDG edge is correct, or that the candidate is eligible for the future held-out set.
- This inventory does not authorize model inference, Kaggle/GPU execution, or changes to protocol readiness.

## Current disposition

**Status: content inventory partially completed; rights review pending.** The two ZIP structures, file counts, archive hashes, CRC checks, license/notice filename scan, and embedded source URLs were inspected. No archive was removed, rewritten, or republished. No legal permission or infringement conclusion is asserted.
