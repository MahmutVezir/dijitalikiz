# PyThaiNLP #1004 — source-aware gold and evidence-tier proposal

**Date:** 21 November 2026  
**Candidate:** PyThaiNLP/pythainlp issue #1004 / PR #1046  
**Dataset instance:** `pythainlp__pythainlp-1046`  
**Status:** **ADVISORY PROPOSAL ONLY — NOT PROJECT-LEAD APPROVED**

## 1. Candidate contract and immutable identity

- Issue: https://github.com/PyThaiNLP/pythainlp/issues/1004
- Fix PR: https://github.com/PyThaiNLP/pythainlp/pull/1046
- Exact buggy base: `188904f22c4c80fd7406706850c798f611690a4a`
- Exact fixed commit: `6f1dc929f853ecd9910d1d25a56716b864b2ee98`
- Base `pythainlp/util/syllable.py` blob: `9d480d815ee23edc74a39f34edea253dd4fd88fc`
- Fixed `pythainlp/util/syllable.py` blob: `bf3d4be4c50d59005f3e752ec426861c53428ba6`
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset row SHA-256: `80b244dd8b406d095f7ec727f968dacbb6b2f620dc8b10c21d44e726ba3e5803`
- Frozen selector: `tests/core/test_util.py::UtilTestCase::test_tone_detector`

The issue reports:
- `tone_detector("ครับ")`: actual `f`, expected `h`.
- `tone_detector("ค่ะ")`: actual `h`, expected `f`.

## 2. Proposed gold mechanism

**G1 — `TONE_DETECTOR_THREE_CONSONANT_LENGTH_BOUNDARY_AND_TONE_MARK_PRECEDENCE`**

The exact buggy base contains two related source-level defects in the processing path that together explain the two reported examples.

### G1a — three-consonant syllable-length boundary

The base `syllable_length` condition is `len(consonants) < 3` before the short-vowel check. The fixed revision changes it to `<= 3`. The `ครับ` example contains three consonants and the short vowel `ั`. Under the buggy boundary, the short-vowel branch is not selected, so the syllable is treated as long and the low / long / close / dead rule returns `f`. The corrected boundary includes a three-consonant syllable in the short-vowel branch.

### G1b — tone-mark-specific rules are evaluated too late

In the exact buggy `tone_detector`, broader consonant-class and syllable-state branches precede the specific tone-mark mappings. For `ค่ะ`, the first consonant `ค` is low-class, the syllable has one consonant (therefore `open`), and its length is `short`. The generic low-class / short / open branch returns `h` before the later low-class-plus-mai-ek (`่`) branch that assigns `f`. The earlier draft incorrectly named the closed/dead branch for this input; the pinned source shows that the matching generic branch is **low / short / open**. The fixed revision moves the tone-mark-specific rules ahead of the generic syllable-state rules.

The gold claim is limited to these two branches and the reported issue examples. It does not assert that all Thai tone-detection errors share this mechanism.

## 3. Plausible alternatives to preserve

- **A1 — syllable-state classification error:** `sound_syllable` or open/close classification is wrong for one or both inputs, causing the wrong generic path to be selected.
- **A2a — initial-consonant class error:** the first consonant `ค` is assigned a class other than low.
- **A2b — tone-mark extraction error:** the mai-ek mark in `ค่ะ` is not recognized or is represented incorrectly before tone-rule evaluation.
- **A3 — generic-condition/precedence alternative:** a generic tone-rule predicate or its precedence, rather than the proposed two-part G1, explains one or both outputs.

These alternatives are not claims of equal probability. The source-backed elimination status at each tier is recorded in `pythainlp_1046/PYTHAINLP_1004_E3_E2_E1_EVIDENCE_ELIMINATION_MATRIX_V0_1_2026-11-21.md`.

## 4. Proposed E3/E2/E1 decisions

The advisory outcomes are **E3 ABSTAIN, E2 ABSTAIN, E1 ANSWER**.

### E3 — proposed ABSTAIN

Evidence:
- the issue narrative and both actual/expected outputs;
- the reporter's “possible solution” source excerpt.

The reporter's excerpt points toward one generic low/long/closed/dead branch that could explain the `ครับ` result. It does not establish the three-consonant boundary mechanism and does not explain why `ค่ะ` is classified as high tone instead of falling tone. The full issue-level cause remains underdetermined. The E3 packet must preserve the reporter's hint as-is; it must not remove it to manufacture uncertainty.

### E2 — proposed ABSTAIN

Evidence:
- E3 unchanged;
- the executed exact-base public-API observations for the two words;
- the exact-base `syllable_length` excerpt showing the strict `< 3` boundary, alongside the three consonants and short vowel in `ครับ`;
- exact-base class evidence: `ค` is included in the package consonant inventory, selected as the first consonant, assigned to the low class by the source lookup, and independently classified as low in the NECTEC Thai consonant chart.

This eliminates A2a (wrong initial-consonant class) for the two issue inputs, because both begin with `ค`. It also supports the length-boundary explanation for `ครับ`. It does **not** reveal tone-mark extraction or the syllable-state and ordered tone-rule paths for `ค่ะ`; A1, A2b and A3 remain live. Thus E2 eliminates at least one predeclared alternative while preserving at least two plausible mechanisms for the complete two-output defect. The E2 packet must not contain the `_tone_mark_detector` internals or the `tone_detector` branch-order excerpt.

### E1 — proposed ANSWER

Evidence:
- E2 unchanged;
- exact-base `_tone_mark_detector`, syllable-state helpers, and ordered `tone_detector` branches with immutable line/blob provenance;
- input-specific source-derived traces showing `ครับ` follows low / long / close / dead → `f`, while `ค่ะ` follows low / short / open → `h` before the later low-class-plus-`่` rule.

Together, the length-boundary and corrected branch-order evidence support the complete G1 mechanism for the two issue outputs. This is a deterministic source-derived trace, not a separately observed intermediate-state runtime log; see the evidence-elimination matrix for that limitation.

**Leakage control:** do not include the fixed source, PR patch, fix commit content, or post-fix implementation in any model-visible evidence packet. The fix is used for hidden technical gold validation only.

## 5. Tier-construction validation still required

The row-level matrix is now recorded at `pythainlp_1046/PYTHAINLP_1004_E3_E2_E1_EVIDENCE_ELIMINATION_MATRIX_V0_1_2026-11-21.md`. It documents:
- E3 leaves the full two-output mechanism unresolved despite the reporter's partial clue.
- E2 eliminates A2a (incorrect initial-consonant class for `ค`) using exact-base class mapping plus the independent NECTEC chart, while A1, A2b and A3 remain live.
- E1 supplies the exact-base syllable-state, tone-mark extraction and branch-order evidence; the actual generic branch for `ค่ะ` is low / short / open, not low / short / closed / dead.

The matrix supports E2 ABSTAIN as a proposal, not an approved decision. It also discloses that its input-specific control-flow trace is source-derived rather than a separately captured runtime intermediate-state log. Do not claim more than the evidence supports; add instrumentation before project-lead approval if the adjudication standard requires observed intermediate values.

## 6. Method and independence limits

- The two one-word reproducers are supporting tests for one issue; they are not two independent cases.
- #1055 is related same-repository issue-family context; it is not an additional accepted project or case.
- Researcher source exposure is full. No blind gold adjudication or inter-rater reliability is claimed.
- Project-lead prior candidate-specific pipeline/debug/test-oracle/prompt-tuning exposure for #1004 is declared **`none`** by direct self-report (decision record: `pythainlp_1046/PROJECT_LEAD_EXPOSURE_DECISION_PYTHAINLP_1046_2026-11-21.md`). This declaration is not independently witnessed or audited. Researcher source exposure remains full.

## 7. Status

Gold and E3/E2/E1 outcomes remain advisory only. Issue-family review, dependency/native notices, pinned data-card provenance, bounded scope acknowledgement, case-record validation, and separate final YES/NO acceptance are not closed. The prior pipeline/debug exposure question is closed as `none` by project-lead self-report; researcher source exposure remains full. PyThaiNLP #1004 remains outside the accepted registry; model inference remains unauthorized.
