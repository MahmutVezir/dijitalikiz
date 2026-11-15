# SWE-rebench V2 — created_at UTC interpretation cross-check

**Audit date:** 15 November 2026  
**Purpose:** Evaluate the timezone assumption used by the metadata-only cohort selection.  
**Scope:** Frozen cohort CSV values compared with upstream GitHub Pull Request API `created_at` values. No source checkout, target-test execution, model loading, inference, fine-tuning, or training was performed.

## 1. Frozen inputs

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Primary cohort artifact: GitHub Actions run [43257277504](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43257277504), artifact ID `13960884569`
- Frozen primary CSV: `SWE_REBENCH_V2_COHORT_96_PRIMARY_2026-11-12.csv`
- Primary CSV SHA-256: `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`
- Cohort manifest SHA-256: `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`

The archived cohort ZIP was retrieved from the recorded GitHub Actions artifact. Its SHA-256 was previously verified as `d9d1fc04cb84233c021006f13205623ea9aa390caa6eb54ca4bc9d974e9a4c6c`; the embedded CSV and manifest hashes matched the frozen values above.

## 2. Why the timezone required review

The metadata audit reads `created_at` from the pinned filtered Parquet as a string. The stored values have no explicit UTC offset. The historical metadata script interprets these naive strings as UTC and emits a `Z`-suffixed value.

There is a schema/documentation discrepancy in the dataset materials inspected on 15 November:

- The current filtered-dataset README feature declaration lists `created_at` as `string`.
- The embedded snapshot of the original Nebius dataset card describes `created_at` as `int64`, specifically Unix milliseconds.
- The filtered-dataset README's displayed generation code loads the original dataset and maps `image_name`; it shows no explicit `created_at` timezone conversion.

Relevant sources:
- [Filtered dataset README at Hugging Face](https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified/blob/main/README.md)
- [Original Nebius dataset card](https://huggingface.co/datasets/nebius/SWE-rebench-V2)
- [Pinned filtered Parquet revision](https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified/tree/fb9aa226b2ce37c708ea7732e7b980abacdadb67)

The README pages inspected here are current `main` snapshots, not proof of the exact card/script contents at the pinned Parquet commit. Therefore documentation alone does not establish the historical conversion path.

## 3. Direct GitHub API spot-check

A post hoc verification sample was drawn from multiple parts of the frozen 96-row cohort, including two records on the cutoff date (20 September 2024) and records extending through July 2025. For each row, the `created_at_utc` text in the frozen cohort CSV was compared byte-for-byte with the upstream PR `created_at` field returned by the GitHub Pull Request API.

| Cohort record | Upstream PR | Cohort `created_at_utc` | GitHub PR `created_at` | Result |
|---|---|---|---|---|
| `aristanetworks__anta-956` | [aristanetworks/anta #956](https://github.com/aristanetworks/anta/pull/956) | `2024-12-09T10:45:26Z` | `2024-12-09T10:45:26Z` | Exact match |
| `reagento__dishka-436` | [reagento/dishka #436](https://github.com/reagento/dishka/pull/436) | `2025-04-15T22:52:26Z` | `2025-04-15T22:52:26Z` | Exact match |
| `ecmwf__earthkit-data-592` | [ecmwf/earthkit-data #592](https://github.com/ecmwf/earthkit-data/pull/592) | `2025-01-22T14:40:06Z` | `2025-01-22T14:40:06Z` | Exact match |
| `wntrblm__nox-922` | [wntrblm/nox #922](https://github.com/wntrblm/nox/pull/922) | `2025-01-31T20:53:30Z` | `2025-01-31T20:53:30Z` | Exact match |
| `amaranth-lang__amaranth-1519` | [amaranth-lang/amaranth #1519](https://github.com/amaranth-lang/amaranth/pull/1519) | `2024-09-20T14:00:49Z` | `2024-09-20T14:00:49Z` | Exact match |
| `drivendataorg__cloudpathlib-474` | [drivendataorg/cloudpathlib #474](https://github.com/drivendataorg/cloudpathlib/pull/474) | `2024-09-20T16:21:56Z` | `2024-09-20T16:21:56Z` | Exact match |
| `pybamm-team__pybamm-4465` | [pybamm-team/PyBaMM #4465](https://github.com/pybamm-team/PyBaMM/pull/4465) | `2024-09-25T06:55:53Z` | `2024-09-25T06:55:53Z` | Exact match |
| `pyccel__pyccel-2038` | [pyccel/pyccel #2038](https://github.com/pyccel/pyccel/pull/2038) | `2024-11-05T09:48:01Z` | `2024-11-05T09:48:01Z` | Exact match |
| `cuthbertlab__music21-1736` | [cuthbertLab/music21 #1736](https://github.com/cuthbertLab/music21/pull/1736) | `2024-10-28T03:20:50Z` | `2024-10-28T03:20:50Z` | Exact match |
| `astropy__ccdproc-901` | [astropy/ccdproc #901](https://github.com/astropy/ccdproc/pull/901) | `2025-07-13T21:05:06Z` | `2025-07-13T21:05:06Z` | Exact match |
| `matthewwithanm__python-markdownify-202` | [matthewwithanm/python-markdownify #202](https://github.com/matthewwithanm/python-markdownify/pull/202) | `2025-03-02T14:41:03Z` | `2025-03-02T14:41:03Z` | Exact match |
| `pyro-ppl__numpyro-1918` | [pyro-ppl/numpyro #1918](https://github.com/pyro-ppl/numpyro/pull/1918) | `2024-11-28T00:54:29Z` | `2024-11-28T00:54:29Z` | Exact match |
| `napalm-automation__napalm-2152` | [napalm-automation/napalm #2152](https://github.com/napalm-automation/napalm/pull/2152) | `2024-11-04T21:41:29Z` | `2024-11-04T21:41:29Z` | Exact match |
| `python-control__python-control-1145` | [python-control/python-control #1145](https://github.com/python-control/python-control/pull/1145) | `2025-04-17T03:16:40Z` | `2025-04-17T03:16:40Z` | Exact match |
| `asdf-format__asdf-1907` | [asdf-format/asdf #1907](https://github.com/asdf-format/asdf/pull/1907) | `2025-03-12T17:51:23Z` | `2025-03-12T17:51:23Z` | Exact match |
| `pypa__virtualenv-2907` | [pypa/virtualenv #2907](https://github.com/pypa/virtualenv/pull/2907) | `2025-07-16T17:58:06Z` | `2025-07-16T17:58:06Z` | Exact match |
| `packit__packit-2556` | [packit/packit #2556](https://github.com/packit/packit/pull/2556) | `2025-03-16T23:52:42Z` | `2025-03-16T23:52:42Z` | Exact match |

**Result: 17/17 successfully retrieved PR timestamps matched exactly.** This supports the UTC interpretation for the sampled records, including both sampled records on the cutoff date. It is a targeted spot-check, not a full audit of all 96 rows.

One additional attempted comparison, [OceanParcels/Parcels #1723](https://github.com/OceanParcels/Parcels/pull/1723), could not be completed because the GitHub API endpoint returned HTTP 301 and the available reader did not follow the repository redirect. It is **unverified**, not a mismatch and not part of the 17/17 denominator.

## 4. Decision

- Retain the frozen cohort and its current cutoff provisionally; do not silently rewrite dates or regenerate the cohort based on an unverified assumption.
- Record the UTC assumption as **sample-validated, full-cohort confirmation pending**.
- Before preregistration, compare all 96 frozen cohort timestamps with the corresponding upstream PR `created_at` values (resolving redirects), or perform an equivalent full-row check against the original source timestamps at a pinned source revision.
- If any mismatch is found, quantify its effect on cutoff eligibility and regenerate the cohort only under a newly versioned seed/artifact; do not overwrite the existing frozen snapshot.
- This audit does not establish that any candidate is a defect, has a reproducible fail-to-pass pair, is legally cleared, is independent, or is an accepted confirmatory case.

**No model loading, inference, fine-tuning, training, upstream target-test execution, or human case adjudication was performed. The V2 registry remains empty and the model-execution gate remains closed.**
