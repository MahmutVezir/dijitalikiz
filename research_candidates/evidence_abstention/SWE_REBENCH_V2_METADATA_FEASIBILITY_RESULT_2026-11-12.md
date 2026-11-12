# SWE-rebench V2 Filtered-Verified — metadata feasibility result

**Run date:** 12 November 2026  
**GitHub Actions run:** https://github.com/MahmutVezir/dijitalikiz/actions/runs/43253531763  
**Artifact ID:** `13960196648`  
**Status:** METADATA FEASIBILITY PASS; DATASET/CASE ACCEPTANCE NOT APPROVED

## 1. Reproducibility record

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Immutable Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- File size: `226272977` bytes
- Expected and observed SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Expected and observed Parquet rows: `6272`
- Reader: `pyarrow==19.0.1`
- Repository commit used by workflow: `2063752d67c48026398aed291aa60af9af3d0de2`
- Candidate CSV SHA-256: `805559607aa5711a2d527e2429733d85e267f592e95609a27e54872bc0f91e14`
- Summary JSON SHA-256: `da36918ee9dab5ea3f004c8c9a9041134d06f332301e4b930ba348759c2576c0`
- Artifact ZIP SHA-256: `f7f3381170f1c432e1733472302762b618d1ad8206b344026ffaf29433c81109`

The workflow verified the file size and SHA-256 before reading it. The observed row count matched the pinned expected count.

## 2. Actual metadata counts

| Filter or measurement | Result |
|---|---:|
| Total train rows | 6,272 |
| Distinct language values observed | 16 |
| Python rows | 1,952 |
| Python rows created on/after 2024-09-20 UTC | 349 |
| Metadata candidates after required-field and duplicate-ID checks | 347 |
| Distinct repositories among those 347 candidates | 154 |

The Parquet schema confirms `created_at` is a string. All 6,272 timestamps were naive strings without a UTC offset. The inventory interpreted these issue/PR creation timestamps as UTC, consistent with GitHub's timestamp convention, and explicitly recorded that assumption. This must remain visible in the report and must be rechecked against the source timestamp conversion before the cutoff is frozen into a preregistration.

The actual data contains 16 language values, not 17 as stated in the README prose. The README's generated split metadata and Viewer agree on 6,272 rows. The separate 8,450-row validation-outcomes file/commit text is not the Parquet train split.

## 3. Candidate source-license distribution

Among the 347 metadata candidates:

| Dataset license field | Candidate rows |
|---|---:|
| MIT | 101 |
| Apache-2.0 | 89 |
| custom-check-github | 72 |
| BSD-3-Clause | 57 |
| MIT-0 | 22 |
| BSD-2-Clause | 4 |
| AFL-3.0 | 1 |
| NCSA | 1 |
| **Total** | **347** |

The `custom-check-github` marker is not treated as an approved SPDX license. The AFL-3.0 and NCSA values were also kept outside the preliminary allowlist for this screening step.

For a conservative *metadata-only sampling pre-screen*, the following standard permissive SPDX identifiers were retained: `MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, and `MIT-0`.

This yields **273 candidate rows across 117 repositories**. It is not final legal clearance: the exact upstream LICENSE file and SPDX identifier still need to be checked at the relevant repository commit for every selected case. The dataset's CC-BY-4.0 license does not replace those source-repository obligations.

## 4. Prior-exposure project exclusion

Earlier BugsInPy feasibility and workflow work exposed project material from multiple repositories. To avoid carrying project familiarity into the new confirmatory pool, this pre-screen conservatively excludes all candidate rows from these overlapping repositories:

| Repository | Excluded candidate rows |
|---|---:|
| `keras-team/keras` | 4 |
| `tornadoweb/tornado` | 5 |
| `scrapy/scrapy` | 2 |
| `pandas-dev/pandas` | 1 |
| **Total** | **12** |

After this whole-repository exclusion, the current metadata-only pool is **261 candidates across 113 repositories**.

This is stricter than exact-issue exclusion. It is a transparent contamination-control decision based on prior project exposure, not evidence that every record in those projects is the same bug.

## 5. What this result establishes

The current dataset appears large enough at the metadata level to proceed with a carefully controlled next phase. There are 261 candidate records across 113 repositories after the preliminary license-ID screen and conservative previous-project exclusion. This provides substantial headroom over the project's target of 60 accepted cases across at least 8 projects, with a target of 80.

**It does not establish 261 acceptable experiment cases.** This workflow did not:
- inspect the source repository's actual license file at the relevant commit;
- run any upstream buggy/fixed tests;
- inspect the gold patch or derive a gold root cause;
- prepare or adjudicate E1/E2/E3 evidence packets;
- inspect exact issue-level overlap, other dataset exposure, or model-training contamination;
- obtain human reviewer consent or complete human ratings;
- load a model, run inference, or fine-tune any weights.

The inventory reads only these eight columns: `instance_id`, `repo`, `base_commit`, `created_at`, `language`, `license`, `FAIL_TO_PASS`, and `problem_statement`. It does not load `patch`, `test_patch`, `pr_description`, `interface`, or `meta` into the Arrow table. Candidate CSV contains identifiers and metadata fields only; problem statement text and test IDs are not exported.

## 6. Decision and next gate

**Decision: proceed to a deterministic metadata-only review cohort, not yet to confirmatory experiments.**

Next bounded phase:
1. Deterministically select 96 candidates from 96 different repositories out of the 261-case conservative pool, leaving additional projects as reserves. This provides 16 candidate cases of headroom above the 80-case target.
2. Freeze the seed, case IDs, source revisions, and selection hash before reviewers or model outputs see them.
3. Review exact source licenses at each base commit; exclude any ambiguous or noncompliant license without relaxing rules.
4. Check issue/PR duplicates and project/author exposure across all prior project work.
5. Only then begin isolated technical verification of buggy/base versus fixed state, recording exact environments and test outcomes.
6. Require independent root-cause and evidence-sufficiency adjudication before any case can increment the accepted count.

The project still has `accepted_confirmatory_cases = 0`. The inference gate and fine-tuning prohibition remain in force.

## 7. Scope

This record describes a metadata feasibility run only. It is not a legal opinion, preregistration, validated dataset, model result, or authorization to run the primary P0/P1 experiment.
