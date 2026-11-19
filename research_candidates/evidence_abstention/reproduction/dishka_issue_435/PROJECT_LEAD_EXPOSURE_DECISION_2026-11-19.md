# Dishka #435 — project-lead exposure decision

**Decision date:** 19 November 2026  
**Candidate:** `reagento__dishka-436`  
**Decision source:** explicit project-lead declaration in the project conversation  
**Status:** excluded from the v0.2 model-evaluation sample

## 1. Project-lead declaration

The project lead declared:

`prior_pipeline_debug_exposure = some`

Specifically, Dishka #435 had prior pipeline/debug/test-oracle exposure before its prospective case-validation assignment. This is a separate variable from the already disclosed `researcher_source_exposure = full`.

No attempt is made to reinterpret `some` as `none`.

## 2. Protocol application

The active v0.2 exploratory case-acceptance schema and validator require:

`prior_pipeline_debug_exposure = none`

Because the factual declaration is `some`, Dishka is not eligible for inclusion in the model-evaluation sample under the current protocol.

**Disposition:** `excluded_prior_pipeline_debug_exposure`

- Do not prepare or submit a proposed acceptance record for the model-evaluation registry.
- Do not weaken or patch the exposure validator.
- Do not add Dishka to the accepted-case registry.
- Do not count it toward the primary 15-project target or the one-case feasibility minimum.
- Preserve the original candidate row, pinned source revisions, reproduction artifacts, hashes, Stage 2 technical pass, and Stage 3 technical adjudication as engineering/reproducibility evidence.
- Retain the full researcher source exposure and single-human-adjudicator limitations in the technical record.

## 3. What this decision does and does not mean

This is an eligibility exclusion, not a finding that the defect reproduction failed. The Stage 2 result remains technically passed, and the existing Stage 3 technical adjudication record remains part of the engineering history.

The exclusion does not authorize model loading, inference, fine-tuning, or training.

## 4. Next candidate

The next candidate in the previously approved order is **NumPyro #1916 / PR #1918**. It has a passed exact Stage 2 reproduction and a constructed nested E1/E2/E3 packet set. The remaining Stage 3 semantic, independence/exposure, license-scope, and final acceptance gates remain open. Structural packet validation is tracked separately and must not be treated as semantic approval.

## 5. Audit integrity

This record captures the project lead's stated classification. It is not represented as a cryptographic signature or as a decision by Hasan, Batuhan, a legal adviser, or an external auditor.
