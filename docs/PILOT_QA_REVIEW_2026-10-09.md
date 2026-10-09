# Frozen Pilot QA Review — 2026-10-09

## Execution and artifact integrity
- GitHub Actions run #85 completed successfully for source commit `d50adaf9b6d0b017a5d30c9ebd9dd404988dbfb5`.
- GitHub artifact: `dijitalikiz-pilot-d50adaf9b6d0b017a5d30c9ebd9dd404988dbfb5`; artifact ID `11634641753`.
- Artifact ZIP size: 81,759 bytes. SHA-256: `b12594415894d5cac18442d3bd6c505e843b1a14027272c1afa398a59101aca0`.
- The included 55-file artifact manifest passed an independent SHA-256 and byte-size recheck.
- 40 pilot inference records were present and unique across four cases × two conditions × five fixed seeds. All records had parsed output, exact frozen model revision/configuration, prompt/context/system-prompt hashes, and raw-output hashes. No parse failures were found.
- Under the *legacy strict complete-diagnostic rubric*, 0/20 records passed in Standard and 0/20 passed in CCDG. This is not evidence that CCDG has no effect; the pilot was designed to surface execution and measurement problems, and the score requires every component/entity/operation/root-cause/relation check to match simultaneously.
- The artifact QA report marked contamination risk unknown for all pilot cases because the minimal Kaggle source bundle excludes the assessments directory. The frozen candidate review is present in the bundle and already records the case-level public-exposure risks. A fallback to that review has been added so risk labels are not lost during QA. “High/medium” means public-exposure risk, not proof of training-set membership.

## Scoring-protocol amendment
The pilot exposed a construct-validity weakness in exact normalized string matching: a natural-language explanation can correctly describe a defect while failing the canonical machine-form root-cause label. The original pilot records and legacy complete-diagnostic evaluation are preserved unchanged.

Before confirmatory inference, the primary endpoint is amended to *case-level root-cause correctness under fixed, case-specific aliases*. Aliases are based on frozen case ground truth/source evidence. Pilot outputs were consulted for scoring-protocol diagnostics; no confirmatory outputs have been consulted, and aliases were not copied from model outputs. The rubric is bound to the main manifest by SHA-256, and the exact legacy complete-diagnostic score remains a secondary metric. This amendment must be described in the final report; it must not be represented as the original pilot endpoint.

This is a deterministic phrase-matching rubric, not a semantic judge. Unmatched paraphrases may remain false negatives. The rubric must be audited and frozen before confirmatory outputs exist; aliases cannot be added after viewing main results.

## Power calculation correction
The exact McNemar power helper had its two discordant-event labels inverted in the documentation. The calculation is symmetric for the two event probabilities, so the recorded numerical power remains 0.807 for 16 cases under the same assumed discordance magnitudes. The manifest and helper now use conventional definitions:
- `p_standard_only`: Standard correct, CCDG incorrect.
- `p_ccdg_only`: Standard incorrect, CCDG correct.

The predeclared assumed alternative remains CCDG-favouring (`p_standard_only = 0.05`, `p_ccdg_only = 0.60`), alpha = 0.05, target power = 0.80. These are design assumptions, not estimates from pilot outcomes.

## Gate decision
The main confirmatory manifest remains `draft`. Do not launch the 160 confirmatory model calls until the rubric hash, per-case aliases, candidate records, manifest validator, runner integrity checks and full test suite pass. No main-benchmark outputs are present or used by this review.
