# cta-observatory/ctapipe issue #2730 — candidate review and Stage 2 result

**Cohort rank:** 31 of 96 primary candidates  
**Dataset instance:** `cta-observatory__ctapipe-2732`  
**Issue:** https://github.com/cta-observatory/ctapipe/issues/2730  
**Fix PR:** https://github.com/cta-observatory/ctapipe/pull/2732  
**Technical Stage 2:** PASS — exact frozen selector and independent HDF5 mixed-type reproducer both fail on the exact buggy base and pass on the exact fixed PR head.  
**Candidate disposition:** Conditional hold pending issue-configuration/provenance reconciliation and Stage 3 review. Not a final accepted case.

## 1. Defect contract and source-level failure mechanism

The exact buggy-base `MuonParametersContainer` declares:

- `skewness = Field(nan, ...)`
- `excess_kurtosis = Field(nan, ...)`

Neither field declares a unit, and neither declares `type`, `dtype`, or `ndim`. This is an untyped field with a plain-float default, not a strict runtime type contract. The exact-base `Field.validate` only requires/converts a Quantity when `self.unit is not None`; because these fields have no unit or other type/dtype/dimension constraint, it accepts both a Quantity and a plain float. The docstring on `radial_light_distribution` nevertheless describes both outputs as `astropy.units.Quantity`; the PR's new test and implementation make the intended output change to plain floats, but the docstring was not updated.

The exact-base HDF5 writer path is:

1. `HDF5TableWriter._add_column_to_schema` detects a Quantity in the first row and creates a `QuantityColumnTransform` using the value's unit when the field has no unit.
2. `QuantityColumnTransform.__call__` evaluates `value.to_value(self.unit)`.
3. `HDF5TableWriter._append_row` applies the already-registered transform to later rows in that same column.
4. When a later row has an ordinary Python float, the transform calls `float.to_value(...)`, producing the observed `AttributeError`.

This is directly supported by the reporter's full issue traceback: `DataWriter.__call__` -> `_write_muon_telescope_events` -> `HDF5TableWriter.write` -> `_append_row` -> `_apply_col_transform` -> `QuantityColumnTransform.__call__` -> `value.to_value(self.unit)`, ending in `AttributeError: 'float' object has no attribute 'to_value'`.

The pipeline source also contains two relevant output paths: valid muon parameters are calculated through `radial_light_distribution`, while invalid-ring processing can return the default `INVALID_PARAMETERS = MuonParametersContainer()`. The direct reproduction below deliberately writes a calculated (base: Quantity-valued) `MuonParametersContainer` followed by a default container (plain float defaults), reproducing the column-transform type mismatch.

## 2. Important issue reproduction discrepancy — still open

The frozen issue problem statement includes this YAML:

```yaml
DataWriter:
  write_muon_parameters: False
```

Yet exact-base `DataWriter.__call__` calls `_write_muon_telescope_events(event)` only under `if self.write_muon_parameters:`, and the reporter traceback proves that the muon writer ran.

Therefore the published YAML, if literally used as the effective configuration without an override, does not explain the observed call path. A transcription error, a different effective configuration, or an override are possible, but none has been established. This discrepancy does not undo the independently reproduced HDF5 mechanism, but it means that the issue YAML is not a self-sufficient reproducer and the original run's effective configuration remains a provenance question.

## 3. Pinned source and frozen dataset identity

- Repository: `cta-observatory/ctapipe`
- Buggy base: `287e7685e0e963f3fb44d92832ca97ac8c265c40`
- Fixed PR head: `5007b6ab61887d7555155edb4d1d296603a9735e`
- Merge commit: `ba4546f2027e2f820982c4e40730097b7e16434c`
- Issue #2730 created: `2025-04-02T15:59:14Z`
- PR/dataset row created: `2025-04-02T17:48:48Z`
- Exact-base root LICENSE Git blob: `7d85dda24fa481e24c4b33dd98dbc13245ee1fd2`
- Exact-base pyproject.toml Git blob: `9f4bbee5eb6619a36bf327d7f34157a2c2ee0bd5`
- Exact-base containers.py blob: `89b33ac0c25516ca57fa23254808e276ac5944d2`
- Exact-base core/container.py blob: `70ce1cc66ea1442c5b228bd3dd619ea89ecb0b3c`
- Exact-base hdf5tableio.py blob: `df7514632f59da73a609179fd916ff316620e77a`
- Exact-base tableio.py blob: `ee059630af80dc746eae5ecbfbaa9727bbfe768a`
- Exact-base datawriter.py blob: `dbd5b36b1528d850537885b956dfc4a1f24be5e4`
- Exact-base features.py blob: `8d547bf52c52dee18a3fa82dd47395a03bded282`
- Fixed features.py blob: `f18f1c3f16b41a5e7b1076512296ca8a4efa1c2f`
- Fixed test_muon_features.py blob: `b9f44ed8d8254ce3f55c6df79471d071f6de7540`
- Exact-base project license declaration: BSD-3-Clause (documentary root-source screen, not legal advice or blanket dependency clearance).

Frozen dataset:
- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Instance ID: `cta-observatory__ctapipe-2732`
- Row SHA-256 (canonical JSON): `9d8e145ebe4681e2b0cd2553b31cd14a65361fea7b64770948d34de6052c534d`
- Frozen `FAIL_TO_PASS` count: **1**
- Exact unchanged selector: `src/ctapipe/image/muon/tests/test_muon_features.py::test_radial_light_distribution`

The row was extracted from the exact pinned Parquet file in a successful Python 3.11.9 audit run. Canonical row JSON and selector text were saved in the artifact, the artifact digest matched GitHub's reported digest, all four internal file hashes passed, and the row SHA-256 was independently recalculated from the retained canonical JSON.
- Row audit run: `44298746628`
- Row audit artifact ID: `14424887790`
- Row audit ZIP SHA-256: `4653884c0f6f127c0d8150b3011924bc1be0c515800a5df762ac839be67c151c`

## 4. Technical Stage 2 — exact base-fail / fixed-pass

A dedicated no-inference workflow used CPython 3.11.9 and pinned direct/test dependencies. The exact upstream PR changed three files:

1. `docs/changes/2732.bugfix.rst`
2. `src/ctapipe/image/muon/features.py`
3. `src/ctapipe/image/muon/tests/test_muon_features.py`

On the buggy base, the workflow applied only the upstream test-file patch; its worktree status confirms only `src/ctapipe/image/muon/tests/test_muon_features.py` was modified. No production fix was applied to the buggy base.

### 4.1 Frozen SWE-rebench selector

- Buggy base: **FAIL** at the regression assertion. Actual observed type was `astropy.units.quantity.Quantity`, whereas the patched test requires `float` or `numpy.floating`. Result: `1 failed in 0.05s`.
- Fixed PR head: **PASS**. Result: `1 passed in 0.02s`.

This was a defect-specific assertion failure, not collection or environment failure.

### 4.2 Independent HDF5 mixed-type reproducer

The supplemental test writes a calculated muon-parameter container and then a default `MuonParametersContainer` through the real `HDF5TableWriter`.

- Buggy base: **FAIL** at the exact HDF5 transform. The traceback ends with `AttributeError: 'float' object has no attribute 'to_value'` in `QuantityColumnTransform.__call__`. Result: `1 failed in 1.08s`.
- Fixed PR head: **PASS**. Result: `1 passed in 1.07s`.

This provides direct mechanism-level evidence beyond the frozen selector's type assertion.

### 4.3 Environment and artifact

- CPython: 3.11.9
- NumPy: 1.26.4
- Astropy: 6.1.7
- pytest: 8.3.5
- pytest-astropy-header: 0.2.2
- PyTables: 3.10.2
- `pip check`: `No broken requirements found`
- Installed distributions captured: 51
- Dependency license metadata: 51 distributions captured; all had at least one of a license field, license classifier, or detected license file. 50 had detected license files; tqdm had a license field and classifiers but no license file among the captured metadata paths. This is an inventory, not human legal clearance.

Primary Stage 2 repeat run:
- Workflow run: `44300812600`
- Job: `134789741250`
- Artifact ID: `14424704542`
- Artifact name: `ctapipe-2732-stage2-base-fixed-44300812600-1`
- Artifact ZIP SHA-256: `bc5c7c022cb0b7685415877beea3d678945a5740dcc21b44b1989e224a0f3426`
- All 22 evidence-file hashes in `SHA256SUMS.txt` were independently checked successfully.
- The artifact additionally includes SHA-256 hashes for the workflow, direct HDF5 test file, exact selector file, frozen row manifest, and dependency input lock.
- The HDF5 reproducer now explicitly calls `validate()` on both the calculated Quantity-valued and default-float containers; both validate successfully before the base writer failure.
- Environment input SHA-256: `1b6e82f8db8dcad6a1720666f19c8868ae5d6ef6e13cae2228d9c0e7e7a62edb`
- Dependency-license metadata SHA-256: `f9151d1e3824a96da76dff15401e4e112a904fd4f25a52c2865903e1e1d3a868`

An earlier complete Stage 2 execution independently gave the same base-fail/fixed-pass outcomes:
- Workflow run: `44299388651`, job `134784814840`
- Artifact ID: `14424942732`
- Artifact ZIP SHA-256: `f6ddfd91afa97b3720c10c0f7816f409a7c354f85883fa61b837bfc823621ea`

A machine-readable combined evidence manifest is stored at `research_candidates/evidence_abstention/reproduction/ctapipe_issue_2730/stage2_evidence_manifest.json`.

## 5. Remaining Stage 3 and provenance gates

1. Resolve or formally record the issue YAML/effective-configuration discrepancy. If it cannot be resolved, preserve the scope limitation and do not claim that the posted YAML alone reproduces the original run.
2. Complete direct/transitive dependency, optional/bundled third-party, and system-level license/provenance review. The recorded 51-distribution metadata inventory is not a substitute for human scope review.
3. Complete independent-project and related-issue-family review.
4. Record researcher exposure and timing/cutoff assessment.
5. Complete human gold-mechanism adjudication and nested E1/E2/E3 evidence-tier decisions.
6. Keep the final accepted case registry unchanged until a schema-conformant acceptance record and separate project-lead decision are recorded.

No model was loaded; no inference or fine-tuning was performed.

## 6. Upstream discussion and test-coverage limitations

- The reporter's issue comment provides the full exception traceback.
- The PR author says some skewness/excess-kurtosis values had a dimensionless unit while others did not, although the container fields declared no units; the author states container validation would reject the inconsistency but was not normally run. **That validation claim conflicts with the exact-base implementation:** `Field.validate` has no unit, type, dtype, or ndim constraint for these fields, and `Container.validate` delegates to that method. The revised direct HDF5 test explicitly calls `validate()` on both a Quantity-valued calculated container and a default-float container; both pass on the buggy base. The error then occurs later, when HDF5TableWriter applies the transform registered from the first row's Quantity to the second row's float.
- A reviewer questioned attaching a dimensionless unit only to remove it later. The author referred to new type assertions.
- The reporter later confirmed that the patched branch created the HDF5 output file; invalid sqrt/log warnings were treated as unrelated.
- A reviewer noted that an integration test writing muon parameters through DataWriter could have caught the defect. The PR author considered type assertions adequate. The missing end-to-end test remains a coverage limitation; the research-side direct HDF5 reproducer now addresses the mechanism for our Stage 2 evaluation.

## 7. Current decision

- Source-level failure mechanism: **corroborated by exact-base code, reporter traceback, and independent HDF5 reproducer**.
- Intended serialized field contract: **unitless numeric values**, supported by `Field(nan)` container declarations and the HDF5 behavior.
- Docstring: **stale/inconsistent** with the field schema and implementation.
- Frozen dataset row and exact selector: **authenticated**.
- Exact frozen selector: **base-fail / fixed-pass**.
- Direct HDF5 mixed-type reproducer: **base-fail / fixed-pass**.
- Technical Stage 2: **PASS**.
- Candidate disposition: **conditional hold pending YAML/config provenance and Stage 3**.
- Stage 3: **not started**.
- Final case acceptance: **not accepted**.
- Model loading/inference/training: **not performed**.
