# SWE-rebench V2 Filtered-Verified — data snapshot correction

**Audit date:** 12 November 2026  
**Purpose:** Correct and refine the initial source-candidate audit after inspecting the live dataset card, Parquet file history, and Dataset Viewer.  
**Status:** Metadata snapshot is now better pinned; row-level eligibility counts remain unmeasured.

## 1. Exact snapshot observed

Dataset repository: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`

- Current repository revision observed: `6a0d56b425a893b018616587cdb71aa499c5fc99`
- Data file: `data/train-00000-of-00001.parquet`
- Latest data-file commit observed: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Data file SHA-256 reported by Hugging Face Xet pointer: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Data file size: `226272977` bytes
- Dataset README `dataset_info.splits.train.num_examples`: `6272`
- Dataset Viewer: `train · 6.27k rows`
- README `num_bytes`: `276137448`

The 6,272 row count is supported by both the generated README split metadata and the Dataset Viewer. It is the published row count for the filtered train split, not the count of eligible Python/post-release/license-cleared cases.

A separate repository file `validation.jsonl` and its commit description refer to 8,450 validation outcomes. That is not the Parquet train-split row count and must not be substituted for it.

## 2. Schema reconciliation — corrected

The first source audit described the `created_at` field as a schema discrepancy between the upstream dataset and the filtered dataset. The current evidence supports a more precise interpretation:

- The filtered dataset's machine-readable README front matter declares `created_at: string`.
- The Dataset Viewer also displays `created_at` as a string/date, with observed values from 2014-12-24 through 2025-10-28.
- A later detailed field-description table in the same README says `created_at` is `int64` Unix milliseconds.

Therefore, the filtered dataset documentation is internally inconsistent. The generated metadata and Viewer agree on a string/date representation, while the later prose table appears to retain the upstream integer description. The actual Parquet physical/logical schema still requires direct inspection before a parser is frozen. The first audit's statement that the filtered Viewer differed from the filtered front matter should not be relied upon.

The proposed cutoff remains 2024-09-20 UTC. The metadata inventory must parse the actual Parquet field safely, report invalid/missing dates, and never guess whether a value is epoch milliseconds or a formatted date string.

## 3. Language-count reconciliation — still open

- Dataset README prose says the filtered set spans 17 languages.
- The Dataset Viewer reports 16 distinct values for the `language` column.

This remains a source-card/viewer discrepancy. Do not assume the viewer is wrong or infer the missing language. The exact distinct values and per-language counts must be computed from the pinned Parquet snapshot.

## 4. What has and has not been verified

| Claim | Evidence | Status |
|---|---|---|
| Filtered train split has 6,272 rows | README generated split metadata + Viewer 6.27k | Published count confirmed |
| Parquet file bytes are pinned | Xet SHA-256 and exact file size | Pointer metadata recorded; bytes not downloaded locally |
| Filtered `created_at` is string | README front matter + Viewer | Reported metadata agrees; Parquet schema still to inspect |
| 17 distinct languages | README prose | Not reconciled with Viewer 16 values |
| Python cases after 2024-09-19 | No row-level inventory yet | Not measured |
| Post-release cases by SPDX license | No row-level inventory yet | Not measured |
| At least 8 distinct eligible repositories | No row-level inventory yet | Not measured |
| At least 60 eligible confirmatory cases | No row-level inventory or technical/human adjudication | Not established |

## 5. Next no-inference inventory

Use the exact repository revision above and verify the Parquet bytes against the SHA-256 before parsing. Then emit:

1. Exact Parquet schema (physical and logical types).
2. Total row count from the file itself.
3. Distinct `language` values and counts.
4. `language == "Python"` count.
5. Parseable `created_at >= 2024-09-20T00:00:00Z` count among Python rows.
6. Those post-cutoff Python rows grouped by exact SPDX `license` value, with missing/unknown values separately counted.
7. Distinct `repo` count after each filter.
8. Duplicate `instance_id`, repeated repo/PR, malformed `base_commit`, missing `FAIL_TO_PASS`, and empty `problem_statement` exclusions with reason codes.
9. A deterministic CSV/JSON inventory with SHA-256 and a run manifest.

Do not copy `patch`, `test_patch`, `pr_description`, `interface`, hidden quality labels, or solution-bearing metadata into the model-input packet. Keep them in a separate adjudication/reproducibility area, access controlled and excluded from prompts.

The metadata inventory is not technical case acceptance. Before a case counts toward the project, source license must be checked at the relevant commit, the target test must fail at the base and pass at the fixed state in its reproducible environment, gold root cause must be independently adjudicated, evidence tiers must be independently validated, and exposure/duplication checks must pass.

## 6. Research status remains unchanged

- Candidate dataset: promising, not finally approved.
- Accepted confirmatory cases: 0.
- Minimum target: 60 cases across at least 8 upstream projects; target 80.
- Model loading/inference: prohibited until dataset, human, protocol, model-license, runtime, and preregistration gates pass.
- Fine-tuning: not part of the primary P0/P1 causal comparison.

## 7. Sources

- Dataset root and revision: https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified/tree/6a0d56b425a893b018616587cdb71aa499c5fc99
- Dataset README at pinned revision: https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified/blob/6a0d56b425a893b018616587cdb71aa499c5fc99/README.md
- Parquet file and Xet pointer metadata: https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified/blob/fb9aa226b2ce37c708ea7732e7b980abacdadb67/data/train-00000-of-00001.parquet
- SWE-rebench V2 paper: https://proceedings.mlr.press/v306/badertdinov26a.html

This correction does not approve the source for confirmatory use and does not authorize upstream tests, model inference, or training.
