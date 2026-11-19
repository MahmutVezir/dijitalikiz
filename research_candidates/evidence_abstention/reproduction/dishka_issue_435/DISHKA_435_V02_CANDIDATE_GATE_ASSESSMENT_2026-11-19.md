# Dishka #435 — v0.2 candidate gate assessment (not an acceptance record)

**Prepared:** 19 November 2026  
**Candidate:** `reagento__dishka-436`  
**Upstream project:** `reagento/dishka` (one case maximum for this project)  
**Dataset role:** primary cohort, rank 2  
**Current disposition:** `proposed_pending_final_project_lead_acceptance`  
**Accepted registry:** still 0  
**Model loading / inference / training:** not performed and not authorized

This pre-acceptance dossier is superseded by the final candidate-level preparation record in section 14. The project lead's bounded documentary license-scope decision is recorded, the complete v0.2 proposal exists, all in-repository reference hashes/paths are checked, and the active Draft 2020-12 case validator plus fail-closed registry checks passed. The only Dishka-specific decision still pending is the separate project-lead YES/NO on final case acceptance. The case remains proposed and not accepted.

## 1. Technical evidence — repeated and independently rechecked

Latest complete reproduction:
- Workflow run: [44570230531](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44570230531)
- Job: `135605947696`
- Artifact: [14553612258](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44570230531/artifacts/14553612258)
- GitHub ZIP SHA-256: `f24f43f48b2678407b381bee40b947b5a02dd9286743c12d3a6adf728af6ba2a`
- Downloaded ZIP SHA-256: `f24f43f48b2678407b381bee40b947b5a02dd9286743c12d3a6adf728af6ba2a` — exact match
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

**Project-lead scope decision: APPROVED within the documented bounded scope on 19 November 2026.** The separate decision record is `PROJECT_LEAD_LICENSE_SCOPE_DECISION_2026-11-19.md`. This is not legal advice, formal legal clearance or blanket redistribution approval.

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

The active v0.2 `Rater_B` role is separate from both technical panel reviewers and is not automatically assigned to either. It requires separate consent and case-specific exposure screening. A panel review is not a legal opinion or independent external audit.

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
- Bounded documentary license-scope decision: approved for the exact listed experimental environment only; not legal advice/redistribution approval. Record SHA-256: `96f89e28ee026fcced8aca6d854770f5a0aefcb47690405f7d1a022fc9405d4d`.
- Full v0.2 proposed acceptance record: `SWE_REBENCH_V2_DISHKA_435_CASE_ACCEPTANCE_PROPOSED_V0_2.json`; current SHA-256 `a23a6b23fb6a8cddde352eb415d52c62c364aa3af3a38a50da72d6c3aa40886f`.
- Active validator result: `structurally_complete_candidate`; final decision remains pending.
- Final case acceptance: NOT ACCEPTED; accepted registry remains empty.
- Accepted registry: 0.
- Model loading/inference/training: not authorized or performed.


## 10. Superseded preliminary exposure disposition — 19 November 2026

An earlier answer was temporarily recorded as `some`, which would have excluded Dishka. This value was later corrected by the project lead after rereading the question; it is not the current factual classification. The correction history is preserved in `PROJECT_LEAD_EXPOSURE_DECISION_2026-11-19.md`.


## 11. Superseding exposure correction — 19 November 2026

The prior section 10 exclusion statement is superseded by the project's corrected exposure record. The project lead clarified that the earlier `some` answer was entered before the question had been read carefully and confirmed the intended factual answer:

`prior_pipeline_debug_exposure = none`

The exact project-lead wording was: “Hayır — Prospektif doğrulama öncesinde pipeline/debug amacıyla kullanılmadı.”

The original `some` entry remains in the correction-history record as superseded; it is not treated as the current factual value. The separate `researcher_source_exposure = full` remains disclosed.

**Current disposition:** continue Dishka's formal v0.2 proposed-case workflow. The case is not yet accepted. Do not skip the bounded license-scope decision, full record preparation, schema/registry validation or separate final decision.


## 12. Active next steps after exposure correction — 19 November 2026

The current project-lead value is `prior_pipeline_debug_exposure = none`; see `PROJECT_LEAD_EXPOSURE_DECISION_2026-11-19.md`. Dishka therefore satisfies this specific eligibility gate and is first for formal v0.2 case checks. The prior `some` answer remains only as superseded history.

Remaining gates:
1. Bounded documentary license-screen decision by the project lead, limited to the exact base, five changed files, the minimal dependency-free reproducer, four explicitly pinned test-runner packages, and the isolated PyArrow 19.0.1 dataset-extraction environment.
2. Complete full proposed v0.2 case JSON with verified hashes/URIs and all approved gold/tier references.
3. Draft 2020-12 schema validation and fail-closed registry validation.
4. Resolve any provenance or semantic mismatch without changing the cohort row or weakening criteria.
5. Separate final project-lead YES/NO acceptance decision.

The case remains not accepted; registry count remains zero; model loading/inference/training remain unauthorized.


## 13. Proposed case record and active validator result — 19 November 2026

The project lead approved the bounded documentary license/provenance screen only for the exact pinned scope in `PROJECT_LEAD_LICENSE_SCOPE_DECISION_2026-11-19.md` (record SHA-256 `cf1f1a7344ced441d04b212292edc0dfefd28986e61bfdadcbb282319e90cbbd`). It expressly excludes legal clearance, optional integrations/extras and blanket redistribution approval.

The complete v0.2 proposed case record is:
- Path: `SWE_REBENCH_V2_DISHKA_435_CASE_ACCEPTANCE_PROPOSED_V0_2.json`
- SHA-256: `a23a6b23fb6a8cddde352eb415d52c62c364aa3af3a38a50da72d6c3aa40886f`
- `acceptance_decision = proposed`
- `final_acceptance.status = pending`; timestamp and decision record are null.
- Exposure: prior pipeline/debug exposure `none`; researcher source exposure `full`.
- Tier membership is linked to the exact pinned E1/E2/E3 manifests (13/9/7 items); approved survivor sets are retained.

The real-record regression tests were added to `tests/test_swe_rebench_v2_exploratory_case_acceptance.py` and run in GitHub Actions:
- Workflow run: [44561953996](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44561953996)
- No-inference preflight job: `135693344292` — **success**
- Preflight log artifact: `14550531292`, SHA-256 `d628b1f56d69edc4a249b929931f1fe43134c3c41eafe9887b16dc1c8c5e3e4a`
- Test groups: 12 + 25 + 6 + 21 + 10 = **74 passed**. The 21-case v0.2 suite includes the two new tests for the actual Dishka proposed record and the unchanged empty accepted registry.
- The real case validator result is `structurally_complete_candidate`; registry validation remains `valid_empty_registry`, 0 accepted cases, and inference unauthorized.

**Still pending:** the separate final project-lead YES/NO case-acceptance decision. Dishka remains **not accepted** and must not be counted toward the feasibility minimum until that decision is recorded. The same preflight report remains `ready_for_inference=false`, 14 global blockers, no model load/inference/fine-tuning.


## 14. Superseding final preparation and CI evidence — 19 November 2026, 19:55 UTC

This section supersedes earlier sections where the proposal SHA, bounded-license decision hash, last reproduction artifact, or CI run numbers are older.

### Canonical case file
- Path: `research_candidates/evidence_abstention/reproduction/dishka_issue_435/SWE_REBENCH_V2_DISHKA_435_CASE_ACCEPTANCE_PROPOSED_V0_2.json`
- Current SHA-256: `a23a6b23fb6a8cddde352eb415d52c62c364aa3af3a38a50da72d6c3aa40886f`
- Git blob SHA-1: `d171fcaec5f5a4b8e9112e44369bd59c918885af`
- `acceptance_decision=proposed`; `final_acceptance.status=pending`; no final-decision timestamp or record exists.
- All 12 in-repository evidence references in this record are pinned to immutable commit `13b4a0c80575cd2de9575cc884038666f34dfaa1`. The case-specific hash regression test also checks that each URI points to the exact local file whose bytes are hashed.

### Bounded documentary scope decision
- Record: `PROJECT_LEAD_LICENSE_SCOPE_DECISION_2026-11-19.md`
- SHA-256: `96f89e28ee026fcced8aca6d854770f5a0aefcb47690405f7d1a022fc9405d4d`
- The decision is limited to the exact pinned source, five changed paths, dependency-free issue reproducer, the four locked dataset-test packages, and isolated PyArrow extraction environment. It is not legal clearance or blanket redistribution approval.

### Latest independently verified Stage 2 artifact
- Workflow run: [44570230531](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44570230531)
- Job: `135723082451` — success.
- Artifact: [14553612258](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44570230531/artifacts/14553612258)
- Outer ZIP SHA-256: `f24f43f48b2678407b381bee40b947b5a02dd9286743c12d3a6adf728af6ba2a` — locally recalculated and equal to GitHub's digest.
- ZIP CRC: PASS; 33 members; all 32 internal `SHA256SUMS.txt` entries PASS.
- Independent issue reproducer: buggy base fails with `AssertionError: 1 != 42`; same reproducer passes on the fixed revision.
- Frozen dataset selectors: 8/8 defect-related failures on buggy base; same 8/8 pass on fixed revision.

### Latest no-inference case-preflight validation
- Workflow run: [44571127276](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44571127276)
- Job: `135726142556` — success.
- Artifact: `14552969335`, SHA-256 `44b768f7d76d65c19935b88b4856ec8aacc59b691ad625113c853ade0f2ad3e9`.
- Case acceptance tests: 22 passed, including the real Dishka proposal, unchanged empty registry, and 12-reference immutable-URI/path/hash consistency regression.
- Study-design / dual-human scoring tests: 10 passed.
- The validator returns `structurally_complete_candidate`. The accepted registry remains `valid_empty_registry`, 0 cases, 0 projects, and inference unauthorized.

**Current Dishka-specific state:** the bounded documentary scope decision, proposal construction, hash/path consistency audit, schema validation and fail-closed registry validation are complete. Dishka remains **not accepted** until the project lead separately records an explicit YES/NO final case-acceptance decision. Do not count it as a feasibility case or add it to the accepted registry before that decision.

**Project-wide state:** the no-inference readiness report still has 14 blockers, including raw dataset provenance, exact model license/runtime, frozen generation/protocol artifacts, and Rater B consent/exposure. No model loading, inference, fine-tuning or training has occurred or is authorized.


## 15. Latest immutable case-file, reproduction-artifact and preflight verification — 19 November 2026

This section supersedes the earlier "latest repeat" references in sections 13–14 where a newer Dishka reproduction/preflight is now available. It does not supersede the case eligibility, exposure, license-scope or final-acceptance decisions.

### Canonical proposed case record

- Canonical path: `research_candidates/evidence_abstention/reproduction/dishka_issue_435/SWE_REBENCH_V2_DISHKA_435_CASE_ACCEPTANCE_PROPOSED_V0_2.json`
- SHA-256 after pinning the latest verified reproduction artifact: `0a234c0f16668e5b58dace671483d4bc94b7f8167150e44662b339dc995ff9ee`
- Git blob SHA-1: `ec884cda706b5a66d2439ea4df60580ae26a0656`
- State remains `acceptance_decision=proposed`, `final_acceptance.status=pending`; no final decision timestamp or final-decision artifact exists.
- The baseline and fixed reproduction records now point to the latest repeat archive: [run 44572926370 / artifact 14553229664](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44572926370/artifacts/14553229664), SHA-256 `7f10db7e6f1b033eef7cd34476e3e34b3dbd28687310ccb3707ffddc5d5a6f10`.

### Independent archive verification of latest Dishka repeat

The artifact was downloaded and checked locally:
- ZIP archive SHA-256: `7f10db7e6f1b033eef7cd34476e3e34b3dbd28687310ccb3707ffddc5d5a6f10`, matching the GitHub-reported digest.
- Archive contents: 33 members; ZIP CRC test PASS.
- Internal `SHA256SUMS.txt`: 32 entries, all 32 verified.
- Issue reproducer on buggy base: failed with `AssertionError: 1 != 42`.
- Same issue reproducer on fixed revision: passed.
- Dataset FAIL_TO_PASS selectors on buggy base: 8/8 executed defect-related failures (not collection failures).
- Same 8 selectors on fixed revision: 8/8 passed.

Dishka job `135733170187` completed successfully. The overall 13-candidate run concluded failure because separate Nox, Werkzeug and Moto candidate jobs failed their own selector contracts. Those failures do not change the successful Dishka job result; the full candidate matrix must not be called green.

### Latest no-inference preflight

- Workflow run: [44572926370](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44572926370)
- No-inference preflight job: `135732610579` — success.
- Log artifact: [14554972064](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44572926370/artifacts/14554972064), SHA-256 `b0dc39e127a375206e7fbe8613292fef6d3f4a77af56b23080b5fd5691665c61`; downloaded ZIP digest independently matched and ZIP CRC passed.
- v0.2 case-acceptance tests: 22 passed, including the actual Dishka proposed record, empty-registry guard, and the 12-reference immutable-URI/path/content-hash regression.
- Study-design / dual-human scoring tests: 10 passed.
- Actual proposed record result: `structurally_complete_candidate`.
- Accepted registry: `valid_empty_registry`; accepted cases 0; accepted projects 0; proposed case not inserted.

The preflight readiness report remains `blocked_before_inference`, `ready_for_inference=false`, with 14 global blockers. Model loading, inference and fine-tuning remain false and unauthorized.

### Current Dishka-specific disposition

The bounded documentary license-scope decision is approved only for its exact pinned research/reproduction/test/extraction environment; it is not legal clearance or redistribution approval. The project-lead prior pipeline/debug exposure value remains `none`; researcher source exposure remains `full`.

The record's internal URI/content-hash references are pinned to immutable commit `13b4a0c80575cd2de9575cc884038666f34dfaa1` and the CI regression confirms all 12 referenced files' content SHA-256 values and path suffixes. This verifies repository-local references; the structural validator does not fetch and authenticate every external URI or confer semantic/legal approval.

**Only the separate final project-lead YES/NO case-acceptance decision remains as the Dishka-specific decision.** Until it is recorded, Dishka stays proposed, does not count toward the one-case feasibility minimum, and remains outside the accepted registry. NumPyro #1916 stays the fallback if the final Dishka decision is NO or a substantive case-level issue is discovered.


## 16. Patch URI/content-hash reconciliation — 19 November 2026

A further audit found that the `source.patch` field previously paired the mutable upstream URI `https://github.com/reagento/dishka/pull/436.diff` with the SHA-256 of a different file. The expected digest `c5a6e5ed...` belongs to the exact `full-pr.diff` generated by `git diff` between pinned base `8718d5af93f9e48bc2506c64827663fdccc5ad89` and fixed `b1eae11734e64551d7b101195f27cb6870e1c364`. The live PR diff endpoint returned a different digest, so the old URI/hash pair was not retained.

The canonical case record now points to the exact file inside the independently verified latest reproduction artifact:
- URI: `https://github.com/MahmutVezir/dijitalikiz/actions/runs/44572926370/artifacts/14553229664#path=full-pr.diff`
- Inner-file SHA-256: `c5a6e5edc41d5a321fb95dc0bdb81ee449870eb53278a5d91582c2478395efde`
- Outer ZIP SHA-256: `7f10db7e6f1b033eef7cd34476e3e34b3dbd28687310ccb3707ffddc5d5a6f10`
- ZIP CRC PASS; 33 members; 32/32 internal SHA256SUMS entries PASS.

The reconciliation is documented in `DISHKA_435_PATCH_REFERENCE_RECONCILIATION_2026-11-19.md`, SHA-256 `b1f550033797d0f82cf4f4f49fb3c0bb42ad883520fbbf81e7608b0814ccdf09`. The workflow stores the artifact for 90 days; if it expires, the exact diff can be recreated from the pinned commits using the recorded command and checked against the same SHA-256. The archive reference does not grant legal clearance or redistribution permission.

The final-acceptance rationale in the JSON is also corrected: case-specific record preparation and structural checks are complete; the only remaining Dishka-specific decision is the separate explicit final project-lead YES/NO. The record itself remains proposed.

**Updated canonical case JSON**
- SHA-256: `0a234c0f16668e5b58dace671483d4bc94b7f8167150e44662b339dc995ff9ee`
- Git blob SHA-1: `c17d908a937c32c7372d1eb19bb9b29990b338e2`
- `acceptance_decision=proposed`; `final_acceptance.status=pending`; registry unchanged.

## 17. Superseding current PR-head verification — 19 November 2026, 18:16 UTC

### Dishka Stage 2 repeat and archive integrity

- Tested PR-head commit: `3c64519737130cf156eda71ea6e9d2fda47b2b72`.
- Workflow run: [44586011672](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44586011672).
- Dishka reproduction job `135779190633`: **success**.
- Artifact `14559803463`; outer ZIP SHA-256 `7284f44942c684eef0f1740fd1c13aa856b9552c6e675e8a7cede8abedc612b7`.
- Independently downloaded archive: outer SHA-256 matched GitHub, ZIP CRC passed, 33 members, 32/32 internal SHA256SUMS entries passed.
- The exact `full-pr.diff` file inside the new archive retains SHA-256 `c5a6e5edc41d5a321fb95dc0bdb81ee449870eb53278a5d91582c2478395efde`. The pinned buggy base and fixed revision remain unchanged.
- Independent issue reproducer: base fails with `AssertionError: 1 != 42`; fixed revision passes.
- Dataset FAIL_TO_PASS selectors: 8/8 defect-related failures on the buggy base and 8/8 passes on the fixed revision.
- Canonical proposed case JSON SHA-256 after advancing the patch/archive references: `bac70ef6a844c5f1d374ef8197c1b41e802e70e0e94556d581699e7f43fe614b`.

### Current no-inference preflight and candidate matrix

- The no-inference preflight job `135778987976` in run `44586011672` completed successfully. Its five test groups passed: 12 + 25 + 6 + 23 + 10 = **76 tests passed**.
- The readiness report is still `blocked_before_inference`, `ready_for_inference=false`, with **14 blockers**, **0 accepted cases**, and **0 accepted projects**. The readiness blocker state is not a failing test result.
- The focused 13-job candidate matrix completed with **10 successful reproductions** (Dishka, NumPyro, PyFar, Python-Control, Meltano, Amaranth, Dymos, EODAG, QuTiP and Robocop) and **3 candidate-specific selector failures** (Nox, Moto and Werkzeug). The matrix is therefore not globally green; these three outcomes do not reverse the successful Dishka job.
- Research Validation run `44586010807`, the uncertainty unit-test workflow `44586011562`, and the Qwen adapter test workflow `44586011558` completed successfully.

### Decision boundary

Dishka remains a proposed candidate, not an accepted case. Its final project-lead YES/NO decision remains pending; accepted registry count remains 0. The newer archive pointer does not change gold/tier adjudication, exposure classification, license-scope limitations, candidate independence, or case acceptance. No model loading, inference, fine-tuning or training was performed or authorized.

## 18. Focused Dishka run, provenance capture and Qwen license evidence — 19 November 2026

### Dishka technical reproduction — newest checked artifact

- PR-head commit: `af12f54f8d3900b79f0264aa7f6739c68dff0e17`.
- Workflow run: [44596435482](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44596435482).
- Dishka job `135816057850`: **success**.
- Artifact [14564379897](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44596435482/artifacts/14564379897).
- Outer ZIP SHA-256: `bed2f0a7b04b21e2753747b1ed3324c4ff15bc789bdf1cfa1264f976178d349c`; independent download matched GitHub, ZIP CRC passed, 33 members, 32/32 internal SHA256SUMS entries verified.
- Inner `full-pr.diff` SHA-256 remains `c5a6e5edc41d5a321fb95dc0bdb81ee449870eb53278a5d91582c2478395efde`.
- Independent issue reproducer: buggy base failed with `AssertionError: 1 != 42`; fixed revision passed.
- Frozen dataset selectors: 8/8 executed defect-related failures on buggy base and 8/8 passes on fixed revision.
- Canonical proposed JSON and its regression test now point at this newer archive. The case remains `proposed`; final acceptance remains `pending`.

### No-inference preflight

- Job `135815854250`: **success**.
- 76 tests passed (12 + 25 + 6 + 23 + 10).
- Artifact [14565817178](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44596435482/artifacts/14565817178), downloaded SHA-256 `f4b5c94ea1be629fabea4757b31ddb5176b2da7c75663493e9868da9b97fa013`, ZIP CRC PASS.
- Readiness remains `blocked_before_inference`, 14 blockers, 0 accepted cases/projects, `valid_empty_registry`; no model loading, inference or fine-tuning.

### Dishka raw source metadata — partial evidence captured, script correction required

- Job `135816056778` attempted raw GitHub issue/PR API capture (response bodies and headers) and the pinned Hugging Face dataset revision/card.
- Artifact [14566406023](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44596435482/artifacts/14566406023), ZIP SHA-256 `e3a3558b7d0789b5a16e168010cfb618c94c4bbc514d758fdc51b72232a082e0`, ZIP CRC PASS.
- The job ended on a Python regex syntax error after uploading the captured files; checksum-manifest/summary generation did not complete. The artifact was therefore inspected independently rather than called a successful workflow.
- Independent local inspection of the artifact found HTTP 200 response headers for issue #435 and PR #436; issue created at `2025-04-14T17:22:16Z`; PR created at `2025-04-15T22:52:26Z`; frozen row `reagento__dishka-436` carries that same PR timestamp; base/fixed pins match; the dataset revision SHA is `fb9aa226b2ce37c708ea7732e7b980abacdadb67`; both revision metadata and README identify `CC-BY-4.0`.
- This closes neither the 113-row raw payload audit nor the broader per-upstream-source license review. The cohort-level one-second SimPEG exception remains open.

### Pinned Qwen license/configuration evidence — successful read-only collection

- Job `135816056966`: **success**.
- Artifact [14565807914](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44596435482/artifacts/14565807914), outer SHA-256 `2b23c6d58c1862105ba4e3cbde739b90b04301a38f014ac22d2ccdd74bfdc0fc`; independent ZIP CRC PASS and 9/9 internal hashes PASS.
- Immutable revision confirmed: `aa8e72537993ba99e69dfaafa59ed015b17504d1`.
- Exact LICENSE SHA-256: `ef52482bb785733093dc9a2e8edd8e764c77d12d8e9d8f10a80c9b547d32d0f9`.
- License title: Qwen Research License Agreement; config metadata confirms `model_type=qwen2` and 36 layers.
- No model weights or model/tokenizer loading occurred. This is collected license evidence, **not** the required human/mentor non-commercial-use decision or legal clearance.

### Current disposition

Dishka technical Stage 2 and candidate-level packet/structural checks remain passed. The separate final project-lead YES/NO acceptance is still pending. The accepted registry remains empty. Project-wide readiness remains blocked; no model operation is authorized.

## 19. Successful Dishka-only workflow and corrected provenance rerun — 19 November 2026

- PR head: `fb7d17633458978406cdc4a37750752f93658e16`.
- Focused workflow: [44599553076](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44599553076) — **success**.
- The four active jobs all succeeded: no-inference preflight `135826905001`; Dishka raw provenance `135827095421`; Qwen pinned license evidence `135827095472`; Dishka Stage 2 reproduction `135827095607`.
- All 12 non-Dishka candidate jobs in the main matrix were skipped. Separate non-Dishka candidate workflows also report `skipped` on the new PR head. Shared file edits no longer launch unrelated candidate reproductions.
- Preflight: 76 tests passed (12 + 25 + 6 + 23 + 10); readiness still `blocked_before_inference`, 14 blockers, 0 accepted cases/projects, registry `valid_empty_registry`.
- Dishka artifact [14567057835](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44599553076/artifacts/14567057835), outer SHA-256 `de85c1828528ead79bcb0af00a5d2a307dc44c3839477d8e7ebb7329854a68a6`; independent download, ZIP CRC PASS, 33 members, 32/32 inner hashes PASS. Inner `full-pr.diff` SHA-256 `c5a6e5edc41d5a321fb95dc0bdb81ee449870eb53278a5d91582c2478395efde`.
- Reproducer remains base-fail with `AssertionError: 1 != 42` / fixed-pass; frozen selectors remain 8/8 base-fail / 8/8 fixed-pass.
- Raw Dishka provenance artifact [14566683002](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44599553076/artifacts/14566683002), outer SHA-256 `e0e107b9d38649d21a159f95586832103d772230ca9ec4348ef936ff107f3d41`; 12 members; ZIP CRC PASS; 11/11 inner hashes PASS. The successful summary records issue #435 time, PR #436 time, the same dataset-row PR timestamp, fixed source commits, immutable dataset revision and `CC-BY-4.0` card license. The other 112 timestamp rows and cohort-wide source-license review remain open.
- Qwen read-only license evidence [14567706680](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44599553076/artifacts/14567706680), outer SHA-256 `eb8d9fcbf17a1f59457b5ca6298778fde91c95096163294431a6de63b1a470b8`; 10 members; ZIP CRC PASS; 9/9 inner hashes PASS. Pinned revision and Research License Agreement confirmed; no weights, model load, tokenizer load, inference or fine-tuning.
- Updated canonical proposed case JSON SHA-256: `a7f284ecfacc1be448791cf1a07a3b8f63cc8e0143e1453bbd0262fe785ca036`. It remains `acceptance_decision=proposed`, `final_acceptance.status=pending`; accepted registry stays 0.

## 20. Final PR-head verification and current artifact reconciliation — 19 November 2026

**Verified PR head:** `ef89cd9bbc04531f576a3b46ce00b1ff524f7274`.

### CI result
- Focused Dishka workflow [44600772416](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44600772416): **success**.
- No-inference preflight job `135831247836`: success; five groups 12 + 25 + 6 + 23 + 10 = **76 tests passed**.
- Dishka reproduction job `135831401881`: success.
- Dishka raw provenance job `135831401970`: success.
- Qwen read-only license/config evidence job `135831401859`: success.
- All 12 non-Dishka matrix jobs: **skipped**.
- Repository/configuration validation run `44600785064`: success; unit tests run `44600785300`: 171 tests; CPU tests run `44600785425`: 171 tests plus 2 additional checks.

### Independently downloaded artifacts
- Dishka [artifact 14566758994](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44600772416/artifacts/14566758994), outer SHA-256 `1bc714ec60e6315907d8273b5842891953af7ba4296d785ba29603feb4d6eed6`; ZIP CRC PASS; 33 members; 32/32 internal SHA256SUMS entries PASS. The base reproducer fails with `AssertionError: 1 != 42`; fixed revision passes; all eight frozen dataset selectors fail on buggy base and pass on fixed. Inner `full-pr.diff` SHA-256 `c5a6e5edc41d5a321fb95dc0bdb81ee449870eb53278a5d91582c2478395efde`.
- Raw provenance [artifact 14567568737](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44600772416/artifacts/14567568737), outer SHA-256 `f099a1e5b8a0a0da45b706b162a634a4a4f9b5c3c4d2335e12389a1cf916f8b9`; ZIP CRC PASS; 12 members; 11/11 internal hashes PASS. Raw issue/PR response bodies and headers preserved. Dishka PR creation timestamp equals the frozen dataset-row timestamp (`2025-04-15T22:52:26Z)); pinned dataset revision `fb9aa226b2ce37c708ea7732e7b980abacdadb67`; card license `CC-BY-4.0`.
- Qwen license/config [artifact 14566504228](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44600772416/artifacts/14566504228), outer SHA-256 `a1357b695ef01cc15277260f578a99e4f3bcc495faf6ccfe149a514014a1bf0c`; ZIP CRC PASS; 10 members; 9/9 internal hashes PASS. Exact pinned revision confirmed; license SHA-256 remains `ef52482bb785733093dc9a2e8edd8e764c77d12d8e9d8f10a80c9b547d32d0f9`. No weights or model/tokenizer load, inference or fine-tuning.
- Preflight [artifact 14568006031](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44600772416/artifacts/14568006031), outer SHA-256 `ba8cca34f1ed4dfc2ae596da82463f6adf005687d4b14d6addb2547f387bd019`; ZIP CRC PASS; six members. Readiness remains `blocked_before_inference`, 14 blockers, 0 accepted cases/projects, `valid_empty_registry`, `inference_authorized=false`.

### Exact interpretation
The Dishka-specific technical, candidate raw-timestamp and bounded documentary checks are now reproducible and archived. They do **not** close the other 112 timestamp records, the cohort-wide upstream source-license review, the Qwen human/mentor use-scope decision, runtime/generation/protocol freezes or the second-rater gate. Dishka remains `proposed`; final project-lead decision remains pending. No case is inserted into the accepted registry and no inference is authorized.
