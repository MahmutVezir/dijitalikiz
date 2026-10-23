# Engineering completion gate — Evidence abstention research

**As of:** 22 October 2026  
**Study status:** Not scientifically complete; confirmatory inference remains prohibited.  
**Purpose:** Distinguish implemented software from evidence that still requires independent people, external registration, or a real GPU study.

## Engineering now implemented

- Qwen candidate-generation adapter with strict structured-output parsing and prompt/seed integrity checks.
- Uncertainty-policy prototype: generation-score token entropy, candidate disagreement, calibration interface, Brier/ECE metrics, and fail-closed diagnosis decision.
- Independent inference gate; current manifest remains closed.
- Deterministic evidence-packet and citation integrity auditor: exact packet/item fields, canonical SHA-256 checks, unique evidence IDs, no known gold-label/answerability fields at packet level, and response references restricted to packet IDs.
- Bridge from structural audit to the decision layer. A semantic-audit prompt/parser interface and adapter mapping have now been added on the current development branch; malformed/missing semantic output still leaves signals unset and forces abstention. The interface has not been validated against independent human ratings.
- Synthetic unit tests for the structural auditor and adapter decision path.
- Reviewer form templates for Keras-5 and Tornado-6; they are blank forms, not completed reviews.
- Exploratory Kaggle smoke audit preserved and explicitly excluded from confirmatory results.

## Scientific completion blockers

| Requirement | Verified state | Exit criterion |
|---|---|---|
| Accepted independent cases | 0 | At least 60 accepted cases from at least 8 upstream projects; target 80 |
| Case root-cause ground truth | Not adjudicated | Two independent reviewers plus recorded disagreement/adjudication per accepted case |
| Evidence sufficiency review | Not complete | Separate, disjoint blinded panel reviews E1/E2/E3 evidence packets |
| Semantic support/contradiction runtime signals | Interface implemented in the current development PR; semantic validity not established | Execute the pinned auditor invocation only after permissions, compare against blinded human ratings on separate calibration data, report agreement/error types, and freeze an audited threshold; gold E-level labels and hidden answers never enter runtime |
| Model/tokenizer/runtime load | Not verified for study lock | Exact pinned non-quantized checkpoint, tokenizer/chat template, Python, PyTorch, Transformers and CUDA device verified without output generation |
| Calibration data and thresholds | Empty/unfrozen | Independent labeled calibration split, documented metrics, thresholds selected before confirmatory results and frozen |
| Preregistration | Draft only | Public, timestamped, auditable preregistration before any confirmatory inference |
| Study outputs and analysis | Not started | Run all predeclared E1/E2/E3 × P0/P1 cells after every gate and explicit authorization; preserve raw outputs/hashes and run predeclared paired analysis |
| Report and reproducibility package | Partial | Final methods/results/limitations, exclusions, environment, hashes, scripts and rubric linked from official report |

## Non-negotiable validity rules

1. A candidate that technically reproduces buggy-fail/fixed-pass is not automatically an accepted research case.
2. Previously opened or used cases remain excluded from the confirmatory sample regardless of outcome.
3. Structural citation validation is not semantic evidence support. The auditor never claims otherwise.
4. Self-reported confidence and repeated generations are not treated as calibrated probability or pure epistemic uncertainty.
5. Synthetic tests, code review, and smoke runs must not be presented as model-efficacy results.
6. The inference gate remains closed while any listed prerequisite is unmet. Do not weaken thresholds retroactively to meet a deadline.

## Current decision

**The engineering prototype has a testable structural-audit component, but the research project is not yet complete.** No valid scientific path permits generating confirmatory outputs before case acceptance, independent evidence review, semantic auditor validation, calibration, runtime verification, preregistration and explicit execution authorization. If the data/reviewer gates cannot be completed by the submission cutoff, report the work as a prototype/feasibility study and state that confirmatory efficacy remains unmeasured; do not claim the original hypothesis was confirmed.
