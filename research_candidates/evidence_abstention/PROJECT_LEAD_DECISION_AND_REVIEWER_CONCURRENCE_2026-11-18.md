# Project-lead decision and reviewer concurrence record

**Record date:** 18 November 2026  
**Repository:** `MahmutVezir/dijitalikiz`  
**Related candidate:** `cta-observatory/ctapipe`, issue #2730 / PR #2732  
**Public handling:** Personal names of the second reviewer are not stored in this public record. The role code `Rater_B` is used where the human-rater role is relevant.

## 1. Decision

The project lead approved the evidence-based classification:

- `prior_pipeline_debug_exposure = some`
- Candidate disposition: **exclude CTAPIpe #2732 from the model-evaluation sample**.
- Retain its exact-base/fixed reproduction, raw technical evidence, audit records, hashes and E1/E2/E3 packets as an **engineering/feasibility pilot record**.
- Do not add this candidate to the accepted-case registry.
- Do not treat the second-reviewer concurrence as a waiver of the exposure rule.

**Approval source:** Explicit project-lead confirmation in the ChatGPT conversation on 18 November 2026. The project lead reported that Panel Reviewer H concurred with this CTAPIpe exposure classification. This is a project-lead-reported concurrence, not a separately signed reviewer statement or cryptographic signature.

## 2. Evidence supporting the classification

The candidate-specific exposure is not inferred from model results. It is supported by the project's pre-existing work record:

1. The candidate's Stage 2 reproduction and test harness were repeatedly refined against CTAPIpe #2732.
2. The real `DataWriter.__call__` / HDF5 reproducer was developed and debugged specifically against this case.
3. The progress ledger already recorded: “CTAPIpe's test harness was refined against this case.”
4. The active v0.2 protocol excludes cases used for earlier candidate-specific pipeline debugging, test-oracle troubleshooting or prompt calibration.

The technical reproduction can remain valid as an engineering result while the case is ineligible for the study's model-evaluation sample. These are separate decisions.

**Technical evidence retained:** Latest repeat run `44324115597`, job `134870646827`, artifact `14436277116`; artifact ZIP SHA-256 `9e3e35f4f499a3a5947e0e6ad803dd7d6d9d1c240695a6558769e7f31ea501b2`; 137 archive members; CRC PASS; 136/136 internal SHA-256 entries verified. Frozen selector failed on the buggy base with the defect-specific Quantity-vs-float assertion and passed on the fixed revision. The direct HDF5 reproducer reproduced the `float.to_value` failure on the buggy base and passed on the fixed revision. No model loading, inference or training was performed.

## 3. Second-reviewer concurrence — scope limitation

The project lead reports that Panel Reviewer H also agreed with the above candidate-exposure decision. That concurrence is recorded only for this decision. It is **not** treated as:
- a signed consent form for the separate Rater B role;
- a completed case-specific source/gold/patch/prompt/output exposure screen;
- proof that Rater B is blind to any particular candidate;
- completion of calibration;
- independent gold/E1/E2/E3 adjudication; or
- an external audit.

For public documents, the second reviewer for this CTAPIpe decision is referred to as `Panel Reviewer H`. This limited concurrence does not assign that person to the separate active v0.2 blind-scoring role `Rater_B`. No private identity, school, contact information or signature is stored here.

## 4. Remaining gates

- CTAPIpe #2732 is excluded from the model-evaluation sample under the current v0.2 exposure rule.
- Its unresolved issue-YAML versus reporter-traceback effective-configuration discrepancy remains disclosed.
- Project-lead license-scope acknowledgement remains pending.
- Gold and E1/E2/E3 membership remain proposals unless separately approved.
- Rater B's role-specific agreement, case-by-case independence screen for any future included cases, and non-study calibration remain separate gates.
- Final accepted-case count remains zero; model inference remains unauthorized.

## 5. Audit rule

This record is an audit trail of the decision source and scope. It does not fabricate a private signature, retroactively remove prior exposure, modify raw reproduction artifacts or convert an excluded engineering pilot into an accepted study case.
