# CTAPIpe frozen-project row family review

**Dataset:** PrimeIntellect/SWE-rebench-V2-Filtered-Verified  
**Revision:** fb9aa226b2ce37c708ea7732e7b980abacdadb67  
**Parquet SHA-256:** 7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9  
**Repository identity:** cta-observatory/ctapipe  
**Full repository row count:** 5  
**Status:** AI-assisted repository-level family review; student project-lead sign-off pending.

## 1. Complete dataset membership

A read-only scan of the entire frozen Parquet returned exactly five records where `repo == "cta-observatory/ctapipe"`. The audit artifact retains each complete row, including its problem statement, PR description, production patch, test patch, original selector arrays, base commit, and canonical row SHA-256.

- Workflow run: 44313191520
- Job: 134832360579
- Artifact ID: 14430704023
- Artifact name: ctapipe-2730-dataset-row-audit-44313191520-1
- ZIP SHA-256: 7da5213baffb781389e44b8d26afa543a5f18b1f0b8609eeb6928f052da99650
- Artifact members: 11
- SHA256SUMS entries: 10/10 independently verified
- Complete row payloads retained: 5/5

| Frozen instance | PR / issue | Date (UTC, dataset row) | Bug family | Original FAIL_TO_PASS | Canonical row SHA-256 |
|---|---|---:|---|---:|---|
| cta-observatory__ctapipe-1872 | PR #1872 / issue #1621 | 2022-04-05 13:50:06 | Simulation configuration API always returns obs_id→config mapping; DataWriter metadata adaptation | 2 | 59d1aeb7e62bd9f53e560f0522fefd7541b5f2681a4a549b59a6dba26659631b |
| cta-observatory__ctapipe-1883 | PR #1883 / issue #1882 | 2022-04-19 16:29:50 | Component/Tool logger hierarchy | 1 | 04e0fc47b2c83c8b55d1e3dce73191478a9f56c6a7bac4d5153be77156f76329 |
| cta-observatory__ctapipe-2320 | PR #2320 / issue #2321 | 2023-04-27 15:27:22 | StereoTrigger assumes list, but real EventSource provides NumPy uint16 array | 3 | 29aa95ca29633ca6cae342f83a5240fddc26a847781587ff71df919aeef294ec |
| cta-observatory__ctapipe-2732 | PR #2732 / issue #2730 | 2025-04-02 17:48:48 | Muon skewness/excess-kurtosis mixed Quantity/float values in HDF5 serialization | 1 | e7d40ebfdfa47f6d2b92940d83d4e1c74afea6a096e9dca0d682ebb0854e7006 |
| cta-observatory__ctapipe-2738 | PR #2738 / issue #2737 | 2025-04-11 15:17:40 | DispReconstructor chooses wrong probability column for sign prediction | 1 | db357eac53cf7fb6675b16b0ad56af595eba2edb357dab35f50808c092bb8a3b |

The instance suffixes match the corresponding PR numbers in the upstream repository. Upstream PR metadata and frozen row patch/test-patch contents were cross-checked.

## 2. Why the other four rows are not the same defect family

### #1872 — simulation configuration shape

- Frozen F2P selectors concern `SimTelEventSource.test_additional_meta_data_from_simulation_config` and `test_properties`.
- Production patch changes `ctapipe/io/datawriter.py`, `hdf5eventsource.py`, and `simteleventsource.py`.
- The DataWriter changes alter simulation-run metadata serialization to iterate through a dictionary of simulation configurations. The patch does not change the muon-table path, `MuonParametersContainer`, `QuantityColumnTransform`, or the skewness/kurtosis fields.
- Same file-level component (DataWriter) is not the same root-cause family.

### #1883 — logger hierarchy

- Frozen selector: `ctapipe/core/tests/test_component.py::test_logging_hierarchy`.
- Production changes are confined to `ctapipe/core/component.py` and `ctapipe/core/tool.py`.
- The defect is parent logger wiring before traitlets initialization, not HDF5 serialization or unit-bearing values.

### #2320 — SoftwareTrigger input container type

- Frozen selectors test `SoftwareTrigger` and real SimTel event behavior.
- Production patch changes `ctapipe/instrument/trigger.py`; it replaces list-specific removal with NumPy-compatible set operations.
- The issue is list-versus-`np.ndarray` handling for telescope IDs, not a Quantity transform or muon table.

### #2738 — DispReconstructor sign prediction

- Frozen selector: `src/ctapipe/tools/tests/test_train.py::test_train_disp_reconstructor`.
- Production patch changes `ctapipe/reco/sklearn.py` to use the positive-class probability column `[:, 1]` instead of `[:, 0]`.
- The defect is a classification probability-index/sign error, not a muon-parameter serialization error.

## 3. Selection under the one-upstream-project rule

The study protocol permits at most one accepted independent case per upstream project. Therefore the five dataset tasks cannot contribute five independent cases to the accepted-case count, irrespective of their distinct row IDs.

**Selected candidate for this project:** `cta-observatory__ctapipe-2732` (issue #2730 / PR #2732).

Reasons:
1. Its issue is directly about the observed `muonparameters_skewness` HDF5 serialization failure.
2. The single frozen F2P test is directly within the modified radial-light-distribution function.
3. Its exact buggy-base/fixed-PR test contrast passes.
4. A separate reproduction calls the exact upstream `DataWriter.__call__`, retains `_write_muon_telescope_events` and the real `HDF5TableWriter`, verifies `False` skips the muon write, and reproduces the `float.to_value` exception on base when the flag is true; the same reproducer passes on the fixed revision.
5. The other four tasks have distinct problem statements, production paths, tests, and root-cause families.

The other four rows are retained as same-repository, non-selected sibling tasks. They are **not** counted as independent projects, separate cases, or evidence for the #2732 root cause.

## 4. Remaining independence limitations

- The repository is canonical (`fork=false`), but that does not establish independence from every fork, derivative, or related codebase.
- The five same-repository rows have been compared at the dataset statement, selector, and patch-path level. This is a strong within-dataset family screen, but not a complete semantic audit of all issues and PRs across all repository history.
- Focused GitHub searches for `muonparameters_skewness`, `radial_light_distribution skewness`, `MuonParametersContainer HDF5`, and `to_value muon` found no second directly matching defect record; broader `to_value/muon` search also returned unrelated #1139.
- Researcher source exposure for #2732 is full. The case is not researcher-blinded. The student's prior pipeline-debug exposure classification remains a project-lead decision.

**Proposed independence conclusion:** among the five frozen CTAPIpe dataset rows, #2732 is the only row belonging to the selected muon Quantity/float HDF5 defect family. The upstream-project one-case rule is satisfied only by counting #2732 once and not treating the other four tasks as independent samples. Final formal independence approval remains with the student project lead.
