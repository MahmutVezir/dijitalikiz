# CTAPIpe #2730 — proposed technical gold and nested E3/E2/E1 evidence tiers

**Candidate:** cta-observatory__ctapipe-2732 (frozen primary cohort rank 31)  
**Upstream project:** cta-observatory/ctapipe  
**Issue / fix:** [Issue #2730](https://github.com/cta-observatory/ctapipe/issues/2730) / [PR #2732](https://github.com/cta-observatory/ctapipe/pull/2732)  
**Status:** AI-assisted technical proposal for the student project lead. **Not human-adjudicated, not accepted, and not an authorization for inference.**

## 1. Proposed technical gold

**Proposed gold mechanism ID:** **G1_MIXED_QUANTITY_FLOAT_HDF5_COLUMN_TRANSFORM_REUSE**

The buggy base contains a per-telescope muon HDF5 table whose column transforms are selected when the table schema is first created. For the unitless MuonParametersContainer.skewness and excess_kurtosis fields:

1. The base implementation of radial_light_distribution returns dimensionless Astropy Quantity objects for non-empty images (base features.py, lines 324–349).
2. The corresponding MuonParametersContainer fields are declared with ordinary nan defaults and no unit, type, dtype, or ndim constraint (base containers.py, lines 1213–1220).
3. The muon processor can place default MuonParametersContainer values into events when the telescope is skipped or the ring radius is invalid (processor.py, lines 154–175 and 247–249). Other events can contain calculated values from radial_light_distribution (processor.py, lines 297–317).
4. The HDF5 writer sees a Quantity while building the table schema and registers a QuantityColumnTransform for that column (hdf5tableio.py, lines 294–298). That transform calls value.to_value(self.unit) (tableio.py, lines 342–350).
5. Later rows reuse the transform while appending values (hdf5tableio.py, lines 442–464). When a later default value is a Python float, the cached transform calls float.to_value and raises the observed AttributeError.

The fixed PR head removes the dimensionless unit from the computed skewness and excess-kurtosis outputs in both the zero-image and nonzero-image branches, returning ordinary numbers consistent with the unitless container defaults. Its added regression assertion requires float or numpy.floating. The fixed code still retains the old docstring declaration that these outputs are astropy.units.Quantity; that documentation mismatch is real and should remain recorded.

**Proposed interpretation:** the primary defect is inconsistent scalar representation across rows of one HDF5 column, combined with a transform registered from the first value and reused for later values. The intended field/storage contract is plain unitless numeric values, as supported by the container declaration and the fixed implementation/test. This is a technical interpretation for human review, not yet a project-lead decision.

## 2. Alternative mechanisms and predictions

These are alternatives to adjudicate, not claims that they are equally likely.

### A1 — DIMENSIONLESS_QUANTITY_IS_THE_INTENDED_FIELD_CONTRACT

**Description:** the function docstring is the intended contract; skewness and excess kurtosis should remain Astropy quantities, and the default/invalid rows or container schema should be updated to use the same dimensionless quantity representation.

**Testable prediction:** the intended model contract would declare or consistently supply dimensionless quantities for every row, including defaults. A consistent all-Quantity column would not trigger the reported float-without-to_value failure. The current base container declaration does not encode that contract; the fixed PR's scalar outputs and new tests favor plain numbers instead.

### A2 — CONTAINER_VALIDATION_REJECTS_MIXED_TYPES_BEFORE_HDF5

**Description:** the inconsistency is detected by Container.validate() and the HDF5 exception is only a secondary symptom or a separate failure path.

**Testable prediction:** validating both a Quantity-valued calculated container and a default-float container should raise before HDF5 append. The exact-base Field.validate implementation only requires/converts a Quantity when field.unit is not None; these two fields have no unit/type/dtype/dimension constraint. The current HDF5 reproducer explicitly validates both containers successfully, then the writer fails on the later float. This alternative is contradicted by the exact-base implementation and the reproduced call path.

### Separate provenance issue — P1_EFFECTIVE_CONFIG_DIFFERS_FROM_PUBLISHED_YAML

This is not a competing explanation for float.to_value; it is an inconsistency in the issue's reproduction record. The frozen issue text says DataWriter.write_muon_parameters: False. However, exact-base ProcessorTool.should_compute_muon_parameters only enables muon processing when self.write.write_muon_parameters is true, and exact-base DataWriter.__call__ only invokes _write_muon_telescope_events under the same true condition. The reporter's traceback proves that this method executed. Therefore the published YAML cannot be the effective configuration for that traceback if its value was literally false and not overridden. The actual effective configuration is unknown; do not silently change the YAML or assert that it is a typo.

## 3. Proposed nested evidence tiers

The tiers are to be prepared from verbatim, provenance-backed source snapshots and exact output logs. Repeated evidence must remain byte-identical across tiers. The packet contents must not include hidden tier labels, policy labels, case IDs, PR patch, fixed commit, gold IDs, or the adjudication record. The outer packet-set manifest is for structural validation only and must not be shown to the model.

### E3 — insufficient evidence

**Proposed visible contents:**
- The frozen SWE-rebench problem statement/issue body only, preserving the published YAML with write_muon_parameters: False.
- The reported symptom text (error title and the description of failure to write muonparameters_skewness).
- No reporter traceback comment, implementation source, PR metadata, fix, or test patch.

**Mechanisms that should remain possible:**
- G1: HDF5 per-column transform reused across values with inconsistent types.
- A1: intended Quantity contract, with inconsistent default/invalid values.
- P1: the published configuration does not actually enable the reported writer, so the effective runtime configuration or report provenance is incomplete.

**Rationale:** the problem statement reports an exception but does not show the internal call stack or the producer paths. The contradictory configuration is visible and should make an unqualified diagnosis risky. A model should be able to state the inconsistency and ask for the effective configuration or traceback rather than treating the pasted YAML as proven runtime state.

### E2 — partial evidence

**E3 is retained unchanged**, plus:
- The reporter's exact traceback comment, preserved as a source snapshot (the trace identifies _append_row, _apply_col_transform, QuantityColumnTransform.__call__, and value.to_value).
- Exact-base MuonParametersContainer declarations for skewness and excess_kurtosis.
- Exact-base Field.validate code showing the conditional unit/type checks.
- Exact-base HDF5TableWriter schema initialization, _append_row, and QuantityColumnTransform implementation.

**Mechanisms that should remain possible:**
- G1: the HDF5 transform is being applied to a later plain float after it was registered from a Quantity.
- A1: the intended schema could instead be Quantity-valued, with default rows requiring correction.
- P1 remains an unresolved effective-configuration discrepancy, separate from the exception's call path.

**Rationale:** E2 localizes the exception to the HDF5 column transform and shows that these container fields do not enforce a unit/type constraint during Container.validate(). It does not yet expose the processor's valid-ring and invalid/default population paths that create the mixed values, nor does it resolve the intended data contract beyond the unitless field declaration.

### E1 — sufficient evidence

**E2 is retained unchanged**, plus:
- Exact-base MuonProcessor source showing the INVALID / INVALID_PARAMETERS default paths and the calculated-parameter path through radial_light_distribution.
- Exact-base ProcessorTool event loop and DataWriter configuration gate showing the order of muon processing and writing, and that the published false flag skips this path.
- Exact fixed PR implementation and regression assertion (used only in the hidden adjudication/source package; the model-visible packet may show the relevant fixed source only if the final protocol allows fix-source evidence at E1).
- Exact frozen-selector base-fail/fixed-pass logs and the independent HDF5 reproducer logs, with the researcher-created test source withheld if it contains hidden labels or prompt-adaptation material.

**Proposed surviving mechanism:** G1 only.

**Rationale:** the event processor can populate the same telescope's muon table with default plain-float values and calculated skewness/kurtosis values. The HDF5 writer registers the conversion transform based on the first observed value and reuses it for subsequent rows. The independent reproduction executes the real DataWriter.__call__ method under an enabled flag, with its unrelated writers isolated, and exercises the actual muon writer plus HDF5TableWriter. The frozen upstream selector independently fails on the exact buggy base and passes on the exact PR head. This combination supports G1 and excludes A1/A2 as explanations of the observed exception. The published YAML/effective-config mismatch remains a separate report-provenance caveat and is not erased by E1.

## 4. Reproduction evidence already available

Frozen row:
- Instance: cta-observatory__ctapipe-2732
- Dataset revision: fb9aa226b2ce37c708ea7732e7b980abacdadb67
- Parquet SHA-256: 7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9
- Canonical row SHA-256: 9d8e145ebe4681e2b0cd2553b31cd14a65361fea7b64770948d34de6052c534d
- Frozen selector: src/ctapipe/image/muon/tests/test_muon_features.py::test_radial_light_distribution
- Exact base: 287e7685e0e963f3fb44d92832ca97ac8c265c40
- Exact fixed PR head: 5007b6ab61887d7555155edb4d1d296603a9735e

Previously verified Stage 2:
- Frozen selector: defect-specific fail on base, pass on fixed.
- Direct HDF5 reproducer: AttributeError: 'float' object has no attribute 'to_value' on base, pass on fixed.
- Both calculated and default containers pass exact-base Container.validate().
- A later reproducer revision calls the real DataWriter._write_muon_telescope_events method through the unbound class method and reproduced base-fail/fixed-pass. The stronger current rerun executes DataWriter.__call__ itself with the muon-write flag both false and true; its result is pending and must be recorded separately.

## 5. Exposure, independence, and license limitations

- Upstream repository API reports cta-observatory/ctapipe as canonical (fork=false).
- The frozen primary cohort queue contains one CTAPIpe candidate at rank 31; no second CTAPIpe candidate is currently listed in the queue.
- The researcher has full source exposure to the issue, source, PR, and reproduction through this review. Do not claim researcher blinding.
- The selected Qwen2.5-3B-Instruct release predates the issue/PR dates; this reduces the likelihood that this exact public issue/PR text was in the original released weights, but does not establish the model's full training-data cutoff or prove absence of related code from training.
- Exact-base root license is BSD-3-Clause. A metadata inventory exists for the 51 installed runtime/test/build distributions; human scope review is not complete. The installed-license notice files are being captured in the latest Stage 2 artifact. This is documentary screening only, not legal advice or a license grant.
- The issue YAML and reporter traceback remain inconsistent unless an effective-config override or transcription error is established. The independent reproducer uses write_muon_parameters=True because the exact source path requires it; that is not a claim that the reporter's pasted YAML was true.

## 6. Human decision boundary

**Project-lead approval status:** PENDING.

The student project lead must decide whether to:
1. accept G1 as the technical gold mechanism;
2. accept A1 and A2 as the predeclared alternatives and the separate P1 config mismatch caveat;
3. accept the proposed E3/E2/E1 boundary and mechanism-survival rationale;
4. accept full researcher exposure and a single-human-adjudicator exploratory limitation;
5. approve the documentary license screen after reviewing the captured notices.

This draft does not mark any of these as human-approved. ChatGPT is an AI research assistant, not a human co-investigator or independent human rater. No model load, inference, or training has been performed or authorized.
