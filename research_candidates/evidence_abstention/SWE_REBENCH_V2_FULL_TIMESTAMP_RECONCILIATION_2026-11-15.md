# Full V2 timestamp register reconciliation — 15 November 2026

**Outcome: 104/104 upstream GitHub records re-fetched successfully. One dataset-vs-GitHub timestamp exception remains open. This does not close the full dataset-validation/provenance gate.**

## Scope

The current V2 timestamp register consists of 13 committed CSV parts, each containing 8 records: **104 records total**, comprising **96 primary candidates and 8 project-reserve records**.

Each record's exact upstream pull-request/issue URL and number was re-fetched through the GitHub connector. The fresh normalized `created_at` value was compared against:

1. the pinned SWE-rebench V2 dataset `created_at` value; and
2. the previously recorded GitHub API `created_at` value in the register.

All 104 rows were queried individually. No fetch errors were returned.

## Aggregate result

| Check | Result |
|---|---:|
| Register rows | 104 |
| Fresh upstream GitHub records fetched | 104/104 |
| Fetch errors | 0 |
| Fresh GitHub timestamp equals previously recorded API timestamp | 104/104 |
| Fresh GitHub timestamp equals dataset timestamp | 103/104 |
| Dataset-vs-GitHub mismatches | 1 |
| Primary records | 96 |
| Project-reserve records | 8 |

## Sole exception

- Record: `simpeg__simpeg-1633`
- Upstream: [simpeg/simpeg#1633](https://github.com/simpeg/simpeg/pull/1633)
- Dataset `created_at`: `2025-03-20T23:46:00Z`
- Previously recorded API `created_at`: `2025-03-20T23:46:01Z`
- Freshly re-fetched GitHub `created_at`: `2025-03-20T23:46:01Z`
- Difference: **+1 second** on the GitHub side relative to the dataset.

The fresh fetch corroborates the stored GitHub-side timestamp. It does not explain the dataset-side one-second difference. Do not infer truncation, rounding, or another normalization rule without authoritative dataset-generation documentation.

## Evidence limitations

- The GitHub connector returned normalized issue/PR fields. It did not preserve the unmodified REST response body, response headers, request IDs, or a cryptographic hash of each raw response.
- This is an independent field-level re-fetch, not a signed/raw HTTP evidence archive.
- The 104 rows were queried by exact URL/number from the committed register. This establishes timestamp consistency for the current register entries, not the validity of the underlying code changes, project independence, license compatibility, test reproducibility, or eligibility as accepted confirmatory cases.
- The 8 reserve rows present in the register remain only 8 of the 17 declared reserve projects; the other 9 declared reserves are still not represented in the 104-row register and must be found or formally retired with reasons.

## Disposition

1. Mark the register-level upstream timestamp re-fetch as **COMPLETE (104/104)**.
2. Keep the `simpeg__simpeg-1633` dataset precision exception **OPEN** until authoritative timestamp-generation semantics or a predeclared handling rule is documented.
3. Keep the overall V2 dataset-validation/provenance gate **OPEN**.
4. Do not accept any candidate solely because its timestamp matches.
5. Accepted confirmatory cases remain **0**; accepted independent projects remain **0**.
6. Model loading, inference, and fine-tuning remain unauthorized.

## Reproducibility note

The 13 source files are:
`timestamp_reconciliation_part_01_2026-11-15.csv` through `timestamp_reconciliation_part_13_2026-11-15.csv`.
The reconciliation was performed against each row's upstream GitHub issue/PR URL and exact issue number on 15 November 2026. The aggregate counts above are the outcome of those individual fetches; no model inference or outcome-label inspection was performed.
