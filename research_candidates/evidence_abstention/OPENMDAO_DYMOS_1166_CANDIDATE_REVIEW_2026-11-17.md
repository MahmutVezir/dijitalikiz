# OpenMDAO/dymos #1166 — Stage 2 candidate review

**Disposition:** Stage 2 technical reproduction passed. Stage 3 scientific adjudication has not started. The case is not accepted into the final registry.

## 1. Provenance and identity

- Repository: https://github.com/OpenMDAO/dymos
- Bug report: https://github.com/OpenMDAO/dymos/issues/1166
- Fix PR: https://github.com/OpenMDAO/dymos/pull/1165
- Issue created: 2025-04-04T20:26:09Z
- PR created: 2025-04-04T20:23:44Z
- PR merged: 2025-04-05T11:30:09Z
- Dataset instance: `openmdao__dymos-1165`
- Buggy base: `3efd1035c3bf62890034eb9e07de543f3d117867`
- Fixed revision: `0ffc82225d6125dcb5c5b5acfb9be9fd712ef949`
- Exact base root license: Apache-2.0; LICENSE blob SHA-1 `55da29e11b1fb2465936598779085f1cbcdf2908`
- Exact base pyproject blob SHA-1 `739e56592adfa10e0583b5f71fa4d36837e5a88c`

The candidate is one upstream project and one frozen dataset row. No alternate Dymos issue or PR is substituted.

## 2. Issue and patch scope

The issue reports that values supplied through `add_control(..., val=...)` or `set_control_options(..., val=...)` do not reach the initial control values. PR #1165 updates the control interpolation setup to form component input defaults from `options['val']` using `reshape_val`; it also changes how the helper normalizes scalar and array values.

The full PR changes six files:
- `dymos/examples/balanced_field/test/test_balanced_field_length.py`
- `dymos/transcriptions/common/control_comp.py`
- `dymos/transcriptions/common/test/test_control_interp_comp.py`
- `dymos/transcriptions/explicit_shooting/explicit_shooting.py`
- `dymos/transcriptions/explicit_shooting/ode_evaluation_group.py`
- `dymos/utils/misc.py`

The buggy-base test patch was generated from only the two test paths. The workflow verified that the exact test-only patch contains no production-code changes and that the full PR's changed-file set matches the six files above.

## 3. Frozen dataset row

- Exact `instance_id`: `openmdao__dymos-1165`
- Repository field: `OpenMDAO/dymos`
- Exact base commit: `3efd1035c3bf62890034eb9e07de543f3d117867`
- `created_at`: `2025-04-04 20:23:44`, matching PR #1165 creation time
- Language: `python`
- Dataset license field: `Apache-2.0`
- Canonical Parquet row SHA-256: `236f9cd1bb8cbacad27fd771e3878802e7dbf6f36a64eff35a60be7a32f6efb5`
- FAIL_TO_PASS count: 1
- Exact selector:

```
dymos/examples/balanced_field/test/test_balanced_field_length.py::TestBalancedFieldLengthDefaultValues::test_default_vals_stick
```

The sole selector is directly aligned to the reported default-value defect. The selector-scope inventory records `direct_default_value_regression=true`.

## 4. Reproduction environment

- Python: 3.11.9
- OpenMDAO: 3.38.0
- NumPy: 1.26.4
- SciPy: 1.13.1
- NetworkX: 3.3
- pytest: 8.3.3
- Remaining direct/transitive pins: see `reproduction/dymos_issue_1166/requirements.lock` and the uploaded dependency-license inventory.
- Parquet extraction dependency: PyArrow 19.0.1, separately pinned and licensed in the artifact.
- No pyoptsparse/IPOPT optimizer was installed. The focused PR test change removes the optimizer-only skip decorator from this `run_model()` regression test; the test does not run an optimization driver.

OpenMDAO 3.38.0 was released on 2025-03-14, before the issue/PR date, and the exact Dymos base declares `openmdao>=3.36.0`. This is a period-compatible pinned environment, not an inference about the upstream CI's original environment.

## 5. Stage 2 result

Workflow run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/44114656908

- Job ID: `134149456631`
- Artifact ID: `14341424466`
- Artifact name: `dymos-issue-1166-reproduction`
- Artifact ZIP SHA-256: `8fc5e1de9ee8c7d4be45c29b48ba9b1a0e6c82194ecb9ce2b7f5757d4fd58051`
- Artifact SHA256SUMS entries: 18; mismatches on independent local verification: 0
- ZIP integrity check: pass

**Buggy base:** The exact selector executed and failed with the expected assertion. The actual value for `traj.rotate.controls:alpha` was `[[1.0], [1.0]]`; the expected value was `[[0], [10]]`. The runner recorded `selector_contracts=1/1 expectation=base-fail`.

**Fixed revision:** The same exact selector passed (`1 passed`). The runner recorded `selector_contracts=1/1 expectation=fixed-pass`.

No selector was dropped, rewritten, or substituted. The full dataset row, test-only patch, full PR patch, source provenance, version inventory, license inventory, raw logs, JSON results, and SHA-256 manifest are retained in the artifact.

Key artifact file hashes:
- base selector JSON: `25f09d80caf9d129a1e758e2542489249236b7a06039e537f42dcd682e8909c7`
- fixed selector JSON: `6d9c9b93eee2866732a3026b9b61813f6e162f5414342df6291da3d08108e58c`
- base selector log: `35b7f3e853e8cfd27bae8a1e0ae6a6f27ced0e765d0a3a26eee18d6020987380`
- fixed selector log: `2f5d59e20e3e1fc67b321b18d3387582c682d2fcdeb902b0216f129856b8fe47`
- test-only patch: `1e5b106e92a3167aea9ea3a46d34d36a95f9009deeaa1defaa102f9c4f7bd774`
- full PR patch: `651c7d79f67ea27405a29859c2367ca3392a833bdf5adca0876acd373ef833d4`

## 6. Preliminary technical interpretation — not a human gold adjudication

The observed base failure is consistent with the issue's claim: the `val=[0, 10]` provided to the polynomial control is not reflected in the initialized control-input values, which remain ones. The fixed source passes the same assertion.

Potential alternatives to consider in Stage 3:
1. A control-option value was normalized or broadcast incorrectly by the helper rather than omitted when creating component input defaults.
2. The original test fixture or prior `set_val` calls masked the defect; the rewritten fresh-model regression removes that confound, but it still needs explicit adjudication.
3. A mismatch between polynomial control node count/shape and the supplied value could produce a similar symptom; inspect the `reshape_val` path and the other control tests before finalizing the mechanism.

These are candidate explanations only. No gold root cause, alternative ranking, E1/E2/E3 membership, or final acceptance decision is asserted here.

## 7. Remaining gates

1. Human review of the complete pinned dependency license inventory. The installed NumPy and SciPy wheels include bundled numerical libraries with additional notices; the inventory records them, but this is not legal clearance.
2. Independence and related-issue review, ensuring one Dymos case only.
3. Human adjudication of the gold mechanism and alternative explanations.
4. Prepare nested E1/E2/E3 packets with manifests and verified source/log hashes; obtain project-lead approval.
5. Construct the complete schema-conformant final case record and pass the fail-closed registry validation.
6. Make a separate final case-acceptance decision.

**Current disposition:** Stage 2 technical pass; Stage 3 not started; `case_acceptance=not_accepted`; no model loaded, inference run, or training performed.
