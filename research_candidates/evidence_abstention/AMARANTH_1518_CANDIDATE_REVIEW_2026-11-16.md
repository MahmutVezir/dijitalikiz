# amaranth-lang/amaranth issue #1518 — candidate review

**Cohort rank:** 30 of 96 primary candidates  
**Dataset instance:** amaranth-lang__amaranth-1519 (exact row identity to be authenticated)  
**Issue:** https://github.com/amaranth-lang/amaranth/issues/1518  
**Fix PR:** https://github.com/amaranth-lang/amaranth/pull/1519  
**Review status (updated 21 Nov 2026):** Stage 2 independent reproducer and exact dataset selector executed; buggy-base fail / fixed-revision pass. Stage 2 archive independently downloaded and integrity-checked. Source-aware E3/E2/E1 matrix and temporal-exposure screen prepared. Project-lead gold/tier, E3 sample-suitability, prior-exposure and temporal acknowledgement decisions remain pending. Not an accepted case.

## 1. Defect contract

Issue #1518 reports that formatting a data.Struct containing braces through Amaranth's Print/Format path produces invalid RTLIL and a YosysError. The source formatter writes literal string chunks directly into the RTLIL format parameter. RTLIL uses braces as structural delimiters, so literal braces must be escaped.

PR #1519 changes string-chunk handling to replace each literal opening brace with double opening braces and each closing brace with double closing braces. It adds a regression test that emits Print("{") and Print("}") and asserts the escaped RTLIL format strings.

The independent reproducer builds a minimal Module with literal brace prints and checks the exact escaped RTLIL format parameters. It does not invoke Yosys or require an external toolchain. On the exact buggy base it fails because the RTLIL FORMAT values contain single braces; the same reproducer passes on the exact fixed revision (1 test).

## 2. Pinned source identity

- Repository: amaranth-lang/amaranth
- Buggy base: 8c5ed4051dd74a6347af8d52f8e397eb53218ac4
- Fixed PR head: 6a10abe6c873e7fb51a34f70801d3dd37cda9061
- Issue #1518 created: 2024-09-20T13:41:02Z
- PR #1519 created: 2024-09-20T14:00:49Z
- Exact-base LICENSE.txt Git blob: cb522426f79b987ad57f265b639a3f6c28214e04
- Exact-base pyproject.toml Git blob: 2f0c4dbb709ebeb6326ba2031a5604ffabc78260
- Exact-base rtlil.py Git blob: cecb11f0f591bcbf4db0f8bf3af3a0e49601c0e9
- Fixed rtlil.py Git blob: 28f428c1aa4e1a5140287601553c1114f6f4820a
- Exact-base license declaration: BSD-2-Clause.

## 3. Reproduction and dependency scope

The minimal test imports Amaranth's Python RTLIL backend and emits RTLIL text. It does not invoke Yosys, access the network, or use external fixtures. The pinned environment contains the declared runtime dependencies jschon, pyvcd, and Jinja2 plus pytest and transitive metadata.

The workflow records installed distribution license metadata before source execution. The inventory includes jschon 0.11.1 (MIT), pyvcd 0.4.0 (MIT), MarkupSafe 3.0.2 (BSD-3-Clause), rfc3986 2.0.0 (Apache 2.0), pytest 8.3.3 (MIT), iniconfig 2.0.0 (MIT), pluggy 1.5.0 (MIT), Pygments 2.18.0 (BSD-2-Clause), and metadata gaps for Jinja2 3.1.4 and packaging 24.2 despite BSD/Apache/BSD classifiers. PyArrow 19.0.1 used only for dataset extraction reports Apache Software License. Canonical Jinja2/packaging license files and applicable notices remain to be reviewed. This is a narrow screen for the RTLIL-only test environment, not blanket clearance for optional Yosys/remote-build extras or redistribution.

## 4. Dataset selector and artifact integrity

The workflow authenticated the exact Parquet row amaranth-lang__amaranth-1519. Canonical row SHA-256: 73be38d692dd5426e755184998fabfa2f0a612cef244bfb75ba5d58ec352c4c7. Its sole FAIL_TO_PASS selector, tests/test_back_rtlil.py::PrintTestCase::test_escape_curly, failed on the exact buggy base and passed on the exact fixed revision (1 test each).

Stage 2 workflow run/job/artifact: 44111403900 / 134137814116 / 14340976999. Artifact size 11,494 bytes; outer SHA-256 f3a1a146bd055eb064f3b043c340c74d584351f22569805de63eaf44492ba5ff. It was independently downloaded; outer digest matched GitHub; ZIP CRC passed; internal SHA256SUMS 14/14 passed.

## 5. Temporal exposure caution

A separate source-backed chronology screen is recorded at:
research_candidates/evidence_abstention/amaranth_1518/AMARANTH_1518_TEMPORAL_EXPOSURE_REVIEW_2026-11-21.md.

The exact pinned checkpoint weights and index were uploaded in Hugging Face commit 3ca5f5b on 17 September 2024 at 14:27 UTC. Qwen announced Qwen2.5 on 19 September 2024. Issue #1518 was created on 20 September 2024 at 13:41:02 UTC, with PR #1519 at 14:00:49 UTC. A November 2026 AACL paper reports October 2023 as the Qwen2.5-3B-Instruct knowledge cutoff (secondary-source statement, not a vendor guarantee). This chronology reduces the likelihood of issue/PR-specific training exposure; it does not establish that pre-existing Amaranth source code was absent from training. Project-lead acknowledgement remains pending.

The student researcher has reviewed the issue and patch during candidate screening; researcher source exposure is full. Perfect blinding must not be claimed.
## 6. Current decision and Stage 3 gates

- Technical Stage 2: passed; independent reproducer and exact frozen selector fail on buggy base / pass on fixed revision.
- Stage 2 archive: independently verified (outer SHA-256 match; ZIP CRC PASS; 14/14 internal hashes).
- Gold proposal: G1 — literal string chunks in RTLIL emit_print are appended into $print FORMAT without brace escaping.
- Evidence matrix: E2 eliminates Struct-only, Yosys-only, and placeholder-only explanations while leaving G1 and later RTLIL parameter normalization alive; E1 source locates G1.
- E3 sample suitability: issue reporter explicitly proposes escaping braces; project-lead review required to determine whether this remains a valid primary abstention case under the evidence-supported-diagnosis rubric.
- Project-lead gold/tier approval: pending.
- Project-lead prior pipeline/debug exposure declaration: pending.
- Project-lead temporal-exposure acknowledgement: pending.
- Dependency canonical licenses/notices and exact pinned dataset-card provenance: pending human review.
- Bounded documentary research scope: pending.
- Final case acceptance: not accepted; registry inclusion false.
- Model loading/inference authorization: false.
