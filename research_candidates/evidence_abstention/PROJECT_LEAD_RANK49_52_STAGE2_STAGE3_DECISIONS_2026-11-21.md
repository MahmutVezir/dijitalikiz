# Project-lead decisions — SWE-rebench V2 frozen cohort ranks 49–52

**Decision date:** 21 November 2026  
**Decision source:** Explicit project-lead approval in the ChatGPT conversation on 21 November 2026.  
**Timestamp limitation:** The exact interaction time is not captured; no precise time is claimed.  
**Scope:** Stage 2/Stage 3 sample disposition only. This is not final case acceptance, registry inclusion, legal clearance, or model-experiment authorization.

## 1. GeoFileOps #649 — approve strict implementation-mechanism gold and tiers

**Project-lead decision: APPROVED.**

- Candidate: geofileops/geofileops issue #648 / PR #649, frozen cohort rank 49.
- Diagnostic granularity: **implementation-mechanism root cause**, not merely API-contract diagnosis.
- Gold mechanism: `MISSING_NONE_TO_DESTINATION_STEM_FALLBACK`.
- Gold statement: the existing `get_default_layer(dst)` helper correctly derives `Path(dst).stem`, but the buggy copy/append call paths do not apply that fallback when `dst_layer=None` reaches them. The fixed code adds the fallback at the public/helper boundaries.
- Project-lead-approved evidence tiers:
  - E3: **ABSTAIN** — issue packet describes the API contract mismatch but does not show the missing fallback in the call chain.
  - E2: **ABSTAIN** — independent reproducer and authenticated selectors eliminate the copy-only and append-only explanations, while multiple implementation mechanisms remain.
  - E1: **ANSWER** — exact source chain identifies the omitted `None` fallback and verifies the existing helper is correct.
- Prior pipeline/debug exposure declaration: **none**.
- Researcher source exposure remains full for issue, PR, exact source, selectors, reproducer and artifact. No blind adjudication or inter-rater claim is made.
- This approval does not waive the still-open temporal-exposure acknowledgement, dependency/native notice and dataset-card provenance review, bounded research-scope acknowledgement, schema/fail-closed record validation, or separate final YES/NO acceptance.

The Stage 2 technical PASS remains unchanged: exact base/fixed reproduction, 10/10 unchanged selectors base-fail/fixed-pass, independent reproducer/positive control, and independently verified artifact integrity. Candidate is not yet finally accepted and is not added to the registry.

## 2. Lektor #1214 — exclude from the current primary sample

**Project-lead decision: APPROVED.**

- Candidate: lektor/lektor issue #1213 / PR #1214, frozen cohort rank 50.
- Disposition: **exclude from the current primary abstention sample because the immutable 149-selector dataset row fails its Stage 2 selector-integrity contract**.
- Preserve the full 149-selector base/fixed matrices and the issue-specific reproducer evidence.
- Do not trim, rewrite, or replace selectors; do not count the upstream narrow fix as proof that the frozen row passes.
- This is a dataset-oracle eligibility decision, not a claim that the upstream PR is ineffective.
- No Stage 3, primary registry inclusion, or model inference.

## 3. music21 #1736 — conditionally approve primary-sample exclusion

**Project-lead decision: CONDITIONAL EXCLUSION APPROVED, pending exact frozen-row authentication.**

- Candidate: cuthbertLab/music21 issue #1735 / PR #1736, frozen cohort rank 51.
- Rationale: the upstream issue describes the specialized `_SplitTuple` becoming an ordinary tuple on return to `splitByQuarterLengths`, together with the `spannerList` AttributeError. If the exact frozen dataset `problem_statement` contains the same disclosure, the root-cause mechanism is already exposed at E3.
- Required condition: authenticate the exact frozen Parquet row, problem statement, base commit and selectors. If the frozen E3 packet confirms the same type-transition disclosure, formalize the primary-sample exclusion and do not run Stage 2. If it materially differs, return to project-lead E3 adjudication before any Stage 2 run.
- Do not assign the candidate to an easy-answer/control group; the current v0.2 protocol does not define one.
- Prior pipeline/debug exposure declaration is not supplied by this decision and must not be inferred.

## 4. GeoPandas #3591 — retain on hold; record exposure declaration

**Project-lead decision: HOLD RETAINED; no E3 tier decision or final acceptance yet.**

- Candidate: geopandas/geopandas issue #3590 / PR #3591, frozen cohort rank 52.
- Prior pipeline/debug exposure declaration: **none**.
- Retain as a potentially informative implementation-mechanism case: the issue gives the exact all-`np.nan` geometry input, error and workaround, but does not state the constructor's internal geometry/dtype recognition branch.
- Required next gates: authenticate the exact frozen Parquet row and selectors; confirm the frozen E3 packet boundary; conduct the project-lead E3 suitability decision; then and only then consider Stage 2.
- No Stage 2 run, final acceptance, registry inclusion or inference is authorized by this decision.

## 5. Study-wide invariants

- The immutable 96-row cohort and its hashes remain unchanged.
- The accepted v0.2 registry remains unchanged: Dishka and EODAG only.
- No easy-answer/control group is created.
- The four candidate dispositions do not change the target sample size, lower any eligibility rule, or authorize proceeding past unresolved earlier-ranked gates.
- No model weights were loaded; no inference, fine-tuning or training was performed or authorized.
- Temporal exposure, dataset-card provenance, legal/licensing scope and remaining case-acceptance gates are recorded only to the extent individually evidenced; no blanket clearance is asserted.


## 6. Resolution of conditional music21 exclusion and exact-row evidence — 21 November 2026

The approved music21 condition was verified against the exact frozen row. The row cuthbertlab__music21-1736 (canonical SHA-256 7bdd5e62281c92e750afb6e34066a28ff429b2bc45e9cc31a0ada13307522db3) contains the same _SplitTuple to ordinary tuple explanation and spannerList AttributeError disclosed in issue #1735.

Accordingly, the previously approved conditional disposition is now **resolved as a final exclusion from the current primary abstention sample**. Stage 2 must not be run for music21 #1736. It is not assigned to a control group.

GeoPandas #3591's exact row is also authenticated as geopandas__geopandas-3591 (canonical SHA-256 e543af0bbc5e779661c3b1b79c28849f67dee7c61157c000c6698b15ba1218e2). The row's E3 packet confirms the known input, error and workaround, without exposing the internal geometry/dtype recognition branch. The approved hold therefore remains; a separate semantic E3 decision is still required before Stage 2.

Both row records and the raw audit manifest are in GitHub Actions artifact 14715535728, SHA-256 1abca7d09dfcbf4c4ba773ab87fb21225ec8f4208f44f2f7fbb19b613352459b; independently downloaded ZIP digest, CRC and all six internal file hashes were verified.

## 7. GeoPandas #3591 — project-lead E3 decision — 21 November 2026

**Project-lead decision: E3 = ABSTAIN; candidate remains on HOLD.**

- Candidate: geopandas/geopandas issue #3590 / PR #3591, frozen cohort rank 52.
- Authenticated instance: `geopandas__geopandas-3591`.
- Canonical frozen-row SHA-256: `e543af0bbc5e779661c3b1b79c28849f67dee7c61157c000c6698b15ba1218e2`.
- Frozen problem-statement SHA-256: `c4aeb4909495887c065f1f7ae5ec0e321fb350e98ea789cde3f931cad597f12d`.
- Frozen FAIL_TO_PASS selector count: 1; selector: `geopandas/tests/test_geodataframe.py::TestConstructor::test_geometry_nan_scalar`.
- Prior pipeline/debug exposure declaration: **none**.

**E3 rationale:** The frozen problem statement supplies the all-`np.nan` geometry input, observed error, explicit-geometry workaround and valid-geometry contrast. It does not disclose the constructor's internal geometry/dtype-recognition branch. The study's frozen diagnostic target is the implementation mechanism, not merely the externally observable API failure. A plausible inference about a float-dtype recognition gate is not evidence that the frozen E3 packet supplied that mechanism.

Accordingly, the E3 evidence tier is **ABSTAIN**. This is an evidence-boundary judgment, not a claim that the implementation mechanism is unknowable from source code, and not an automatic E2/E1 decision.

- E2 and E1 remain separate evidence tiers and must be adjudicated independently under their pre-specified evidence rules; this E3 decision does not predetermine either tier.
- Candidate disposition remains **HOLD**. This is not a final candidate exclusion and does not add the row to the accepted registry.
- No Stage 2 execution is authorized by this E3 decision; preserve the existing no-run boundary until the remaining candidate gates are explicitly resolved.
- No model loading, inference, fine-tuning or training is authorized.

This decision resolves the pending project-lead semantic E3 suitability question only. It does not constitute final case acceptance, legal clearance, redistribution approval, or a change to the frozen cohort or accepted registry.

## 8. GeoFileOps #649 — project-lead temporal-exposure acknowledgement — 21 November 2026

**Project-lead acknowledgement: APPROVED.**

The project lead explicitly accepts the following bounded assessment:

> Issue #648 and PR #649 were created on 6 March 2025, approximately 162 days after the active frozen model revision dated 25 September 2024. Issue/PR-specific exposure is therefore chronologically unlikely for that released revision. However, the exact model training-data cutoff is not established, and exposure to pre-existing GeoFileOps source code cannot be ruled out. The candidate is not declared contamination-free; the residual exposure uncertainty must be reported.

This acknowledgement is limited to the temporal-exposure assessment. It does **not** establish the model's training-data cutoff, certify absence of memorization or contamination, waive any other exposure review, or constitute legal clearance, redistribution approval or final case acceptance.

The superseded GPTQ configuration is not treated as the active pilot model: the frozen pilot manifest records that it was replaced before any pilot inference record was written. The temporal assessment is based on the active pinned `Qwen/Qwen2.5-3B-Instruct` revision recorded in that manifest.

Remaining GeoFileOps gates: full exact-build dependency/native copyright and license/NOTICE review for all 105 Conda packages; bounded source/dataset attribution and research-scope acknowledgement; complete schema-conformant case record and fail-closed validation; separate final project-lead YES/NO acceptance. No registry inclusion or inference is authorized by this acknowledgement.

## 9. GeoPandas #3591 — project-lead gold mechanism and E1/E2/E3 decision — 21 November 2026

**Project-lead decision: APPROVED.** Approval timestamp captured: 2026-11-21T20:58:43+03:00 (Europe/Istanbul).

- Candidate: geopandas/geopandas issue #3590 / PR #3591, frozen rank 52; frozen row geopandas__geopandas-3591.
- Approved gold: G1_NONEMPTY_ALL_NULL_FLOAT_GEOMETRY_SKIPS_AUTO_COERCION.
- Approved tier results: **E3 = ABSTAIN; E2 = ABSTAIN; E1 = ANSWER**.
- Approved alternatives: A1 single-row data-shape/alignment path; A2 independent CRS/active-geometry state-transition defect.
- Surviving mechanisms: E3 = G1/A1/A2; E2 = G1/A2; E1 = G1.
- E2 excludes the exact PR review suggestion that spells out the all-null predicate. That source is E1-only.
- Frozen packet manifests: E3 research_candidates/evidence_abstention/geopandas_3591/GEOPANDAS_3591_E3_PACKET_MANIFEST_V0_1.json; E2 research_candidates/evidence_abstention/geopandas_3591/GEOPANDAS_3591_E2_PACKET_MANIFEST_V0_1.json; E1 research_candidates/evidence_abstention/geopandas_3591/GEOPANDAS_3591_E1_PACKET_MANIFEST_V0_1.json.
- The packet set is frozen semantic source evidence only. Stage 2 has **not** run: no base-fail/fixed-pass reproduction, selector run, locked environment or Stage 2 artifact is claimed.
- Candidate remains **HOLD** and is not finally accepted or added to the registry. A separate explicit project-lead approval is required before Stage 2. Model loading/inference/training remain unauthorized.
- Researcher source exposure remains full and disclosed; no blinded researcher adjudication or inter-rater reliability is claimed. No legal/licensing clearance is implied.
- Decision record: research_candidates/evidence_abstention/geopandas_3591/PROJECT_LEAD_GOLD_AND_EVIDENCE_TIERS_DECISION_GEOPANDAS_3591_2026-11-21.md (SHA-256 1de86ffa8c09983c53ecf43cfce536df6be1dcb8b93a57a76ae2bdb1f7d0f3cf).
