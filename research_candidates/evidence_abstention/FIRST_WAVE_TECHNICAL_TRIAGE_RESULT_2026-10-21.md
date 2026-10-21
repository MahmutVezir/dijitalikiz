# First-wave technical triage report — 21 October 2026

**Workflow:** [run 39644280706](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39644280706)  
**Research branch:** `research/evidence-abstention-draft-2026-10-19`  
**Branch HEAD at review:** `9621b5910f18417b98b59d8c7fc81c69e4d214b4`  
**Purpose:** Diagnostic screening only. No LLM inference was performed. No candidate in this report is accepted for confirmatory analysis.

## Result summary

All seven matrix jobs completed and uploaded integrity-audited artifacts. “Job success” means the diagnostic workflow completed and preserved its report; it does **not** mean the upstream test pair passed or that a case is eligible.

| Candidate | Raw buggy-fail/fixed-pass signals | Environment/harness concern | Decision |
|---|---|---|---|
| `BugsInPy-luigi-1` | Incomplete | Yes; buggy log resembles dependency/plugin/environment error | Exclude from confirmatory pool; diagnose or replace |
| `BugsInPy-fastapi-1` | Present in raw signals | Yes; buggy log resembles dependency/plugin/environment error | Exclude from confirmatory pool; diagnose or replace |
| `BugsInPy-black-2` | Present | No automated warning in artifact audit | Technical candidate only; prior exposure means not confirmatory |
| `BugsInPy-sanic-1` | Incomplete | Yes; buggy log resembles dependency/plugin/environment error | Exclude from confirmatory pool; diagnose or replace |
| `BugsInPy-tornado-1` | Present | No automated warning in artifact audit | Technical candidate only; prior exposure means not confirmatory |
| `BugsInPy-thefuck-1` | Incomplete | Yes; buggy log resembles dependency/plugin/environment error | Exclude from confirmatory pool; diagnose or replace |
| `BugsInPy-scrapy-1` | Present | No automated warning in artifact audit | Technical candidate only; prior exposure means not confirmatory |

“Present” refers only to automated exit-code/log markers. The artifact audit is not ground truth, and even a clean signal pair needs manual review of the raw test output, test specificity, patch, provenance, license, leakage, and evidence-level rubric. This screen is a previously exposed feasibility wave; do not promote any of these cases into the blinded confirmatory set.

## What the run establishes

- All seven jobs completed the technical-screen workflow and emitted artifacts.
- The final artifact audit reported integrity checks passing for the artifacts it audited.
- Three candidates (`black-2`, `tornado-1`, `scrapy-1`) produced paired raw test signals without an automated environment/harness warning.
- Four candidates (`luigi-1`, `fastapi-1`, `sanic-1`, `thefuck-1`) showed incomplete signals and/or an environment/harness warning. In particular, FastAPI's raw pair markers do not override the environment warning.
- Every candidate remains `accepted_for_confirmatory=false`, `confirmatory_eligible=false`, and `llm_inference_performed=false`.

## Decision and next step

This wave improves the technical triage record but does not satisfy the data gate. Keep the confirmatory registry empty. Do not run model inference.

Next, use this wave only to refine the candidate-screening method; select a **fresh, unexposed** candidate pool for confirmatory review. For each new candidate, independently establish exact-runtime reproducibility, bug-specific failure versus setup failure, fixed-pass evidence, patch/root-cause provenance, license, leakage, and E1/E2/E3 evidence sufficiency. Two independent reviewers must assess gold root cause; a separate pair must assess evidence sufficiency. Any setup or dependency failure is not a positive buggy-failure signal.

The minimum remains 60 accepted independent cases across at least 8 upstream projects (target 80), with all preregistration, hash-freeze, reviewer-calibration, and runtime gates completed before inference.
