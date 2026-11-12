# SWE-rebench V2 — deterministic 96-project pre-review cohort result

**Run date:** 12 November 2026  
**GitHub Actions run:** https://github.com/MahmutVezir/dijitalikiz/actions/runs/43257277504  
**Artifact ID:** `13960884569`  
**Result:** SUCCESS — deterministic metadata-only selection  
**Scientific acceptance:** 0 cases

## 1. Reproducibility pins

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Immutable Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Metadata candidate CSV SHA-256: `805559607aa5711a2d527e2429733d85e267f592e95609a27e54872bc0f91e14`
- Selection seed: `tubitak-2204a-evidence-abstention-cohort-v1-2026-11-12`
- Selection implementation: `scripts/select_swe_rebench_project_cohort.py`
- Sampler test file: `tests/test_select_swe_rebench_project_cohort.py`
- Six synthetic unit tests passed; input-order invariance and duplicate-ID fail-closed behavior are covered.

## 2. Sampling frame and allocation

The metadata-only pre-screen starts with 347 rows. Applying the previously declared source-license identifier allowlist and removing the four upstream repositories exposed during the earlier BugsInPy work leaves:

- 261 metadata candidate rows
- 113 distinct GitHub repositories
- 5 license strata

The four whole repositories excluded for prior exposure are:
- `keras-team/keras`
- `pandas-dev/pandas`
- `scrapy/scrapy`
- `tornadoweb/tornado`

Project quotas use Hamilton proportional allocation according to the number of repositories in each source-license stratum. Within each stratum, repositories are ranked by SHA-256 of the fixed seed plus the stratum and repository name. One candidate instance per repository is selected by a second SHA-256 ranking. This makes selection reproducible and independent of input row order.

| Dataset license field | Available projects | Primary quota |
|---|---:|---:|
| MIT | 47 | 40 |
| Apache-2.0 | 33 | 28 |
| BSD-3-Clause | 29 | 24 |
| MIT-0 | 2 | 2 |
| BSD-2-Clause | 2 | 2 |
| **Total** | **113** | **96** |

## 3. Outputs

| Output | Rows | Distinct repositories | SHA-256 |
|---|---:|---:|---|
| Primary pre-review cohort | 96 | 96 | `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db` |
| Project-level reserves | 17 | 17 | `43957115a4eeaa748e178f3456df61cb319b6be422fc74f2ecc25713b2d21019` |
| Within-project alternatives | 148 | 53 | `b417bc094de271afe01a4505a3717efe6a6ea70e4221cbff72f355b7af535aa9` |

The within-project alternatives are potential replacement issues from repositories already represented in the primary or reserve list. They are not additional independent projects. A single repository contributes at most one selected primary case.

Manifest SHA-256: `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`.

## 4. Interpretation and remaining gates

This is a **pre-review candidate cohort**, not a preregistered confirmatory sample and not a validated dataset. The source dataset's per-row license metadata is only a screening signal. For each chosen case, reviewers must inspect the actual source license at the exact base commit and record the license-file hash and SPDX value. Repositories that are forks or share a common upstream project must be grouped or excluded so 96 GitHub repository names are not mistakenly treated as 96 independent projects.

Before any case is accepted:
1. Verify exact source license and applicable reuse/attribution obligations at the base commit.
2. Check repository forks, shared project ancestry, duplicate issues/PRs, and all prior exposure records.
3. Retrieve the exact base revision and validate the target test in a reproducible environment; the intended failure/pass pair must be demonstrated.
4. Independently adjudicate the gold root cause.
5. Prepare E1/E2/E3 evidence packets without leaking the patch, fixed commit, PR solution description, or hidden labels.
6. Obtain independent, disjoint human-panel ratings for root-cause correctness and evidence sufficiency, with consent and required institutional approval.
7. Freeze the final sample, prompts, model/tokenizer/runtime revisions, analysis plan and hashes in a preregistration before inference.

The project's target remains at least 60 accepted independent cases across at least 8 genuinely independent upstream projects, with 80 as the target. If filtering and verification leave fewer than 60, report an exploratory/feasibility study rather than relaxing the criteria after seeing outcomes.

## 5. No-inference statement

This selection workflow:
- read only the precomputed metadata candidate CSV;
- did not fetch upstream source code or run upstream tests;
- did not inspect or copy gold patches;
- did not run human adjudication;
- did not load model weights;
- did not perform LLM inference or fine-tuning;
- records `accepted_confirmatory_cases = 0`.

The primary model inference gate remains closed. This document does not authorize technical tests, confirmatory sampling, model execution, or training.
