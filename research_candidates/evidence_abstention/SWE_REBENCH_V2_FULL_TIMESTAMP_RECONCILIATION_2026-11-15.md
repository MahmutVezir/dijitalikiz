# Full V2 timestamp register reconciliation — 15 November 2026

**Outcome: 113/113 upstream GitHub records re-fetched successfully. One dataset-vs-GitHub timestamp exception remains open. This does not close the full dataset-validation/provenance gate.**

## Scope

The frozen V2 cohort artifact declares **96 primary candidates and 17 project reserves**. The first committed timestamp register covered all 96 primary candidates and only 8 reserves (104 records). The remaining 9 reserve rows were missing from that register; they have now been retrieved from the original frozen cohort reserve CSV and individually re-fetched from their exact GitHub pull-request URLs.

The expanded timestamp register now contains **113 records in 14 CSV parts**:
- 96 primary candidates;
- 17 project reserves;
- 0 declared reserve rows missing from the timestamp register.

For each record, the fresh normalized GitHub `created_at` value was compared with the pinned dataset timestamp. For the original 104 register entries, it was also compared with the previously recorded GitHub API timestamp.

## Aggregate result

| Check | Result |
|---|---:|
| Full primary + reserve cohort rows | 113 |
| Fresh upstream GitHub records fetched | 113/113 |
| Fetch errors | 0 |
| Original 104 stored API timestamps corroborated by fresh fetch | 104/104 |
| Dataset timestamps matching fresh GitHub timestamps | 112/113 |
| Dataset-vs-GitHub mismatches | 1 |
| Primary records represented | 96/96 |
| Project reserves represented | 17/17 |

## Sole exception

- Record: `simpeg__simpeg-1633`
- Upstream: [simpeg/simpeg#1633](https://github.com/simpeg/simpeg/pull/1633)
- Dataset `created_at`: `2025-03-20T23:46:00Z`
- Previously recorded API `created_at`: `2025-03-20T23:46:01Z`
- Freshly re-fetched GitHub `created_at`: `2025-03-20T23:46:01Z`
- Difference: **+1 second** on the GitHub side relative to the dataset.

The fresh fetch corroborates the stored GitHub-side timestamp. It does not explain the dataset-side one-second difference. Do not infer truncation, rounding, or another normalization rule without authoritative dataset-generation documentation.

## Nine reserve rows newly added

All nine previously missing project-reserve records were individually fetched successfully and matched the pinned dataset timestamp exactly:

| Instance | Upstream PR | Dataset / fresh GitHub timestamp |
|---|---|---|
| `mne-tools__mne-bids-1362` | [mne-tools/mne-bids#1362](https://github.com/mne-tools/mne-bids/pull/1362) | `2025-01-02T18:07:21Z` |
| `biotite-dev__biotite-795` | [biotite-dev/biotite#795](https://github.com/biotite-dev/biotite/pull/795) | `2025-04-28T11:46:23Z` |
| `quantecon__quantecon.py-769` | [QuantEcon/QuantEcon.py#769](https://github.com/QuantEcon/QuantEcon.py/pull/769) | `2025-06-22T13:14:57Z` |
| `pypa__setuptools-4911` | [pypa/setuptools#4911](https://github.com/pypa/setuptools/pull/4911) | `2025-03-24T17:25:40Z` |
| `spikeinterface__spikeinterface-3829` | [SpikeInterface/SpikeInterface#3829](https://github.com/SpikeInterface/SpikeInterface/pull/3829) | `2025-04-02T09:24:15Z` |
| `pyvrp__pyvrp-682` | [PyVRP/PyVRP#682](https://github.com/PyVRP/PyVRP/pull/682) | `2024-11-08T20:19:38Z` |
| `delgan__loguru-1303` | [Delgan/loguru#1303](https://github.com/Delgan/loguru/pull/1303) | `2025-02-18T11:46:51Z` |
| `koaning__scikit-lego-736` | [koaning/scikit-lego#736](https://github.com/koaning/scikit-lego/pull/736) | `2025-03-16T21:14:07Z` |
| `yukinarit__pyserde-618` | [yukinarit/pyserde#618](https://github.com/yukinarit/pyserde/pull/618) | `2024-12-04T01:47:42Z` |

These remain metadata reserve candidates only. No reserve is accepted as a confirmatory case by this timestamp check.

## Evidence limitations

- The GitHub connector returned normalized issue/PR fields. It did not preserve the unmodified REST response body, response headers, request IDs, or a cryptographic hash of each raw response.
- This is an independent field-level re-fetch, not a signed/raw HTTP evidence archive.
- Timestamp agreement does not establish validity of the underlying code changes, project independence, license compatibility, test reproducibility, or eligibility as accepted confirmatory cases.
- The reserve list is now fully represented, but all 17 reserve candidates remain unreviewed for case-level eligibility.

## Disposition

1. Mark the cohort timestamp register coverage as **COMPLETE (113/113: 96 primary + 17 reserves)**.
2. Keep the `simpeg__simpeg-1633` dataset precision exception **OPEN** until authoritative timestamp-generation semantics or a predeclared handling rule is documented.
3. Keep the overall V2 dataset-validation/provenance gate **OPEN**.
4. Do not accept any candidate solely because its timestamp matches.
5. Accepted confirmatory cases remain **0**; accepted independent projects remain **0**.
6. Model loading, inference, and fine-tuning remain unauthorized.

## Register files

The 14 source files are `timestamp_reconciliation_part_01_2026-11-15.csv` through `timestamp_reconciliation_part_14_2026-11-15.csv`. Part 14 contains the nine previously missing reserve records. No model inference or outcome-label inspection was performed.
