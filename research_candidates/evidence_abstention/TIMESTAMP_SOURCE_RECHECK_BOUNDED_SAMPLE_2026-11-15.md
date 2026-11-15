# Timestamp source recheck — bounded sample, 15 November 2026

**Status: PARTIAL RECHECK ONLY. This does not close the timestamp provenance gate.**

## Scope and method

The committed reconciliation CSV parts 01 and 02 were read. Ten rows (the first eight primary rows in part 01 and first two primary rows in part 02) were independently re-fetched from their exact GitHub pull-request URLs using the GitHub issue/PR fetch endpoint. The returned normalized `created_at` values were compared with both the pinned dataset value and the previously stored API value.

This is a bounded 10-row recheck, not a random sample and not a complete 104-row reconciliation. The connector exposed normalized issue fields; this did not preserve unmodified REST response bodies or headers and therefore is not raw-payload cryptographic provenance.

## Results

- Rows re-fetched: **10**
- Fetch errors: **0**
- Fresh GitHub `created_at` exactly matched the pinned dataset timestamp: **10/10**
- Fresh GitHub `created_at` matched the previously recorded API timestamp: **10/10**
- Any mismatch in this bounded sample: **0**

| Instance | GitHub `created_at` |
|---|---|
| `aristanetworks__anta-956` | `2024-12-09T10:45:26Z` |
| `reagento__dishka-436` | `2025-04-15T22:52:26Z` |
| `theupdateframework__python-tuf-2808` | `2025-03-07T12:48:47Z` |
| `ecmwf__earthkit-data-592` | `2025-01-22T14:40:06Z` |
| `googleapis__python-bigquery-2140` | `2025-03-06T23:18:44Z` |
| `wntrblm__nox-922` | `2025-01-31T20:53:30Z` |
| `googlecloudplatform__cloud-sql-python-connector-1221` | `2025-01-10T17:44:12Z` |
| `databricks__dbt-databricks-995` | `2025-04-15T21:29:47Z` |
| `getmoto__moto-8296` | `2024-11-07T20:51:42Z` |
| `dwavesystems__dwave-system-554` | `2025-01-29T20:18:13Z` |

## Separate exception recheck

A separate fresh fetch of [simpeg/simpeg#1633](https://github.com/simpeg/simpeg/pull/1633) returned `created_at=2025-03-20T23:46:01Z`, corroborating the previously recorded GitHub-side timestamp. The pinned dataset stores `2025-03-20T23:46:00Z`; the one-second difference remains unresolved. See `SIMPEG_1633_TIMESTAMP_EXCEPTION_RECHECK_2026-11-15.md`.

## Disposition

- The 10-row bounded sample supports the correctness of those ten stored timestamp pairs only.
- It does not validate the other 93 register rows, prove timestamp semantics for the dataset, or authenticate original API payloads.
- The nine missing declared reserve rows remain unaccounted for.
- Keep `dataset_validation_gate = OPEN`; accepted cases remain 0; inference remains unauthorized.
