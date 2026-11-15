# pdoc #812 — technical reproduction record

**Record date:** 15 November 2026  
**SWE-rebench V2 cohort row:** 95 (`mitmproxy__pdoc-813`)  
**Technical status:** `BASE_FAIL_FIX_PASS_CONFIRMED`  
**Confirmatory disposition:** `EXCLUDED_BY_PREDECLARED_EXPOSURE_RULE`  
**Model status:** no model load, inference, fine-tuning, or training.

## 1. Frozen dataset and candidate identity

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Immutable Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Frozen 96-row cohort CSV: `SWE_REBENCH_V2_COHORT_96_PRIMARY_2026-11-12.csv`
- Cohort CSV SHA-256: `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`
- Cohort manifest SHA-256: `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`
- Row/instance: `95 / mitmproxy__pdoc-813`

The earlier static scope record is preserved separately: [PDOC_813_PRE_REPRODUCTION_REVIEW_2026-11-15.md](PDOC_813_PRE_REPRODUCTION_REVIEW_2026-11-15.md).

## 2. Upstream source identities

- Repository: [mitmproxy/pdoc](https://github.com/mitmproxy/pdoc)
- Issue: [#812 — pdoc does not work if "." is specified while specifying the directory](https://github.com/mitmproxy/pdoc/issues/812)
- Fix PR: [#813 — Make `pdoc .` work](https://github.com/mitmproxy/pdoc/pull/813)
- Exact base commit: `57ee1d628027feffbd734180287e74294ddab7df`
- Exact fix commit: `75863d3abac0843a4ca0f3d562db2bc21d6ba6dc`
- Upstream merge commit: `7391e8a5fb966d4c2c98fe6030c1d3b552949e54`

The changed production logic resolves a relative `Path` to an absolute path in the branch where the given string is treated as a local file/directory because no importable module of that name is found.

## 3. Exact reproduction harness

Project harness PR: [#195](https://github.com/MahmutVezir/dijitalikiz/pull/195), merged.  
Project workflow run: [43712582477](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43712582477).  
Relevant job: `132807166042` — Upstream pdoc.

The harness pins the exact upstream base and fix commits. It creates one temporary synthetic project root containing:
- `pyproject.toml` with project name `pdoc-issue-812-project`;
- `__init__.py`, importing a helper function;
- `helper.py`, containing one documented function.

The same temporary project root is used for both upstream commits. No upstream source file or fixture was copied into the benchmark repository.

The identical CLI invocation at both commits is:

`python -m pdoc . --output-directory <temp-dir>`

The `--output-directory` option makes successful rendering deterministic by generating HTML instead of starting a long-lived local web server. The issue-relevant module specification remains exactly `.`.

## 4. Frozen environment

- Runner: Ubuntu 24.04
- Python: **3.11.5**, matching an upstream pdoc CI matrix entry
- uv: **0.6.7**, the version pinned in the exact-base `uv.lock`
- Dependency install: `uv sync --python "$(command -v python)" --frozen --all-extras --dev`
- `uv pip check`: passed; the final check reported 32 packages
- Base and fix were checked out sequentially inside the same working tree and virtual environment
- Runtime freeze SHA-256 and the SHA-256 digests of the `uv.lock`, base CLI log, and fix CLI log were written to the GitHub Actions job summary for run 43712582477

The explicit `--python` selection is intentional: an earlier trial initially selected Python 3.13.2 despite the setup-python step selecting 3.11.5. That trial is superseded and is not the result reported here. The passing run verifies the venv interpreter is exactly Python 3.11.5.

## 5. Reproduction result

### Exact base

Commit: `57ee1d628027feffbd734180287e74294ddab7df`

- The actual CLI command exited nonzero.
- The captured error contained the exact issue-specific message: `ValueError: No modules found matching spec: .`.
- The CI step verified that exact message before marking the expected base failure successful.

### Exact fix

Commit: `75863d3abac0843a4ca0f3d562db2bc21d6ba6dc`

- The exact same CLI command ran against the same project root and same virtual environment.
- The command completed successfully.
- The output directory contained at least one generated `.html` file.
- The CI step verified HTML output before marking the fix pass successful.

**Technical conclusion:** pdoc #812 is reproduced at the pinned base and corrected at the pinned fix under the same frozen runtime.

## 6. License and provenance correction

The earlier static note incorrectly treated the root LICENSE as standard MIT and raised a possible discrepancy with the project metadata. This was corrected after reviewing the exact-base license text and its history.

- Exact-base `pyproject.toml`: `license = { text="MIT-0" }`
- Exact-base root LICENSE Git blob SHA-1: `9d75d3de543742e219b1c7301901a95f65ad353a`
- Fix commit root LICENSE Git blob SHA-1: same `9d75d3de543742e219b1c7301901a95f65ad353a`
- Root NOTICE: absent in the exact-base tree.
- Upstream transition: [65b8242f3b75e0c499135e31f20f01caa70f7a04 — Unlicense to MIT-0](https://github.com/mitmproxy/pdoc/commit/65b8242f3b75e0c499135e31f20f01caa70f7a04).

The LICENSE text omits the standard MIT attribution-condition sentence; the exact-base metadata and root license are consistent with MIT-0. The narrow classification concern is closed. This is not legal advice and does not replace per-file/nested-license review if any upstream file is later redistributed.

## 7. Scientific disposition

This candidate has now undergone technical debugging and reproduction. Under the project's predeclared exposure rule, it is **excluded from the confirmatory sample**, even though base-fail/fix-pass succeeded.

- Do not add row 95 to `CASE_REGISTRY.json`.
- Do not count it toward the minimum 60 independent cases / 8 upstream projects.
- Do not use this result as evidence for or against the P0/P1 hypothesis.
- Human Panel A root-cause/provenance adjudication and Panel B E1/E2/E3 evidence-adequacy scoring were not performed.
- No model load, inference, fine-tuning, or training occurred.

## 8. Repository validation and readiness

For the same Research Validation run [43712582477](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43712582477):
- pdoc exact base/fix reproduction job: passed;
- repository/configuration validation: **414 tests + 56 subtests passed**;
- separate historical archive integrity job: failed because the old CCDG ZIP is absent from `data/historical/confirmatory_artifact_2026-10-09.zip`. That historical archive gate is independent of this pdoc test.

No-inference preflight run [43712582464](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43712582464):
- fail-closed tests: **13/13 passed**;
- evidence-packet/citation auditor tests: **12/12 passed**;
- readiness remains `ready=false`, **21 blockers**, 0 accepted cases, 0 accepted upstream projects, `model_inference_performed=false`.

## 9. Next work package

Next candidate for static issue/test-oracle/provenance review: SWE-rebench V2 cohort row 90, `pyfar/pyfar` PR #722. Confirm exact base SHA, issue semantics for energy/power/RMS normalization, the changed test oracle, changed-file list, and nested/per-file provenance before any upstream test/build. Do not weaken the 60-case / 8-project threshold or open the inference gate.
