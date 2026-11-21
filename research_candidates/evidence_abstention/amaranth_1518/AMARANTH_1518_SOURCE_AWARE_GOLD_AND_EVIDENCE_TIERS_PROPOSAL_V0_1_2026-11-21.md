# Amaranth #1518 — source-aware gold and E1/E2/E3 proposal

**Date:** 21 November 2026  
**Candidate:** amaranth-lang/amaranth issue #1518 / fix PR #1519  
**Dataset instance:** amaranth-lang__amaranth-1519  
**Status:** ADVISORY PROPOSAL ONLY — NOT PROJECT-LEAD APPROVED; E3 SAMPLE-SUITABILITY REVIEW REQUIRED; CASE NOT ACCEPTED

## 1. Candidate contract

The reported defect occurs when Amaranth serializes a formatted Print operation containing a data.Struct. The generated RTLIL $print FORMAT parameter contains literal structural braces as single braces; downstream Yosys rejects that format string with “Unexpected character in format substitution”. The reporter hypothesizes that the braces enclosing the Struct need escaping.

PR #1519 changes literal string-chunk handling in the RTLIL emitter to double opening and closing braces before joining those chunks into the $print FORMAT parameter. It also adds a regression test using Print("{") and Print("}").

Scope: one Amaranth defect and one upstream project. The independent reproducer and frozen selector are two evidence routes for this one candidate, not two cases.

## 2. Proposed gold mechanism

**G1 — RTLIL literal string chunks are appended to $print FORMAT without escaping structural braces.**

In the exact buggy base, RTLILBuilder.emit_print iterates through the chunks of the Print format. If a chunk is a plain string, the code appends the chunk unchanged. The accumulated list is joined directly into the $print FORMAT parameter. Literal braces are therefore passed through in the format string instead of escaped into the doubled-brace representation required by the RTLIL/Yosys formatting grammar.

The mechanism is limited to literal string chunks in RTLIL Print/format emission. It does not claim that all formatting failures, all data.Struct serialization failures, or all Yosys format errors share this cause.

## 3. Predeclared alternative explanations

- **A1 — Struct-only / placeholder-expansion defect:** the issue may arise only when a data.Struct placeholder expands into brace-delimited text, rather than from plain literal string chunks.
- **A2 — downstream Yosys or Verilog conversion defect:** RTLIL may be correct and the failure may arise only when Yosys parses the format or when Verilog conversion invokes Yosys.
- **A3 — placeholder argument or width/type conversion defect:** the error may be caused by argument packing or conversion of typed format placeholders, not by raw literal string chunks.
- **A4 — later RTLIL parameter normalization/serialization defect:** the literal string chunk may be preserved correctly by emit_print but altered by a later parameter-processing step before the RTLIL text is returned.

These alternatives are diagnostic hypotheses. They are not claims of equal likelihood.

## 4. Proposed E3/E2/E1 tiers

### E3 — proposed ABSTAIN; material clue-leakage risk

Evidence:
- the full issue narrative, including the Struct example, generated RTLIL excerpt, and downstream Yosys error;
- the reporter's explicit suggestion that the braces enclosing the Struct are likely the problem and need escaping.

The reporter's proposed explanation is unusually close to the repair. It must remain visible in the E3 packet. It cannot be hidden or rewritten to manufacture uncertainty. E3 ABSTAIN is defensible only if the evaluation rubric requires a source-backed causal location and treats the reporter's suggestion as an unverified hypothesis rather than proof of the specific RTLIL emitter mechanism.

If merely proposing the likely repair is sufficient for ANSWER, then E3 may already be answerable and this case may be unsuitable for the primary abstention sample. This suitability decision requires explicit project-lead review.

### E2 — proposed ABSTAIN; strengthened alternative-elimination criterion satisfied

Evidence:
- E3 unchanged;
- exact-base direct RTLIL output from an independent reproducer using only Print("{") and Print("}");
- exact-base frozen dataset selector tests/test_back_rtlil.py::PrintTestCase::test_escape_curly;
- matching fixed-revision pass results for the same reproducer and selector.

The independent reproducer does not instantiate data.Struct, does not use a format placeholder, does not invoke Yosys, and does not convert to Verilog. It directly inspects the RTLIL output. The buggy base emits single-brace FORMAT values; the fixed revision emits doubled-brace values and passes.

This eliminates A1 as a sole explanation (the failure occurs without Struct or placeholders), A2 as a sole explanation (the RTLIL output is already wrong before Yosys), and A3 as a sole explanation (zero-argument literal Print still fails). However, E2 does not expose the internal source location. Both G1 and A4 remain plausible until E1.

### E1 — proposed ANSWER

Evidence:
- E2 unchanged;
- exact buggy-base amaranth/back/rtlil.py source excerpts around RTLILBuilder.emit_print;
- immutable source-line and blob provenance showing that string chunks are appended unchanged and then joined into the FORMAT parameter.

At E1, G1 is distinguished from A4: the unescaped braces are introduced at the literal string-chunk branch itself, not by a later serializer transformation.

Leakage control: do not include the fixed implementation, PR patch, or post-fix source in any model-visible diagnostic packet. Retain the fix only for hidden technical-gold validation.

## 5. Evidence-elimination matrix

The row-by-row matrix is recorded at:

research_candidates/evidence_abstention/amaranth_1518/AMARANTH_1518_E3_E2_E1_EVIDENCE_ELIMINATION_MATRIX_V0_1_2026-11-21.md

Surviving mechanism sets:
- E3: G1, A1, A2, A3, A4.
- E2: G1, A4.
- E1: G1.

E2 therefore removes at least one predeclared alternative while leaving at least two plausible mechanisms unresolved.

## 6. Temporal exposure assessment

The study's pinned model is Qwen/Qwen2.5-3B-Instruct at revision aa8e72537993ba99e69dfaafa59ed015b17504d1.

The pinned revision is a repository metadata update on 25 September 2024. The Hugging Face repository history shows the checkpoint weights and model index were uploaded on 17 September 2024 at 14:27 UTC in commit 3ca5f5b. Qwen announced the Qwen2.5 family publicly on 19 September 2024. The Amaranth issue was created on 20 September 2024 at 13:41:02 UTC, and the fix PR was created at 14:00:49 UTC.

A November 2026 AACL paper by Hassan et al. lists October 2023 as the reported knowledge cutoff for Qwen2.5-3B-Instruct (Table 5). This is a secondary-source report, not a vendor guarantee; the official model card does not state a precise training-data cutoff.

Interpretation: the specific issue and fix PR postdate the initial checkpoint-weight upload and public Qwen2.5 announcement; the paper's reported cutoff is earlier still. This reduces the likelihood of issue/PR-specific training exposure. It does not prove that pre-existing Amaranth source code was absent from the model's training data. Keep issue/patch exposure separate from exposure to the source code that existed before the issue was reported.

Sources:
- Official Qwen2.5 announcement, 19 September 2024: https://qwenlm.github.io/blog/qwen2.5/
- Hugging Face Qwen2.5-3B-Instruct model page: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct
- Hugging Face repository commit history showing 3ca5f5b on 17 September 2024: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/commits/main
- Initial uploaded checkpoint tree at 3ca5f5b: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/tree/3ca5f5bff0f44b2b436a9aba99b900ab157c9a27
- Hassan et al., AACL-IJCNLP 2026, Table 5: https://aclanthology.org/2026.aacl-long.168/

## 7. Methodological and acceptance boundaries

- Stage 2 exact-base/fixed reproduction and artifact integrity: passed.
- E2 alternative elimination: supported by direct RTLIL output and the frozen selector.
- E3 clue leakage / primary-sample suitability: requires project-lead review.
- Project-lead source-aware gold and tier decision: pending.
- Project-lead prior pipeline/debug exposure declaration: pending.
- Project-lead temporal-exposure acknowledgement: pending; the chronology does not prove absence of pre-existing source exposure.
- Researcher source exposure: full; no blind adjudication or inter-rater reliability claim.
- Exact dataset-card provenance, dependency canonical licenses/notices, and bounded documentary scope: separate open gates.
- Final case acceptance: not accepted; registry inclusion: false.
- Model loading, inference, fine-tuning and training: not performed and not authorized.