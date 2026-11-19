# Human review panel — yes/no decision packet v0.1 (19 November 2026)

**Study:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Purpose:** obtain explicit, attributable human decisions on the research design, candidate acceptance path, two second-pass reconsiderations, human-evaluator roles, and the separate model-training study.

**This packet is for review only. It does not accept a case, close a legal gate, authorize model use, or authorize training.**

## 1. Proposed review team and authority

| Person / role | Proposed responsibility | Boundary |
|---|---|---|
| Mahmut — student project lead | Own protocol, maintain source records, propose candidate decisions, record deviations, and make the final project-lead decision | Has prior source exposure to screened candidate issues/patches; must not be described as blinded |
| Panel Reviewer H | Independent technical/methodology review; proposed for Hasan | Not automatically a legal reviewer, external auditor or blind output rater |
| Panel Reviewer T | Independent technical/methodology review; proposed for Batuhan | Not automatically a legal reviewer, external auditor or blind output rater |
| Rater B | Separate role in the active v0.2 manifest for independent blind model-output scoring; no individual is assigned by this packet | Must not be conflated with Panel Reviewer H or T; requires separate consent and case-specific exposure screen |
| ChatGPT | Research-assistant critique, structured evidence and reproducibility support | Not a human reviewer, not a voting member, not a human rater, and never counted for inter-rater reliability |

The two reviewers' public identities are kept pseudonymous in repository records. Their participation, expertise/role, and per-case exposure are not assumed; they must be confirmed directly.

## 2. Critical role separation before sharing case materials

Each reviewer must choose a role for each candidate before receiving its full packet:

- **Full technical case review:** reviewer may see issue, source, patch, tests, gold mechanism and E1/E2/E3 material. They can assess technical scope and candidate acceptance. They cannot later be described as blinded to those materials when scoring that case's model response.
- **Blind model-output scoring:** reviewer sees only the exact evidence packet visible to the model and a randomized raw response ID. They must not see repository/issue/PR, source patch/fixed source, hidden gold, hidden E1/E2/E3 label, P0/P1 identity, paired response, or another rater's score. They must not take part in full technical case review for that case.
- **Protocol-only review:** reviewer assesses the study design/rubric without case identities, patches, gold, or outputs. This can preserve eligibility for later blind output scoring if they remain unexposed.

If both Panel Reviewer H and Panel Reviewer T review full case sources, neither may be claimed as a blinded scorer for those cases. The active v0.2 role Rater B must then be a different, unexposed person, or the scoring plan must be prospectively amended before model outputs are generated. Do not make a false blinding claim just to preserve a dual-rater plan.

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
| D10 | The first case should be Dishka #435, subject to its formal record and final gates | Proceed to prepare the full acceptance record; do not mark accepted until schema, registry and final project-lead decision pass |

## 5. Candidate-specific decisions requested

### C1 — Dishka #435 / PR #436 (first acceptance candidate)

Evidence already recorded:
- Exact dataset selectors: 8/8 actual defect failures on buggy base and 8/8 passes on fixed revision.
- Independent issue reproducer: buggy-base failure / fixed-revision pass.
- Project-lead technical gold, alternatives and E1/E2/E3 design approval.
- Researcher full source exposure and single-human-adjudicator limitations disclosed and acknowledged.
- Stage 3 technical adjudication completed.

Open before formal acceptance:
- Build the complete v0.2 case record with exact dataset row, source, artifact hashes, timestamp evidence, independence/exposure, documentary license scope and tier manifests.
- Run Draft 2020-12 schema validation and fail-closed registry checks.
- Record a separate final project-lead acceptance decision.
- Keep model inference/training unauthorized until the independent global gates also pass.

**Question:** approve Dishka as the first case to complete formal acceptance checks, without pre-accepting it? YES / NO / REVISE.

### C2 — NumPyro #1916

- Stage 2 exact selectors: 2/2 buggy-base failures and 2/2 fixed passes.
- Nested E1/E2/E3 packet set has been created.
- Real-packet structural CI check and independent semantic review remain pending.
- Dependency/native component notice scope, independence and exposure review remain open.

**Question:** prioritize NumPyro as the next Stage 3 case after Dishka? YES / NO / REVISE.

### C3 — Remaining Stage 2 technical passes

The current 15-pass list is: Dishka, NumPyro, Dymos, EODAG, SkyPilot, Napalm, PyThaiNLP, Modin, Robocop, Meltano, Amaranth, CTAPIpe, Python-Control, QuTiP and PyFar.

A Stage 2 pass means only that a pinned technical reproduction contract passed. It does not mean the candidate is invalid or unusable. Fourteen are eligible for continued Stage 3/provenance/exposure review, each subject to its own gates. CTAPIpe is different: the project lead recorded prior candidate-specific pipeline/debug exposure as `some`; the current protocol requires `none` for model-evaluation inclusion. Keep CTAPIpe as an engineering/feasibility pilot, not a model-evaluation case, unless a prospectively revised protocol and independent review establish a scientifically defensible alternative.

| Candidate | Why it is not accepted yet | Proposed next step |
|---|---|---|
| Dishka | Formal acceptance record, schema/registry and separate final decision | First priority |
| NumPyro | Packet structural CI, blind semantic review, dependency/native notices, independence/exposure | Second priority |
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

**Question:** approve this as the priority order after Dishka and NumPyro, while retaining every candidate's current gates? YES / NO / REVISE.

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

## 7. Priority order approved for project execution (subject to review feedback)

1. Finish Dishka's formal acceptance record and checks; keep registry at zero until the separate final decision.
2. Complete NumPyro's packet structural test, then independent semantic review.
3. Progress other Stage 2 passes through Stage 3 and candidate-specific provenance/license/exposure checks.
4. Execute PSyclone #2755 Stage 2 after the project lead manually confirms the exact workflow inputs; discovery and environment lock alone are not Stage 2.
5. Run the two candidate reconsideration checks (dbt and SimPEG) without changing the frozen cohort selectors.
6. Close global source/timestamp, protocol freeze, human reviewer consent, model license and runtime gates.
7. Only then authorize the primary P0/P1 inference study.
8. The separate LoRA training study follows only when its higher, project-disjoint dataset gate is met and separately authorized.

## 8. Decision record template — one copy per technical panel reviewer

- Reviewer pseudonym (Panel Reviewer H or Panel Reviewer T):
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


## 9. Role-conflict correction — 19 November 2026

The initial draft used “Reviewer B” for Batuhan while the active v0.2 manifest separately uses the technical role code `Rater_B` for a future blinded model-output scorer. Those labels could be mistaken for the same person/role. They are now explicitly separated:

- Panel Reviewer H and Panel Reviewer T are the two proposed technical/methodology reviewers (Hasan and Batuhan respectively).
- `Rater_B` remains an unassigned role for a separate blind model-output scorer.
- A panel reviewer who sees a case's issue/PR/source/patch/gold/tier material is not eligible to be called blinded to those materials for that case's output scoring.
- The technical reviewers' yes/no recommendations are advisory evidence for the project lead; they do not automatically populate the accepted registry and do not constitute legal clearance.
- The project lead reports shared agreement with the previously discussed Dishka technical/gold/tier/limitations proposal. Individual reviewer decisions and signatures are not fabricated; any formal concurrence record must be based on the reviewers' actual submitted decisions.
