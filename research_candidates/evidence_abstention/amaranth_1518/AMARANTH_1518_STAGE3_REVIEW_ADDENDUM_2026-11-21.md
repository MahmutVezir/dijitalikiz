# Amaranth #1518 — Stage 3 review addendum

**Date:** 21 November 2026  
**Candidate:** amaranth-lang/amaranth issue #1518 / fix PR #1519  
**Dataset instance:** amaranth-lang__amaranth-1519  
**Disposition:** Stage 2 technical reproduction and artifact integrity passed; source-aware E3/E2/E1 matrix and model temporal-exposure screen prepared; project-lead gold/tier, exposure, sample-suitability, and final acceptance decisions pending.

## 1. Stage 2 technical gate

- Exact buggy base: 8c5ed4051dd74a6347af8d52f8e397eb53218ac4
- Exact fixed PR head: 6a10abe6c873e7fb51a34f70801d3dd37cda9061
- Dataset row: amaranth-lang__amaranth-1519
- Dataset revision: fb9aa226b2ce37c708ea7732e7b980abacdadb67
- Dataset row SHA-256: 73be38d692dd5426e755184998fabfa2f0a612cef244bfb75ba5d58ec352c4c7
- Workflow run/job/artifact: 44111403900 / 134137814116 / 14340976999
- Artifact SHA-256: f3a1a146bd055eb064f3b043c340c74d584351f22569805de63eaf44492ba5ff
- Artifact was independently downloaded; outer SHA-256 recomputed and matched GitHub; ZIP CRC PASS; internal SHA256SUMS 14/14 PASS.
- Python 3.11.9; pinned minimal RTLIL runtime and test dependencies.

Independent reproducer creates a Module with Print("{") and Print("}") and calls rtlil.convert directly. On the exact base it observes unescaped single braces in the $print FORMAT parameter and fails the expected doubled-brace assertion; the same reproducer passes on the exact fixed PR head (1 test).

The exact dataset selector tests/test_back_rtlil.py::PrintTestCase::test_escape_curly also fails on the exact base and passes on the exact fixed PR head (1 test). This selector and reproducer are two evidence routes for one candidate, not two independent cases.

## 2. Stage 3 source-aware evidence review

- Gold proposal: G1 — literal string chunks in RTLIL emit_print are appended into $print FORMAT without escaping structural braces.
- Matrix: AMARANTH_1518_E3_E2_E1_EVIDENCE_ELIMINATION_MATRIX_V0_1_2026-11-21.md.
- Proposal: AMARANTH_1518_SOURCE_AWARE_GOLD_AND_EVIDENCE_TIERS_PROPOSAL_V0_1_2026-11-21.md.
- E2 eliminates Struct-only, downstream Yosys-only, and placeholder-argument-only explanations, while leaving G1 and a later RTLIL parameter-normalization explanation unresolved. E2 therefore meets the strengthened alternative-elimination criterion.
- E1 exact-base source lines show emit_print appends literal string chunks unchanged and later joins them into the $print FORMAT parameter.
- E3 issue narrative includes the reporter's suggestion that braces need escaping. This is a material answer-leakage risk: E3 ABSTAIN requires the scoring rubric to demand a source-backed mechanism rather than a likely repair. Project-lead sample-suitability review is required.

## 3. Temporal model exposure

Temporal review: AMARANTH_1518_TEMPORAL_EXPOSURE_REVIEW_2026-11-21.md.

The exact checkpoint weights and index were publicly uploaded in HF commit 3ca5f5b on 17 September 2024; Qwen announced Qwen2.5 on 19 September 2024; the issue and fix PR were created on 20 September 2024. A November 2026 AACL paper reports an October 2023 knowledge cutoff for Qwen2.5-3B-Instruct. This lowers the likelihood of issue/PR-specific training exposure but does not establish that pre-existing Amaranth source code was absent from training. Project-lead acknowledgement remains pending.

## 4. Independence, exposure and open gates

- One issue, one fix PR, one frozen selector, one upstream project. The independent reproducer is not a second case.
- Issue #1518 has no comments in the retrieved issue-comment list. PR #1519 has one approval review asking for a backport. This is limited issue-family screening, not an exhaustive repository-wide defect-family audit.
- Researcher source exposure: full. No blind adjudication or inter-rater reliability claim.
- Project-lead prior pipeline/debug exposure declaration: pending.
- Project-lead source-aware G1 and E3/E2/E1 decision: pending.
- Project-lead E3 primary-sample suitability review: pending.
- Project-lead temporal-exposure acknowledgement: pending.
- Exact pinned dataset-card bytes, dependency canonical licenses/notices, and bounded documentary research scope: pending.
- Schema-conformant proposed case record and fail-closed validation: pending.
- Separate final project-lead YES/NO case acceptance: pending.
- Final case acceptance: not accepted; registry inclusion: false.
- Model loading, inference, fine-tuning and training: not performed and not authorized.