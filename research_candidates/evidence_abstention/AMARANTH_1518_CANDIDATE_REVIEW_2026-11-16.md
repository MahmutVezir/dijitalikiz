# amaranth-lang/amaranth issue #1518 — candidate review

**Cohort rank:** 30 of 96 primary candidates  
**Dataset instance:** amaranth-lang__amaranth-1519 (exact row identity to be authenticated)  
**Issue:** https://github.com/amaranth-lang/amaranth/issues/1518  
**Fix PR:** https://github.com/amaranth-lang/amaranth/pull/1519  
**Review status:** source/patch and minimal runtime screen passed; exact dataset selector execution pending. Temporal exposure is close to the model release and must be explicitly reviewed. Not an accepted case.

## 1. Defect contract

Issue #1518 reports that formatting a data.Struct containing braces through Amaranth's Print/Format path produces invalid RTLIL and a YosysError. The source formatter writes literal string chunks directly into the RTLIL format parameter. RTLIL uses braces as structural delimiters, so literal braces must be escaped.

PR #1519 changes string-chunk handling to replace each literal opening brace with double opening braces and each closing brace with double closing braces. It adds a regression test that emits Print("{") and Print("}") and asserts the escaped RTLIL format strings.

The independent reproducer builds a minimal Module with literal brace prints and checks the exact escaped RTLIL format parameters. It does not invoke Yosys or require an external toolchain.

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

The workflow records installed distribution license metadata before source execution. This is a narrow screen for the RTLIL-only test environment, not blanket clearance for optional Yosys/remote-build extras or redistribution.

## 4. Dataset selector requirement

The workflow authenticates the exact Parquet row amaranth-lang__amaranth-1519, records its canonical row hash and FAIL_TO_PASS selectors, applies the exact PR diff to the buggy base, and runs every selector on both base and fixed revisions. Base failures must be caused by unescaped literal braces; fixed selectors must pass.

## 5. Temporal exposure caution

The issue and PR were created on 2024-09-20, immediately after the public September 2024 release window of the pinned Qwen2.5-3B-Instruct family. This is not enough to prove the issue was absent from training data. The exact model revision's training-data cutoff and release chronology must be checked before this case is accepted. The student researcher has also reviewed the issue and patch during candidate screening; perfect blinding must not be claimed.

## 6. Current decision

Issue/patch alignment: strong.  
Independent RTLIL reproducer: prepared; workflow pending.  
Dataset FAIL_TO_PASS selectors: pending exact-row authentication and execution.  
Minimal dependency/license inventory: pending workflow evidence and human review.  
Temporal exposure: elevated caution due close release timing.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading/inference authorization: false.
