# pyfar #721 / PR #722 — pre-reproduction static candidate review

**Review date:** 15 November 2026  
**SWE-rebench V2 cohort row:** 90 (`pyfar__pyfar-722`)  
**Status:** `STRONG_STATIC_DEFECT_CANDIDATE` / `TECHNICAL_REPRODUCTION_NOT_RUN` / `HUMAN_ADJUDICATION_PENDING`  
**Scope:** Issue, PR, patch, exact-base/fix source, test oracle, root license and changed-file scope were reviewed statically. No upstream test/build, package installation, or model inference was performed.

## 1. Frozen candidate identity

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Immutable Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Frozen cohort CSV: `SWE_REBENCH_V2_COHORT_96_PRIMARY_2026-11-12.csv`
- Cohort CSV SHA-256: `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`
- Cohort manifest SHA-256: `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`
- Row / instance: **90 / `pyfar__pyfar-722`**

The cohort's 89–96 scope audit classified row 90 as a strong defect candidate, not an accepted experiment case.

## 2. Issue and upstream change

- Repository: [pyfar/pyfar](https://github.com/pyfar/pyfar)
- Issue: [#721 — dsp.normalize's reference_methods "power" and "energy" behave unexpectedly](https://github.com/pyfar/pyfar/issues/721)
- Fix PR: [#722 — Normaliztation: Force energetic properties to match the target after normalization](https://github.com/pyfar/pyfar/pull/722)
- Exact base: `648dda4c60c5a6f74acf335f7808c590c9d23929`
- PR head / fix: `a4d72d380bb8ddb0950d334eb1b0793ee6d86e0e`
- Upstream merge commit: `ecd0589a3fef83ec17e8d72a4bd5a3c64ef7c445`
- PR explicitly closes issue #721.

### Reported failure

The issue reports that `normalize(..., reference_method="energy", target=1)` does not normalize signals to total energy 1. A signal with input energy 20 was reported to leave with energy 0.05; input energy 5 left energy 0.2. A separate example reports 2000-sample and 4000-sample signals with energies 20 and 40, which normalize to 0.05 and 0.025. The issue author expects both outputs to have the specified target energy.

The issue is labelled `bug`, `hot`, `dsp`, and `discuss`; it is closed and linked to the merged PR. These issue examples are upstream reports, not independently reproduced results in this project.

## 3. Exact source and test identities

PR #722 changes exactly two paths:

| Path | Exact-base Git blob SHA-1 | Fix Git blob SHA-1 |
|---|---|---|
| `pyfar/dsp/dsp.py` | `b44dbac7817be97126bd3bbac88add4b6a1ebd54` | `c032e89e156921d990b4d6b5977fe39229fb66ff` |
| `tests/test_dsp_normalize.py` | `224e8c501db5b763374ae74f9d9d40fc0205e0a4` | `69fde6699c70a8ce42cf18e2b4c04a81a1a8f643` |

No source tree was checked out and no tests were run as part of this static review.

## 4. Root-cause hypothesis and mathematical consistency

The exact-base implementation obtains an energetic reference (energy or power), applies the configured channel reduction, then normalizes using:

`y = x \times T / R`

For a quadratic metric such as energy or power, scaling the signal by (k) scales the metric by (k^2). If the raw metric is (E), the old scale factor (k=T/E) yields:

`E(y) = E × (T/E)² = T²/E`

That is the inverse relationship reported in issue #721 when (T=1).

The fix first applies channel handling to the raw reference, then takes square roots of both reference and target:

`R_eff = sqrt(R); T_eff = sqrt(T)`

The resulting scale factor is:

`k = sqrt(T/R)`

Therefore:

`E(y) = E × (sqrt(T/E))² = T`

This is mathematically consistent with the issue's desired energy/power invariant. The order of channel handling matters: for `channel_handling="mean"`, the implementation first calculates the mean of channel energy/power values and then square-roots the aggregate. The new docstring explicitly says the square root is applied after channel handling.

The same square-root transformation is applied to `target`, not only to `reference_norm`. This is important because the PR author noted in a follow-up that the first draft of the fix was correct only when `target=1`; the final PR corrected this and expanded tests for multiple target values.

## 5. Test-oracle review

### Existing test before the PR

The old `test_normalization` parameterization covered `max`, `mean`, `rms`, `power`, and `energy` with `channel_handling` values `max`, `individual`, `min`, and `mean`, using a three-sample impulse with two channel amplitudes. For energy and power, it asserted expected amplitude values derived from the formula.

### New test introduced by the PR

The PR splits the ordinary amplitude tests from a new invariant test, `test_normalization_energy_power_rms`. The new parameter grid is:

- Reference method: `energy`, `power`, `rms` (3)
- Target: `0.5`, `1`, `2` (3)
- Channel handling: `max`, `individual`, `min`, `mean` (4)

That creates **36 parametrized combinations**. Each case normalizes the impulse, measures the resulting signal again using the corresponding public `pf.dsp.energy`, `pf.dsp.power`, or `pf.dsp.rms` function, applies the channel reducer, and asserts that the measured value equals the target.

This is a strong oracle for the public contract: it tests the resulting energetic property, rather than only an intermediate amplitude. It covers target values other than 1 and includes RMS as a control. The ordinary max/mean amplitude tests remain separate.

### Maintainer review of mean-channel semantics

A PR reviewer asked whether `channel_handling="mean"` means the mean energy is computed before square-rooting, rather than taking the mean of square-rooted channel energies. The PR author answered that the implementation was correct and updated the documentation to make the order explicit. The exact source code does the aggregation first and the square root second.

### Remaining test-coverage questions

These are not proof of a defect in the patch, but should be tracked before any candidate acceptance:

1. The new fixture is a short impulse with two channel amplitudes; it does not reproduce the issue's exact two-signals-of-different-lengths example. A later technical reproducer should include that original behavior as a separate regression assertion if the candidate is ever opened.
2. New target coverage is scalar `0.5`, `1`, `2`; the broader API supports array-like targets. Array-valued energetic targets are not explicitly covered by this new parametrization.
3. `return_reference=True` for energy/power is not explicitly asserted in the added test. The implementation now returns the square-rooted effective reference, which matches the updated docstring's description of the reference used for normalization; that public return behavior should be documented and tested if this API is part of the study packet.

The PR's new tests do address the reported normalization invariant and are materially stronger than simply asserting that the new code path executes.

## 6. License and changed-file provenance

- Exact-base root `LICENSE` Git blob SHA-1: `430184952c6fcb292ee01cb114bb9c39f32f78ff`.
- Root LICENSE is an MIT license naming The pyfar developers.
- Exact-base `setup.py` declares `license="MIT license"` and classifies the project as MIT.
- Exact-base `NOTICE` path was not present (contents API returned not found).
- PR #722 changes only `pyfar/dsp/dsp.py` and `tests/test_dsp_normalize.py`; neither is a license file or third-party fixture.
- No source snippet or test fixture from upstream is copied into this review report.

This closes the narrow root-license/path-scope screen only. It is not legal advice or full rights clearance. If a case packet later includes copied upstream source or test text, file-level attribution and redistribution basis must be reviewed and recorded.

## 7. Static disposition

**Decision: strong static defect candidate; no technical reproduction performed.**

Why it remains strong:
- Issue gives a concrete numerical counterexample and desired invariant.
- The exact PR base matches the frozen cohort base SHA.
- The production patch is narrow and mathematically consistent with energy/power being quadratic under signal scaling.
- New tests measure the resulting public energy/power values across three targets and four channel-handling modes.
- PR received maintainer review/approval and was merged upstream.
- Root license is identifiable as MIT, and the PR changes only the implementation module and its test file.

Open before case acceptance:
- Exact-base/fix technical test pair has not been executed.
- The issue's exact different-length example is not yet covered by the upstream new test; a reproduction plan should preserve it.
- Human Panel A root-cause/test/provenance adjudication has not occurred.
- Human Panel B E1/E2/E3 evidence-sufficiency assessment has not occurred.
- Dataset exposure / pretraining contamination checks for the exact cohort row still apply.
- No case was added to `CASE_REGISTRY.json`.

**Accepted confirmatory cases remain 0.** This static inspection is not a model result, not a case acceptance, and not evidence for or against P0/P1. No model loading, inference, training, or upstream test/build was performed.

## 8. Recommended next action (without opening the candidate)

Keep row 90 in the unexecuted, strong-candidate queue while reviewing additional untouched candidates. Before deciding whether this row enters a blinded confirmatory cohort, obtain independent Panel A and Panel B review plans and complete the exact-row exposure checks. Do not run an upstream test or build solely to raise a candidate count: any technical debugging/reproduction of this row would invoke the predeclared exposure exclusion rule for confirmatory use.
