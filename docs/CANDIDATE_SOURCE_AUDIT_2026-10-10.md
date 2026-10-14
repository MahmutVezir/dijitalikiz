# Calibration Candidate Source Audit — 2026-10-10

**Status:** Provisional desk review; not independent human adjudication.  
**Scope:** The seven candidates reserved for scoring-instrument calibration, not for the future confirmatory sample.  
**Inference authorization:** None. The case-pool manifest remains unfrozen and `model_inference_permitted=false`.

## Why this audit exists

A successful pre-fix/fixed-revision regression reproduction establishes that a test distinguishes two software revisions for the tested scenario. It does not automatically prove that (a) the proposed root cause is complete, (b) each CCDG edge is source-grounded, or (c) the case is suitable for measuring cross-component reasoning. Those are separate review decisions.

Every candidate below remains `pending_independent_review`. This document records a preliminary source/structure check only; it must not be represented as an independent human review or as a completed ground-truth adjudication.

## Candidate decisions

| Candidate | Preliminary suitability | Reason / risk | Required independent review |
|---|---|---|---|
| [Commons Compress #770](https://github.com/apache/commons-compress/pull/770) | Strong candidate for calibration | Streaming `TarArchiveInputStream` and file-based `TarFile` paths converge on shared PAX handling. The pinned oversized-header regression is reproduced. Public exposure means training-data contamination is possible but not proven. | Verify each caller→handler→parser edge in both revisions; distinguish unbounded accumulation from the exact size-limit guard and its exception behavior. |
| [Commons Collections #694](https://github.com/apache/commons-collections/pull/694) | Strong candidate for calibration | A synchronized decorator and the wrapped expiring map's cached collection views interact; expiration cleanup and index maintenance are relevant. Public issue exposure remains a contamination risk. | Verify which view methods/iterators bypassed cleanup before the fix and which side effects the fixed implementation restores. Do not label every symptom as an independent root cause. |
| [Commons Collections #731](https://github.com/apache/commons-collections/pull/731) | Moderate candidate for calibration | The bulk insertion path and null-safe value-conversion path provide a plausible helper boundary, but this is narrower than the strongest cross-component examples. | Confirm the exact `putAll(K, Iterable)` behavior, the null-transformer contract, and the role of `transformValue`; distinguish the root cause from the resulting NullPointerException. |
| [Commons Lang #1783](https://github.com/apache/commons-lang/pull/1783) | Strong candidate for calibration | The exact-signature fast path can return a method declared on a non-public runtime class rather than a publicly accessible interface declaration. The PR discussion explicitly discloses AI-assisted discovery/fix drafting; that is a provenance fact, not proof the fix is wrong. | Verify the final merged commit and static/private interface exclusions; review against regression evidence rather than relying on the PR narrative alone. |
| [Commons Codec #443](https://github.com/apache/commons-codec/pull/443) | Moderate candidate for calibration | UTF-16 ordering and unsigned UTF-8 byte ordering differ for some names; this affects the identifier produced downstream. Most of the path is internal to one utility. The PR explicitly discloses AI-assisted discovery/fix drafting. | Verify the final merged changes and the tie-handling case for names that encode to the same UTF-8 replacement bytes. Decide whether this is genuine cross-component reasoning or mainly a local comparator defect. |
| [Commons Compress #803](https://github.com/apache/commons-compress/pull/803) | Weak for a single cross-component chain; calibration-only | The case bundles LZ4 empty-frame and Snappy padding paths. They are parallel decoder paths, not one causal chain from the LZ4 component to the Snappy component. A shared symptom does not itself establish a cross-component dependency. | Keep the two paths explicitly separate. Review whether the combined issue is a defensible unit for calibration; do not select it as a primary CCDG-effect case without a stronger rationale. |
| [Commons Lang #1808](https://github.com/apache/commons-lang/pull/1808) | Weak single-component boundary control; calibration-only | An exclusive upper bound excludes a documented endpoint. Useful for checking simple root-cause scoring, but weak evidence for a cross-component graph claim. | Retain only as a calibration/control example; do not use it to inflate the main study's cross-component case count. |

## Reproduction state and consistency

The current repository contains archived pre-fix failure/fixed-revision pass evidence for the #770 candidate in [run 37993954772](https://github.com/MahmutVezir/dijitalikiz/actions/runs/37993954772) and for the other six candidates in [run 38045048274](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38045048274). These are reproduction results for the targeted regression scenarios, not independent adjudications of all ground-truth statements or CCDG edges.

The case records now carry a version-bound snapshot consisting of:
- source repository URL;
- exact pre-fix revision;
- regression-test identifier;
- observed failure signal.

The case-pool manifest and each case record also use a consistent reproduction status. The ground-truth review status remains pending. No historical pilot or confirmatory score was changed.

## Provenance and contamination

All seven cases are public repository history. The model's exact training-data exposure is unknown. Public exposure is therefore a contamination risk, not evidence that the model definitely memorized any case. The calibration pool must not be reused as the future confirmatory pool: after it is used to assess or tune the scoring instrument, it is no longer held out.

Two candidates' upstream pull requests (#1783 and #443) explicitly state that AI tools assisted with discovery and/or fix drafting. Record this transparently in provenance and source interpretation. It does not invalidate the defects, but makes independent review of the ground-truth and fix evidence more important.

## Required exit criteria before calibration inference

1. An independent reviewer verifies each root cause and each relation against pre-fix code, fixed code, tests, and change history.
2. The reviewer records a rationale and evidence links without seeing a model's predicted diagnosis or condition assignment.
3. Any ambiguous or multi-mechanism record is narrowed, split only when the subcases are genuinely independent, or excluded with a recorded reason.
4. Only cases that pass this gate can be frozen for calibration. Calibration responses must be genuine, versioned model outputs or clearly labeled human/synthetic controls; no fabricated model responses or human labels.
5. A separate scoring-calibration set must pass the predeclared reviewer-agreement gate before the next confirmatory protocol can be frozen.

Until those requirements are met, all case-pool entries remain drafts and no new model inference is authorized.
