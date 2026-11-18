# CTAPIpe #2732 — candidate-specific pipeline/debug exposure decision

**Date:** 18 November 2026  
**Status:** Decision recorded and approved by the project lead on 18 November 2026. Candidate excluded from the model-evaluation sample; retained as an engineering/feasibility pilot.

## 1. Protocol rule

The active v0.2 exploratory protocol states that a candidate used for earlier pipeline debugging, test-oracle troubleshooting, or prompt calibration is excluded from the study sample. Exposure must be recorded and cannot be silently waived.

## 2. Evidence in the project record

The CTAPIpe #2732 candidate was used while developing and refining its own Stage 2 reproduction and test harness. The progress ledger explicitly states that “CTAPIpe's test harness was refined against this case” and that the project lead must classify the prior pipeline-debug exposure. The work includes:
- repeated debugging of the candidate-specific base/fixed reproduction workflow;
- development and refinement of the direct DataWriter.__call__ / HDF5 reproducer against this exact defect;
- correction of test/harness and evidence-inventory issues discovered while running this candidate;
- repeated use of the selected candidate to validate the reproduction and evidence-packet pipeline.

The technical reproduction itself is valid and remains a useful engineering and feasibility artifact. That does not imply the candidate is eligible for model-output evaluation under the frozen exposure rule.

## 3. Recommended classification

**Recommended prior_pipeline_debug_exposure: some (candidate-specific exposure).**

Under the current v0.2 rule, this classification means CTAPIpe #2732 should be excluded from the model-evaluation sample. Preserve its Stage 2 reproduction, source snapshots, audit records and E1/E2/E3 packets as an engineering/pilot record. Do not insert it into the accepted case registry.

Adding a second blinded human output rater does not remove the project lead's prior candidate-specific pipeline/debug exposure and does not reverse this exclusion.

## 4. Decision recorded on 18 November 2026

- Final decision: **approved — `prior_pipeline_debug_exposure = some`.**
- Decision maker: student project lead.
- Decision date: 18 November 2026.
- Decision source: explicit project-lead confirmation in the conversation record; the project lead also reported Hasan's concurrence.
- Consequence: exclude CTAPIpe #2732 from the model-evaluation sample; retain its technical reproduction and audit packet as an engineering/feasibility pilot; do not add it to the accepted-case registry.
- Rationale: the candidate-specific reproduction/test harness and direct HDF5 reproducer were developed and refined against this exact case, which meets the active v0.2 prior pipeline/debug exposure definition.
- Public evidence record: `research_candidates/evidence_abstention/PROJECT_LEAD_DECISION_AND_REVIEWER_CONCURRENCE_2026-11-18.md`.

This decision does not accept the case for evaluation, authorize inference, or waive the separate issue-configuration, licensing, gold/tier, and Rater B eligibility gates.
