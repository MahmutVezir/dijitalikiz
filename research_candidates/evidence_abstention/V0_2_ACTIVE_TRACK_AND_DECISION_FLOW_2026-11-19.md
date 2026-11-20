# Active v0.2 research track and human decision flow — 19 November 2026

## 1. Single active study definition

The active study is **SWE-rebench V2 evidence-abstention, v0.2 exploratory/feasibility**.

- Research question: whether a policy allowing evidence-conditioned abstention reduces unsupported or contradicted definitive root-cause claims when visible evidence is insufficient, compared with a diagnosis-required policy.
- Primary P0/P1 comparison: same exact frozen base-model weights, tokenizer, runtime, prompts except the predeclared policy change, and generation settings.
- Evidence support and hidden-gold correctness are separate outcomes.
- Minimum for a case-level feasibility demonstration: 1 fully accepted independent case.
- Primary target: 15 accepted cases from 15 distinct upstream projects.
- Stretch target: 20.
- Keep every case that passes unchanged criteria if fewer than 15 pass; report the smaller exploratory result without confirmatory efficacy claims.
- One case maximum per upstream project.
- Model training is a separate secondary hypothesis and authorization; primary inference acceptance does not authorize fine-tuning.

The authoritative v0.2 artifacts are:
- `SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json`
- `SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json`
- `SWE_REBENCH_V2_EXPLORATORY_CASE_ACCEPTANCE_SCHEMA_V0_1.json`
- `implementation/swe_rebench_v2_exploratory_case_acceptance.py`
- `scripts/swe_rebench_v2_exploratory_preflight.py`

## 2. Legacy files are retained, not active

The following files are historical v0.1 confirmatory artifacts and must not be mixed into the active v0.2 flow:
- `SWE_REBENCH_V2_EXPERIMENT_MANIFEST_V0_1.json`
- `SWE_REBENCH_V2_CASE_REGISTRY_V0_1.json`
- `SWE_REBENCH_V2_CASE_ACCEPTANCE_SCHEMA_V0_1.json`
- `implementation/swe_rebench_v2_case_acceptance.py`
- `scripts/swe_rebench_v2_no_inference_preflight.py`
- `HUMAN_REVIEW_ROLE_GOVERNANCE_V0_1.md`

The old validator requires a Panel A/Panel B/external-audit/confirmatory workflow and a 60-project threshold. Those are **not** v0.2 exploratory requirements. The old script already labels itself legacy; the old human role-governance draft now carries a matching legacy notice. Do not run it as the active readiness report or use its 60-case gate to reject v0.2 cases.

## 3. Case decision flow — proposal is not acceptance

The prior v0.2 case schema required `acceptance_decision="accepted"` even for a case that still needed validation and a final project-lead decision. That was circular and could make a draft look accepted too early.

The active schema and validator now distinguish:
- `proposed`: full case record can be structurally checked; final decision must be pending, with no final-decision timestamp or artifact. This status cannot enter the accepted registry.
- `accepted`: only after the project lead makes a separate explicit YES decision; the record must include a timestamped, hashed final-decision artifact. Registry validation permits only this state.
- `rejected`: the negative decision and its record may be preserved outside the accepted registry.

The validator remains structural and consistency-only. It does not verify URLs/artifacts, establish legal clearance, prove scientific truth, or authorize model execution.

## 4. Human reviewer roles are separated

Three roles must not be conflated:

1. **Project lead (Mahmut):** owns the final case and protocol decision.
2. **Technical/methodology panel reviewers:** Panel Reviewer H and Panel Reviewer B (private identity mapping is held outside the public repository) are proposed for unblinded yes/no review of case evidence and research design. The project lead reports shared agreement with the previously presented Dishka technical/gold/tier/limitations summary, but this does not substitute for either reviewer's own recorded decision.
3. **Blind model-output scorer `Rater_B`:** a separate role in the active v0.2 manifest. It is not automatically either technical panel reviewer. Anyone who sees the case issue, PR, source, patch, gold mechanism or hidden evidence-tier decision cannot be called blind to those materials for the same case's model-output scoring.

If both technical panel reviewers inspect full technical case materials, they remain valid technical reviewers but are not eligible as blinded output scorers for that case. A separate unexposed scorer or a prospectively amended scoring design is needed. ChatGPT remains advisory and is never a human rater or external auditor.

## 5. Dishka #435 — first formal acceptance candidate, not yet accepted

Dishka is the first candidate to complete the formal v0.2 case-acceptance route because:
- exact issue reproducer failed on the buggy base and passed on the fixed revision;
- all 8 frozen dataset selectors failed on the buggy base and the same 8 passed on the fixed revision;
- latest independently verified Stage 2 artifact is 14553612258 from run 44570230531; outer SHA-256 matches GitHub, ZIP CRC passes, 33 members are present, and 32/32 inner hashes pass;
- the project lead's technical gold, alternatives and E1/E2/E3 rationale approvals are recorded;
- `researcher_source_exposure = full` is disclosed; single-human-adjudicator and exploratory-only limitations remain explicit.

The project lead's corrected factual declaration is `prior_pipeline_debug_exposure = none`. The earlier `some` answer is superseded because the project lead clarified that the question had not yet been read carefully and explicitly selected NO. The correction history is preserved in `reproduction/dishka_issue_435/PROJECT_LEAD_EXPOSURE_DECISION_2026-11-19.md`. The separate full source exposure remains `full`; it is not conflated with prior pipeline/debug exposure.

Completed Dishka-specific steps:
1. The project lead approved the bounded documentary license-screen scope for the exact listed research/reproduction/test/extraction environment only; this is not legal advice or blanket redistribution approval.
2. Created the full v0.2 case JSON with exact dataset, source, test, artifact, gold and tier references; the record is `proposed`.
3. Active Draft 2020-12 schema and fail-closed case validator passed in latest no-inference preflight run `44571127276`, job `135726142556`. The actual proposed-record regression test checks the complete Dishka JSON, confirms `eligible_for_registry=false`, confirms the registry remains empty, and checks 12 in-repository document references against file hashes and immutable commit-pinned URIs.
4. Fail-closed registry validation passed as `valid_empty_registry`; accepted count remains 0.

**Only Dishka-specific decision still open:** the separate final YES/NO project-lead case-acceptance decision. Until then, Dishka is **not accepted**.

If any remaining Dishka gate fails, do not make an exception; preserve the result and move to NumPyro #1916. Case acceptance alone would still not authorize model inference or training.

## 6. Candidate fallback rule

Dishka is first because it currently satisfies the prior pipeline/debug exposure rule and has the most complete candidate-level technical and Stage 3 record. This priority does not waive its remaining gates. If Dishka's bounded license scope, evidence provenance, schema/registry checks or final project-lead decision fail, do not relax the standard; preserve the evidence and proceed to **NumPyro #1916 / PR #1918**, whose Stage 2 and packet structural checks have already passed but whose semantic adjudication remains open.

## 7. Current state

- Dishka technical Stage 2: PASS.
- Dishka gold/tier decision: project-lead approval recorded.
- Dishka accepted registry state: **not accepted**.
- Active case registry: 0.
- Prior pipeline/debug exposure: `none` (explicit corrected project-lead declaration; earlier `some` answer is preserved as superseded history).
- Bounded documentary license-screen scope: approved only for the exact listed source/reproduction/test/extraction environment; not legal advice, formal legal clearance, or redistribution approval.
- Project-wide model/license/runtime/protocol/hash and Rater_B gates: still open.
- No model load, inference, fine-tuning or training performed.


## 8. NumPyro #1916 — verified fallback candidate (19 November 2026)

- Upstream issue #1916 / fix PR #1918; dataset row `pyro-ppl__numpyro-1918`.
- Exact Stage 2 rerun: workflow run `44537219541`, NumPyro job `135605947673` completed successfully. Both frozen AIES and ESS selectors ran and met the exact buggy-base-fail/fixed-revision-pass contract.
- Latest 19 November artifact `14536697284` has GitHub-reported digest `88273ec9df2633d2d3a360e0f5c86188d92c5e87318e312a183bc77bf1071556`; independent local archive verification is not yet recorded for this newest artifact. The 18 November artifact remains independently archive-verified (ZIP CRC and 15/15 internal payload hashes passed).
- Real E1/E2/E3 packet-set SHA-256: `7156e7c0bebf694946495b638f8dd21fbe45b7fbafde2607e6cc11e8b4f9bdfc`.
- The exact real-packet structural test passed in the no-inference preflight at run `44537219541`, job `135605725983`. It asserts the external packet hash, strict nesting and exact tier additions; it also asserts that semantic sufficiency is not assessed and that no model inference occurred.
- The entire candidate workflow run concluded failure because Nox, Werkzeug and Moto candidate jobs failed their own selector contracts. The NumPyro job and no-inference preflight job themselves succeeded; do not report the full matrix as green.
- The main Stage 3 question remains open: do the two E1 source excerpts actually eliminate the plausible alternative that the ensemble sampler itself should support/map batched PRNG keys? Independent reviewers must be allowed to reject the proposed E1 tier if that alternative remains defensible.

### Reviewer eligibility boundary

The existing NumPyro Panel B protocol requires at least two independent, source-unexposed semantic reviewers who are disjoint from Panel A, the project lead and Panel Reviewer H. Reviewer H has already seen the design proposal and is explicitly ineligible for Panel B under the current protocol. Panel Reviewer B's eligibility is unknown until this reviewer completes the case-specific exposure/conflict declaration. Mahmut is the custodian and is not a blinded rater. If two eligible Panel B reviewers and a separate adjudicator cannot be appointed, keep the semantic tier review pending; do not substitute simple YES votes from people who have seen the design or code.

Panel A technical review is also separate: at least two source-aware reviewers must make independent mechanism/alternative assessments, with their initial records preserved. Reviewers cannot serve simultaneously as Panel A and Panel B for this case. Reviewer delivery must be restricted, randomized and access-logged; the public GitHub repository is not a controlled review channel.

**Next operational gate:** complete the reviewer exposure/role screen and confirm that the required independent human panel and restricted delivery route can actually be assembled. Only then prepare and deliver coded packet copies. No model load, inference or training is authorized.


## 9. Dishka exposure correction — 19 November 2026

The earlier section 5–8 entry that treated Dishka as excluded for `some` exposure has been superseded. The corrected current project-lead declaration is `prior_pipeline_debug_exposure = none`; the previous `some` answer is retained only as correction history. See `reproduction/dishka_issue_435/PROJECT_LEAD_EXPOSURE_DECISION_2026-11-19.md`.

Current active order: Dishka formal case checks first; NumPyro second if Dishka cannot pass the remaining unchanged requirements. Accepted-case count remains 0; no model load, inference or training is authorized.


## 10. Dishka proposed record validation — 19 November 2026

The proposed case file is `reproduction/dishka_issue_435/SWE_REBENCH_V2_DISHKA_435_CASE_ACCEPTANCE_PROPOSED_V0_2.json` (current SHA-256 `a23a6b23fb6a8cddde352eb415d52c62c364aa3af3a38a50da72d6c3aa40886f`). It binds the project-lead limited documentary license-scope decision, prior-exposure correction, exact dataset row/timestamp, source pins, latest reproduction artifact, human gold record and original E1/E2/E3 manifests.

GitHub Actions run `44571127276` / no-inference job `135726142556` passed. The preflight artifact is `14552969335` (SHA-256 `44b768f7d76d65c19935b88b4856ec8aacc59b691ad625113c853ade0f2ad3e9`). The v0.2 case-acceptance group passed 22 tests; the study-design/dual-human scoring group passed 10 tests. The active case validator reports `structurally_complete_candidate`; the fail-closed accepted registry validator reports `valid_empty_registry` with 0 accepted cases. The workflow's readiness report remains `ready_for_inference=false`, 14 global blockers, and no model loading/inference/fine-tuning. The separate final project-lead acceptance decision has not been made.


## 11. Dishka — superseding current case and reproduction evidence (19 November 2026)

This section controls over older hashes and artifact/run numbers in sections 5, 7 and 10.

- Canonical proposed record: `reproduction/dishka_issue_435/SWE_REBENCH_V2_DISHKA_435_CASE_ACCEPTANCE_PROPOSED_V0_2.json`.
- Current record SHA-256: `a23a6b23fb6a8cddde352eb415d52c62c364aa3af3a38a50da72d6c3aa40886f`; Git blob `d171fcaec5f5a4b8e9112e44369bd59c918885af`.
- The record has 12 in-repository evidence references, all pinned to immutable commit `13b4a0c80575cd2de9575cc884038666f34dfaa1`; latest CI regression checks each local file hash and matching URI path.
- Bounded license-scope decision SHA-256: `96f89e28ee026fcced8aca6d854770f5a0aefcb47690405f7d1a022fc9405d4d`. It remains limited to the exact listed experimental scope and is not legal clearance.
- Latest Stage 2 rerun: run `44570230531`, job `135723082451`, artifact `14553612258`; downloaded outer ZIP SHA-256 `f24f43f48b2678407b381bee40b947b5a02dd9286743c12d3a6adf728af6ba2a` matches GitHub, ZIP CRC PASS, 33 members, 32/32 inner hashes PASS. The issue reproducer is base-fail/fixed-pass and all 8 dataset selectors are base-fail/fixed-pass.
- Latest no-inference preflight: run `44571127276`, job `135726142556`, success; 22 v0.2 case acceptance tests + 10 design/scoring tests; artifact `14552969335`, SHA-256 `44b768f7d76d65c19935b88b4856ec8aacc59b691ad625113c853ade0f2ad3e9`.
- Registry: `valid_empty_registry`, accepted_case_count 0, accepted_project_count 0; proposal is not inserted.
- Dishka's single remaining case-level decision is Mahmut's separate final YES/NO. It remains `proposed`, not accepted, and cannot be counted toward the minimum feasibility case until this decision is recorded.
- Global no-inference readiness remains blocked with 14 gates. No model load, inference, fine-tuning or training has occurred or is authorized.

## 12. NumPyro — next scientific gate after Dishka preparation

NumPyro #1916 / PR #1918 remains the next candidate in the approved sequence, not an already accepted case. Stage 2 technical reproduction and packet structural validation have passed in prior runs. The open Stage 3 question remains whether the E1 excerpts genuinely eliminate the alternative mechanism that the ensemble sampler itself should support/map batched PRNG keys. An independent reviewer must be free to retain that alternative or reject the proposed E1 tier.

Do not convert an unblinded technical YES into semantic Stage 3 approval. The current reviewer protocol requires separate source-aware technical review and source-unexposed semantic rating; role, consent, exposure, conflicts, and restricted delivery route must be established first. Reviewer H is ineligible for the blind Panel B role because that reviewer has seen the design proposal; Reviewer B's eligibility is not known until a case-specific exposure/conflict declaration is completed. The project lead is the custodian, not a blind rater. If the independent human setup cannot be assembled, keep NumPyro Stage 3 pending and report that limitation rather than weakening the rubric.


## 13. Dishka latest artifact and exact case-preflight — superseding update (19 November 2026)

This section supersedes earlier latest-run IDs and artifact digests for Dishka in sections 10–11.

- Canonical proposed case JSON: `reproduction/dishka_issue_435/SWE_REBENCH_V2_DISHKA_435_CASE_ACCEPTANCE_PROPOSED_V0_2.json`; SHA-256 `0a234c0f16668e5b58dace671483d4bc94b7f8167150e44662b339dc995ff9ee`; Git blob `ec884cda706b5a66d2439ea4df60580ae26a0656`.
- The case record remains `proposed`; final acceptance remains `pending`; registry remains empty.
- Latest Dishka repeat: run `44572926370`, Dishka job `135733170187` success, artifact `14553229664`; ZIP SHA-256 `7f10db7e6f1b033eef7cd34476e3e34b3dbd28687310ccb3707ffddc5d5a6f10` independently matches GitHub; 33 members, CRC PASS, 32/32 internal hash entries PASS.
- Issue reproducer: buggy base fails `AssertionError: 1 != 42`; fixed revision passes. All 8 dataset selectors fail with defect-related failures on buggy base and the same 8 pass on fixed revision.
- The overall 13-candidate workflow run is failure because Nox, Werkzeug and Moto candidate jobs failed. This does not change the successful Dishka reproduction job.
- Same-run no-inference job `135732610579` succeeded. Preflight artifact `14554972064`, SHA-256 `b0dc39e127a375206e7fbe8613292fef6d3f4a77af56b23080b5fd5691665c61`, was independently downloaded and CRC-checked.
- The case test group passed 22 tests (including the canonical proposed record, empty registry guard and 12 immutable document-reference checks); design/scoring group passed 10 tests.
- Case validator: `structurally_complete_candidate`; registry: `valid_empty_registry`; accepted cases/projects 0. Global readiness still reports 14 blockers and `ready_for_inference=false`.

Dishka remains the first proposed case and is **not accepted**. The separate final project-lead YES/NO decision is still required. NumPyro #1916 remains fallback if Dishka is rejected or a substantive case-level defect is discovered. No model operation is authorized.


## 14. Dishka patch-pointer correction — 19 November 2026

The case record's `source.patch` URI was corrected because the mutable upstream PR diff URL did not correspond to the stored SHA-256. It now points to the exact `full-pr.diff` file inside verified artifact 14553229664 (run 44572926370), with inner SHA-256 `c5a6e5edc41d5a321fb95dc0bdb81ee449870eb53278a5d91582c2478395efde`. Outer archive SHA-256 `7f10db7e6f1b033eef7cd34476e3e34b3dbd28687310ccb3707ffddc5d5a6f10`; CRC PASS; 32/32 internal hashes PASS. The 90-day retention and exact regeneration command are documented in `DISHKA_435_PATCH_REFERENCE_RECONCILIATION_2026-11-19.md`.

Current canonical case JSON SHA-256 is `0a234c0f16668e5b58dace671483d4bc94b7f8167150e44662b339dc995ff9ee` (blob `c17d908a937c32c7372d1eb19bb9b29990b338e2`). It remains proposed, with the separate final project-lead decision pending. Registry remains 0 accepted cases; global readiness remains blocked.

## 15. Current execution update — Dishka-only focus and global gate plan (19 November 2026)

- The automatic main preflight now keeps the no-inference tests and Dishka reproduction active by default; its 12 other candidate jobs require an explicit manual-dispatch input.
- Separate non-Dishka Stage 2 candidate workflows are being changed to manual-dispatch-only so shared research-file edits do not start unrelated candidate reproductions.
- Latest Dishka Stage 2 job: run `44596435482`, job `135816057850`, artifact `14564379897`; ZIP and 32/32 internal hashes verified; independent reproducer and 8/8 selectors remain base-fail/fixed-pass.
- Latest no-inference preflight job: run `44596435482`, job `135815854250`; 76 tests passed. Readiness remains blocked with 14 global gates, 0 accepted cases and 0 accepted projects.
- The pinned Qwen revision LICENSE/config evidence was collected without downloading weights (artifact `14565807914`); human/mentor research-use review remains pending.
- Dishka raw issue/PR and dataset-card responses were captured in artifact `14566406023`; the first validator script failed on a regex syntax error. Manual inspection confirms the Dishka PR timestamp matches the frozen row and the pinned dataset card declares CC-BY-4.0. A corrected rerun is required before treating the workflow audit as passed.
- Case acceptance remains pending and must not be inferred from Stage 2 success, archive integrity, or structural validation.
- The detailed 14-gate owners, evidence requirements and closure order are recorded in `DISHKA_AND_V02_PROJECT_GATE_CLOSURE_PLAN_2026-11-19.md`.

## 16. Verified successful Dishka-only run — 19 November 2026

The corrected workflow now completes successfully on PR head `fb7d17633458978406cdc4a37750752f93658e16`:

- Run [44599553076](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44599553076): **success**.
- no-inference preflight: 76 tests passed; readiness still 14 blockers and 0 accepted cases.
- Dishka reproduction passed and its new archive is independently verified (33 members, CRC PASS, 32/32 inner hashes).
- Dishka raw provenance passed and its archive is independently verified (12 members, CRC PASS, 11/11 inner hashes); PR timestamp matches the frozen row.
- Qwen pinned license/config capture passed; archive 9/9 inner hashes; no weights or model load.
- The 12 non-Dishka candidate jobs were skipped. All separate candidate-specific PR workflows in the run were also skipped by their dispatch-only guard.
- Dishka remains proposed and final acceptance pending; no model inference is authorized.

## 17. Latest final verification — 19 November 2026

PR #222 head `ef89cd9bbc04531f576a3b46ce00b1ff524f7274` was checked end to end:

- Focused workflow [44600772416](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44600772416): **success**.
- Dishka reproduction, raw Dishka provenance, Qwen license evidence and no-inference preflight: all **success**.
- Other 12 candidate jobs: **skipped**.
- 76 no-inference contract tests passed; separate repository/config validation, unit tests (171) and CPU tests also passed.
- Dishka Stage 2 archive [14566758994](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44600772416/artifacts/14566758994): SHA-256 `1bc714ec60e6315907d8273b5842891953af7ba4296d785ba29603feb4d6eed6`, CRC PASS, 33 members, 32/32 internal hashes.
- Dishka raw provenance [14567568737](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44600772416/artifacts/14567568737): SHA-256 `f099a1e5b8a0a0da45b706b162a634a4a4f9b5c3c4d2335e12389a1cf916f8b9`, CRC PASS, 12 members, 11/11 internal hashes.
- Qwen pinned license capture [14566504228](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44600772416/artifacts/14566504228): SHA-256 `a1357b695ef01cc15277260f578a99e4f3bcc495faf6ccfe149a514014a1bf0c`, CRC PASS, 10 members, 9/9 internal hashes.
- Readiness remains 14 blockers, 0 accepted cases, valid empty registry; no model inference authorization.
- Dishka candidate remains proposed; final project-lead YES/NO acceptance decision remains pending.

## 18. Last checked run before final acceptance — 19 November 2026

PR head `dcea5055b086644a3b1b3307a3be38e59740b67f` has a fully successful Dishka-focused pipeline:

- Run [44602442485](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44602442485): **success**.
- Dishka reproduction, raw provenance, Qwen license capture and no-inference preflight: all success.
- Other 12 candidate jobs: skipped.
- Preflight tests: 76 passed; global readiness remains 14 blockers, 0 accepted cases, 0 accepted projects.
- Dishka artifact [14569001619](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44602442485/artifacts/14569001619): CRC PASS, 33 members, 32/32 internal hashes.
- Raw provenance artifact [14567824500](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44602442485/artifacts/14567824500): CRC PASS, 12 members, 11/11 internal hashes.
- Qwen evidence artifact [14569350314](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44602442485/artifacts/14569350314): CRC PASS, 10 members, 9/9 internal hashes.
- Separate repo validation, 171 unit tests and CPU tests passed.
- Case record remains proposed; final YES/NO acceptance is the sole Dishka-specific project-lead step; no inference is authorized.

## 19. Dishka acceptance and next sequential candidate — 20 November 2026

- The project lead recorded **YES** for `SRV2E-DISHKA_435`, accepted into the v0.2 exploratory/feasibility registry only. The final decision record is `reproduction/dishka_issue_435/PROJECT_LEAD_FINAL_ACCEPTANCE_DECISION_DISHKA_435_2026-11-20.md`.
- The project lead additionally reports that Hasan asked/recommended acceptance. This is supplementary reported input only; no separate signed statement or independent technical adjudication is claimed. The formal decision remains the project lead's.
- The case record, exploratory registry, manifest and progress ledger are reconciled to one accepted case from one upstream project. The no-inference CI run must validate the amended documents and tests before the repository state is called technically verified.
- The next sequential independent-project candidate is **NumPyro #1916 / PR #1918** (`pyro-ppl/numpyro`), as listed in the progress ledger. This supersedes earlier wording that NumPyro was only a fallback if Dishka failed; Dishka has now been accepted, so NumPyro is the next intake candidate.
- NumPyro Stage 2 reproduction and E1/E2/E3 packet integrity have been demonstrated, but semantic sufficiency of the tiers, fork/lineage and exposure screens, human dependency/license-scope acknowledgement, and a schema-conformant case record remain open. E1 must not force a unique mechanism if the sampler-contract alternative remains plausible.
- Model weights must not be downloaded; model loading, inference, fine-tuning and training remain prohibited. Dishka acceptance does not change this restriction.

## 20. Post-Dishka validation and NumPyro next-candidate update — 20 November 2026

Dishka #435 acceptance was validated by Research Validation run 44727985114 (452 passed, 6 skipped, 56 subtests passed) and no-inference preflight run 44727984941. The v0.2 registry is structurally valid with one accepted exploratory case from one upstream project. Global readiness remains blocked by 13 gates; inference remains unauthorized.

NumPyro #1916 / PR #1918 is the next sequential intake candidate. A separate proposed v0.2 packet set adds the pinned buggy-base EnsembleSampler.init excerpt to E1 (the sampler takes a batch for chain count, then selects rng_key[0] and stores a scalar state key). Proposed set SHA-256: e1730956eb9cfc9015bb43c5725f49d3ebff9dfc3c564594060209bab5e5485d. The prior 19 November set is preserved. Proposed structure has E3=1, E2=2, E1=5; CI validation and independent semantic adjudication remain pending.

The project lead and Hasan are both source/design exposed for this case and are not eligible for blinded Panel B. Two independent, consented, source-unexposed Panel B reviewers and a separate adjudicator are required by the approved protocol. Source/dependency licensing and upstream issue-family independence are also open. Do not accept the candidate or authorize inference before these gates close.
