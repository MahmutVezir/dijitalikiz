# simpeg/simpeg#1633 — documentary source-license screen (16 November 2026)

**Status: no obvious prohibition identified for research use; not legal advice or formal legal clearance.** This is a source-license screen only, not case acceptance.

## Pinned identity

- Dataset instance: `simpeg__simpeg-1633`
- Upstream PR: https://github.com/simpeg/simpeg/pull/1633
- Dataset/base commit: `f2440e63c6ab92191ae4f452808a9e4169af84e3`
- PR head: `77a41d3fe25e3ea881ff9ca0be88d9ba0d3b7410`

## Root license at the exact base commit

- File: `LICENSE`
- Git blob SHA-1: `cd67a7669e3e768bb03686567ec0c3088d79560d`
- Content SHA-256: `550328033a0e8ecdb533739b9f4bb7b85881d081c470d57a500df73739d92fb1`
- SPDX expression: MIT
- The license grants broad use, modification, and distribution subject to retaining the copyright and permission notice.
- The exact-base repository tree contains `LICENSE` and `pyproject.toml`; no root `NOTICE`, `COPYING`, or `COPYRIGHT` file was found by the tree query.

## Changed-file scope

The PR changes five files: three source modules and two test files. The exact PR-head Git blob IDs and documentary observations are recorded in `SIMPEG_1633_CHANGED_FILE_LICENSE_MANIFEST_V0_1.json` (SHA-256: `5ed05695311801a26f5475083ee65e28f787d275a6878779732ed5098327342f`).

No third-party source code or new license text is introduced in the reviewed diff. The changed files inherit the repository-level MIT license unless a later full-file review finds a separate file-specific notice.

## Dependency check

The exact-base `pyproject.toml` (Git blob `3d0efb96d4cfdb17b29ac1a1685bcd37dae77fcd`) already declares `typing_extensions; python_version<'3.13'` as a runtime dependency. The PR uses it only as the compatibility fallback for `warnings.deprecated`; it does not add a new dependency.

## Decision and limitations

- Documentary source-license screen: `no_obvious_prohibition_identified`.
- Root MIT notice retention requirement must be respected in any redistribution of substantial source portions.
- No formal legal opinion was obtained.
- A complete transitive environment license inventory has not been performed.
- Technical reproduction, exact test behavior, independence, gold adjudication, and E1/E2/E3 packet review remain outstanding.

**This record does not accept the case.** It only clears the preliminary root-source-license screen; the case remains a candidate pending all other acceptance gates.
