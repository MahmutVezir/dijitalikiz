# SWE-rebench V2 Filtered-Verified — source candidate audit

**Audit date:** 12 November 2026  
**Status:** CANDIDATE ONLY — not approved for confirmatory sampling  
**Scope:** Public metadata/card review, release-date reasoning, source and task-field suitability. No model inference, no fine-tuning, no upstream project tests were run in this audit.

## 1. Decision

The best alternative identified so far to BugsInPy is:

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Upstream dataset: `nebius/SWE-rebench-V2`
- Dataset card license: CC-BY-4.0
- Filtered split reported by the current dataset card: 6,272 rows
- The card describes the filtered data as a subset of 32,079 upstream tasks and reports 17 languages in its summary.
- The Hugging Face Dataset Viewer currently displays 6.27k rows, 16 language values and 13 license values. This differs from the card summary and must be resolved from a pinned snapshot before intake.

**Decision:** use this dataset as the leading replacement candidate for a metadata-only feasibility audit. Do not yet replace BugsInPy in the project manifest and do not use any row as an accepted case. The 6,272 rows are the entire filtered pool, not 6,272 Python cases, not 6,272 post-model-release cases, and not 6,272 confirmatory cases.

## 2. Why this source is promising

The upstream SWE-rebench V2 paper reports 32,079 tasks across 20 programming languages and 3,617 repositories. It describes an automated collection and validation pipeline, and instance-level metadata for common confounders such as underspecified descriptions and overly restrictive tests.

The filtered-verified derivative applies additional screening, according to its published card and reproduction code:

- LLM-judge metadata: difficulty is present; `code == "A"`; `intent_completeness == "complete"`; all detected issue flags B1–B6 are false; confidence is at least 0.95; and no external URLs are present.
- Issue/PR cross-references in problem statements are excluded.
- A manual environment-image blocklist and repository blocklist are applied.
- Gold-patch validation must pass with reward 1.0.
- An independent second validation removes flaky rows.
- No-edit-pass rows are excluded.
- Further always-fail cases are revalidated and excluded.

This is stronger screening than a raw metadata inventory. It still does not establish that a case has a unique root cause, valid E1/E2/E3 evidence tiers, a legally reusable code snapshot, or independent ground truth for this project's research question.

## 3. Important source fields and leakage rules

The current source schema exposes:

- `instance_id`, `repo`, `base_commit`, `created_at`
- `language`, `license`
- `problem_statement`, `pr_description`, `interface`
- `patch`, `test_patch`
- `FAIL_TO_PASS`, `PASS_TO_PASS`
- `install_config`, `meta`

The filtered dataset card states that `problem_statement` is the raw GitHub issue body and `pr_description` is the raw merged PR description.

For model input, the default safe starting point is the issue body plus a separately constructed, hashed evidence packet drawn from the repository at `base_commit`. The following must not be exposed to the model:

- `patch` (the gold fix)
- `test_patch` (tests added/changed by the fixing PR)
- `pr_description` (can reveal the completed fix)
- `interface` and `meta` (derived descriptions/quality annotations that may disclose solution information)
- fixed commit identifiers, hidden labels, reviewer decisions, or answerability labels

`FAIL_TO_PASS` and `PASS_TO_PASS` are adjudication/validation metadata, not model evidence. They may be used by the human panel and reproducibility gate, but their names and contents must not leak into prompts where they disclose the fix.

The dataset's LLM-judge `code` and B1–B6 labels are screening aids only. They must not be treated as this study's gold labels or as independent human judgments.

## 4. Model-release-date screen

The official Qwen announcement dates the Qwen2.5 release, including the 3B size, to 19 September 2024.

For the frozen candidate `Qwen/Qwen2.5-3B-Instruct`, revision `aa8e72537993ba99e69dfaafa59ed015b17504d1`, the proposed conservative metadata screen is:

- retain only rows whose original GitHub issue/PR `created_at` is on or after **2024-09-20 UTC**;
- use the field's actual type and semantics from a pinned dataset snapshot, not assumptions from the UI;
- report the date filter as a mitigation against exact issue/PR memorization, not proof of zero contamination. Public repositories and earlier source code may still be familiar to the model.

The dataset page shows dates spanning 2014-12-24 to 2025-10-28. The post-2024-09-19 Python/licensed subset has not yet been counted.

## 5. License boundary

The dataset card declares CC-BY-4.0 and says the license of each underlying repository at the relevant commit is supplied per row. These are separate layers:

1. CC-BY-4.0 applies to the dataset release as stated by its publisher.
2. The source repository's recorded `license` value and the actual license file at the exact base/fixed commits govern the source code and patches.

Do not infer that CC-BY-4.0 relicenses repository code. Before accepting any case, independently inspect the exact repository license at the relevant commits, record SPDX identifier and license-file hash, confirm any attribution/notice/share-alike obligations, and obtain maintainer or institutional guidance where unclear. Do not copy upstream source code or patches into this repository unless redistribution is explicitly permitted.

BugsInPy remains blocked as a primary data source until its license/permission status is clarified. This audit does not resolve that separate blocker.

## 6. Required metadata-only feasibility filters

Before any technical testing or model execution, run a pinned, reproducible inventory that reports counts and identifiers after each successive filter:

1. Exact dataset revision and Parquet-file SHA-256 values pinned.
2. Language is exactly Python.
3. `created_at >= 2024-09-20T00:00:00Z`, after parsing the actual source representation.
4. Non-empty `repo`, valid 40-hex `base_commit`, non-empty problem statement, and non-empty `FAIL_TO_PASS`.
5. Per-row source license is present and included in a separately reviewed allowlist; unknown/custom/missing license values are excluded pending review.
6. No duplicate `instance_id`, same PR/issue, or same underlying bug/root-cause family.
7. Count distinct repositories/projects and ensure exposure exclusions are applied.
8. Record every exclusion with a machine-readable reason.

The audit must explicitly reconcile two currently visible representation differences before it is considered complete:
- the Hub overview summary says 17 languages, while the Dataset Viewer currently shows 16 language values;
- the upstream card schema describes `created_at` as an integer timestamp in milliseconds, while the filtered Dataset Viewer labels it as a date string.

These may reflect card/UI serialization differences, but must be verified from the pinned data bytes. Do not silently coerce or guess.

## 7. Case acceptance after metadata screening

A metadata-eligible row is still only a candidate. For each proposed case, all of the following are required:

- upstream repository and exact base commit are retrievable;
- exact per-repository license is reviewed and documented;
- the target test is executed at the buggy/base state and fixed state in the prescribed reproducible environment; expected buggy-fail/fixed-pass behavior is observed and logged;
- gold root cause is established from source/test/fix evidence by the root-cause panel;
- E1 (sufficient), E2 (partial) and E3 (insufficient) packets are prepared without fabricated evidence or answer leakage;
- the separate evidence-support panel confirms that E3 does not uniquely support the gold diagnosis and that E1 does;
- reviewers are blind to model outputs and each other's labels until adjudication;
- exposure, duplicates, contamination risks and hashes are recorded.

The filtered dataset's quality labels do not replace these project-specific checks.

## 8. Sample-size gate and decision rule

The confirmatory target remains 80 accepted independent cases, with a minimum of 60 cases from at least 8 distinct upstream projects. Only cases that pass every legal, reproducibility, gold-label, evidence, and exposure gate count toward this total.

If the filtered Python/post-release/licensed pool yields fewer than 60 accepted cases, do not relax filters after seeing results. Either broaden to another independently audited source under a frozen, documented rule or report the work as exploratory/feasibility. Do not represent metadata candidates as accepted cases.

## 9. Current state and next action

| Item | Status |
|---|---|
| Candidate source identified | Done |
| Public card and paper reviewed | Done |
| Dataset and source-license distinction documented | Done |
| Exact dataset revision pinned | Not done |
| Python + post-2024-09-19 + license counts | Not done |
| Language-count and created_at representation reconciled | Not done |
| Per-repository license audit | Not done |
| Technical fail-to-pass checks | Not done |
| Independent root-cause/evidence panels | Not done |
| Accepted confirmatory cases | 0 |
| Model inference / fine-tuning | Prohibited until all gates pass |

**Next bounded task:** build a no-inference metadata inventory for the exact filtered-verified dataset revision. It should pin the source revision, count Python cases after the proposed release-date cutoff by exact repository license, report distinct projects, validate schema types, and emit hashes plus explicit exclusion reasons. It must not download or store gold patches in the model-input area, run tests, load the model, or change the inference gate.

## 10. Sources

- SWE-rebench V2 paper, PMLR 306 (2026): https://proceedings.mlr.press/v306/badertdinov26a.html
- Upstream dataset: https://huggingface.co/datasets/nebius/SWE-rebench-V2
- Filtered-verified dataset and full filter/reproduction description: https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified
- Qwen2.5 release announcement (19 September 2024): https://qwenlm.github.io/blog/qwen2.5/
- Hugging Face Dataset Viewer filter API documentation: https://huggingface.co/docs/dataset-viewer/filter

This document records a source candidate and its limitations; it is not a preregistration, legal opinion, approved dataset, or experiment result.
