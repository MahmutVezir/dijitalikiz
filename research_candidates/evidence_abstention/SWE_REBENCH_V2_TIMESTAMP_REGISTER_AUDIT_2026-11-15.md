# Timestamp reconciliation register audit — 15 November 2026

**Status: FULL REGISTER STRUCTURAL PASS WITH ONE OPEN TIMESTAMP EXCEPTION — not a dataset-validation gate closure.**

## Recomputed register inventory

The 14 committed CSV parts were read and reconciled structurally:

| Check | Result |
|---|---:|
| CSV parts present | 14 |
| Rows | 113 |
| Unique instance IDs | 113 |
| Unique repositories | 113 |
| Primary candidates | 96 |
| Project reserves present | 17 of 17 declared |
| Exact timestamp matches | 112 |
| One-second differences | 1 |
| Other mismatches / API errors recorded | 0 |

The sole one-second difference is `simpeg/simpeg#1633`: dataset value `2025-03-20T23:46:00Z`, fresh GitHub value `2025-03-20T23:46:01Z`. It remains a manual-review exception and is not automatically admitted.

## Independent source re-fetch

On 15 November 2026, all 113 upstream GitHub records represented by the expanded register were individually fetched through the GitHub connector. All fetches succeeded. The fresh GitHub `created_at` field matched the dataset timestamp for 112/113 records. For the original 104 register rows, the fresh GitHub value also matched the previously stored API value in 104/104 cases. The nine previously omitted reserve records were newly fetched and all nine matched the pinned dataset timestamp exactly.

The connector returned normalized issue/PR fields, not unmodified REST response bodies or headers. This is field-level source re-fetch, not raw-payload cryptographic authentication.

## Why the overall gate remains open

1. The one-second dataset/GitHub discrepancy remains unexplained; do not infer truncation or rounding without authoritative dataset-generation documentation.
2. Timestamp agreement does not validate defect correctness, test reproduction, exact-base licensing, project independence, exposure status, or evidence-tier judgments.
3. All 17 reserve rows are now represented in the timestamp register, but all remain metadata candidates until separately reviewed for case eligibility.
4. The GitHub connector did not preserve raw REST response bodies, response headers, request IDs, or cryptographic hashes of individual responses.

## Code updated

- `scripts/audit_swe_rebench_timestamp_register.py` — deterministic, no-network structural audit of all 14 CSV parts.
- `tests/test_audit_swe_rebench_timestamp_register.py` — expected counts updated to 113 rows (96 primary + 17 reserves), with duplicate, delta, and missing-part checks.

The script's success means only that the stored register is structurally coherent. It does not make GitHub API requests.

## Decision

Keep `dataset_validation_gate = OPEN`. The timestamp register is complete for the 96 primary and 17 reserve candidates, but the one-second discrepancy and broader source-provenance, code-license, reproducibility, and case-eligibility gates remain open. Accepted confirmatory cases remain 0; model inference remains unauthorized.
