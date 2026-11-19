# Human review panel — yes/no decision packet v0.1 (19 November 2026)

**Study:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Purpose:** obtain explicit, attributable human decisions on the research design, candidate acceptance path, two second-pass reconsiderations, human-evaluator roles, and the separate model-training study.

**This packet is for review only. It does not accept a case, close a legal gate, authorize model use, or authorize training.**

## 1. Proposed review team and authority

| Person / role | Proposed responsibility | Boundary |
|---|---|---|
| Mahmut — student project lead | Own protocol, maintain source records, propose candidate decisions, record deviations, and make the final project-lead decision | Has prior source exposure to screened candidate issues/patches; must not be described as blinded |
| Panel Reviewer H | Independent technical/methodology review; identity mapping held outside the public repository | Not automatically a legal reviewer, external auditor or blind output rater |
| Panel Reviewer B | Independent technical/methodology review; identity mapping held outside the public repository | Not automatically a legal reviewer, external auditor or blind output rater |
| `Rater_B` | Separate, currently unassigned role in the active v0.2 manifest for blind model-output scoring | Not the same as Panel Reviewer B; requires a different unexposed person or a prospective protocol amendment |
| ChatGPT | Research-assistant critique, structured evidence and reproducibility support | Not a human reviewer, not a voting member, not a human rater, and never counted for inter-rater reliability |

The repository uses only the pseudonyms Reviewer H and Reviewer B. Identity mappings are kept outside public-facing records. Each reviewer's willingness, relevant expertise, assigned scope and case-specific prior exposure must be confirmed directly before a review is treated as completed.

## 2. Critical role separation before sharing case materials

Each reviewer must choose a role for each candidate before receiving its full packet:

- **Full technical case review:** reviewer may see issue, source, patch, tests, gold mechanism and E1/E2/E3 material. They can assess technical scope and candidate acceptance. They cannot later be described as blinded to those materials when scoring that case's model response.
- **Blind model-output scoring:** reviewer sees only the exact evidence packet visible to the model and a randomized raw response ID. They must not see repository/issue/PR, source patch/fixed source, hidden gold, hidden E1/E2/E3 label, P0/P1 identity, paired response, or another rater's score. They must not take part in full technical case review for that case.
- **Protocol-only review:** reviewer assesses the study design/rubric without case identities, patches, gold, or outputs. This can preserve eligibility for later blind output scoring if they remain unexposed.

If both technical reviewers inspect a case's issue/source/patch/gold/tier packet, neither may later be counted as blinded to those materials when scoring that case's model output. The separate `Rater_B` role must be filled by another unexposed person, or the scoring plan must be amended prospectively before outputs are generated. Do not make a false blinding claim just to preserve a dual-rater plan.

## 3. Reviewer declaration — required before case-level review

Each human reviewer should answer separately for each proposed case:

1. Have you previously seen its issue, PR, repository, or source code? YES / NO / UNSURE
2. Have you seen its fix patch, fixed revision, regression test, or reproduction logs? YES / NO / UNSURE
3. Have you helped debug, reproduce, or construct tests for this exact candidate? YES / NO / UNSURE
4. Have you seen the candidate's gold mechanism, E1/E2/E3 labels, or adjudication notes? YES / NO / UNSURE
5. Have you seen any model-generated response or its P0/P1 condition? YES / NO / UNSURE
6. Can you agree not to discuss your independent decision with other reviewers until your original review is recorded? YES / NO
7. Are you willing to perform the role assigned to you and have your role/decision recorded under a pseudonym? YES / NO

A YES to prior exposure does not automatically disqualify a technical reviewer; it does disqualify a claim that the person is blind to the exposed material. Any uncertain answer remains unresolved until clarified.

## 4. Study-level decisions requested

Each reviewer returns YES / NO / REVISE / OUT OF SCOPE with a short reason. Mahmut records the final project-lead decision separately.

| ID | Decision proposal | What a YES means |
|---|---|---|
| D1 | The primary research question is scientifically meaningful and falsifiable | Test the effect of permitting abstention under insufficient visible evidence, not whether the model “knows” its own uncertainty |
| D2 | The primary P0/P1 comparison must use identical frozen model weights, tokenizer, runtime and generation settings | Weight changes are not confounded with the policy effect |
| D3 | Evidence support and hidden-gold correctness must be scored separately | A correct guess is not automatically a supported diagnosis |
| D4 | The v0.2 exploratory sample policy is appropriate | Minimum one accepted case for case-level feasibility; primary target 15 distinct upstream projects; stretch target 20; keep all unchanged-criteria cases if fewer than 15 pass |
| D5 | The strict acceptance requirements must not be relaxed to reach the sample target | Invalid selectors, mixed-scope rows, exposure and license issues cannot be waived to increase N |
| D6 | The secondary LoRA study is a separate hypothesis and must not replace the primary P0/P1 experiment | Training is assessed only against a project-disjoint holdout after its higher data gate |
| D7 | The planned train/validation/test split of 60/10/10 from at least 80 accepted independent projects is a reasonable minimum proposal for the secondary training study | The locked test projects remain unseen during training and tuning |
| D8 | The human-evaluation workflow and exposure rules are acceptable | Roles, consent, calibration and blinding claims match what each reviewer actually saw |
| D9 | The use of a pinned Qwen research-license model is acceptable in principle for the planned non-commercial research | This is a research-scope recommendation only, not legal clearance or permission to redistribute weights/adapters |
| D10 | Dishka #435 should remain the first case to complete formal acceptance checks after the corrected exposure declaration, subject to all remaining gates | Proceed with the proposed case record and checks; do not pre-accept. If a gate fails, move to NumPyro #1916 |

## 5. Candidate-specific decisions requested

### C1 — Dishka #435 / PR #436 (first formal acceptance candidate; not accepted)

The project lead has clarified the earlier exposure answer. The current factual value is `prior_pipeline_debug_exposure = none`; the earlier `some` response is superseded and retained only in the correction history. The separate `researcher_source_exposure = full` remains disclosed. This satisfies the prior pipeline/debug exposure gate but does not close any other acceptance requirement.

Already recorded: exact 8/8 frozen selector base-fail/fixed-pass, an independent issue reproducer base-fail/fixed-pass, approved technical gold/alternatives/E1-E2-E3 rationale, and independent archive/hash checks.

Remaining steps: bounded documentary license-scope sign-off, complete proposed v0.2 case record, Draft 2020-12 schema validation, fail-closed registry validation, resolve all mismatches, then a separate final project-lead YES/NO decision. A YES to this C1 item authorizes proceeding with those checks only; it does not accept the case.

**Question:** approve Dishka as the first case to complete formal acceptance checks under the unchanged protocol, without pre-accepting it? YES / NO / REVISE.

### C2 — NumPyro #1916

- Stage 2 exact selectors: 2/2 buggy-base failures and 2/2 fixed passes.
- Nested E1/E2/E3 packet set has been created.
- Real-packet structural CI check and independent semantic review remain pending.
- Dependency/native component notice scope, independence and exposure review remain open.

**Question:** approve NumPyro as the fallback candidate if Dishka fails a remaining gate, subject to strict semantic-review, independence and license requirements? YES / NO / REVISE.

### C3 — Remaining Stage 2 technical passes

The current 15-pass list is: Dishka, NumPyro, Dymos, EODAG, SkyPilot, Napalm, PyThaiNLP, Modin, Robocop, Meltano, Amaranth, CTAPIpe, Python-Control, QuTiP and PyFar.

A Stage 2 pass means only that a pinned technical reproduction contract passed. It does not mean the candidate is accepted or automatically usable. CTAPIpe #2732 remains excluded from model evaluation because its prior candidate-specific pipeline/debug exposure is `some`. Dishka #435 has a corrected prior pipeline/debug exposure value of `none` and may continue formal case checks; its researcher source exposure remains `full`. Therefore 14 of the 15 Stage 2 technical passes remain in the further-review queue, each subject to its own Stage 3/provenance/independence/license gates. CTAPIpe is not counted in the model-evaluation sample; Dishka is not yet accepted.

| Candidate | Why it is not accepted yet | Proposed next step |
|---|---|---|
| Dishka | Full proposed case record, bounded license scope, schema/registry checks and separate final decision remain open | First priority; do not pre-accept |
| NumPyro | Semantic review, dependency/native notices, independence/exposure and final acceptance remain open; structural packet CI passed | Fallback if Dishka fails a gate |
| Dymos | Stage 3 gold/alternatives/E tiers and dependency/license/human review | Stage 3 |
| EODAG | Stage 3 gold/E tiers, related-issue and dependency-license review | Stage 3 |
| SkyPilot | Stage 3, dependency scope, independence and exposure | Stage 3 |
| Napalm | Cisco NX-OS fixture provenance/redistribution and dependency license scope | Resolve fixture provenance or maintain hold |
| PyThaiNLP | ICU/native dependency license scope, independence and Stage 3 | Human license-scope review then Stage 3 |
| Modin | Issue title says AutoSwitchBackend ON; PR and frozen selectors test OFF/False | Human issue-scope reconciliation; keep conditional |
| Robocop | Stage 3 gold/E tiers and pathspec/dependency license compatibility review | Stage 3 |
| Meltano | Stage 3 gold/E tiers, exact dependency/license screen and independence | Stage 3 |
| Amaranth | Issue/PR near model release; temporal/model exposure assessment and Stage 3 | Human exposure decision first |
| CTAPIpe | Prior pipeline/debug exposure recorded as some | Engineering pilot only; exclude from main model-evaluation sample |
| Python-Control | Stage 3 gold/E tiers and dependency scope | Stage 3 |
| QuTiP | Stage 3 gold/alternatives/E tiers and dependency license scope | Stage 3 |
| PyFar | Stage 3 gold/E tiers and updated netCDF4/cftime dependency notice review | Stage 3 |

**Question:** approve this as the priority order, keeping Dishka first and NumPyro as fallback, while retaining every candidate's current gates? YES / NO / REVISE.

### C4 — Databricks dbt-databricks #994 / PR #995 (second-pass exclusion reconsideration)

Earlier rejection was made by the project's internal second-pass technical screen, not by an external jury. Its PR tests are insensitive to the reported defect: one passes on the buggy code; the other uses `re.match` and fails to inspect the UUID characters after the leading underscore; neither tests session-close cleanup.

Proposed route: independently author a deterministic issue-specific reproducer from the issue's observable invalid-identifier/cleanup behavior; run exact buggy base vs fixed commit; preserve original selectors untouched; treat this as supplemental unless the reviewers approve a documented protocol amendment.

**Question:** authorize that independent-reproducer feasibility check? YES / NO / REVISE.

### C5 — SimPEG #1609 / PR #1633 (second-pass exclusion reconsideration)

Earlier rejection was also made by the project's internal second-pass screen, not by an external jury. A new review of the original issue shows that the report itself acknowledges the expected survey-level value is ambiguous when receivers have different components. PR #1633 deprecates the property because using only the first receiver is misleading and directs callers to iterate receivers.

Proposed route: review it as an ambiguous API-contract defect, not as an “integer-return” bug. Authenticate the original selectors and demonstrate the deprecation contract on exact buggy/fixed revisions; independently adjudicate the gold and alternatives. Keep it supplemental/conditional until reviewers approve the framing and original selector alignment.

**Question:** reopen the issue-scope/oracle review under this reframed contract? YES / NO / REVISE.

## 6. Legal, license and provenance review boundary

Reviewers may inspect repository LICENSE files, SPDX headers, dependency inventories, notices, fixtures, source provenance and intended research use, then recommend whether the documentary scope appears acceptable.

They must not record “legal clearance” unless they are qualified and authorized to provide it. Package metadata or a root LICENSE file does not automatically clear transitive native libraries, generated fixtures, notices, redistribution, model weights or adapters.

For unresolved questions, the valid answer is **OUT OF SCOPE / external legal review required**, not an assumed YES.

## 7. Priority order proposed for project execution (subject to reviewer feedback and project-lead gates)

1. Complete Dishka's formal proposed-case record, bounded license-scope decision, schema/registry checks and separate final decision. Keep the registry unchanged until a separate YES and clean validators.
2. NumPyro is the fallback if Dishka fails a remaining gate: its real-packet structural CI test has passed; proceed to independent semantic review only after reviewer-role and exposure prerequisites are satisfied.
3. Progress the remaining Stage 2 technical passes through Stage 3 and candidate-specific provenance/license/exposure checks; retain each candidate's individual hold and do not equate technical PASS with acceptance.
4. Execute PSyclone #2755 Stage 2 after the project lead manually confirms the exact workflow inputs; discovery and environment lock alone are not Stage 2.
5. Re-review dbt and SimPEG as separate conditional candidates using independently authored, defect-sensitive tests; do not edit the frozen cohort selectors or restore either to the primary cohort without a versioned protocol/ledger decision.
6. Close global source/timestamp, protocol freeze, evaluator consent/role separation, exact model-license and runtime gates. A documentary license screen is not legal clearance.
7. Only after all case-level and global gates pass, and after an explicit separate authorization, consider the primary P0/P1 inference study.
8. Keep LoRA training disabled. Consider it only after its higher project-disjoint dataset gate is met, a separate protocol is frozen, and separate explicit authorization is recorded.

## 8. Decision record template — one copy per technical panel reviewer

- Reviewer pseudonym (Panel Reviewer H or Panel Reviewer B):
- Date:
- Proposed role for this review:
- Relevant expertise / scope:
- Candidate exposure declarations completed: YES / NO
- Protocol decisions D1–D10: YES / NO / REVISE / OUT OF SCOPE + rationale
- Candidate decisions C1–C5: YES / NO / REVISE / OUT OF SCOPE + rationale
- License questions marked OUT OF SCOPE where appropriate:
- Any conflicts or prior involvement:
- Reviewer consent to be identified by pseudonym in the research record: YES / NO

Mahmut's final project-lead decision and rationale must be recorded separately after the independent reviewer responses. No reviewer decision is presumed from silence.


## 9. Role mapping and decision boundary — corrected 19 November 2026

- Reviewer H and Reviewer B are pseudonyms only. Their actual consent, relevant expertise and case-specific exposure declarations remain pending until each person answers.
- `Rater_B` is a separate v0.2 scoring-role identifier. It is not the same role as Panel Reviewer B and must not be filled by a technical reviewer who has seen the hidden gold or case materials for that same case.
- A technical YES means “recommend proceeding under the stated gates”; it does not mean the case is accepted, the license is legally cleared, or inference is authorized.
- The earlier Dishka exclusion was based on an exposure answer later clarified by the project lead. The current prior pipeline/debug value is `none`; Dishka is first for formal checks and NumPyro is fallback. This route is a prioritization decision, not semantic approval or case acceptance.
- Reviewer decisions must be recorded only after each reviewer actually submits their own answers. No individual vote, consent or concurrence is inferred from the project lead's statement.


## 10. Candidate transition update — 19 November 2026

The project lead has clarified Dishka prior pipeline/debug/test-oracle exposure as `none`; the earlier `some` response is superseded and retained in the correction-history record. C1 is reinstated as the first formal acceptance-review path, but Dishka remains not accepted until every remaining gate and the separate final decision pass.

NumPyro #1916 is the fallback candidate. Its Stage 2 reproduction is passed, and the real E1/E2/E3 packet-set structural test passed in run `44537219541`. Semantic sufficiency remains unadjudicated. The NumPyro review protocol requires two Panel A technical reviewers, two disjoint source-unexposed Panel B raters, a separate disagreement adjudicator, restricted delivery and exposure/consent records. Panel Reviewer H is not eligible for Panel B because this reviewer has seen the design proposal; Panel Reviewer B's eligibility is not yet established. A simple YES/NO endorsement is not a substitute for the required free-form causal-mechanism ratings.


## 11. Superseding Dishka exposure correction — 19 November 2026

The project lead clarified the earlier exposure answer after reading the question and explicitly confirmed `prior_pipeline_debug_exposure = none`. The earlier `some` entry is preserved as superseded correction history. The current value and audit trail are in `reproduction/dishka_issue_435/PROJECT_LEAD_EXPOSURE_DECISION_2026-11-19.md`.

Dishka therefore remains the first case for formal v0.2 proposed-record and acceptance checks. It is **not accepted**. NumPyro #1916 is fallback if a remaining Dishka gate fails. CTAPIpe #2732 remains separately excluded because its prior exposure is still `some`.
