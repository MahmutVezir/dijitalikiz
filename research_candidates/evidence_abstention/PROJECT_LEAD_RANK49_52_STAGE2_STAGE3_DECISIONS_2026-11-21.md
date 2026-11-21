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
