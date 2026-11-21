# CS-SI/eodag issue #1530 — candidate review

**Cohort rank:** 16 of 96 primary candidates  
**Dataset instance:** `cs-si__eodag-1536` (exact pinned Parquet row authenticated)  
**Issue:** https://github.com/CS-SI/eodag/issues/1530  
**Fix PR:** https://github.com/CS-SI/eodag/pull/1536  
**Review status:** Stage 2 technical reproduction and project-lead source-aware gold/tier adjudication passed. The project lead self-declared no prior pipeline/debug use of this candidate. Bounded dependency-license scope acknowledgement and final acceptance remain pending. Not an accepted case.

## 1. Defect contract

Issue #1530 reports that the default user configuration template contains two top-level YAML mapping entries both named `geodes`. The first block is the public Geodes provider and contains an `apikey` credential. The second is the Geodes S3 provider and contains AWS credentials. With ordinary YAML mapping semantics, the later duplicate key replaces the earlier mapping. The resulting configuration no longer contains the public Geodes credential shape and can make the public provider request AWS credentials.

PR #1536 renames the second key to `geodes_s3`. The issue-specific contract is therefore: parsing the template must preserve both provider configurations under distinct keys, with `geodes.auth.credentials.apikey` and `geodes_s3.auth.credentials.aws_access_key_id/aws_secret_access_key/aws_session_token`.

The PR also changes provider initialization to include `StacListAssets` and modifies several provider tests for that additional feature. This is mixed scope. The minimal reproducer isolates only the duplicate-key defect; the dataset FAIL_TO_PASS selectors must still be inspected to determine whether they isolate #1530 or combine the unrelated #1517 feature.

## 2. Pinned source identity

- Repository: `CS-SI/eodag`
- Buggy base: `b7cc06e19025e5bbf14e28a0975f1749e21e9be3`
- Fixed PR head: `312966a46513a082333d46cd7212bdce36aaf769`
- Merge commit: `697b5c851f7f15ccb48c9e749061314118f26e3b`
- Issue #1530 created: `2025-02-20T11:38:36Z`
- PR #1536 created: `2025-02-21T10:04:30Z`
- PR #1536 merged: `2025-02-21T12:28:31Z`
- Exact-base YAML template Git blob: `0d6c9e24a3294dd12c2b09e844ef3990b01a0a5b`
- Fixed YAML template Git blob: `5221bd2d052bdd60363367d3be51044e1cc95c76`
- Exact-base root LICENSE Git blob: `1a9893b43e8e6d46ff5cda60ab6562850b7f78ff`
- Exact-base NOTICE Git blob: `9f763bc3c2f90854b8209ce60e23c8fc03c6ec7e`
- Exact-base setup.cfg Git blob: `fdf8cc087fe720c835e0bfceeeabd1c66aed47a4`

The workflow will authenticate the dataset row timestamp against the exact PR resource before any claim is made about timestamp agreement.

## 3. Narrow source and dependency license screen

- Exact-base root license: Apache-2.0.
- Exact-base NOTICE identifies PyYAML as MIT.
- Exact-base setup.cfg declares PyYAML as a runtime dependency.
- The minimal reproducer reads the exact upstream YAML resource and imports only PyYAML; it does not import EODAG, install the full geospatial stack, call external services, or use remote test fixtures.
- Pinned minimal test dependency: PyYAML 6.0.2. The package's release page identifies MIT licensing; the upstream NOTICE independently records PyYAML under MIT.
- The workflow will record installed distribution metadata and verify the exact version before executing the source reproducer.

This is a documentary screen for the minimal YAML reproducer only. It is not legal advice or blanket clearance for the full EODAG dependency graph, optional providers, external data, or redistribution.

## 4. Independent reproducer

Path: `research_candidates/evidence_abstention/reproduction/eodag_issue_1530/test_issue_1530.py`

The same test loads `eodag/resources/user_conf_template.yml` at the exact buggy base and fixed revision. It requires:
- both `geodes` and `geodes_s3` keys to exist;
- public `geodes` to contain only the `apikey` credential field;
- `geodes_s3` to contain the three AWS credential fields.

Expected base failure: missing `geodes_s3` because the second duplicate `geodes` mapping overwrites the first. Expected fixed pass: both distinct mappings are preserved.

This is an issue-specific source reproducer, not a substitute for the dataset FAIL_TO_PASS selectors.

## 5. Independence and exposure

- The v0.2 primary cohort contains one row for CS-SI/eodag; this repository can contribute at most one accepted case.
- Issue #1530 and PR #1536 were created after the September 2024 public release of the pinned Qwen2.5-3B-Instruct model. This reduces the likelihood that this exact public issue/patch was present in the released weights, but does not establish complete training-data provenance.
- The student researcher has reviewed the issue and patch during candidate screening. This exposure must be recorded; perfect blinding must not be claimed.
- Related issue-family review remains required before final acceptance.

## 6. Stage 2 result — 2026-11-17

The issue-specific YAML reproducer and both exact dataset selectors were run on the pinned buggy base and fixed revision in workflow run [44117944004](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44117944004), job `134161227052`.

- Exact Parquet instance: `cs-si__eodag-1536`
- Row `created_at`: `2025-02-21 10:04:30`, matching PR #1536 creation time.
- Canonical row SHA-256: `35f612f1b6524f37cca6766f25a0637bc5d5740da9695427dba556354ce61a47`
- Selector count: 2.
- Buggy base: both selectors executed and failed as expected (`selector_contracts=2/2 expectation=base-fail`). The second test raised `UnsupportedProvider: geodes_s3`; the first asserted a difference in provider sortables.
- Fixed revision: the same two selectors passed (`selector_contracts=2/2 expectation=fixed-pass`).
- Test-only patch scope: `tests/units/test_core.py` only; workflow scope audit reports `production_code_changed=false`.
- Artifact ID: `14344421574`; ZIP SHA-256: `0d9b4cf38b22cf094d080d6f8a87b1ff6373c9ab3a7d8ece68cc003b35964b33`.
- Artifact SHA256SUMS: 22 entries independently checked; 0 mismatches.
- Focused test environment: Python 3.11.9; 52 installed distributions recorded in the license metadata inventory; `pip check` passed. The installed package inventory is evidence for review, not blanket legal clearance.

The two exact selectors are directly related to `geodes_s3` provider registration/sortables. The PR also touches a separate `StacListAssets` feature, but that production change is not in the applied test-only patch and neither of the two selectors is a StacListAssets test.

## 7. Current decision and remaining gates

Issue/patch alignment for the duplicate YAML-key defect: strong.  
Minimal YAML reproducer: base-fail/fixed-pass.  
Exact dataset selectors: 2/2 base-fail and 2/2 fixed-pass.  
Focused dependency environment and license metadata inventory: recorded; project-lead scope signoff remains pending.  
Researcher source exposure: partial screening exposure recorded; no blinding claim.  
Related issue-family / independence review: pending.  
Gold mechanism, alternatives and nested E1/E2/E3 evidence: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading/inference authorization: false.

## Superseding Stage 2 and scope addendum — 20 November 2026

The later current-branch reproduction matrix completed EODAG #1530 successfully:
- Workflow run: 44331092872; job: 134895967977 — success.
- Artifact: 14440370494; GitHub-reported SHA-256: 6a732364873d12d78d407f41aa671cc56851f67b58492c4762ff33e36a59a437.
- The same independent duplicate-key YAML reproducer failed on the exact buggy base and passed on the exact fixed revision.
- The two exact frozen dataset selectors again failed on the test-only patched buggy base and passed on the exact fixed revision.

This repeat confirms the earlier Stage 2 pass; it is not another case. The independent reproducer isolates the actual defect: in the pinned base YAML, the two top-level provider blocks both use the key geodes, so normal YAML parsing loses the first mapping; the fix preserves the public provider under geodes and gives the S3 provider the separate geodes_s3 key.

**Scope limitation retained:** PR #1536 also contains a separate StacListAssets feature. The exact dataset selectors and minimal reproducer used for this case concern the geodes/geodes_s3 configuration defect, not the separate feature. Keep these scopes separate in the gold statement and evidence packets.

**Current disposition:** Stage 2 technical reproduction PASS; candidate remains not accepted. Related issue/lineage review, project-lead source-aware gold/E1-E2-E3 decision, truthful candidate-specific prior pipeline/debug exposure declaration, bounded dependency/source/dataset license-scope acknowledgement, proposed case record and fail-closed registry validation remain open. The earlier scope review's 52-package inventory is evidence of captured metadata, not legal clearance.

## Superseding issue-family and frozen-selector scope correction — 20 November 2026

A direct comparison of the exact upstream PR #1536 file list and the linked issue #1517 requires a more precise description than the earlier mixed-scope note.

- PR #1536's upstream description says **“Fixes #1530”**. Its three changed files are `eodag/config.py` (adds `StacListAssets` to a search-type list), `eodag/resources/user_conf_template.yml` (renames the second duplicate `geodes` key to `geodes_s3`), and `tests/units/test_core.py` (adds `geodes_s3` to provider/product-type/sortables expectations).
- Issue #1517 is a distinct report: `fetch_product_types_list` reaches `default_discovery_conf["result_type"]` and raises `KeyError: 'result_type'` when fetching Geodes S3 product types.
- The exact frozen selector `test_list_product_types_for_provider_ok` calls `list_product_types(provider=..., fetch_providers=False)`; it does not enter the issue #1517 remote `fetch_product_types_list` path. The other frozen selector `test_available_sortables` checks the registered provider's local sortable metadata.
- The reproduction artifact records the base-side failures as missing/unsupported `geodes_s3` and missing expected sortable metadata. These are consistent with the duplicate-key configuration preventing the default `geodes_s3` user configuration entry from being loaded. The independent minimal YAML reproducer directly isolates the core #1530 defect by showing that the later duplicate `geodes` mapping overwrites the earlier public Geodes mapping.

Therefore, retain #1517 as a **related but distinct provider-discovery issue**, not as a second EODAG case and not as part of #1530's gold mechanism. Exclude the separate `StacListAssets` code path from the #1530 gold statement. Keep the existing two frozen selectors only with the above bounded interpretation; the independent YAML reproducer is direct corroboration, not a replacement for them.

## Project-lead selection decision

## Project-lead first-batch selection — 20 November 2026

The student project lead explicitly accepted EODAG #1530 as one of the strong first-batch candidates to continue through v0.2 Stage 3 case evaluation, applying the unchanged Dishka-equivalent criteria.

This is candidate-selection approval only. It does **not** approve the proposed EODAG gold mechanism or E1/E2/E3 tier membership; those remain for a separate source-aware project-lead decision. The bounded 52-distribution dependency/native-notice scope acknowledgement, candidate-specific prior pipeline/debug exposure declaration, related issue/lineage review, complete case record, fail-closed registry validation and separate final case YES/NO remain pending.

The #1517 result_type issue remains recorded as related but distinct; it is not folded into #1530's gold. This candidate remains not accepted as a final case. No model load, inference, fine-tuning or training is authorized.


## Project-lead source-aware gold/tier decision — 21 November 2026

The project lead approved the duplicate-key technical gold and the proposed E1/E2/E3 dispositions:
- **E3 — ABSTAIN**
- **E2 — ABSTAIN**
- **E1 — ANSWER**

The E2 packet demonstrates the duplicate-key parse result in the exact pinned template but does not include the in-repository fixture/loading path; provider-registration and configuration-override alternatives therefore remain. E1 adds the test-fixture source excerpt showing the packaged template is loaded by `yaml.safe_load` and iterated to generate provider configuration. The approved surviving-mechanism sets are E3={G1,A1,A2,A3}, E2={G1,A2,A3}, E1={G1}.

Decision record: [PROJECT_LEAD_GOLD_AND_EVIDENCE_TIERS_DECISION_EODAG_1530_2026-11-21.md](eodag_1530/PROJECT_LEAD_GOLD_AND_EVIDENCE_TIERS_DECISION_EODAG_1530_2026-11-21.md)  
SHA-256: `b48db64273f6d552c12ef82e5b9d75992f85e266e987491feb9cf7db23e8e52e`

This is a source-aware, single-project-lead exploratory adjudication. Full researcher source exposure is disclosed; no blinded or inter-rater reliability claim is made.

**Still open:** candidate-specific prior pipeline/debug exposure declaration; bounded documentary license-scope acknowledgement; complete schema-conformant case record; fail-closed registry validation; formal accepted-registry update. EODAG is approved to continue through these gates but is not yet inserted into the accepted registry. No model loading, inference, fine-tuning or training is authorized.


## Project-lead prior pipeline/debug exposure declaration — 21 November 2026

The project lead answered **none** to the candidate-specific question: before prospective candidate validation, EODAG #1530 had not been used to solve, debug, calibrate, or repair the shared research pipeline, test runner, dataset selector, test oracle, or prompt.

This is a project-lead self-declaration, not independently verified telemetry. It does not imply source blinding. Full researcher source exposure remains disclosed, and the case was reviewed source-aware during candidate screening and gold/tier adjudication.

Decision record: [PROJECT_LEAD_PRIOR_PIPELINE_DEBUG_EXPOSURE_DECLARATION_EODAG_1530_2026-11-21.md](eodag_1530/PROJECT_LEAD_PRIOR_PIPELINE_DEBUG_EXPOSURE_DECLARATION_EODAG_1530_2026-11-21.md)  
SHA-256: `5a51adf26ae3597e398d5aad5494a55e5a553fe4a787a79de4bc8d3afb89ae38`

**Remaining:** bounded documentary license-scope acknowledgement; complete schema-conformant case record; fail-closed registry validation; separate project-lead final case YES/NO. EODAG remains outside the accepted registry. No model loading, inference, fine-tuning or training is authorized.


## Project-lead bounded documentary license-scope acknowledgement — 21 November 2026

The project lead acknowledged the bounded documentary scope proposal for one EODAG defect, one immutable dataset row, the pinned CPU-only reproduction, minimal source excerpts, immutable upstream links, attribution and applicable NOTICE preservation.

The acknowledgement excludes redistribution of the complete dataset, complete EODAG repository, installed wheels/binaries/native libraries or the complete dependency environment; it grants no blanket permission for optional extras, third-party provider data or commercial use. The dataset's CC-BY-4.0 license remains distinct from EODAG's Apache-2.0 source license.

Decision record: [PROJECT_LEAD_BOUNDED_LICENSE_SCOPE_ACKNOWLEDGEMENT_EODAG_1530_2026-11-21.md](eodag_1530/PROJECT_LEAD_BOUNDED_LICENSE_SCOPE_ACKNOWLEDGEMENT_EODAG_1530_2026-11-21.md)  
SHA-256: `6513f066df7130173deb8ba9316ab24ed4cded73b25487e88c9013bff01a8af6`

This is not legal advice, formal legal review, legal clearance, SPDX certification or a complete native/bundled dependency audit. The 52-package metadata inventory is not legal clearance.

**Remaining:** complete schema-conformant proposed case record and fail-closed registry validation, followed by a separate final project-lead YES/NO. EODAG remains outside the accepted registry. No model loading, inference, fine-tuning or training is authorized.


## Proposed v0.2 case record prepared — 21 November 2026

A complete candidate record has been prepared at [SWE_REBENCH_V2_EODAG_1530_CASE_ACCEPTANCE_PROPOSED_V0_2.json](eodag_1530/SWE_REBENCH_V2_EODAG_1530_CASE_ACCEPTANCE_PROPOSED_V0_2.json). It records the pinned dataset row and source revisions, technical reproduction, project-lead-approved gold and E1/E2/E3 survivor sets, full researcher source exposure, the self-declared absence of prior pipeline/debug use, and the bounded documentary license-scope acknowledgement.

The record's `acceptance_decision` is **proposed** and `final_acceptance.status` is **pending**. EODAG is not inserted into the accepted registry. Latest-head CI must run the structural case validator and fail-closed registry validation. No model execution is authorized.


## Superseding case-record validation result — 21 November 2026

The proposed EODAG record passed the v0.2 case-acceptance schema and deterministic cross-field validator. The no-inference preflight job on commit `f143be00ee6634a9c0838379ac88c93cc0674ded` succeeded: run [44894847180](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44894847180), job `136818188559`; the EODAG review-contract suite passed **5/5**. The same job confirmed the existing accepted registry is structurally valid and unchanged at **1 case / 1 upstream project (Dishka only)**.

Research Validation also succeeded on the same branch head: run [44894847259](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44894847259), job `136818190862`: **477 passed, 6 skipped, 56 subtests passed**.

The proposed EODAG case record remains `acceptance_decision=proposed`, `final_acceptance.status=pending`, and is not in the registry. **The only remaining EODAG-specific gate is the separate project-lead final YES/NO.** The overall study still has 13 readiness blockers; model loading, inference, fine-tuning and training remain unauthorized.
