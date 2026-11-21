# PyThaiNLP #1004 — E3/E2/E1 evidence-elimination matrix

**Date:** 21 November 2026  
**Candidate:** PyThaiNLP/pythainlp issue #1004 / fix PR #1046  
**Dataset instance:** `pythainlp__pythainlp-1046`  
**Status:** **SOURCE-AUDITED ADVISORY MATRIX — NOT A PROJECT-LEAD GOLD/TIER DECISION; CASE NOT ACCEPTED**

## 1. Question the matrix must answer

Does E2 eliminate at least one predeclared alternative explanation while leaving at least two plausible mechanisms for the complete two-output defect unresolved?

**Proposed answer: yes, with a narrower and explicitly scoped elimination.** E2 can eliminate the hypothesis that the initial consonant `ค` was assigned to the wrong consonant class in the implementation. It does not resolve the cause of the `ค่ะ` output. At least two explanations for that remaining symptom stay live at E2.

This is an evidence-elimination statement, not a claim that the remaining alternatives have equal probability.

## 2. Frozen provenance

- Issue: https://github.com/PyThaiNLP/pythainlp/issues/1004
- Fix PR: https://github.com/PyThaiNLP/pythainlp/pull/1046
- Exact buggy base: `188904f22c4c80fd7406706850c798f611690a4a`
- Exact-base `pythainlp/util/syllable.py` blob: `9d480d815ee23edc74a39f34edea253dd4fd88fc`
- Exact-base `pythainlp/__init__.py` blob: `8f5ea86690ca2c8bb567a9d2d98d5cadf6c863d6`
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset row SHA-256: `80b244dd8b406d095f7ec727f968dacbb6b2f620dc8b10c21d44e726ba3e5803`

The issue reports `tone_detector("ครับ")` as `f` rather than expected `h`, and `tone_detector("ค่ะ")` as `h` rather than expected `f`. The issue reporter's possible-solution excerpt mentions the generic low-class / long / closed / dead-syllable branch, which is a partial clue for `ครับ`; it is not a complete explanation of both examples.

## 3. Predeclared alternatives

| ID | Alternative explanation | What it would mean |
|---|---|---|
| A1 | Initial-consonant class assignment is wrong | The first consonant `ค` is not correctly recognized as a low-class consonant in the failing inputs. |
| A2 | Tone-mark recognition/extraction is wrong | The mai-ek mark in `ค่ะ` is absent or misread before tone-rule evaluation. |
| A3 | Syllable-state classification is wrong | The live/dead, open/close, or length state supplied to tone logic is incorrect and causes a generic tone branch to be selected. |
| A4 | Generic-rule condition or precedence is wrong | A generic syllable-state rule is selected before a more specific tone-mark rule that should determine the result. |

G1 remains the proposed two-part mechanism: (G1a) the strict three-consonant boundary in `syllable_length` misclassifies the length path for `ครับ`; and (G1b) for `ค่ะ`, a generic low-class / short / open rule precedes and captures the input before the low-class-plus-mai-ek mapping.

## 4. E3 → E2 → E1 elimination matrix

| Evidence item / hypothesis | E3 | Added at E2 | E2 disposition | Added at E1 |
|---|---|---|---|---|
| A1: wrong initial class for `ค` | Not independently resolved. The reporter's hint refers to a low-class branch but is not a source-backed trace for both inputs. | Exact-base consonant inventory includes `ค`; exact-base tone path selects the first consonant; class table puts `ค` in the low class. An independent NECTEC Thai consonant chart also places `ค` in the paired-low column. | **Eliminated for these two inputs**, within the scope of initial-consonant class assignment. | Retained as eliminated; no need to expose more class-table source in the model packet. |
| A2: wrong tone-mark extraction in `ค่ะ` | Live. | E2 deliberately does not reveal the tone-mark extractor or its parsed value. | **Still live.** | Exact-base mark inventory and extractor show that `่` is a recognized tone mark and is extracted from `ค่ะ`. |
| A3: wrong syllable-state calculation in `ค่ะ` | Live. | E2 reveals the length boundary relevant to `ครับ`, but not the `sound_syllable` or open/close implementation for `ค่ะ`. | **Still live.** | Exact-base state-function excerpts and the input-specific derivation show the values used by the first matching tone branch. |
| A4: generic-rule condition/precedence | Reporter supplies a partial generic-branch clue for `ครับ`; complete two-input explanation remains unresolved. | E2 does not reveal the ordered `tone_detector` branches. | **Still live.** | Exact-base branch order shows the generic low/short/open branch for `ค่ะ` precedes the low-class-plus-`่` branch. |
| G1a: three-consonant length boundary for `ครับ` | Possible, not established. | Exact-base `syllable_length` uses `len(consonants) < 3`; `ครับ` contains three consonants and a short-vowel character. | **Strongly supported as a causal contributor**, but not by itself a complete explanation of both outputs. | Full source-derived path is available when combined with the remaining exact-base tone logic. |
| G1b: tone-mark precedence for `ค่ะ` | Not resolved by issue narrative or reporter's partial clue. | Ordered tone-rule source remains withheld. | **Unresolved.** | Confirmed by the exact-base branch-order excerpt and input-specific state derivation. |

### Why A1 is genuinely eliminated at E2

The immutable exact-base sources establish the full chain:

1. `pythainlp/__init__.py` line 7 includes `ค` in `thai_consonants`.
2. `pythainlp/util/syllable.py` lines 243–244 select the first character in the input that belongs to `thai_consonants`.
3. Lines 44 and 51–59 place `ค` in the `low` consonant class and build the lookup from character to class.
4. Both issue inputs begin with `ค`.
5. Independently, the NECTEC technical paper's Thai consonant chart places `ค` in the paired-low column (Table 1, PDF page 1).

Thus, for these two inputs, the initial-consonant-class hypothesis is not a viable explanation: the implementation's class assignment agrees with the independent Thai consonant classification. This does **not** eliminate A2, A3, or A4.

### Why G1a is relevant but does not settle the complete issue at E2

- Exact-base `pythainlp/__init__.py` line 7 provides the consonant inventory used by the utility.
- Exact-base `pythainlp/util/syllable.py` line 32 defines the short-vowel set, including `ั`.
- Lines 186–192 count consonants and return short only when `len(consonants) < 3` (or the separate regex applies).
- `ครับ` has three consonants (`ค`, `ร`, `บ`) and contains `ั`; the strict `< 3` check therefore does not select the short-vowel branch.

This supports the length-boundary explanation for the `ครับ` symptom. E2 still does not disclose enough of the `ค่ะ` processing path to distinguish A2, A3, and A4.

## 5. Two or more mechanisms still live after E2

At E2, at least these two complete causal accounts remain possible for the unresolved `ค่ะ` symptom, alongside the supported `ครับ` length-boundary contributor:

- **H1 — mark-extraction account:** the first consonant is correctly low-class and the `ครับ` length boundary is implicated, but the mai-ek mark in `ค่ะ` is not correctly extracted or represented before tone-rule evaluation.
- **H2 — syllable-state account:** the first consonant is correctly low-class and the `ครับ` length boundary is implicated, but one or more syllable-state values for `ค่ะ` (sound/dead-live or open/close) cause a generic rule to be selected.
- **H3 — rule-precedence account:** the first consonant and mark may both be correctly extracted, but a generic low-class syllable-state branch captures `ค่ะ` before the specific low-class-plus-mai-ek rule.

E2 does not include the exact-base source lines needed to choose among H1–H3. Therefore E2 meets the minimum requirement of eliminating one predeclared alternative while retaining at least two plausible explanations. The conclusion is scoped to this candidate and these two examples.

## 6. E1 source evidence and corrected input-specific path

The exact-base source audit identifies the actual generic branch for `ค่ะ`. It is **not** the low / short / closed / dead branch. The source-derived path is:

| Input | Initial class | Length | Open/close | Sound state | First matching generic branch in exact buggy base | Observed result |
|---|---|---|---|---|---|---|
| `ครับ` | low | long (three consonants fail strict `< 3`) | close | dead | low + long + close + dead → `f` | `f` |
| `ค่ะ` | low | short | open (one consonant) | dead | low + short + open → `h` | `h` |

For `ค่ะ`, the exact-base extractor returns the mark `่`; however, the generic low / short / open branch at lines 297–301 occurs before the specific low-class-plus-`่` branch at lines 312–313. Because these are an ordered `if/elif` chain, the generic branch wins and the specific mapping is not reached.

For `ครับ`, the strict `< 3` boundary leaves the short vowel `ั` outside the short branch, so the long / close / dead path reaches the reporter-identified generic branch at lines 290–295 and returns `f`.

E1 may therefore support ANSWER for the complete two-part G1 when the packet includes these exact-base source excerpts and the derivation above. The fixed PR implementation, patch, or post-fix source must remain excluded from all model-visible evidence packets; it is retained only for hidden technical-gold validation.

**Trace limitation:** this matrix is a deterministic, source-derived control-flow analysis anchored to the pinned base source and the already-reproduced public-API outputs. A separate instrumented runtime log of intermediate helper return values was not part of the currently rechecked evidence bundle. Do not describe this as a separately observed intermediate-state trace. If the final adjudication standard requires runtime instrumentation, add a minimal exact-base diagnostic run before project-lead gold/tier approval.

## 7. Decision consequence

- E3 = ABSTAIN remains a proposal.
- E2 = ABSTAIN is now **methodologically supported as a proposal**: A1 is eliminated, while A2/A3/A4 remain plausible for the unresolved `ค่ะ` symptom.
- E1 = ANSWER remains a proposal, supported by the two-part source-derived path, subject to the stated trace limitation and project-lead review.
- This matrix is not project-lead gold/tier approval, not final case acceptance, not registry inclusion, and not inference authorization.
- The case remains one PyThaiNLP candidate (issue #1004 / fix PR #1046), not two cases.

## 8. Source references

- Exact buggy base `pythainlp/__init__.py`, lines 7 and 18: https://github.com/PyThaiNLP/pythainlp/blob/188904f22c4c80fd7406706850c798f611690a4a/pythainlp/__init__.py
- Exact buggy base `pythainlp/util/syllable.py`, lines 12–59, 84–162, 165–200, 241–313: https://github.com/PyThaiNLP/pythainlp/blob/188904f22c4c80fd7406706850c798f611690a4a/pythainlp/util/syllable.py
- Issue #1004 and the reporter's partial possible-solution clue: https://github.com/PyThaiNLP/pythainlp/issues/1004
- Theppitak Karoonboonyanan, NECTEC, *Standardization and Implementations of Thai Language*, Table 1, PDF page 1: https://www.nectec.or.th/www.nectec.or.th/it-standards/thaistd.pdf
