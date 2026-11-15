# SWE-rebench V2 `created_at` timestamp-semantics audit

**Date:** 15 November 2026  
**Status:** Unresolved source-schema lineage; fail-closed screening rule adopted  
**Scope:** Metadata timestamp interpretation only. This is not case acceptance, legal clearance, or permission to run upstream tests or a model.

## 1. Question

Can `created_at` in the pinned `PrimeIntellect/SWE-rebench-V2-Filtered-Verified` dataset be safely interpreted as UTC for the cohort cutoff `2024-09-20T00:00:00Z`?

**Finding:** Not for timezone-naive strings. The reviewed public dataset evidence is internally inconsistent about the field's representation, and no authoritative timezone semantics for naive strings were found. Assigning UTC would be an unsupported assumption.

## 2. Evidence reviewed

1. The filtered dataset page and its published feature/schema description declare `created_at` as a string. The pinned Parquet schema type recorded by the earlier metadata-only audit is also `string`. Example values are date-like strings without an explicit UTC offset.
2. The embedded upstream `nebius/SWE-rebench-V2` dataset card describes `created_at` as `int64`, with units of Unix milliseconds.
3. The visible filtered-dataset generation excerpt loads the upstream dataset and applies filtering/mapping, but the reviewed excerpt only demonstrates rewriting `image_name`; it does not demonstrate a `created_at` conversion or timezone normalization.
4. No authoritative data-lineage statement was found that explains the upstream int64-to-filtered string change, or that states naive values are UTC.
5. A string without an offset, such as `2021-06-22 22:21:33`, does not identify its timezone by itself.

### Sources

- Filtered dataset card/schema: https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified
- Filtered dataset README at the pinned file revision: https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified/blob/fb9aa226b2ce37c708ea7732e7b980abacdadb67/README.md
- Upstream dataset card: https://huggingface.co/datasets/nebius/SWE-rebench-V2
- Upstream embedded-card description of `created_at` as Unix milliseconds is in the source material embedded in the filtered dataset README.
- Metadata parser and prior screen: `scripts/audit_swe_rebench_filtered_verified.py` and its earlier output artifact.

## 3. Consequence for the cohort

The former metadata screen attached UTC to naive timestamp strings. Its output was used to build a 96-primary / 17-project-reserve / 148-within-project-alternate screening cohort.

Those counts and their SHA-256 values remain preserved as historical artifacts so the prior work is reproducible. They are **not** evidence that the time cutoff was applied correctly. The old cohort is therefore quarantined from confirmatory sampling pending timestamp reconciliation and a new, versioned selection run. No candidate is being silently reclassified or moved into the accepted case registry.

## 4. Operational rule adopted

The metadata auditor now uses `naive_policy="reject"` by default:

- ISO timestamps with an explicit timezone/offset are normalized to UTC.
- Numeric values are converted as Unix milliseconds only when the exact source type/unit has been verified for the relevant pinned data.
- Naive strings and naive datetime values return no UTC instant and are excluded with `created_at_timezone_unverified`.
- Missing, malformed, and unsupported values remain excluded.
- An explicitly named `assume_utc_historical_only` mode exists only to reproduce the previous feasibility screen. It is not exposed as a normal CLI switch, and its report marks the assumption and explicitly says it is not permitted for confirmatory use.
- The global source-schema lineage review remains unresolved even when individual strings contain offsets. Explicit offsets make those individual timestamp values parseable, but do not resolve the dataset's broader representation lineage.

## 5. Required resolution before cohort rebuild

At minimum, obtain an authoritative timestamp for each selected task from the exact referenced GitHub issue/PR record and compare it with the dataset value. Record the repository, issue/PR number, dataset row identifier, raw dataset value, authoritative API value, exact source revision/record URL, normalized UTC instant, comparison result, retrieval timestamp, and evidence hash.

A dataset value should only be accepted as a usable timestamp when the normalization/precision comparison is documented and passes the predeclared rule. Any missing source record, ambiguous task mapping, timezone mismatch, precision ambiguity affecting the cutoff, or unexplained conflict must be excluded from the date-eligible pool. If field-level API verification is not practical for all retained rows, use only rows with explicit timezone-bearing timestamps and disclose the resulting coverage; do not restore the naive-UTC assumption.

After resolution, rebuild into a **new** versioned cohort snapshot with new output filenames, CSV hashes, manifest hash, selection seed, and preflight record. Do not overwrite the historical 96-row artifacts.

## 6. Scope and safety status

- No source repository tests or builds were executed as part of this timestamp audit.
- No model was loaded; no inference, fine-tuning, or training occurred.
- Accepted confirmatory cases/projects remain 0/0.
- This audit does not resolve underlying source-code licenses, PR/base ancestry, test sensitivity, defect independence, ground truth, evidence-level semantic validity, or human reviewer approvals.
- Model inference remains unauthorized.

**Decision:** Keep the date/timezone gate open. Fail closed for timezone-naive timestamp values. Rebuild the eligible candidate cohort only after authoritative timestamp provenance has been reconciled.


## 7. Full pinned-snapshot check (15 November 2026)

The updated fail-closed auditor was run against the exact pinned Parquet file in GitHub Actions run [43726530902](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43726530902), on repository head `91fb65cbf76eabcb6ecf84ce9e66a843698b45c4`.

Observed report:

- Rows read: **6,272**.
- Arrow/Parquet `created_at` type: **string**.
- Date representations: **6,272 `string_naive_timezone_unverified`**.
- Naive values assigned UTC: **0**.
- Timezone-unverified values: **6,272**.
- Python rows eligible after the UTC cutoff: **0**.
- Metadata candidates after required-field and duplicate checks: **0**.
- Cohort generation: **skipped by timestamp gate**.
- Synthetic parser tests: **14 passed**; deterministic sampler tests: **6 passed**.
- No upstream project tests, model loading, inference, fine-tuning, or training were performed.

The retained workflow artifact is [artifact 14166229237](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43726530902/artifacts/14166229237), SHA-256 `92904f74309eb9c8dc48ad8c327de6d0103304aa7ebe448c6f86f8004f0deb79`.

This empirical result confirms that the timezone-naive representation is present in every row of the pinned filtered snapshot. It does **not** prove that the original source timestamps are in a non-UTC timezone, nor does it establish the transform used to serialize them. The prior 96-row cohort remains quarantined. The next admissible step is an authoritative row-to-GitHub-record reconciliation, not restoring the naive-UTC assumption.


## 8. Independent GitHub REST API spot-check

To test whether the naive strings are derived from GitHub issue creation timestamps, a deterministic random sample of 51 unique candidate issue identifiers was queried using the GitHub issue API through the connected GitHub integration. GitHub's REST documentation states that timestamps returned by the API are UTC ISO 8601 values (`YYYY-MM-DDTHH:MM:SSZ`): https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api.

Results:

- **50/51** dataset time values matched the corresponding API `created_at` value exactly to the second.
- **1/51** differed by one second: `simpeg/simpeg#1633`, dataset-derived historical value `2025-03-20T23:46:00Z`, API value `2025-03-20T23:46:01Z`.
- All 51 returned issue objects, not pull-request objects.
- The queries were sampled from the historical 347-row candidate inventory using fixed deterministic shuffles (seeds `42` and `20261115`); the two samples overlapped on one identifier, leaving 51 unique issue identifiers.

This is strong evidence that the filtered `created_at` strings are likely GitHub issue `created_at` values with the timezone designator omitted during serialization. It does **not** prove this for every row, nor explain the one-second discrepancy or the stale/inconsistent upstream-card type declaration.

### Decision after spot-check

Do not revert the fail-closed parser and do not directly assume UTC for raw strings. Instead, use the authoritative GitHub issue API `created_at` timestamp for the date cutoff after exact repository/issue mapping. A full reconciliation of all historical candidate rows (and every row intended for the new cohort) is still required. Rows with missing issues, wrong mapping, API errors, or material timestamp mismatches remain excluded pending review. The one-second discrepancy is retained as a finding; any tolerance rule must be defined before the full reconciliation and may not silently overwrite the API value.
