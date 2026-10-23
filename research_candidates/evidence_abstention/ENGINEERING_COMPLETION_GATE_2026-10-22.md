# Engineering completion gate — Evidence abstention research

**As of:** 22 October 2026  
**Study status:** Not scientifically complete; confirmatory inference remains prohibited.  
**Purpose:** Distinguish implemented software from evidence that still requires independent people, external registration, or a real GPU study.

## Engineering now implemented

- Qwen candidate-generation adapter with strict structured-output parsing and prompt/seed integrity checks.
- Uncertainty-policy prototype: generation-score token entropy, candidate disagreement, calibration interface, Brier/ECE metrics, and fail-closed diagnosis decision.
- Independent inference gate; current manifest remains closed.
- Deterministic evidence-packet and citation integrity auditor: exact packet/item fields, canonical SHA-256 checks, unique evidence IDs, no known gold-label/answerability fields at packet level, and response references restricted to packet IDs.
- Bridge from structural audit to the decision layer. The semantic-audit prompt/parser interface and adapter mapping are in the main branch; input validation was further hardened in the current follow-up branch. Twelve isolated local tests for the semantic-audit module passed, but the full GitHub Actions/adapter suite and semantic validity against independent human ratings are not confirmed.
- Synthetic unit tests for the structural auditor and adapter decision path.
- Reviewer form templates for Keras-5 and Tornado-6; they are blank forms, not completed reviews.
- Exploratory Kaggle smoke audit preserved and explicitly excluded from confirmatory results.

## Scientific completion blockers

| Requirement | Verified state | Exit criterion |
|---|---|---|
| Accepted independent cases | 0 | At least 60 accepted cases from at least 8 upstream projects; target 80 |
| Case root-cause ground truth | Not adjudicated | Two independent reviewers plus recorded disagreement/adjudication per accepted case |
| Evidence sufficiency review | Not complete | Separate, disjoint blinded panel reviews E1/E2/E3 evidence packets |
| Semantic support/contradiction runtime signals | Hash-bound prompt/parser/adapter interface implemented; semantic validity not established | This is a separate uncertainty-adapter prototype, not an input to the core prompt-only P0/P1 confirmatory contrast. Before making efficacy/operational-threshold claims, run the full integrated tests, validate against separate blinded human ratings and freeze the calibration threshold; never expose gold E-level labels or hidden answers. |
| Model/tokenizer/runtime load | Not verified for study lock | Exact pinned non-quantized checkpoint, tokenizer/chat template, Python, PyTorch, Transformers and CUDA device verified without output generation |
| Calibration data and thresholds | Empty/unfrozen | Required for the separate score/entropy/semantic-auditor adapter efficacy claim. The main prompt-only P0/P1 confirmatory experiment must not add threshold scores or mix this adapter into P1 unless a new protocol version is frozen before any inference. |
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

**The engineering prototype has a testable structural-audit component, but the research project is not yet complete.** The core confirmatory design is the frozen prompt-only E1/E2/E3 × P0/P1 comparison; it requires accepted cases, independent root-cause and evidence-sufficiency reviews, exact runtime verification, hash freezing, a verifiable preregistration and explicit execution authorization. It does not use the separate entropy/semantic-auditor adapter. That adapter remains unvalidated and must be separately calibrated and tested before any operational-threshold or efficacy claim about it. If the core data/reviewer gates cannot be completed by the submission cutoff, report the work as a prototype/feasibility study and state that confirmatory efficacy remains unmeasured; do not claim the hypothesis was confirmed.
