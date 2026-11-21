# Project-lead final acceptance decision — EODAG #1530

**Decision date:** 2026-11-21  
**Decision timestamp:** 2026-11-21T13:36:50+03:00 (Europe/Istanbul)  
**Decision maker:** student project lead  
**Candidate:** CS-SI/eodag issue #1530 / PR #1536  
**Dataset row:** `cs-si__eodag-1536`  
**Case ID:** `SRV2E-EODAG_1530`

## Final decision

**YES — accept EODAG #1530 into the v0.2 exploratory/feasibility accepted-case registry.**

This is a separate final case-acceptance decision, following the earlier gold/evidence-tier adjudication, prior pipeline/debug exposure self-declaration, bounded documentary license-scope acknowledgement, proposed case-record construction, and successful fail-closed structural/registry validation.

## Basis recorded

- Stage 2 technical reproduction passed on the exact buggy base and fixed PR revision; the independent YAML reproducer and two issue-aligned frozen dataset selectors were executed as base-fail/fixed-pass.
- Project-lead-approved source-aware technical gold: the duplicated top-level `geodes` key in the packaged YAML template is parsed by `yaml.safe_load` such that the later AWS credential mapping overwrites the earlier public API-key mapping, with no separate `geodes_s3` mapping.
- Project-lead-approved evidence-tier decisions: E3 **ABSTAIN**, E2 **ABSTAIN**, E1 **ANSWER**. The adjudication was single-project-lead and source-aware; full researcher source exposure is disclosed. No independent blinded Panel A/Panel B or inter-rater reliability claim is made.
- The project lead self-declared `prior_pipeline_debug_exposure = none`; full source exposure remains separately disclosed.
- The project lead acknowledged the bounded documentary license scope. That acknowledgement is not legal advice, formal legal review, legal clearance, SPDX certification, a complete native/bundled dependency audit, or blanket redistribution permission.
- The proposed v0.2 case record passed the schema and deterministic cross-field checks. The fail-closed validator confirmed the existing registry was structurally valid before this addition.

## Acceptance boundaries

This decision accepts the case **only** into the v0.2 exploratory/feasibility registry. It is not acceptance into a confirmatory sample, external audit, independent adjudication, legal clearance, or proof that training-data contamination is absent.

The case remains subject to the study's disclosed design and sample limitations. One accepted case does not satisfy the preferred 15-project analysis threshold.

**Model loading:** not authorized.  
**Model inference:** not authorized.  
**Fine-tuning or training:** not authorized.  
**Registry scope:** v0.2 exploratory/feasibility only.

The study-wide readiness report remains blocked by 13 global prerequisites. This case-level acceptance does not override those blockers or the inference gate.
