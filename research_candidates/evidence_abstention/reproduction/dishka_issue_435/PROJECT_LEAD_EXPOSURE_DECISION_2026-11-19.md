# Dishka #435 — project-lead exposure decision and correction

**Record date:** 19 November 2026  
**Candidate:** `reagento__dishka-436`  
**Decision source:** direct project-lead declarations in the project conversation  
**Current value:** `prior_pipeline_debug_exposure = none`  
**Current study disposition:** eligible to continue formal v0.2 case-acceptance checks; **not accepted**

## 1. Superseding factual declaration

The project lead has now confirmed:

`prior_pipeline_debug_exposure = none`

The project lead's answer to the specific question was:

> Hayır — Prospektif doğrulama öncesinde pipeline/debug amacıyla kullanılmadı.

This means Dishka was not used before its prospective case-validation assignment to debug the generic runner/pipeline or troubleshoot the target test oracle. The value `none` applies only to prior pipeline/debug/test-oracle exposure.

It does **not** change the separate, already disclosed value:

`researcher_source_exposure = full`

The project lead has reviewed the issue, PR, patch and source materials. No researcher blinding is claimed.

## 2. Correction history and audit trail

An earlier answer in this conversation recorded `prior_pipeline_debug_exposure = some`. The project lead later explained that the prior question had not yet been read carefully and clarified that the correct answer is the explicit NO above.

The earlier `some` entry is therefore **superseded and not the current factual classification**. It is retained here for audit transparency, not treated as evidence that prior pipeline/debug exposure occurred. This correction does not alter the underlying reproduction artifacts, frozen selectors, hashes or protocol.

## 3. Protocol application

The active v0.2 eligibility rule requires:

`prior_pipeline_debug_exposure = none`

The corrected project-lead declaration satisfies this particular eligibility gate. It does not automatically accept the case or close the remaining provenance, license, schema, registry or project-wide readiness gates.

**Current disposition:** `eligible_pending_other_case_gates`

- Continue the formal Dishka v0.2 case-acceptance record.
- Preserve `researcher_source_exposure = full` and single-human-adjudicator limitations.
- Do not describe the project lead as blinded.
- Do not mark the case accepted until the complete proposed record, independent evidence checks, schema validation, fail-closed registry validation and separate final project-lead decision are complete.
- No model loading, inference, fine-tuning or training is authorized by this exposure correction.

## 4. Technical evidence remains unchanged

- Buggy base: `8718d5af93f9e48bc2506c64827663fdccc5ad89`
- Fixed revision: `b1eae11734e64551d7b101195f27cb6870e1c364`
- Latest independently archive-verified repeat: run `44537219541`, job `135605947696`, artifact `14536192821`.
- ZIP SHA-256: `b8dfe9e89e44f246fbf8d093ba31dc01c74c6dc167434555405693d6a0f1df52`; CRC PASS; 32/32 internal hashes PASS.
- Independent issue reproducer: buggy-base failure / fixed-revision pass.
- Frozen dataset selectors: 8/8 defect-related failures on buggy base and 8/8 passes on fixed revision.

These are technical reproduction findings, not proof of global readiness or final case acceptance.

## 5. Next required steps

1. Project-lead decision on the bounded documentary license-screen scope described in `DISHKA_435_V02_CANDIDATE_GATE_ASSESSMENT_2026-11-19.md`. This is not a legal opinion or blanket redistribution approval.
2. Complete the full proposed v0.2 case JSON with verified artifact references, provenance, independence, exposure, license and E1/E2/E3 fields.
3. Validate the proposed record against the active Draft 2020-12 schema and fail-closed registry validator.
4. Resolve every structural or evidentiary blocker without relaxing any gate.
5. Present a separate short final YES/NO project-lead case-acceptance decision.
6. Only after a YES and successful validators may the case be marked accepted and inserted into the registry.

## 6. Limitations and authority

This record captures the project lead's factual declaration and its correction history. It is not a cryptographic signature, a statement by another reviewer, legal clearance, or external audit.
