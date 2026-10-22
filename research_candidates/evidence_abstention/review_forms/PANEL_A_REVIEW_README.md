# Panel A independent review forms — V9 candidates

**Purpose:** Prepare independent eligibility/root-cause review for two technical candidates. This document is a form pack, not an acceptance decision. It does not authorize model inference.

## Independence and blinding

- Recruit two reviewers with sufficient Python/debugging experience. They must independently complete a separate copy of each form before discussion.
- Use pseudonymous reviewer IDs in the research record; keep any identity-to-ID key private.
- Panel A may inspect source, tests, buggy/fixed revisions, patch, raw test logs, dataset issue/PR, provenance and license.
- Panel A must not inspect model responses or P0/P1 outcome summaries.
- A technical screen pass is not sufficient. If source/test/patch linkage, license, distinctness, or exposure status is uncertain, mark HOLD or REJECT, never ACCEPT.
- Do not put private identity information or blinded Panel B materials in this public repository.
- Reviewers must cite exact URLs and source commit IDs, not just paraphrase the CI report.

## Candidate pack

1. [Keras-5 form](PANEL_A_KERAS_5_FORM.md)
2. [Tornado-6 form](PANEL_A_TORNADO_6_FORM.md)

## Decision logic

Each reviewer submits one independent form per candidate. Compare only after both are locked. Any disagreement goes to a documented adjudicator; original scores are preserved. Candidate acceptance requires agreement or adjudication and every mandatory gate passing. No candidate is added to `CASE_REGISTRY.json` by this form pack.

## Current state

- Keras-5: technical buggy-fail/fixed-pass signal reported; independent review pending.
- Tornado-6: two target tests reportedly buggy-fail/fixed-pass; independent review pending.
- Accepted confirmatory cases: 0.
- Model inference for this study: not authorized.
