# cta-observatory/ctapipe issue #2730 — updated candidate review

**Cohort rank:** 31 of 96 primary candidates  
**Dataset instance:** cta-observatory__ctapipe-2732 (row and selectors not yet authenticated)  
**Issue:** https://github.com/cta-observatory/ctapipe/issues/2730  
**Fix PR:** https://github.com/cta-observatory/ctapipe/pull/2732  
**Review status:** source-level root-cause mechanism corroborated by the reporter's traceback and exact-base writer code. Candidate remains on hold pending dataset-row authentication, the issue-config discrepancy, and pinned base/fixed reproduction. Not an accepted case.

## 1. Defect contract and source-level mechanism

The relevant field contract is defined by the exact buggy-base source:

- `MuonParametersContainer.skewness = Field(nan, ...)`
- `MuonParametersContainer.excess_kurtosis = Field(nan, ...)`

Neither field declares a unit. The `Field` implementation documents `unit=None` as no unit conversion; its validation only requires a Quantity when `self.unit is not None`. Thus the container schema expects ordinary unitless numeric values for these two fields. The function docstring in `radial_light_distribution` still describes both as `astropy.units.Quantity`; that docstring is stale relative to the container schema and is not sufficient evidence that Quantity is the intended serialized contract.

The exact-base HDF5 write path explains the exception:

1. `HDF5TableWriter._add_column_to_schema` detects a Quantity value and installs a `QuantityColumnTransform` for that column.
2. `QuantityColumnTransform.__call__` returns `value.to_value(self.unit)`.
3. `HDF5TableWriter._append_row` applies the previously registered column transform to each later row's value.
4. If a later row supplies a Python float for a column whose transform was registered from a prior Quantity value, the transform calls `float.to_value(...)` and raises the observed AttributeError.

This mechanism is not merely inferred from the issue title: the reporter's issue comment includes the full traceback. It identifies `DataWriter.__call__` -> `_write_muon_telescope_events` -> `HDF5TableWriter.write` -> `_append_row` -> `_apply_col_transform` -> `QuantityColumnTransform.__call__` -> `value.to_value(self.unit)`, ending in `AttributeError: 'float' object has no attribute 'to_value'`. The source and traceback therefore corroborate the mixed-type, per-column-transform failure mechanism.

PR #2732 normalizes skewness and excess kurtosis to plain numeric values in both the zero-image and nonzero-image branches. Its regression test asserts float/np.floating outputs for the nonzero uniform-image case. The zero-image test checks NaN but does not assert the output types. The docstring remains unchanged in the fixed source, so a documentation mismatch remains, but the container schema plus HDF5 serialization contract support plain unitless numbers as the intended storage type.

## 2. Important issue reproduction discrepancy

The issue body shows this configuration:

```yaml
DataWriter:
  write_muon_parameters: False
```

However, exact-base `DataWriter.__call__` only invokes `_write_muon_telescope_events(event)` inside `if self.write_muon_parameters:`. The reporter's traceback explicitly shows that this method was invoked. Therefore the pasted configuration, if applied literally and without later override, cannot produce the reported muon-parameter write path.

This is an unresolved provenance/reproduction discrepancy. Possibilities include a transcription error in the issue's YAML, an effective configuration override, or a different run configuration. None may be assumed. Before claiming an end-to-end reproduction of issue #2730, the effective value of `write_muon_parameters` must be established. This discrepancy does not invalidate the traceback's evidence for the HDF5 mixed-type transform failure, but it prevents us from treating the published YAML as a self-sufficient reproducer.

## 3. Pinned source identity

- Repository: cta-observatory/ctapipe
- Buggy base: `287e7685e0e963f3fb44d92832ca97ac8c265c40`
- Fixed PR head: `5007b6ab61887d7555155edb4d1d296603a9735e`
- Merge commit: `ba4546f2027e2f820982c4e40730097b7e16434c`
- Issue #2730 created: `2025-04-02T15:59:14Z`
- PR #2732 created: `2025-04-02T17:48:48Z`
- Exact-base root LICENSE Git blob: `7d85dda24fa481e24c4b33dd98dbc13245ee1fd2`
- Exact-base pyproject.toml Git blob: `9f4bbee5eb6619a36bf327d7f34157a2c2ee0bd5`
- Exact-base containers.py Git blob: `89b33ac0c25516ca57fa23254808e276ac5944d2`
- Exact-base core/container.py Git blob: `70ce1cc66ea1442c5b228bd3dd619ea89ecb0b3c`
- Exact-base hdf5tableio.py Git blob: `df7514632f59da73a609179fd916ff316620e77a`
- Exact-base tableio.py Git blob: `ee059630af80dc746eae5ecbfbaa9727bbfe768a`
- Exact-base datawriter.py Git blob: `dbd5b36b1528d850537885b956dfc4a1f24be5e4`
- Exact-base features.py Git blob: `8d547bf52c52dee18a3fa82dd47395a03bded282`
- Fixed features.py Git blob: `f18f1c3f16b41a5e7b1076512296ca8a4efa1c2f`
- Fixed test_muon_features.py Git blob: `b9f44ed8d8254ce3f55c6df79471d071f6de7540`
- Exact-base project license declaration: BSD-3-Clause (documentary screen only; not legal advice or complete dependency clearance).

## 4. Upstream discussion evidence

- The reporter's issue comment supplies the full exception traceback described above.
- The PR author states that the container had inconsistent values: some dimensionless quantities and some plain values, despite the container fields declaring no units; container validation would reject the inconsistent values, but is not normally run.
- A reviewer questioned why a dimensionless unit was attached and then removed. The author pointed to type assertions added in tests.
- The reporter later said the patched branch created the HDF5 output file; unrelated invalid sqrt/log RuntimeWarnings were raised separately.
- A reviewer noted that an end-to-end DataWriter integration test could have caught the issue. The PR author considered type assertions sufficient. This remains a test-coverage limitation worth recording.

## 5. Remaining gates — do not skip

1. Authenticate the exact SWE-rebench frozen Parquet row for `cta-observatory__ctapipe-2732`, canonical row SHA-256, and every original `FAIL_TO_PASS` selector. No selector may be guessed, rewritten, or silently removed.
2. Resolve the issue YAML contradiction: establish why the published configuration says `write_muon_parameters: False` while the traceback proves the muon writer ran. If it cannot be resolved, document the issue report as internally inconsistent and limit the claim to the independently corroborated traceback/source mechanism.
3. Prepare an exact-base test-only patch and pinned minimal environment. Run the unchanged dataset selectors on buggy base and exact fixed revision. A valid Stage 2 result requires defect-specific test failures on base and passes on fixed; collection/setup failures do not count.
4. Ensure the test reproduces the mixed per-column type sequence that triggers the transform (Quantity first, float later), not merely the return type assertion. Prefer a focused HDF5TableWriter regression test or a source-faithful minimal reproducer.
5. Complete direct/transitive dependency and fixture license/provenance review.
6. Record raw logs, environment lock, source and row hashes, artifact manifest, and independent project/exposure review.
7. Only after Stage 2, perform human gold-mechanism and nested E1/E2/E3 adjudication. No model inference or training is authorized.

## 6. Current decision

- Source-level mechanism: **corroborated** by exact-base implementation and reporter traceback.
- Intended field/storage contract: **plain unitless numeric values**, supported by container field declarations and HDF5 serialization behavior.
- Docstring: **stale/inconsistent**; not evidence that the serialized field should be Quantity.
- Issue YAML: **internally inconsistent with the reported traceback** unless an override or transcription error is established.
- Frozen dataset row/selectors: **not yet authenticated**.
- Base-fail/fixed-pass: **not run**.
- License: exact-base root BSD-3-Clause documentary screen passed; full dependency scope pending.
- Stage 2: **hold**.
- Stage 3: not started.
- Final case acceptance: **not accepted**.
- Model inference/training: not authorized and not performed.
