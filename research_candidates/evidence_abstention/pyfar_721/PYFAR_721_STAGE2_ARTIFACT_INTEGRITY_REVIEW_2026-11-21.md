# PyFar #721 — Stage 2 artifact integrity review

Date: 2026-11-21

## Frozen technical result

- Workflow run: `44331092872`
- Job: `134895967816`
- Artifact: `14440390942`
- GitHub-reported ZIP SHA-256: `17e80ba9a81153ea833ce0cee05271f1815c6c6d597653c12f9bbe11f0f95bf8`
- Independently downloaded ZIP SHA-256: exact match
- ZIP CRC: PASS
- Internal SHA256SUMS: **14/14 files matched**
- Dataset row: `pyfar__pyfar-722`
- Canonical row SHA-256: `82444bd1dcaa0c52bcac4a5c0b76efc20ed0ad26606de1edc338265843aca6bd`
- Runtime: CPython 3.12.4
- Pinned runtime distributions: 32
- Frozen FAIL_TO_PASS selectors: 23

## Exact fail-to-pass result

The workflow executed each of the 23 row selectors on the exact buggy base with the test-only regression-test diff applied. All 23 executed and failed on the expected energy/power target assertion (**23/23**). The same 23 selectors were then executed on the exact fixed revision and all passed (**23/23**).

A collection or dependency error is not being counted as a defect failure. The first historical attempt did fail during collection because `netCDF4` was missing; it is excluded from the Stage 2 result. The corrected lock includes `netCDF4==1.7.2`, `cftime==1.6.4.post1`, and `certifi==2024.8.30`.

## Selector and independence limitation

The 23 selectors are one frozen regression selector set from the single PyFar dataset row. They are not 23 independent cases. The selectors are all drawn from the upstream PR's added `test_normalization_energy_power_rms` parameterization and in this dataset row cover energy/power values, target values, and channel-handling modes. They do not constitute a separately authored public-API reproducer. No such standalone issue-level reproducer is claimed to have been run.

## Retained integrity files

The artifact contains `dependency-license-inventory.json`, `test-environment-freeze.txt`, row snapshot, selector list, exact PR patch, test-only patch, base/fixed test logs and JSON result records, and a SHA256SUMS manifest.

The dependency metadata screen has 32 runtime entries. Four distributions lack a raw `License` field and rely on classifiers; two entries contain multiple license classifiers. NumPy and SciPy metadata disclose bundled OpenBLAS/LAPACK and GCC runtime/libquadmath components. Canonical license texts, applicable notices, native/bundled binary details, and full dataset-card provenance remain separate human-review gates.

**Disposition:** Stage 2 technical reproduction and archive-integrity checks PASS. This does not approve the gold/tier proposal, close license/provenance review, accept the case, or authorize model execution.
