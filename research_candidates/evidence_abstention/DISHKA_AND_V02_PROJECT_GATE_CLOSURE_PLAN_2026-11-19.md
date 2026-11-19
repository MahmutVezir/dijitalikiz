# Dishka-first execution plan and v0.2 project gate closure
**Date:** 19 November 2026  
**Status:** execution plan; not a case-acceptance decision, legal opinion or inference authorization.

## 1. Objective and operating rule

The immediate scientific objective is to obtain the first accepted independent case for the v0.2 exploratory feasibility study, beginning with Dishka #435. GitHub Actions is suitable for frozen-row extraction, exact-source reproduction, no-inference contract tests, raw provenance capture and evidence artifact generation. Standard hosted GitHub runners are not being treated as a guaranteed CUDA inference environment. The eventual 3B-model experiment requires a separately verified GPU runtime (Google Colab/Kaggle or another explicitly measured environment) after the protocol, model-use review and user authorization gates are closed. No Colab inference notebook should be run before those gates pass.

One upstream project contributes at most one case. The v0.2 feasibility minimum is one accepted independent project; the primary target is 15 and the stretch target is 20. These are targets, not permission to relax candidate criteria. Dishka and NumPyro are distinct upstream projects; NumPyro is the fallback only if Dishka fails a substantive candidate-level gate or receives a NO decision.

## 2. Current verified state

### Dishka #435
- Exact buggy base: `8718d5af93f9e48bc2506c64827663fdccc5ad89`.
- Exact fixed revision: `b1eae11734e64551d7b101195f27cb6870e1c364`.
- Independent issue reproducer: base failure `AssertionError: 1 != 42`; fixed pass.
- Frozen dataset selectors: 8/8 executed defect-related failures on base; same 8/8 passes on fixed.
- Latest reproduction: run `44596435482`, job `135816057850`, artifact `14564379897`; outer SHA-256 `bed2f0a7b04b21e2753747b1ed3324c4ff15bc789bdf1cfa1264f976178d349c`, ZIP CRC PASS, 33 members, 32/32 internal hashes PASS.
- E1/E2/E3 evidence packets: 13/9/7 items; structural/hash validation passes. Semantic gold/tier rationale is recorded separately as project-lead adjudication, not established by the structural validator.
- Gold mechanism: `G1_STALE_PER_SCOPE_FACTORY_REGISTRATION`. E3 retains G1/A1/A2; E2 retains G1/A1; E1 retains G1.
- Corrected prior pipeline/debug exposure: `none`; researcher source exposure: `full` and disclosed.
- Bounded documentary source/license scope decision: approved for the exact listed upstream revisions, five changed paths and pinned reproduction/extraction environments only. It is not legal clearance or blanket redistribution permission.
- Canonical case remains `acceptance_decision=proposed`, `final_acceptance.status=pending`. Registry remains empty.

### Recent project-wide controls
- Dishka-only candidate reproduction and no-inference preflight are now the default in the main workflow. Twelve other candidate jobs in that matrix are manual-only.
- Separate non-Dishka candidate workflows are being made manual-only to prevent common-file PR changes from starting unrelated work.
- Latest no-inference preflight run `44596435482`, job `135815854250`: 76 tests passed (12 + 25 + 6 + 23 + 10). This is a passing test suite, not a readiness approval.
- Latest readiness: `blocked_before_inference`, 14 blockers, 0 accepted cases, 0 accepted projects, valid empty registry; no model load, inference or fine-tuning.
- Qwen exact revision `aa8e72537993ba99e69dfaafa59ed015b17504d1` license/config evidence was collected without model weights (artifact `14565807914`). Human/mentor use-scope review remains pending.
- Dishka raw issue/PR and dataset-card data were captured (artifact `14566406023`). The first audit job failed on a Python regex syntax error after capture; independent inspection confirmed HTTP 200 responses, exact issue/PR dates and commits, a matching Dishka row timestamp, and pinned dataset card license `CC-BY-4.0`. A corrected successful rerun is still required.

## 3. The 14 open readiness blockers, owners and closure evidence

| # | Open gate | Accountable owner | Required evidence to close |
|---:|---|---|---|
| 1 | Dataset-wide provenance/license gate (roll-up) | Project lead + research audit workflow | All 96 primary and 17 reserve records reconciled against immutable dataset/source identities; per-record raw provenance, licensing scope and explicit exceptions; no unresolved material contradiction hidden by a summary status. |
| 2 | Underlying upstream-source and changed-file license review | Project lead, supported by exact-base source audits; mentor for uncertain rights questions | Exact base LICENSE/NOTICE/third-party provenance and changed paths for every candidate considered for intake; dependencies and copied fixtures screened; ambiguous or incompatible candidates held/excluded. Dishka's bounded scope does not clear other repositories. |
| 3 | Raw dataset timestamp authentication | Project lead + automated raw API capture | Preserve raw upstream JSON bodies and response headers for all 113 timestamp-register records, hash them, and compare PR rows to `/pulls/{n}` and issue rows to `/issues/{n}`. Resolve the SimPEG one-second exception through authoritative semantics or a predeclared conservative treatment; do not guess rounding/truncation. |
| 4 | Exact Qwen revision research-use review | Qualified mentor/institutional reviewer; project lead records outcome | Review the exact Qwen Research License Agreement at the pinned revision against non-commercial competition/research use and intended paper/prompt/output dissemination. Record permitted scope, attribution and any restrictions. This is not legal advice from the assistant. |
| 5 | Exact model/tokenizer/runtime verification | Project lead + reproducibility workflow | Lock Python, torch, transformers, accelerate, CUDA, GPU model/driver, dtype, tokenizer files/chat template and all package hashes. Run a no-output load/identity preflight only after license approval; fingerprint loaded model/tokenizer; preserve logs. Current candidate lock is not yet verified. |
| 6 | Generation settings frozen | Project lead | Finalize deterministic decoding, max tokens, stop conditions, output schema, prompt/temperature/seed fields, retry/repair policy and exactly one raw response per case-condition. Add tests and SHA-256. |
| 7 | Internal protocol/analysis/generation/scoring hash freeze | Project lead | Freeze the approved versions of the protocol, analysis plan, generation settings and scoring rules together; publish a manifest of paths, SHA-256 values and freeze timestamp. |
| 8 | Study Design Decision document frozen | Project lead; technical reviewers may advise | Resolve outstanding methodological choices, record the final decision and SHA-256, then set manifest frozen status. |
| 9 | v0.2 protocol document frozen | Project lead | Resolve sample/conditions/endpoints/deviations and make the final protocol immutable by SHA-256. |
| 10 | Analysis Plan document frozen | Project lead; independent statistician/mentor input recommended | Lock case-level pairing, primary endpoint, complete-pair handling, partial/invalid outcomes, exact McNemar scope, interval method and sensitivity analyses before model outcomes are viewed. |
| 11 | Human Evaluator Amendment frozen | Project lead + prospective Rater_B | Finalize consent, exposure, independence, calibration and blind-delivery rules before freezing; do not mark it frozen while the actual role remains unresolved. |
| 12 | Dual-human scoring rubric frozen | Project lead + Rater_B | Run calibration on non-study examples, revise rubric once, freeze/hash it before scoring; preserve six-category labels and keep evidence support distinct from hidden-gold correctness. |
| 13 | Rater_B consent, independence/exposure and calibration | A separate human scorer; project lead verifies privately | Explicit consent, case-specific source/patch/gold exposure screen, independence/conflict declaration, calibration completion and secure blinded delivery plan. Panel Reviewer B is not automatically Rater_B. Anyone who has seen Dishka's source/patch/gold cannot be called blinded for that same case. |
| 14 | At least one fully accepted independent case in registry | Mahmut as project lead; validator/CI checks structure | Dishka receives a separate timestamped YES/NO decision. Only YES plus passing case/schema/registry checks changes the record to accepted and inserts it. A NO is recorded outside the accepted registry; then NumPyro becomes the fallback. |

The 14-blocker count includes one roll-up gate (#1), source-license and raw-timestamp child gates (#2–3), model/legal/runtime/protocol/rater gates (#4–13), and the empty-registry gate (#14). Some child items overlap conceptually; they are separate validator conditions and must be closed with the evidence their individual rules require.

## 4. Execution order

### Phase A — finish Dishka's candidate-specific record
1. Rerun the corrected raw provenance job and verify its own checksum manifest.
2. Confirm latest Stage 2 artifact + proposed JSON + regression test all point to the same immutable artifact.
3. Recheck E1/E2/E3 manifests, survivor sets, gold record, source-exposure disclosure and bounded license decision.
4. Present the case-level decision packet to the project lead. Do not change `proposed` to `accepted` without a separate explicit YES.

### Phase B — decide the first case
- **YES:** write a separate timestamped and SHA-256-addressed decision record; update the canonical JSON; run schema/case/registry validators; only then insert Dishka into accepted registry.
- **NO:** preserve the rejection rationale and keep the registry empty; move to NumPyro #1916 under exactly the same unchanged criteria.
- A YES on case acceptance does not authorize model inference.

### Phase C — close global readiness
Complete gates #1–13 with responsible human evidence. Do not make the manifest say CLOSED merely because a single Dishka record or a unit-test suite passed. Re-run the no-inference readiness gate; require 0 blockers, a valid registry with at least one accepted case and an independently frozen protocol/runtime.

### Phase D — authorize and execute model inference
Only after readiness is clear and a separate user authorization is recorded:
1. Use a verified GPU environment for the exact immutable model/tokenizer pins.
2. Execute the six predeclared cells per case (P0/P1 × E1/E2/E3) with no hidden state, no retries and raw output preservation.
3. Randomize and blind outputs for human raters; preserve original ratings before adjudication.
4. Analyze evidence support and hidden-gold correctness separately; report unsupported/contradicted definitive diagnosis as the primary E3 endpoint.
5. Retain invalid/unscorable outputs separately and report sensitivity analyses without silently recoding them.

## 5. Stop rules and non-goals

- No repeated candidate reproductions when source pins, inputs and successful artifact hashes are unchanged.
- A failed non-Dishka selector does not invalidate a successful Dishka reproduction; non-Dishka candidate jobs remain manual-only during the Dishka-first phase.
- No loosening selectors, license rules, independence or exposure criteria to increase N.
- No model weights, load, inference, fine-tuning or training before their gates and separate authorization.
- GitHub Actions is the evidence/CI channel for repo checks and CPU reproductions. GPU execution is a later, separately fingerprinted step; standard hosted runners are not assumed to supply CUDA.
