# CTAPIpe #2732 — source and dependency license screen (draft)

**Candidate:** cta-observatory/ctapipe issue #2730 / PR #2732  
**Pinned buggy base:** `287e7685e0e963f3fb44d92832ca97ac8c265c40`  
**Pinned fixed PR head:** `5007b6ab61887d7555155edb4d1d296603a9735e`  
**Status:** documentary inventory and source-path screen completed; **student project-lead sign-off pending**. This document is not legal advice.

## 1. Exact upstream source and changed files

GitHub identifies the canonical `cta-observatory/ctapipe` repository as not a fork. The exact-base repository license is BSD 3-Clause.

- Root `LICENSE` at the buggy base:
  - Git blob SHA-1: `7d85dda24fa481e24c4b33dd98dbc13245ee1fd2`
  - Content SHA-256: `c6bbc92e621766f4c19c9cd223d377cfa40df0073908da2398b2efbf9e5085b2`
- Exact-base `pyproject.toml` declares `BSD-3-Clause` and is unchanged between the exact base and fixed PR head.
- Root `LICENSE` is unchanged between the exact base and fixed PR head.
- No root `NOTICE` file exists at the pinned base.

The exact PR #2732 changed three paths, and the pinned artifact captured each fixed-revision Git blob and SHA-256:

| Changed path | Fixed Git blob SHA-1 | Content SHA-256 |
|---|---|---|
| `docs/changes/2732.bugfix.rst` | `d5ded894ad8b3b7e03aa6cdc4a4e4c305c0b3218` | `ab478d259346d0620bde9f0ced58461510fd91a5fef3f71f83560665d002fc11` |
| `src/ctapipe/image/muon/features.py` | `f18f1c3f16b41a5e7b1076512296ca8a4efa1c2f` | `b00199158b9e8e23855892a8edbefb7f8c24af4be821a0f377890c13354b9ea3` |
| `src/ctapipe/image/muon/tests/test_muon_features.py` | `b9f44ed8d8254ce3f55c6df79471d071f6de7540` | `1322901eda5a2ff7c7f497c4dcfb3ed86e6b3ec169d5d841735e2bbe8a842f90` |

No individual file license header or third-party notice was found in these three changed paths during this source review. The documentary screen treats them as covered by the repository BSD-3-Clause license. No vendored third-party source was identified in those changed paths. This is a source-path screen, not an independent legal opinion.

## 2. Reproduction environment inventory

The latest successful Stage 2 artifact includes the exact-base root license, a `pip freeze` snapshot, metadata for installed distributions, and captured installed license/notice files.

- Workflow run: `44308927754`
- Job: `134817682862`
- Artifact ID: `14429866192`
- Artifact name: `ctapipe-2732-stage2-base-fixed-44308927754-1`
- ZIP SHA-256: `55b08b31634afcdc052c2f8ef973db35a1fea49c342e9e5974adf386729bbd4f`
- All `136/136` entries listed in `SHA256SUMS.txt` were re-hashed successfully; the ZIP contains 137 files including the checksum file.
- Installed distributions inventoried: **51**
- License/notice files detected from installed-distribution metadata: **106**
- License/notice files copied into artifact: **106**
- Detected files not captured by the 2 MB per-file capture rule: **0**
- `pip check`: `No broken requirements found`
- Python: CPython 3.11.9; NumPy 1.26.4; Astropy 6.1.7; SciPy 1.15.2; Numba 0.60.0; llvmlite 0.43.0; PyTables 3.10.2; pytest 8.3.5; pytest-astropy-header 0.2.2.

The machine-readable inventory is `dependency-license-file-manifest.json` (SHA-256 `51a9b64dfca57fa03a0553e2ad23bb96dcb0f70d85c4a8d263f4a019ee5fa66f`). The separate package metadata inventory is `dependency-license-metadata.json` (SHA-256 `f9151d1e3824a96da76dff15401e4e112a904fd4f25a52c2865903e1e1d3a868`). The root license and its hash file are also retained in the artifact.

## 3. Items requiring careful human review

The inventory is not a single-license list. Some distribution notice files contain bundled or third-party components whose terms differ from the primary package license. Examples identified in the captured notices include:

- **NumPy 1.26.4:** its distribution notice describes bundled OpenBLAS/LAPACK components, and GCC runtime components including libgfortran under GPL-3.0 with the GCC Runtime Library Exception and libquadmath under LGPL-2.1-or-later. The notice also identifies other bundled components under MIT, BSD and Zlib terms.
- **SciPy 1.15.2:** its distribution notice identifies bundled runtime components including libgfortran (GPL-3.0 with GCC exception) and libquadmath (LGPL-2.1-or-later), alongside BSD-licensed and other third-party components.
- **Blosc2 4.15.0:** its installed license tree includes miniexpr/TinyCC, SLEEF, TinyExpr, YYJSON and related notices; some of these have distinct license terms including LGPL and permissive licenses.
- **Docutils 0.21.2:** its COPYING notice says most project files are public domain but lists exceptions, including files with separate BSD/Zope Public License/GPL terms. The inventory does not map each installed Docutils file used by this reproduction to its exception status.
- **llvmlite 0.43.0 / Numba 0.60.0:** third-party license bundles are present, including Apache/LLVM-related notices and additional permissively licensed dependencies.
- **tqdm 4.67.1:** its LICENCE file distinguishes MPL-2.0 coverage from MIT-licensed exceptions.

These are references in package notices, not a conclusion that CTAPIpe source code is relicensed under those terms. This workflow used installed packages for a test environment; the Stage 2 archive contains license/notice texts and logs, not the installed package binaries. Any later redistribution of environment binaries, source bundles, or compiled artifacts would need a separate distribution-specific review.

## 4. Scope and limits

This screen establishes the exact upstream root license, exact changed-file identities, no change to the root license or project license declaration between base and fix, and a reproducible inventory of installed dependency notices. It does **not** establish:

- legal advice or a legal determination for TÜBİTAK/publication;
- complete source provenance for every binary wheel or transitive dependency beyond installed metadata and captured notice files;
- a blanket permission to redistribute dependency binaries or upstream source;
- a conclusion about patent, trademark, attribution, or other non-copyright obligations;
- student project-lead approval.

No upstream source or dependency license was changed in the research repository. This is a research-side audit record only.

## 5. Proposed review decision — not yet approved

**AI-assisted recommendation:** the three PR-changed source files appear to inherit the exact-base repository BSD-3-Clause license, and no obvious license prohibition was identified in this documentary screen for the research use being performed. However, the dependency notices contain bundled/third-party license cases that should remain disclosed. Record the scope limitation as documentary screening only, not legal advice.

**Human project-lead decision:** PENDING. The student project lead must review this inventory and either accept the documentary scope limitation for exploratory research use or hold/exclude the candidate. ChatGPT is not a legal reviewer and cannot supply the human sign-off.
