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

The base `syllable_length` condition is `len(consonants) < 3` before the short-vowel check. The fixed revision changes it to `<= 3`. The `ครับ` example contains three consonants. Under the buggy boundary, the short-vowel branch is not selected by that condition, which can send downstream tone logic through the wrong syllable-length case. The fixed condition includes a three-consonant syllable.

### G1b — tone-mark-specific rules are evaluated too late

In the exact buggy `tone_detector`, broader consonant-class and syllable-state branches precede the specific tone-mark mappings. For the low-class initial consonant and mai-ek mark (`่`) in `ค่ะ`, the generic low-class / short / closed / dead-syllable branch can return `h` before the specific low-class-plus-tone-mark rule that returns `f` is reached. The fixed revision moves the tone-mark-specific rules ahead of the generic syllable-state rules.

The gold claim is limited to these two branches and the reported issue examples. It does not assert that all Thai tone-detection errors share this mechanism.

## 3. Plausible alternatives to preserve

- **A1 — shared phonetic-state classification error:** `sound_syllable`, syllable openness/closure, or related phonetic-state calculation is wrong for one or both inputs, rather than the length boundary or rule precedence being causal.
- **A2 — initial-consonant class or tone-mark interpretation error:** the initial consonant class or the mark extracted by the tone-mark detector is misidentified.
- **A3 — a single generic tone-rule condition is wrong:** the reporter's proposed low/long/closed/dead condition is a useful hypothesis for `ครับ`, but may not explain both reported outputs; it must remain a live partial explanation at lower evidence.

These alternatives are candidates for the E3/E2 evidence-elimination matrix, not claims of equal probability. The E1 packet must distinguish the full two-part G1 from alternatives.

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
- the exact-base `syllable_length` excerpt showing the strict `< 3` boundary, alongside the fact that `ครับ` contains three consonants.

This reveals a causal contributor to the `ครับ` path and narrows the explanation for that output. It does not identify why `ค่ะ` still follows a generic branch before its tone-mark-specific mapping. At least two mechanisms remain live for the complete two-output defect. The E2 packet should not contain the relevant `tone_detector` branch-order excerpt that resolves this second part.

### E1 — proposed ANSWER

Evidence:
- E2 unchanged;
- exact-base `tone_detector` source excerpt showing the specific low-class / mai-ek branch located after a generic low-class / short / closed / dead branch;
- immutable source line/blob provenance for both source excerpts.

Together, the length-boundary and branch-order evidence support the complete G1 mechanism for the two issue outputs and distinguish it from A1–A3.

**Leakage control:** do not include the fixed source, PR patch, fix commit content, or post-fix implementation in any model-visible evidence packet. The fix is used for hidden technical gold validation only.

## 5. Tier-construction validation still required

Before project-lead approval, prepare and validate a row-level evidence elimination matrix that makes these statements explicit:
- E3 leaves the full two-output mechanism unresolved, despite the reporter's partial clue.
- E2 adds an immutable source clue for the `ครับ` branch, but leaves the `ค่ะ` branch underdetermined.
- E1 adds the remaining exact-base branch-order evidence and leaves only G1.

If the matrix cannot show that E2 eliminates at least one predeclared alternative while at least two mechanisms still remain possible, the E2 packet must be revised or the case left unclassified. Do not force the prescribed ABSTAIN label to fit the design.

## 6. Method and independence limits

- The two one-word reproducers are supporting tests for one issue; they are not two independent cases.
- #1055 is related same-repository issue-family context; it is not an additional accepted project or case.
- Researcher source exposure is full. No blind gold adjudication or inter-rater reliability is claimed.
- The project lead must separately declare prior candidate-specific pipeline/debug/test-oracle/prompt-tuning exposure for #1004. No value is inferred here.

## 7. Status

Gold and E3/E2/E1 outcomes remain advisory only. Issue-family review, candidate exposure, dependency/native notices, pinned data-card provenance, bounded scope acknowledgement, case-record validation, and separate final YES/NO acceptance are not closed. PyThaiNLP #1004 remains outside the accepted registry; model inference remains unauthorized.
