# OpenMDAO/dymos #1166 — Stage 2 candidate review

**Disposition:** Stage 2 technical reproduction passed. Stage 3 scientific adjudication has not started. The case is not accepted into the final registry.

## 1. Provenance and identity

- Repository: https://github.com/OpenMDAO/dymos
- Bug report: https://github.com/OpenMDAO/dymos/issues/1166
- Fix PR: https://github.com/OpenMDAO/dymos/pull/1165
- PR created: 2025-04-04T20:23:44Z
- Linked issue created: 2025-04-04T20:26:09Z (2 minutes 25 seconds after the PR)
- PR merged: 2025-04-05T11:30:09Z

The dataset timestamp is authenticated against the PR resource, not the linked issue resource. The PR-before-issue ordering is unusual but is preserved as observed; it is not silently normalized or presented as an issue-before-PR chronology.
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

## 7. Independent artifact verification note

The downloaded artifact ZIP was independently checked outside the workflow:
- ZIP SHA-256: `8fc5e1de9ee8c7d4be45c29b48ba9b1a0e6c82194ecb9ce2b7f5757d4fd58051`
- `SHA256SUMS.txt`: 18 entries, all 18 payload files present and hash-matched.
- Canonical dataset row bytes independently re-hash to `236f9cd1bb8cbacad27fd771e3878802e7dbf6f36a64eff35a60be7a32f6efb5`.

This confirms artifact integrity, not the legal sufficiency of the license metadata inventory or the scientific gold adjudication.

## 7. Remaining gates

1. Human review of the complete pinned dependency license inventory. The installed NumPy and SciPy wheels include bundled numerical libraries with additional notices; the inventory records them, but this is not legal clearance.
2. Independence and related-issue review, ensuring one Dymos case only.
3. Human adjudication of the gold mechanism and alternative explanations.
4. Prepare nested E1/E2/E3 packets with manifests and verified source/log hashes; obtain project-lead approval.
5. Construct the complete schema-conformant final case record and pass the fail-closed registry validation.
6. Make a separate final case-acceptance decision.

**Current disposition:** Stage 2 technical pass; Stage 3 not started; `case_acceptance=not_accepted`; no model loaded, inference run, or training performed.


## Independent public-API reproducer, Stage 3 proposal and CI — 20 November 2026

A second reproduction route was added separately from the frozen SWE-rebench selector. The independent test builds a fresh one-phase Brachistochrone model, calls `add_control(val=[5.0, 15.0])`, runs setup/run_model, and reads the promoted `phase0.controls:theta` input directly. It does not import or reuse PR #1165's modified balanced-field regression test and does not call an optimization driver.

- Test: `research_candidates/evidence_abstention/reproduction/dymos_issue_1166/test_issue_1166.py`, SHA-256 `70f5c522c7617d392238d1107fe3eb4472a53850db581d91e4f8901138b8eaf9`.
- Workflow run: `44739419824`, job `136298973618`, successful.
- Buggy base: `3efd1035c3bf62890034eb9e07de543f3d117867`; the public-API test executed and failed with actual `[[1.0], [1.0]]` rather than `[[5.0], [15.0]]`.
- Fixed PR head: `0ffc82225d6125dcb5c5b5acfb9be9fd712ef949`; the same test and environment passed (`1 passed in 0.49s`).
- Artifact: `14629598269`; SHA-256 `33bb899d7e4e56d177fe4c9d119eebea49519528e88d74af3efc4acf7def08d8`; local outer digest match, ZIP CRC PASS, 15/15 internal SHA256SUMS entries PASS.
- Runtime: CPython 3.11.9; OpenMDAO 3.38.0; NumPy 1.26.4; SciPy 1.13.1; NetworkX 3.3; no optional optimizer installed or invoked.

The candidate therefore has two complementary technical routes: the exact frozen dataset selector (18/18 artifact payload hashes verified) and a separate public-API reproducer (15/15 artifact payload hashes verified). Both execute on the exact buggy base, fail for the specified default-value mismatch, and pass on the exact fixed revision.

### Related issue-family disposition

Dymos #531 (2021) is retained as a historical predecessor in the same broad default-value family; it was explicitly resolved by PR #533. #1166 is a later regression after the control-interpolation component's containment/configuration changed and the old `set_input_defaults` route disappeared. #531 is not counted again as an independent case. #1131 concerns a separate control-rate/explicit-shooting mechanism. Dymos contributes at most one case.

### Proposed Stage 3 evidence packet

New files under `research_candidates/evidence_abstention/dymos_1166/`:
- Proposed operational E1/E2/E3 packet set: `OPERATIONAL_EVIDENCE_PACKET_SET_PROPOSED_V0_1_2026-11-20.json`
- Provenance: `EVIDENCE_PACKET_PROVENANCE_PROPOSED_V0_1_2026-11-20.json`
- Issue-family/independence screen: `DYMOS_1166_ISSUE_FAMILY_INDEPENDENCE_REVIEW_V0_1_2026-11-20.json`
- Dependency/license scope inventory: `DYMOS_1166_DEPENDENCY_LICENSE_SCOPE_REVIEW_V0_1_2026-11-20.json`
- Proposed technical gold and tier rationale: `DYMOS_1166_GOLD_AND_EVIDENCE_TIERS_DRAFT_V0_1_2026-11-20.md`

The corrected packet-set SHA-256 is `07b9547ba6bc30dd525acff0b9916542b81e47f9ed8451f2b0fba5ca8a22b17d`, with E3=1, E2=3, E1=6. The evidence content hashes bind to the exact pinned row, the actual independent reproducer file, the base-failure log summary, and three single-line source excerpts from the pinned buggy base. The upstream fix and fixed-pass output are excluded from model-visible packet contents. This is a proposal, not semantic gold adjudication.

### Branch-head no-inference CI

- Workflow run: `44741554783`, commit `1afb274a2044d7f418d034c199605c23cecd01e4`.
- No-inference preflight job: `136306184954`, successful.
- Dymos packet/provenance/license/independence tests: **5 passed**.
- NumPyro packet/provenance/license/independence/bundle tests in the same run: **8 passed**.
- Other groups: packet audit 12; operational/nested packet contracts 25; selector runner 6; exploratory acceptance/readiness 24; study design/scoring 10. Total: **65 tests passed**.
- Readiness remained blocked before inference: one accepted case/project (Dishka), 13 global blockers, `ready_for_inference=false`, no model loading, inference or fine-tuning.
- Preflight log artifact: `14631870140`; digest `sha256:a26ff02fce4af5d2833975a77fcad2a7efb306ea5358b26a6b04be1181bcd78e`.

The first run on the initial Dymos test draft failed at module import (missing implementation path); the second run exposed stale test expectations after the packet contents were rebound to exact source bytes. The test path and evidence-delta assertions were corrected. The successful result above is from the later exact-hash branch-head run.

### Current Dymos disposition

Stage 2 dataset reproduction: PASS. Independent public-API reproduction: PASS. Proposed packet structure/CI: PASS. Issue-family grouping: documented, with #531 clustered as historical related context and not double-counted. Source/dependency inventory: recorded. Project-lead bounded license-scope acknowledgement, exact pinned dataset-card license authentication, candidate-specific prior pipeline/debug exposure declaration, and source-aware gold/E1-E2/E3 decision remain open. Final case acceptance remains **not accepted**; no model operation is authorized.


## Superseding Stage 2 / Stage 3 status update — 20 November 2026

The independent issue reproducer and the proposed Stage 3 packet contract have since passed on the refreshed branch head.

### Latest independent reproducer

- Workflow: [Dymos #1166 independent issue reproducer run 44741768163](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44741768163).
- Job: `136306920964`, conclusion: success.
- Buggy base: `3efd1035c3bf62890034eb9e07de543f3d117867`.
- Fixed PR head: `0ffc82225d6125dcb5c5b5acfb9be9fd712ef949`.
- Independent test: `reproduction/dymos_issue_1166/test_issue_1166.py`, SHA-256 `70f5c522c7617d392238d1107fe3eb4472a53850db581d91e4f8901138b8eaf9`.
- Base: the test executed and failed because the initial polynomial control values were `[[1.0], [1.0]]), not the requested `[[5.0], [15.0]]`.
- Fixed: same test passed (`1 passed`) in the same pinned Python/OpenMDAO/NumPy/SciPy environment.
- Artifact: `14631740733`; SHA-256 `3c3b2d96d0ad7b82d945aa7fcbc4014e64674496967eeb98288f070af8f39f00`. Downloaded independently: outer SHA-256 matched GitHub, ZIP CRC PASS, and all 15/15 internal SHA256SUMS entries PASS.

### Stage 3 packet structure CI

The proposed E1/E2/E3 packet set now passes its dedicated no-inference contract tests on the latest reviewed head. The successful branch-head preflight is run `44741767911`, job `136306921046`; the Dymos-specific test step reports **5 passed**. The run also passed the NumPyro review contracts (8 passed), general packet/selector/design tests and readiness reporting. This establishes packet hash/nesting and record-contract validity only, not semantic gold/tier sufficiency.

- Packet set: `dymos_1166/OPERATIONAL_EVIDENCE_PACKET_SET_PROPOSED_V0_1_2026-11-20.json`
- Packet-set SHA-256: `07b9547ba6bc30dd525acff0b9916542b81e47f9ed8451f2b0fba5ca8a22b17d`
- Nested counts: E3=1, E2=3, E1=6.
- Provenance, issue-family and bounded dependency-license inventory records are stored alongside the packet set.

### Adjudication route — same exploratory standard as Dishka

The active v0.2 protocol and Dishka #435 accepted precedent allow the student project lead to make the source-aware technical gold, alternatives and E1/E2/E3 decision as the single human adjudicator, with full researcher-source exposure disclosed. ChatGPT is advisory only. Hasan's input may be recorded as project-lead-reported supplementary source-aware technical input; it is not a second signed independent adjudication or a blind rating. Two human raters remain required for the separate later task of scoring raw model responses for evidence support; that requirement is not a two-person gold/tier gate.

The project lead's gold/tier decision for Dymos remains **pending**. The bounded documentary license acknowledgement, exact pinned dataset-card license authentication, and explicit candidate-specific prior pipeline/debug exposure declaration also remain pending. Dymos #531 is a historical related predecessor and is not counted as a second case. No inference is authorized.

**Current Dymos disposition:** Stage 2 dataset selector PASS; independent public-API reproducer PASS; proposed E1/E2/E3 structural contract PASS; single-project issue-family screen recorded; not yet accepted. Final case acceptance must remain unchanged until the project lead's technical decision, exposure/license declarations, complete schema-conformant case record, registry validation, and separate final YES/NO decision are recorded.


### Latest branch-head rerun — 20 November 2026

The independent public-API reproducer was rerun after the portfolio/adjudication-record updates on branch head `efe677f49088eb9493fef6e8c6615b5bcb061dcb`.

- Run: [44745436377](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44745436377), job `136319403418`, success.
- Artifact: `14632153920`; GitHub SHA-256 `b70d1572ed0a8dbc89f1331da09caaa8848a7581efb2b85c9aceefef09874be2`.
- Local re-download verification: outer SHA-256 exact match; ZIP CRC PASS; 15/15 internal SHA256SUMS entries PASS.
- Buggy base: the fresh Brachistochrone API test executed and failed with actual `[[1.0], [1.0]]` rather than requested `[[5.0], [15.0]]`.
- Fixed PR head: same test passed (`1 passed in 0.66s`).

This is a repeat of the same Dymos case, not an additional case. The related #531 issue remains a historical predecessor in the same broad family and is not double-counted. Final acceptance remains pending source-aware project-lead gold/tier decision, bounded license acknowledgement, exact dataset-card scope, exposure declaration, case record and registry check.


### Final current-branch rerun — 20 November 2026

A second current-head repeat completed successfully on branch head `b73b3ef11b633603ae84b5d85af47eb55fa7d1c9`.

- Workflow: [44745926619](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44745926619), job `136321086021`, success.
- Artifact: `14632443444`; SHA-256 `a59eea38a7a0384ade55d150f053cc8243fe1d27256a1a41178824101cf27241`.
- Local verification: outer digest match, ZIP CRC PASS, 15/15 internal hashes PASS.
- Buggy base produced the expected assertion mismatch `[[1.0], [1.0]]` vs `[[5.0], [15.0]]`; fixed PR head passed the same test (`1 passed in 0.63s`).

This is a verification repeat, not another case. The issue-family, source-aware adjudication, license, exposure, acceptance and no-inference boundaries remain unchanged.

## Project-lead selection decision

## Project-lead first-batch selection — 20 November 2026

The student project lead explicitly accepted Dymos #1166 as one of the strong first-batch candidates to continue through v0.2 Stage 3 case evaluation, applying the unchanged Dishka-equivalent criteria.

This is candidate-selection approval only. It does **not** approve the proposed Dymos gold mechanism or E1/E2/E3 tier membership; those remain for a separate source-aware project-lead decision. The candidate-specific prior pipeline/debug exposure declaration, bounded dependency/source/dataset license-scope acknowledgement, complete case record, fail-closed registry validation and separate final case YES/NO also remain pending.

The candidate remains not accepted as a final case at this point. It contributes at most one Dymos upstream-project case. No model load, inference, fine-tuning or training is authorized.


## Superseding project-lead prior pipeline/debug exposure declaration — 20 November 2026

The project lead explicitly declared `prior_pipeline_debug_exposure = none` for Dymos #1166: the candidate was not used before prospective case validation to debug the shared pipeline, runner, dataset selectors, or test oracle.

- Decision record: `research_candidates/evidence_abstention/dymos_1166/PROJECT_LEAD_EXPOSURE_DECISION_DYMOS_1166_2026-11-20.md`
- Decision-record SHA-256: `3d38e3b45f2d27cc6531ede3d73d8f2439deee0b6970c6d4618d4e02e55733ea`
- Evidence class: direct project-lead self-report from the 20 November 2026 conversation; not an independently witnessed audit.
- `researcher_source_exposure = full` remains separately disclosed because the project lead has reviewed the issue, PR, pinned source, reproductions, and evidence packets.

This closes only the candidate-specific prior pipeline/debug exposure declaration gate. It does not close source exposure, license scope, exact pinned dataset-card verification, source-aware gold/E1/E2/E3 adjudication, case-record validation, final acceptance, or inference authorization. Earlier references in this review to the prior pipeline/debug declaration being pending are superseded by this dated addendum.

**Current disposition remains:** selected for Stage 3 evaluation; not a final accepted case; no model loading, inference, fine-tuning, or training authorized.


## Superseding current-head verification after exposure declaration — 20 November 2026

On the current research branch head `44882123757cad187dce27376eea051d92ad96a7`:

- Dymos independent-reproducer workflow [44771791810](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44771791810), job `136411068945`: **success**.
- The fresh-model public-API reproducer executed on the pinned buggy base and failed with the expected all-ones control input instead of the requested `[5.0, 15.0]`; the same test passed on exact fixed PR head `0ffc82225d6125dcb5c5b5acfb9be9fd712ef949` (`1 passed in 0.65s`).
- New artifact `14648082079`; GitHub-reported SHA-256 `fe4a8754125ca750cc7080f631c6455f417cde9021cb82ebdd65190cdfd75218`. This newest archive was not locally downloaded and rehashed in this update; prior four Dymos independent-reproducer repeats have their own recorded local integrity checks.
- No-inference preflight [44771791808](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44771791808), job `136411069190`: **success**. Dymos packet/provenance/license/independence/exposure review tests: **6 passed**. The readiness report remains blocked with 13 global blockers, one accepted case/project (Dishka #435), `ready_for_inference=false`, and `inference_authorized=false`. All other candidate reproduction jobs were skipped in this preflight.
- Research Validation [44771791988](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44771791988), job `136411075528`: **success**, `469 passed, 6 skipped, 56 subtests passed`.
- Implementation unit-test workflow [44771792053](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44771792053): **success**.

These are no-inference technical/contract checks. They do not approve semantic gold/tier sufficiency, close the bounded license scope or exact pinned dataset-card license gate, create a final case record, or constitute final case acceptance. No model weights were loaded; no inference, fine-tuning, or training was performed or authorized.


## Superseding project-lead source-aware technical gold and evidence-tier decision — 20 November 2026

The project lead explicitly **APPROVED** the technical gold mechanism and tier decisions after reviewing the exact pinned source chain and reproduction evidence. The approval was stated as: “Onaylıyorum ama projenin ilerleyişini bozmazsa.” This qualification is recorded as a requirement to preserve the existing staged project gates; recording the technical adjudication does not bypass any gate or authorize model execution.

- Decision record: `research_candidates/evidence_abstention/dymos_1166/PROJECT_LEAD_GOLD_AND_EVIDENCE_TIERS_DECISION_DYMOS_1166_2026-11-20.md`
- Decision-record SHA-256: `9ae99f74020479bdfc7d7b686b7dd7d7b3ca5afa24c827b08e4cc5108ccfd392`
- Approved gold: `Phase.add_control(val=...)` forwards the caller value to `set_control_options`; the value is stored and passed through `TranscriptionBase` to `ControlInterpComp`; the buggy polynomial-control input is nevertheless initialized with `np.ones(input_shape)`, discarding the supplied default.
- E3: **ABSTAIN** — issue narrative only.
- E2: **ABSTAIN** — issue narrative plus independent reproduction/output, but no implementation-path evidence.
- E1: **ANSWER** — adds the active pinned API-to-component source chain and the decisive all-ones initialization.
- Method: Dishka-equivalent v0.2 exploratory source-aware single project-lead human adjudicator. ChatGPT is advisory only; full researcher source/reproduction exposure remains disclosed; no blind or inter-rater reliability claim is made.

This closes only the source-aware technical gold/tier adjudication gate. The bounded dependency/source/dataset documentary license-scope acknowledgement and exact pinned dataset-card license verification remain open. The schema-conformant case record, fail-closed registry validation, and separate final case YES/NO remain required. **Final case acceptance remains not_accepted; inference remains unauthorized.**


## Current-head adjudication and no-inference verification — 20 November 2026

The project-lead source-aware technical gold/tier decision is recorded and approved (decision-record SHA-256 `9ae99f74020479bdfc7d7b686b7dd7d7b3ca5afa24c827b08e4cc5108ccfd392`). The approval closes the source-aware gold/E1/E2/E3 gate only; final case acceptance remains `not_accepted`.

On branch head `98df08d0ddc4c8972ee653016bf6ac9f2912e560`:

- No-inference preflight [44777046085](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44777046085), job `136429516755`: **success**; Dymos decision/packet/independence/license contract tests **8 passed**. Readiness: 1 accepted case/project (Dishka #435), 13 global blockers, `ready_for_inference=false`, `inference_authorized=false`.
- Research Validation [44777046162](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44777046162), job `136429519129`: **success**, **471 passed, 6 skipped, 56 subtests passed**.
- Dymos independent reproducer [44777046281](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44777046281), job `136429516642`: **success**. The pinned buggy base produced the required executed mismatch; the identical reproducer passed on fixed PR head `0ffc82225d6125dcb5c5b5acfb9be9fd712ef949` (`1 passed in 0.65s`).
- Artifact `14649973489`, SHA-256 `82aba14dbd3ffcc975989a8f3984712a0b4b3a5b89458f7d142fe1dfea4ed16b`: downloaded locally; outer SHA-256 matched GitHub, ZIP CRC PASS, and `SHA256SUMS.txt` **15/15 PASS**.
- Implementation uncertainty unit tests and Qwen adapter CPU tests succeeded; the runner smoke test also succeeded.

No model weights were loaded; no inference, fine-tuning, or training occurred. Dymos remains a Stage 3 candidate. The bounded documentary license-scope acknowledgement, exact pinned dataset-card license verification, schema-conformant case record, fail-closed registry validation, and separate final YES/NO acceptance decision remain required.


## Superseding exact pinned dataset-card license and bounded scope proposal — 20 November 2026

The dataset-card license for the exact pinned revision is now authenticated from the immutable Hub commit page:

- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`.
- Exact revision page: https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified/commit/fb9aa226b2ce37c708ea7732e7b980abacdadb67
- License displayed on that exact revision: **CC-BY-4.0**.
- The selected row `openmdao__dymos-1165` has row-level `license=Apache-2.0`, which describes the Dymos source repository for that row, not the dataset repository's overall license.

The bounded project-lead acknowledgement proposal is stored at `research_candidates/evidence_abstention/dymos_1166/PROJECT_LEAD_BOUNDED_LICENSE_SCOPE_ACKNOWLEDGEMENT_PROPOSAL_DYMOS_1166_2026-11-20.md` (SHA-256 `844e36ea92bb947f990ecc2ec564e9ea5c718c380e1c6405aaf6ff46423530b2`). It inventories the exact current CI artifacts, including the full upstream PR patch and captured source snapshots, one dataset row, and the NumPy/SciPy bundled notices. It expressly excludes the full dataset/repository, binary wheel redistribution and commercial use. The project's repository and CI artifacts are not private-only.

The exact pinned dataset-card verification is closed. **Project-lead scope acknowledgement remains pending**, and no legal clearance is claimed. Final case acceptance remains `not_accepted`; inference remains unauthorized.


## Latest license-scope verification and CI audit — 20 November 2026

The exact pinned dataset-card license is authenticated at the immutable dataset revision `fb9aa226b2ce37c708ea7732e7b980abacdadb67`: the Hub commit page displays **CC-BY-4.0**. The selected row's `license` field is **Apache-2.0** for its upstream `OpenMDAO/dymos` source repository; these are separate scopes.

The bounded project-lead scope proposal is stored at `research_candidates/evidence_abstention/dymos_1166/PROJECT_LEAD_BOUNDED_LICENSE_SCOPE_ACKNOWLEDGEMENT_PROPOSAL_DYMOS_1166_2026-11-20.md`, SHA-256 `e8185465d8466512d3de08e622115a9442450f5665fbde4857facddc76341405`. It expressly inventories the current CI artifact contents (including the full upstream PR patch and source snapshots) and the 14-package runtime, with separate NumPy/SciPy bundled notices. The project-lead acknowledgement remains **pending**; this is not legal clearance.

Current branch-head verification (`66ae020c498bd7a0e0159f76b523a68c9c9a31ad`):

- No-inference preflight [44779507956](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44779507956), job `136438118615`: success; Dymos review-contract tests **8 passed**; 13 global blockers remain; inference is not authorized.
- Research Validation [44779508142](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44779508142), job `136438155861`: success; **471 passed, 6 skipped, 56 subtests passed**.
- Independent reproducer [44779508337](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44779508337), job `136438121470`: success; exact buggy-base failure / fixed-revision pass. Artifact `14651026003`, SHA-256 `84f884f0ff358c5811221099983bb2531ded7dfe501e1a042da7765ab298aa25`; downloaded locally with matching outer SHA-256, ZIP CRC PASS, 15/15 internal hashes PASS.

Dymos remains a Stage 3 candidate, not an accepted case. No model weights were loaded and no inference, fine-tuning, or training was performed.


## Latest independent-reproducer and artifact-integrity repeat — 21 November 2026

The independent issue-level public-API reproducer was rerun on the current research branch:
- Workflow run: `44903822528`; job `136845091011` — **success**.
- Exact buggy base: `3efd1035c3bf62890034eb9e07de543f3d117867` produced the expected all-ones polynomial-control input `[[1.0], [1.0]]` instead of the requested `[[5.0], [15.0]]`; the defect-specific test executed and failed as required.
- Exact fixed PR head: `0ffc82225d6125dcb5c5b5acfb9be9fd712ef949`; the identical reproducer passed (`1 passed`).
- Artifact: `14707022685`; GitHub SHA-256 `698e2f6b9d37522fd276f58ce57d85934bb0e8df16cd978284c3e79ef3a346dc`.
- Independently downloaded archive SHA-256 exactly matched GitHub. ZIP CRC passed and internal SHA256SUMS verified **15/15** files.

This repeats the independent reproducer result and strengthens the artifact trail. It does not alter the approved G1/E1/E2/E3 decisions or the bounded documentary scope acknowledgement. The case record remains structurally complete and proposed, but the separate final project-lead YES/NO acceptance decision remains pending. Dymos remains outside the accepted registry; model loading/inference/fine-tuning/training remain unauthorized.
