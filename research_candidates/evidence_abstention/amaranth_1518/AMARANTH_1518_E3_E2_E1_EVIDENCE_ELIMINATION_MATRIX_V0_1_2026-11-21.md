# Amaranth #1518 — E3/E2/E1 evidence-elimination matrix

**Date:** 21 November 2026  
**Candidate:** amaranth-lang/amaranth issue #1518 / fix PR #1519  
**Dataset row:** amaranth-lang__amaranth-1519  
**Status:** SOURCE- AND ARTIFACT-AUDITED ADVISORY MATRIX; E3 SAMPLE-SUITABILITY RISK FLAGGED; NOT PROJECT-LEAD APPROVED; CASE NOT ACCEPTED

## 1. Purpose and conclusion

This matrix applies the strengthened tier criterion: E2 must eliminate at least one predeclared alternative explanation while leaving at least two plausible mechanisms unresolved.

**E2 meets this criterion.** A direct RTLIL reproducer emits literal opening and closing braces through Print, without a data.Struct, format placeholder, Yosys, or Verilog conversion. The exact buggy base emits single braces where doubled braces are required; the same reproducer passes on the exact fixed revision. The frozen dataset selector confirms the same behavior. This eliminates a Struct-only explanation, a Yosys-only explanation, and a placeholder-argument explanation. E2 does not yet locate the exact internal source step; alternatives concerning literal-chunk construction and later RTLIL normalization remain open.

**E3 carries a material clue-leakage risk.** The reporter explicitly suggests that braces need escaping. This must remain visible. E3 ABSTAIN is defensible only if the rubric requires a source-backed causal location and treats the reporter's proposed fix as an unverified hypothesis rather than an established mechanism. The project lead must review whether this is suitable for the primary abstention sample.

## 2. Frozen provenance

- Issue: https://github.com/amaranth-lang/amaranth/issues/1518
- Fix PR: https://github.com/amaranth-lang/amaranth/pull/1519
- Exact buggy base: 8c5ed4051dd74a6347af8d52f8e397eb53218ac4
- Exact fixed PR head: 6a10abe6c873e7fb51a34f70801d3dd37cda9061
- Merge commit: e30d822a7d93ee615e70e95a9958051dcc794802
- Issue created: 2024-09-20T13:41:02Z
- PR created: 2024-09-20T14:00:49Z
- Dataset revision: fb9aa226b2ce37c708ea7732e7b980abacdadb67
- Dataset instance: amaranth-lang__amaranth-1519
- Dataset-row created_at: 2024-09-20 14:00:49
- Canonical dataset-row SHA-256: 73be38d692dd5426e755184998fabfa2f0a612cef244bfb75ba5d58ec352c4c7
- Frozen selector: tests/test_back_rtlil.py::PrintTestCase::test_escape_curly
- Independent reproducer: research_candidates/evidence_abstention/reproduction/amaranth_issue_1518/test_issue_1518.py
- Exact-base amaranth/back/rtlil.py blob: cecb11f0f591bcbf4db0f8bf3af3a0e49601c0e9
- Fixed amaranth/back/rtlil.py blob: 28f428c1aa4e1a5140287601553c1114f6f4820a

## 3. Stage 2 artifact integrity

- Workflow run/job/artifact: 44111403900 / 134137814116 / 14340976999
- Artifact size: 11,494 bytes
- Outer SHA-256: f3a1a146bd055eb064f3b043c340c74d584351f22569805de63eaf44492ba5ff
- Artifact was independently downloaded; recomputed outer SHA-256 matched GitHub.
- ZIP CRC: PASS; internal SHA256SUMS: 14/14 PASS.
- Exact runtime: Python 3.11.9 with pinned Amaranth RTLIL dependencies and pytest.

Independent reproducer result: exact buggy base produced unescaped single braces and failed the assertion; the identical test passed on the exact fixed revision (1 test). The reproducer calls rtlil.convert directly and does not invoke Yosys.

Frozen selector result: tests/test_back_rtlil.py::PrintTestCase::test_escape_curly failed on the exact buggy base and passed on the exact fixed revision (1 test each).

The independent reproducer and frozen selector are two evidence routes for one Amaranth candidate, not two independent cases.

## 4. Predeclared alternatives

| ID | Alternative explanation | Distinguishing prediction |
|---|---|---|
| G1 | The RTLIL backend copies literal string chunks into the $print FORMAT parameter without escaping braces. | The exact-base source has an unescaped string-chunk branch and joins that content directly into FORMAT. |
| A1 | The defect is limited to data.Struct formatting or placeholder expansion. | A direct Print of literal braces, without Struct or placeholders, would pass. |
| A2 | The downstream Yosys or Verilog conversion path alone rejects otherwise-correct RTLIL. | A direct RTLIL output test, without Yosys, would produce a correct FORMAT value. |
| A3 | Placeholder parsing or argument-width/type conversion causes the failure. | A zero-argument literal Print test would pass if placeholder processing were required. |
| A4 | A later RTLIL parameter-normalization or serialization step loses escaping; the bug is not in emit_print string-chunk construction. | E2 can show raw braces at the RTLIL output boundary, but E1 source tracing is required to locate the responsible step. |

These are competing explanations, not claims of equal probability.

## 5. E3 → E2 → E1 evidence-elimination matrix

| Evidence / alternative | E3 | E2 | E2 disposition | E1 |
|---|---|---|---|---|
| G1: unescaped literal string chunk | Plausible, but exact source location is not shown. | Direct literal braces generate single braces in RTLIL, not the doubled form required by the RTLIL FORMAT grammar. | Remains plausible, not source-located. | Exact source shows string chunks appended unchanged, then joined into FORMAT. |
| A1: Struct-only / placeholder-only defect | Live from the reported Format(''{}'', data.Struct) example. | Direct Print('{') and Print('}') with no Struct or placeholder still reproduce. | Eliminated as the sole explanation. | The failing code path is the general string-chunk branch, separate from the placeholder branch. |
| A2: Yosys / Verilog-only defect | Live from the reported downstream YosysError. | rtlil.convert output itself contains the incorrect FORMAT parameter; the reproducer does not run Yosys. | Eliminated as the sole explanation. | The wrong parameter is constructed before any external Yosys conversion. |
| A3: placeholder argument conversion | Live from the reported Format(''{}'', a) case. | Zero-argument literal Print still reproduces the issue. | Eliminated as the sole explanation. | The literal string-chunk and non-string placeholder paths are separate source branches. |
| A4: later parameter normalization or serialization | Live. | E2 shows the output but not the exact internal line that formed it. | Still live at E2. | Source trace locates the unescaped append in emit_print, before the FORMAT parameter is joined. |

Surviving mechanism sets:
- E3: {G1, A1, A2, A3, A4}
- E2: {G1, A4}
- E1: {G1}

E2 therefore eliminates at least three predeclared alternatives while leaving two plausible internal mechanisms unresolved.

## 6. E1 exact-base source chain

Pinned source: https://github.com/amaranth-lang/amaranth/blob/8c5ed4051dd74a6347af8d52f8e397eb53218ac4/amaranth/back/rtlil.py

At the exact buggy base, RTLILBuilder.emit_print performs this sequence:
1. Lines 1129–1133 initialize a format list and iterate over cell.format.chunks.
2. Lines 1134–1135 handle string chunks with format.append(chunk); literal braces are not transformed.
3. The non-string branch at lines 1136 onward handles typed placeholders and generated substitution specifiers. The no-argument literal-brace reproducer does not enter this branch.
4. Lines 1187–1190 join the list into the $print FORMAT parameter.

The fixed PR changes the string branch to replace each literal opening brace with a doubled opening brace and each closing brace with a doubled closing brace. That fixed implementation is hidden technical-gold evidence only and must not be included in model-visible diagnostic packets.

## 7. E3 clue leakage and sample suitability

The issue author includes the generated RTLIL FORMAT string, the Yosys “Unexpected character in format substitution” error, and the hypothesis that the braces enclosing the Struct are the problem and need escaping. Preserve that hint in the E3 packet. Do not remove or paraphrase it away to manufacture uncertainty.

E3 ABSTAIN is defensible only if the scoring rubric requires an evidence-backed source-level cause and treats the reporter's suggestion as an unverified hypothesis. If proposing the likely repair is sufficient to count as ANSWER, E3 may be answerable and the candidate may be unsuitable for the primary abstention sample. Project-lead review is required.

## 8. Temporal exposure assessment for the pinned model

The protocol pins Qwen/Qwen2.5-3B-Instruct revision aa8e72537993ba99e69dfaafa59ed015b17504d1.

Chronology checked on 21 November 2026:
- Qwen's official Qwen2.5 announcement is dated 19 September 2024.
- Hugging Face repository history shows the checkpoint weight shards and model index uploaded in commit 3ca5f5b on 17 September 2024, 14:27 UTC.
- The pinned aa8e725 revision is a later repository metadata update dated 25 September 2024, not a fresh weight upload.
- Issue #1518 was opened on 20 September 2024, 13:41:02 UTC; PR #1519 and the dataset-row timestamp are 20 September 2024, 14:00:49 UTC.
- AACL 2026 Table 5 reports an October 2023 knowledge cutoff for Qwen2.5-3B-Instruct. This is a secondary-source report, not a vendor guarantee; the official model card does not provide an exact training-data cutoff.

Interpretation: the issue and fix postdate both the initial public checkpoint upload and public announcement. The reported October 2023 cutoff further lowers the likelihood of issue/PR-specific text contamination. These dates do not prove absence of exposure to pre-existing Amaranth source code, which existed before the issue. Separate issue/patch exposure from prior-source exposure; do not claim all buggy source was absent from pretraining.

References for the chronology:
- Official Qwen announcement: https://qwenlm.github.io/blog/qwen2.5/
- Hugging Face model repository: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct
- November 2026 AACL paper by Hassan et al., “Private Evaluation Protocol: Contamination-Resistant Black-Box Evaluation via Public-Slice Surrogates,” Table 5: https://aclanthology.org/2026.aacl-long.168/ (reports October 2023 cutoff for Qwen2.5-3B-Instruct; this is a secondary-source statement, not a vendor guarantee).

## 9. Decision boundaries

- E2 alternative-elimination criterion: satisfied by the independent reproducer plus the frozen selector.
- E3 ABSTAIN: advisory only; material clue-leakage and primary-sample suitability risk remain.
- E2 ABSTAIN: advisory only; two plausible source-level mechanisms remain before E1.
- E1 ANSWER: advisory only; exact-base emit_print source chain locates G1.
- Project-lead gold/tier decision: pending.
- Project-lead primary-pipeline/debug exposure declaration: pending.
- Project-lead temporal-exposure acknowledgement: pending. Chronology lowers issue/PR-specific exposure likelihood but does not prove pre-existing source absence.
- Exact dataset-card provenance, dependency canonical licenses/notices, and bounded documentary scope: separate open gates.
- Final case acceptance: not accepted; registry inclusion: false.
- Model loading, inference, fine-tuning and training: not performed and not authorized.