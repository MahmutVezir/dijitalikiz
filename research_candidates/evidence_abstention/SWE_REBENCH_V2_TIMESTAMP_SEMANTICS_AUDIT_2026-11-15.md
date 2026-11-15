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
