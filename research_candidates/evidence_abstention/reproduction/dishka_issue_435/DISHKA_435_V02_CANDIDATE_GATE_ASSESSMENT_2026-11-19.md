# Dishka #435 — v0.2 candidate gate assessment (not an acceptance record)

**Prepared:** 19 November 2026  
**Candidate:** `reagento__dishka-436`  
**Upstream project:** `reagento/dishka` (one case maximum for this project)  
**Dataset role:** primary cohort, rank 2  
**Current disposition:** `proposed_pending_license_and_formal_record`  
**Accepted registry:** still 0  
**Model loading / inference / training:** not performed and not authorized

This record is a pre-acceptance dossier. The project lead has clarified the prior pipeline/debug/test-oracle exposure answer as `none`; this satisfies that one v0.2 eligibility requirement. The case remains not accepted because license-scope sign-off, full proposed record, schema/registry checks and a separate final project-lead decision remain.

## 1. Technical evidence — repeated and independently rechecked

Latest complete reproduction:
- Workflow run: [44537219541](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44537219541)
- Job: `135605947696`
- Artifact: [14536192821](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44537219541/artifacts/14536192821)
- GitHub ZIP SHA-256: `b8dfe9e89e44f246fbf8d093ba31dc01c74c6dc167434555405693d6a0f1df52`
- Downloaded ZIP SHA-256: `b8dfe9e89e44f246fbf8d093ba31dc01c74c6dc167434555405693d6a0f1df52` — exact match
- ZIP CRC: PASS
- Archive members: 33
- Internal SHA256SUMS: 32/32 PASS

Exact upstream pins:
- Buggy base: `8718d5af93f9e48bc2506c64827663fdccc5ad89`
- Fixed revision: `b1eae11734e64551d7b101195f27cb6870e1c364`
- Dataset Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Canonical row SHA-256: `c548969ec886af21b56c93daae34db1a86b3a10c8dd1473d3d5c886549a9e86d`
- Row: `reagento__dishka-436`

Observed test outcomes:
- Independent issue reproducer `test_issue_435_override_lower_scope`: buggy base fails with `AssertionError: 1 != 42`; fixed revision passes.
- Frozen dataset FAIL_TO_PASS selectors: 8/8 real defect-related failures on the buggy base; the same 8/8 pass on the fixed revision.
- No collection error was used as a defect failure.

This establishes technical reproducibility. It does not, by itself, prove the study's model-facing evidence tiers or make the case accepted.

## 2. Gold mechanism and evidence tiers

The project lead's existing human adjudication record approves:
- Gold: `G1_STALE_PER_SCOPE_FACTORY_REGISTRATION`.
- Alternative A1: `A1_SCOPE_CHAIN_PRECEDENCE`.
- Alternative A2: `A2_CONSUMER_BINDING_OR_CACHE`.
- E3 survivors: G1, A1, A2.
- E2 survivors: G1, A1.
- E1 survivor: G1.

The human decision and rationale are preserved in:
- `reproduction/dishka_issue_435/HUMAN_ADJUDICATION_DECISION_DISHKA_435_V0_1_DRAFT_2026-11-16.md`
- `reproduction/dishka_issue_435/DISHKA_435_STAGE2_STAGE3_GATE_REVIEW_V0_1_2026-11-16.md`

Operational packet-set structural validation:
- Status: `valid`
- Packet-set SHA-256: `55de204e87a9c2b5e24b56b4cb366fb3fc6a620ad7cbffd506c3c76fbca75604`
- E1/E2/E3 item counts: 13 / 9 / 7
- Strictly nested: true

The validator explicitly reports `semantic_sufficiency_assessed=false`; it is a structural/hash validator, not a semantic judge. The separate human adjudication record is the source of the project's semantic approval. We must not conflate those two roles.

## 3. Dataset resource and timestamp

The dataset row is PR-derived:
- Resource URL: [PR #436](https://github.com/reagento/dishka/pull/436)
- Dataset row timestamp: `2025-04-15T22:52:26Z`
- PR resource timestamp: `2025-04-15T22:52:26Z` — exact match.
- Separate defect issue: [Issue #435](https://github.com/reagento/dishka/issues/435), created `2025-04-14T17:22:16Z`.

A historical timestamp register incorrectly recorded the PR row as `is_pull_request=false`. The correction is documented in `REAGENTO_DISHKA_436_RESOURCE_TYPE_RECONCILIATION_2026-11-16.md` and the post-run provenance correction. The historical CSV is not silently rewritten.

**Boundary:** candidate-specific PR resource/timestamp matching is documented. The project-wide raw-payload/header authentication gate remains open. Do not claim the global dataset provenance gate is closed because this one row reconciles.

## 4. Independence

- Canonical upstream repository: `reagento/dishka`.
- GitHub metadata reports `fork=false` and `mirror_url=null`.
- The frozen primary cohort has one row for this upstream project.
- Related-issue review did not identify a duplicate of this same cross-scope registry defect.
- One project can contribute at most one independent case.

Candidate-level independence evidence is documented in `DISHKA_435_CASE_ACCEPTANCE_READINESS_2026-11-18.md`. The evidence does not establish independence for every other candidate.

## 5. License and reproduction scope — bounded, not legal clearance

Recorded source evidence:
- Exact-base root license: Apache-2.0.
- Root LICENSE blob SHA-1: `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`.
- Changed-file license manifest SHA-256: `34e09fdcf5d33849659490e2e50cdf80c8c5c8e6f01108dd542c60de203cf360`.
- The independent issue reproducer uses the source by `PYTHONPATH`, standard-library unittest, and no pip-installed upstream runtime dependencies.
- Dataset selector environment is isolated and pins pytest 8.3.5, iniconfig 2.0.0, packaging 24.2, pluggy 1.5.0.
- Dataset extraction uses a separate isolated PyArrow 19.0.1 environment.

Scope limitations:
- This is a documentary screen for the exact source files and the listed reproduction/selector/extraction environments.
- It is not legal advice, formal legal clearance, blanket clearance for optional integrations/development extras, nor permission to redistribute upstream source or third-party dependencies.
- The project-wide source/license inventory and raw provenance gate remain open.

**Project-lead scope decision: pending.** A YES would mean only that the documented, bounded screening is adequate for this exploratory case file, with the limitations above preserved. It must not be recorded as formal legal approval.

## 6. Exposure — two separate variables

The project lead has already acknowledged:
- `researcher_source_exposure = full` — issue, patch and source materials were reviewed; no researcher blinding is claimed.
- Single human adjudicator: Mahmut; ChatGPT is advisory and is not a second human rater.
- No human-human inter-rater reliability or Cohen's kappa claim is made for gold/tier adjudication.
- Dishka is limited to the exploratory feasibility study, not confirmatory efficacy evidence.

This is separate from:
- `prior_pipeline_debug_exposure` — whether Dishka was used before its prospective case-validation assignment to debug the generic runner/pipeline or troubleshoot the target test oracle.

The readiness audit notes that Dishka is not listed in the prior pipeline/debug exclusion records, but the project-lead classification `none` was only proposed and still requires an explicit factual confirmation. Full source exposure does **not** imply prior pipeline-debug exposure, and one must not be substituted for the other.

**Prior pipeline/debug classification: `none` — clarified by the project lead on 19 November 2026.** The corrected declaration and superseded earlier answer are preserved in `PROJECT_LEAD_EXPOSURE_DECISION_2026-11-19.md`. The earlier `some` answer is not the current factual classification; the project lead explained that the earlier question had not yet been read carefully. The separate researcher source-exposure classification remains `full` and must not be conflated with prior pipeline/debug exposure.

## 7. Reviewer roles

The project lead reports shared agreement with the previously discussed technical result, gold mechanism, alternatives, evidence-tier rationale and disclosed limitations.

Proposed technical reviewers:
- Panel Reviewer H — technical/methodology reviewer; identity mapping is held outside the public repository.
- Panel Reviewer B — technical/methodology reviewer; identity mapping is held outside the public repository.

Their technical/methodology review may be unblinded. If either sees the issue, PR, source, patch, gold mechanism or hidden E-tier decisions, that person must not later be described as a blind model-output scorer for this case.

The active v0.2 `Rater_B` role is separate from Panel Reviewer B and is not automatically assigned to either technical reviewer. It requires separate consent and case-specific exposure screening. A panel review is not a legal opinion or independent external audit.

## 8. Acceptance workflow — no premature acceptance

The active v0.2 accepted-case schema now supports a distinct `proposed` state:
- A proposed case can be schema/structure-validated before any final decision.
- Its final acceptance status must be `pending`, with no decision timestamp and no final decision artifact.
- A proposed or rejected case cannot enter the accepted-case registry.
- Only a record marked `accepted` with a separate timestamped, hashed project-lead decision record may be inserted into the registry.

This corrects the previous circular procedure where a schema-valid record had to say `accepted` before the project lead could make the final decision.

### Current disposition after the corrected exposure declaration

The corrected value `none` satisfies the active v0.2 prior pipeline/debug exposure requirement. Continue with a complete proposed acceptance JSON and the remaining evidence gates; do not mark the case accepted in advance. The bounded documentary license-screen sign-off, source/timestamp evidence, independence/exposure references, E1/E2/E3 evidence manifests, schema validation, fail-closed registry checks and separate final project-lead decision remain required.

## 9. Current result

- Technical Stage 2: PASS.
- Gold/tier decision: project-lead approval recorded.
- Packet structure/hash validation: PASS; semantic validation is in the separate human record.
- Candidate PR timestamp/resource reconciliation: PASS; project-wide raw-payload authentication remains open.
- Independence: documented.
- Researcher source exposure: full, disclosed.
- Prior pipeline/debug exposure: `none` (clarified project-lead declaration, 2026-11-19; correction record linked).
- Study eligibility: eligible to continue case-level checks, subject to every remaining gate.
- Full v0.2 proposed acceptance record: still to be prepared.
- Final case acceptance: NOT ACCEPTED; no registry entry exists.
- Accepted registry: 0.
- Model loading/inference/training: not authorized or performed.


## 10. Final exposure disposition — 19 November 2026

The project lead explicitly declared prior pipeline/debug/test-oracle exposure as `some`. The separate decision record is `PROJECT_LEAD_EXPOSURE_DECISION_2026-11-19.md`.

Dishka is therefore **excluded from the model-evaluation sample** under the unchanged v0.2 rule. Its successful technical reproduction and prior Stage 3 technical adjudication remain valid engineering evidence; they do not make the candidate eligible. No acceptance record will be constructed for the study registry. The next candidate is NumPyro #1916.


## 11. Superseding exposure correction — 19 November 2026

The prior section 10 exclusion statement is superseded by the project's corrected exposure record. The project lead clarified that the earlier `some` answer was entered before the question had been read carefully and confirmed the intended factual answer:

`prior_pipeline_debug_exposure = none`

The exact project-lead wording was: “Hayır — Prospektif doğrulama öncesinde pipeline/debug amacıyla kullanılmadı.”

The original `some` entry remains in the correction-history record as superseded; it is not treated as the current factual value. The separate `researcher_source_exposure = full` remains disclosed.

**Current disposition:** continue Dishka's formal v0.2 proposed-case workflow. The case is not yet accepted. Do not skip the bounded license-scope decision, full record preparation, schema/registry validation or separate final decision.
