# GeoFileOps #649 — project-lead decision attestation

**Decision date:** 21 November 2026  
**Decision maker:** student project lead  
**Decision source:** explicit project-lead approvals in the conversation on 21 November 2026.

## Gold and evidence tiers

- Diagnostic target frozen as implementation-mechanism root cause, not merely API-contract diagnosis.
- Gold: `G1_MISSING_NONE_TO_DESTINATION_STEM_FALLBACK`.
- E3: `ABSTAIN`; E2: `ABSTAIN`; E1: `ANSWER`.
- Rationale: the issue states the API-contract mismatch but not the internal missing fallback; E2 eliminates copy-only and append-only explanations while multiple mechanisms remain; E1 source shows the existing helper is correct and the buggy path does not apply it.
- Project-lead prior pipeline/debug exposure declaration: `none`.

## Temporal exposure

Approved bounded assessment: issue/PR #648/#649 dates postdate the active frozen model revision by approximately 162 days, making issue/PR-specific exposure chronologically unlikely. Exact model training-data cutoff and exposure to pre-existing GeoFileOps source code remain unknown. The candidate is not declared contamination-free.

## Bounded research scope

Approved limited use of the exact buggy/fixed source revisions, five PR changed paths, one frozen dataset row and revision, exact 105-package Conda lock, ten frozen selectors, independent reproducer and named evidence artifacts. Redistribution of Conda binaries or the complete environment, out-of-scope versions/integrations, dataset redistribution beyond its license and attribution, model weight downloads/loading, inference, fine-tuning and training remain excluded.

## Decision boundary

These are project-lead decisions for gold/tier adjudication, exposure declaration and bounded documentary research scope. They are not the separate final case acceptance decision, legal advice, legal clearance, a blanket license compatibility finding, or model-inference authorization. The case remains `proposed` pending fail-closed validation and a separate final YES/NO decision.

**Timestamp limitation:** exact interaction times were not captured. This attestation deliberately records the date but does not invent the time of the original chat messages.