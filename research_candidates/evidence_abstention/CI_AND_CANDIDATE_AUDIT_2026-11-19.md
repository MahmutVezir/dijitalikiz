# Research and CI audit — 19 November 2026

**Repository:** `MahmutVezir/dijitalikiz`  
**PR:** [#222 — Continue v0.2 evidence validation](https://github.com/MahmutVezir/dijitalikiz/pull/222)  
**Branch:** `research/2026-11-16-followup-evidence-validation`  
**Branch head when this audit was prepared:** `4c564a44f0b878279cb6b7e9c03202abd13e5384`  
**Latest broad CI evidence summarized below:** tested commit `d9ca5b9ff0976ffe59f16955e3924fa13fbf08e2`. The commits after that tested head add documentation only; this audit does not claim the new documentation commit has already passed its own workflow run.

## 1. Overall status

- Research Validation (repository/configuration validation, no inference): PASS, run [44527515859](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515859).
- Qwen adapter unit tests: PASS, run [44527515630](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515630).
- Evidence-abstention uncertainty unit tests: PASS, run [44527515800](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515800).
- The no-inference preflight job inside run [44527515547](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515547) passed its five test groups: 12 packet-audit tests, 25 operational/nested-packet/ledger tests, 6 selector-runner tests, 15 v0.2 acceptance/preflight tests, and 9 v0.2 design tests (67 total).
- The aggregate candidate-matrix workflow [44527515547](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515547) concluded FAILURE because three candidate reproduction jobs did not satisfy their complete frozen-selector contract: Nox, Moto and Werkzeug. This does not negate the successful no-inference preflight subjob.
- The latest readiness report still records `ready_for_inference=false`, `accepted_case_count=0`, `blocker_count=14`, and no model loading, inference or training.

## 2. Candidate-level results

### Exact Stage 2 base-fail / fixed-pass results in the 19 November run set

| Candidate | Run / artifact | Technical outcome | Remaining disposition |
|---|---|---|---|
| PyThaiNLP #1046 / issue #1004 | [Run 44527515499](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515499), artifact 14533236026, SHA-256 `8f50213b6811d745f218686c351fc04a4ad5a4b57214743bd84a6806a99ceef3` | Exact frozen selector failed on buggy base and passed on fixed revision; two one-word issue examples also reproduced independently as supporting tests | Stage 3, dependency/native-license review, independence and exposure review pending; not accepted |
| Modin #7554 / issue #7553 | [Run 44527515483](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515483), artifact 14532441159, SHA-256 `585aefcd2115ded47b652bea8df50d7f2ba8cc090c06b2bda85b5f56463ec381` | Both exact parameterized selectors failed on buggy base and passed on fixed revision | Conditional hold: issue title says AutoSwitchBackend is ON, while PR and frozen selectors test OFF/False; human scope decision and Stage 3 remain open |
| Napalm #2152 / issue #2151 | [Run 44527515728](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515728), artifact 14532001249, SHA-256 `c95bfef60012dd5337394cc448a087e2aa5c559d0f94468c82ebb67990403573` | Exact frozen selector failed on buggy base and passed on fixed revision; a separate minimal synthetic parser check also passed its base-fail/fixed-pass contract | Conditional hold: Cisco NX-OS upstream fixture source and redistribution provenance/license remain unresolved; full dependency-license scope and Stage 3 pending |
| SkyPilot #5985 / issue #5981 | [Run 44527515362](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515362), artifact 14532511241, SHA-256 `caad01392540cdd256cf667958429eedf49a1a4207ab96f9df2a660cecb4cd52` | Exact frozen SSH selector failed on buggy base with the incorrect `taging` context result and passed on fixed revision | Stage 3, dependency-license review, repository/issue-family independence, exposure review and final acceptance pending |
| CTAPIpe #2732 / issue #2730 | [Run 44527515529](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515529), artifact 14530898015, SHA-256 `e965d39a9bca12ec15e901ec828828a6ce363157c930382fe67c06c6b6ea1250` | Frozen selector and direct HDF5/DataWriter reproduction passed the base-fail/fixed-pass contract | Technically valid engineering/feasibility pilot only. Project-lead decision records `prior_pipeline_debug_exposure=some`; exclude from the model-evaluation sample. Issue YAML/effective-configuration discrepancy and license scope remain documented |

The exact outcome above is based on the raw job logs and candidate records. A passing Actions job is not itself final case acceptance.

### Other successful reproduction jobs in the same preflight matrix

The following candidate jobs completed successfully: Dishka #435, Meltano #3090, NumPyro #1916, Robocop #1371, Dymos #1166, QuTiP #2646, Amaranth #1518, PyFar #721, Python-Control #1144 and EODAG #1530. These are Stage 2 workflow outcomes only. The current case registry still contains zero accepted cases. Candidate-specific Stage 3, license, independence, exposure and acceptance requirements remain authoritative.

### Candidates that remain held or incomplete

- **Nox #919:** latest selector matrix did not meet the complete contract (24/27 base selector checks). Immutable dataset selectors include malformed/obsolete cases and references to `UV_VERSION` not present in the pinned base. Do not call this an upstream defect reproduction pass.
- **Moto #8269:** the independent ECR reproducer produced the expected missing-tag assertion on the buggy base, but the immutable dataset row has 18 selectors and 12 collection errors. The aggregate runner correctly fails closed; the dataset row remains mixed-scope and cannot be accepted by counting only the one issue-specific selector.
- **Werkzeug #2955:** one of two frozen parameterized selectors is malformed/truncated and produces “not found / no tests ran”; only one selector executes. The complete row contract therefore remains blocked.
- **DataComPy #404:** [run 44527515783](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515783) authenticated the row and selectors only. Candidate review identifies a mixed-scope target-test mismatch with issue #58 (empty NumPy arrays); no Stage 2 base/fix result is claimed.
- **PSyclone #2755:** see section 3. Dataset discovery and environment lock passed; the exact Stage 2 test workflow has not been manually dispatched.

## 3. PSyclone #2755 — latest artifact integrity and next action

The latest branch-head discovery and environment-lock artifacts were downloaded and independently verified in the local working environment:

| Artifact | Run | Artifact ID | Outer SHA-256 | ZIP CRC | Internal SHA-256 |
|---|---:|---:|---|---|---|
| Frozen row/selector discovery | [44527515429](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515429) | 14533280891 | `6e3313297edf36101f2978e8d9674e3cf420ddcdbffde549e8f7dcbffc73c6a1` | PASS | 7/7 PASS |
| Python 3.13 environment lock | [44527515544](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44527515544) | 14533171129 | `bf097d110428032801666b2ff26164a09413f68014251bf9c902ca0266d1aeea` | PASS | 9/9 PASS |

Both uploaded ZIP digests exactly matched GitHub's artifact digests. Discovery confirms frozen row `stfc__psyclone-2767`, 3 FAIL_TO_PASS selectors and 84 PASS_TO_PASS selectors. Static preflight confirms the production and test patches apply to the buggy base and all selector functions are present on both the test-patched base and fixed revision.

Environment lock: Ubuntu 22.04 x86_64, Python 3.13.0, 37 locked packages and 37 hashed wheels. The lock-resolution job builds/installs the local upstream PSyclone wheel as part of dependency resolution but executes no source tests. Human dependency-license review remains open.

**Stage 2 has not been run.** The workflow `.github/workflows/psyclone-2755-stage2-reproduction.yml` is manual-only and requires both `confirm_stage2_protocol=true` and `confirm_model_inference_disabled=true`. Its next action is to execute all three exact FAIL_TO_PASS selectors on the buggy base and fixed revision, plus the 84 frozen PASS_TO_PASS controls. Environment-lock success is not reproduction success.

## 4. Model-training decision and plan

A separate secondary training plan was added at:

`research_candidates/evidence_abstention/MODEL_TRAINING_PLAN_V0_1_DRAFT_2026-11-19.md`

It records the project lead's goal of training a model while preserving the causal interpretation of the primary experiment:

- The primary P0/P1 comparison must use the same frozen base model and must not be confounded by changed weights.
- A later LoRA/adaptor study is a separate secondary hypothesis, compared against the same base model under the same P1 policy on a project-disjoint holdout.
- The proposed training gate is at least 80 accepted independent cases from 80 distinct upstream projects, with 60 training, 10 validation and 10 locked-test cases as minimum split sizes. This is stricter than, and does not waive, the existing inference gate.
- Training labels must be independently adjudicated from visible evidence; hidden gold, patches, fixes, E-tier labels and test outputs must not leak into model-visible inputs.
- The exact Qwen revision's `qwen-research` license and derivative/adapter terms require human review. No adapter or weights have been created.

This is a design record only. It authorizes no model download, load, generation, fine-tuning or training.

## 5. Research gates still open

1. Dataset-level provenance, raw timestamp authentication, upstream/source/dependency licenses and exact model-license review.
2. Candidate Stage 3 gold mechanism, alternatives and semantic E1/E2/E3 adjudication.
3. Rater B's explicit consent and candidate-specific independence/exposure screening; separate calibration and locked rubric.
4. Protocol, analysis plan, prompts, output schema, generation settings and relevant artifacts frozen and hash-recorded.
5. At least one fully accepted case before any inference under the existing gate; 60 accepted cases across at least eight projects for the current inference-gate threshold; the secondary training plan proposes a higher 80-case/80-project threshold.
6. Explicit, separately recorded authorization for the permitted operation.

**Current final state:** accepted cases 0; inference readiness false; 14 blockers; no model loading, inference, fine-tuning or training performed.


## 6. Latest branch-head repeat — commit `a6c4ca3d8edddb3adedcf13185fdc178b69530a3` (13:07 UTC)

The documentation and PSyclone integrity-record update triggered another independent set of workflows on the updated branch head.

Completed:
- Research Validation run [44530391459](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391459): PASS.
- Uncertainty unit tests run [44530392002](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530392002): PASS.
- Qwen adapter tests run [44530391635](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391635): PASS.
- Runner smoke test run [44530391474](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391474): PASS.
- PyThaiNLP #1046 exact-selector repeat [44530391899](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391899): PASS.
- PyThaiNLP #1046 pinned sanitized Stage 2 [44530391414](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391414): PASS.
- CTAPIpe #2732 engineering-pilot Stage 2 [44530391450](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391450): PASS technically; prior pipeline/debug exposure still excludes it from model evaluation.
- Napalm #2151 pinned Stage 2 [44530391712](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391712): PASS technically; Cisco fixture provenance/license hold remains.
- Napalm synthetic reproducer [44530391677](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391677): PASS.
- Modin #7554 exact selector repeat [44530391704](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391704): PASS technically; ON vs OFF/False scope hold remains.
- SkyPilot #5981 pinned repeat [44530391449](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391449): PASS technically; Stage 3/license/independence gates remain.
- PSyclone row discovery [44530391485](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391485): PASS (discovery only).
- PSyclone Python 3.13 environment lock [44530391587](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391587): PASS (environment build only).
- DataComPy #404 row discovery [44530391592](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391592): PASS (discovery only).
- Modin #7554 row discovery [44530391585](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391585): PASS (discovery only).

The aggregate no-inference preflight run [44530391462](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44530391462) remains in progress at the latest poll because QuTiP's exact buggy-base source build has not completed. Its no-inference preflight job [135581824587] has completed successfully. That job passed the same five test groups (67 tests total) and reports `ready_for_inference=false`, 14 blockers, 0 accepted cases, `model_loading_performed=false`, and `model_inference_performed=false`.

The current matrix still shows three immutable-selector contract failures:
- Nox: malformed/incompatible selectors and base-source attribute mismatch; no full row reproduction claim.
- Werkzeug: a malformed parameterized node ID; one selector is not found and no test runs.
- Moto: the full dataset row has 12 collection errors among 18 selectors; its independent ECR reproducer does not cure the row-level failure.

At the latest review, no PSyclone Stage 2 Exact Base-Fail / Fixed-Pass run exists. A search of the recent workflow history found no run with that Stage 2 workflow name. The manual-only Stage 2 workflow still needs the project lead to open the Actions page and explicitly set both required confirmations true. No model loading, inference or training was performed.
