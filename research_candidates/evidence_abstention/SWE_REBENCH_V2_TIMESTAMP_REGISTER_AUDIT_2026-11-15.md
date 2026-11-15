# Timestamp reconciliation register audit — 15 November 2026

**Status: PARTIAL PASS — not a dataset-validation gate closure.**

## Recomputed register inventory

The 13 committed CSV parts were read and reconciled structurally:

| Check | Result |
|---|---:|
| CSV parts present | 13 |
| Rows | 104 |
| Unique instance IDs | 104 |
| Unique repositories | 104 |
| Primary candidates | 96 |
| Project reserves present | 8 of 17 declared |
| Exact timestamp matches | 103 |
| One-second differences | 1 |
| Other mismatches / API errors recorded | 0 |

The sole one-second difference is `simpeg/simpeg#1633`: dataset value `2025-03-20T23:46:00Z`, recorded GitHub API value `2025-03-20T23:46:01Z`. It remains a manual-review exception and is not automatically admitted.

## Why the gate remains open

1. The stored register is internally consistent but does not preserve raw GitHub API response payloads or a cryptographically verifiable capture of those responses.
2. Only 8 of the 17 declared project-level reserves appear in the committed parts.
3. The one-second discrepancy has not been resolved under a documented predeclared rule.
4. A timestamp match does not validate defect correctness, test reproduction, exact-base licensing, project independence, exposure, or evidence-tier judgments.

## Code added

- `scripts/audit_swe_rebench_timestamp_register.py` — deterministic, no-network audit of the committed CSV parts.
- `tests/test_audit_swe_rebench_timestamp_register.py` — tests for expected counts, duplicates, incorrect deltas, and missing parts.

The audit script's report explicitly states that it does not make API requests or authenticate original API payloads. Its success means only that the stored register is structurally coherent.

## Decision

Keep `dataset_validation_gate = OPEN`. Do not use the 104-row register as an accepted case registry and do not authorize model inference from this audit. The next dataset action is to preserve verifiable API provenance, resolve the one-second record, and account for the nine missing reserve rows (or formally retire the unused reserve rows in a versioned cohort protocol).
