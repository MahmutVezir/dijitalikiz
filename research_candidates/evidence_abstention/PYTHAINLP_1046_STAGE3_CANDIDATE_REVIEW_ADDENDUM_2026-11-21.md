# PyThaiNLP #1046 — Stage 3 candidate-review addendum

**Date:** 21 November 2026  
**Candidate:** PyThaiNLP/pythainlp issue #1004 / fix PR #1046  
**Dataset instance:** `pythainlp__pythainlp-1046`  
**Disposition:** Stage 2 technical evidence independently integrity-checked; source-aware gold/tier proposal prepared separately. Not accepted.

## 1. Stage 2 evidence recheck

- Issue #1004: https://github.com/PyThaiNLP/pythainlp/issues/1004
- Fix PR #1046: https://github.com/PyThaiNLP/pythainlp/pull/1046
- Buggy base: `188904f22c4c80fd7406706850c798f611690a4a`
- Fixed commit: `6f1dc929f853ecd9910d1d25a56716b864b2ee98`
- Dataset instance: `pythainlp__pythainlp-1046`
- Dataset row SHA-256: `80b244dd8b406d095f7ec727f968dacbb6b2f620dc8b10c21d44e726ba3e5803`
- Frozen selector: `tests/core/test_util.py::UtilTestCase::test_tone_detector`
- Buggy-base exact selector: executed and failed on the first issue assertion (`ครับ`: actual `f`, expected `h`).
- Same selector on exact fixed commit: passed.
- Two independent single-word public-API support reproducers were also run:
  - `ครับ`: base `f` vs expected `h`; fixed pass.
  - `ค่ะ`: base `h` vs expected `f`; fixed pass.
- These are support reproducers for one issue and one dataset case; they are not additional independent cases.
- Test-only patch touched only `tests/core/test_util.py`, adding the two assertions; no production patch was applied to the buggy base.

Downloaded archive recheck:
- Artifact ID: `14351751109`
- Outer SHA-256: `ce2ab3bbefd3148510992a7503d8c07b17fb87fe2c2a76173c1971d21e12dcb8` (matches the recorded digest)
- ZIP CRC: pass
- Internal SHA256SUMS: 17/17 match

## 2. Source-level mechanism candidate

PR #1046 makes two production changes that jointly explain the two reported outputs:

1. **Three-consonant short-syllable boundary:** in `syllable_length`, the condition changes from `len(consonants) < 3` to `len(consonants) <= 3`. The word `ครับ` contains three Thai consonants; the old boundary prevents the short-vowel condition from applying at three consonants. The downstream tone branch can consequently take the wrong long/closed/dead path.
2. **Tone-mark rule precedence:** in `tone_detector`, tone-mark-specific cases are moved ahead of broader consonant-class and syllable-state rules. For `ค่ะ`, one consonant makes the syllable `open`; the generic low-class/short/open branch returns `h` before the specific low-class plus mai-ek (`่`) mapping is reached. The earlier closed/dead branch description was incorrect for this input.

The issue reporter's “possible solution” excerpt suggests one potentially relevant generic low/long/closed/dead branch for `ครับ`. That is a useful E3 clue but is not a complete explanation of both outputs: it does not establish the three-consonant boundary change and does not explain the `ค่ะ` tone-mark precedence correction.

Proposed combined gold identifier:
`TONE_DETECTOR_THREE_CONSONANT_LENGTH_BOUNDARY_AND_TONE_MARK_PRECEDENCE`

The gold record must preserve both submechanisms rather than selecting only one changed line. It must also preserve alternatives involving syllable sound/closure classification and tone-rule evaluation.

## 3. Candidate evidence-tier construction

A source-aware advisory proposal is in `PYTHAINLP_1046_SOURCE_AWARE_GOLD_AND_EVIDENCE_TIERS_PROPOSAL_2026-11-21.md`.

- **E3 — proposed ABSTAIN:** issue narrative, two actual/expected outputs, and the reporter's partial possible-solution hint. The hint addresses at most part of the `ครับ` symptom; at least the mechanism of `ค่ะ` remains unresolved.
- **E2 — proposed ABSTAIN:** add exact-base `syllable_length` evidence plus the exact-base initial-consonant class lookup for `ค`, independently corroborated by the NECTEC chart. This eliminates the predeclared wrong-initial-class alternative for both inputs and supports the `ครับ` length-boundary contributor, while leaving tone-mark extraction, syllable-state classification and rule precedence unresolved for `ค่ะ`.
- **E1 — proposed ANSWER:** add exact-base tone-mark extraction, syllable-state helper and branch-order excerpts. The actual generic branch for `ค่ะ` is low / short / open, not low / short / closed / dead. The fixed patch itself must not be included in the model-visible diagnosis packet.

The row-level matrix is now recorded at `pythainlp_1046/PYTHAINLP_1004_E3_E2_E1_EVIDENCE_ELIMINATION_MATRIX_V0_1_2026-11-21.md`. It shows that E2 eliminates at least one predeclared alternative while leaving at least two plausible mechanisms live. The input-specific E1 path is a deterministic source-derived trace; a separately captured intermediate-state runtime log is not yet in the rechecked evidence bundle. These remain proposals, not project-lead decisions. Project-lead review and any additional instrumentation required by the adjudication standard remain open.

## 4. Related-issue family and exposure

- PyThaiNLP #1055 is a related but not identical report in the same `sound_syllable`/`tone_detector` function family. It reports other syllable/tone symptoms and its issue diff reproduces the `ครับ` and `ค่ะ` test additions already present in #1046, then adds different failing cases. It must be treated as related family context, not as another independent project/case.
- #918 is a documentation issue about the detector's output labels.
- #1120 is a separate later `tone_detector` error report involving another input. It is family context, not a duplicate of the two #1004 outputs.
- The single-project sampling rule permits at most one accepted PyThaiNLP case.
- Project-lead prior pipeline/debug exposure declaration for #1004: **`none` by direct project-lead self-report**. Decision record: `pythainlp_1046/PROJECT_LEAD_EXPOSURE_DECISION_PYTHAINLP_1046_2026-11-21.md`. This was not independently witnessed or audited.
- Researcher source exposure is `full` after issue, PR, source, selector and artifact review. No blind adjudication or inter-rater claim is made.

## 5. License and model-exposure gates

- Exact-base root repository license: Apache-2.0.
- Dataset-row license metadata: Apache-2.0; dataset card CC-BY-4.0 is a separate data-source license.
- The pinned runtime inventory contains 20 distributions. Three have null license fields despite MIT classifiers (`exceptiongroup`, `setuptools`, `wheel`). NumPy 2.2.6 package metadata includes bundled OpenBLAS, LAPACK, GCC runtime with its exception, and libquadmath; PyICU 2.17 and ICU 70.1 native/runtime scope also needs explicit review.
- Exact pinned dataset-card README revision/bytes, canonical dependency licenses and applicable notices remain open. No bounded research-scope acknowledgement or legal clearance is recorded.
- Pinned model in the protocol: `Qwen/Qwen2.5-3B-Instruct`, revision `aa8e72537993ba99e69dfaafa59ed015b17504d1`, license identifier recorded as `qwen-research`. Its exact terms/use review remains a separate open gate.
- The public model update/release predates the #1004 report, but the reviewed model metadata does not establish an exact training-data cutoff. This chronology is not proof that the issue or related material was absent from pretraining data.

## 6. Current status

- Stage 2 technical gate: passed; evidence archive SHA/CRC/internal hashes rechecked.
- Gold/tier: advisory proposal only; project-lead decision pending.
- Related issue-family review: prepared; project-lead review pending.
- Prior pipeline/debug exposure: declared `none` by project-lead self-report; researcher source exposure remains `full`.
- Bounded documentary scope: pending source/data/dependency/native notice review and explicit acknowledgement.
- Final case acceptance: not accepted.
- Registry inclusion: false.
- Model loading, inference, fine-tuning and training: not performed and not authorized.
