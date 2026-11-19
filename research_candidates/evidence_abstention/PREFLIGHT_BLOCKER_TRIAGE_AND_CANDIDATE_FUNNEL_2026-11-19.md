# Preflight blocker triage and candidate funnel — 19 November 2026

**Active branch:** `research/2026-11-16-followup-evidence-validation`  
**Latest inspected preflight:** [run 44531400493](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44531400493), job `135585362885`  
**Readiness:** `ready_for_inference=false`; 14 reported blockers; 0 accepted cases; no model load, inference, fine-tuning or training performed.

## 1. What the 14 blockers mean

These are fail-closed readiness gates, not 14 failing unit tests and not 14 source-code bugs. The no-inference job passed its five test groups (67 tests total); the gate remains closed because required evidence, decisions, and frozen documents are absent.

The list has overlapping roll-up entries: blocker 1 summarizes blockers 2–3; blocker 7 summarizes the freeze state of blockers 8–12. Therefore, 14 is the reported gate count, not 14 independent root causes.

| # | Current preflight message | Why it blocks | Can it be resolved? / evidence needed |
|---:|---|---|---|
| 1 | Dataset validation gate open: source provenance/license and raw timestamp authentication incomplete | Aggregate guard for candidate source and timestamp evidence | Yes, by closing #2 and #3 without weakening cohort rules |
| 2 | Upstream source and changed-file license review not closed | Dataset CC-BY metadata does not license upstream code, fixtures, notices or native/dependency components | Partly systematic, partly human: exact base LICENSE, changed paths, bundled notices, fixtures and runtime dependency review; preserve a project-lead scope decision |
| 3 | Timestamp provenance not authenticated against raw upstream payloads | A timestamp copied from the wrong resource (issue vs PR) can create false chronology | Yes: retain raw resource-type-matched API payloads, canonical URLs, retrieved-at timestamps and SHA-256; compare PR-derived rows to PR resource timestamps and issue-derived rows to issue timestamps |
| 4 | Exact immutable model revision license/use not approved | The pinned model identifies as `qwen-research`; this is not an Apache-2.0 license | Human scope assessment required. The exact pinned LICENSE says non-commercial use is for research/evaluation only and specifies redistribution/attribution conditions. TÜBİTAK submission, report, adapter and any public distribution must be reviewed against the exact text; do not assume clearance |
| 5 | Exact model/tokenizer/runtime not verified | The candidate runtime lock is not an inspected successful verification of the exact checkpoint/tokenizer and environment | Yes after #4: freeze Python/PyTorch/Transformers/Accelerate, GPU/runtime details, tokenizer/model revision and file identities; conduct the specifically authorized no-output preflight only |
| 6 | Generation settings draft and not frozen | P0/P1 comparison would be irreproducible if decoding or output rules changed after seeing results | Yes: freeze one response per cell, decoding, token limit, stop rules, prompt versions, schema, no retry/no repair, seed policy and output capture |
| 7 | Protocol, analysis plan, generation and scoring rules not hash-frozen | No immutable pre-outcome record exists for the experiment | Yes after the underlying decisions are final; hash every active protocol artifact and validate the freeze manifest |
| 8 | Study design decision v0.2 not frozen | Working study type/sample policy may still change | Yes: approve final text, SHA-256 and manifest entry |
| 9 | v0.2 protocol not frozen | Case eligibility, evidence tiers, conditions and scoring procedure must be immutable before outcomes | Yes: final review, SHA-256, manifest entry |
| 10 | v0.2 analysis plan not frozen | Endpoints, exclusions, missing/invalid output handling and statistics must be set before scoring | Yes: freeze the exact plan and analysis code/version |
| 11 | Human evaluator amendment not frozen | Rater roles, blinding, consent and exposure rules are still draft | Yes after Rater B decision; freeze the agreed governance document |
| 12 | Dual-human scoring rubric not frozen | Rater B and project lead need the same calibrated rubric before output scoring | Yes after separate calibration; freeze rubric and examples before study outputs are scored |
| 13 | Rater B consent and case-specific independence/exposure screening not confirmed | The current v0.2 plan promises two-human output scoring, but the second person's participation and blindness cannot be assumed | Requires a real person's explicit consent and per-case exposure/independence screen, then separate calibration. If unavailable, only a deliberate pre-outcome protocol amendment to a single-rater exploratory design could change this; do not claim inter-rater reliability |
| 14 | No accepted case registered; at least one fully accepted independent case required before inference | Stage 2 PASS and Stage 3 draft do not equal final case acceptance | Yes: complete a case record, validate Draft 2020-12 schema and fail-closed registry, then obtain the project lead's separate final acceptance decision |

**Important version clarification:** The current gate is v0.2 exploratory/feasibility. It does not apply the superseded v0.1 requirements (such as mandatory 60 accepted cases or external preregistration). The v0.2 minimum is one fully accepted case for case-level feasibility; the primary target is 15 independent upstream projects and the stretch target is 20. The proposed secondary training study has a separate higher threshold and does not inherit the primary inference minimum.

## 2. Candidate count — frozen 96-row primary cohort

The machine-readable cohort ledger contains 96 primary records from 96 distinct upstream repositories. Its funnel is:

| Bucket | Count | Interpretation |
|---|---:|---|
| Primary frozen cohort | 96 | Candidate metadata, not accepted cases |
| Static exclusions | 29 | Enhancement, feature addition, non-production/test-only change, or otherwise outside the strict bug-root-cause pool |
| Additional second-pass exclusions | 2 | Defect-insensitive test oracle or mixed/unsuitable scope |
| Remaining broad primary shortlist | **65** | Still in the technical/review queue; not 65 validated defects |
| Stage 2 technical passes within the 65 | 15 | Exact technical base-fail/fixed-pass evidence recorded; Stage 3/final gates remain |
| Stage 2 not started | 42 | Work remains |
| Stage 2 blocked or held | 8 | Specific row, fixture, scope or test-oracle issue must be resolved or candidate remains out |
| Stage 3 technical adjudication completed | 1 | Dishka #435 |
| Final accepted cases | **0** | Registry remains empty |

The equation is `65 = 15 + 42 + 8`. The separately tracked reserve pool contains **17 additional distinct upstream projects**, so there are **82 primary-shortlist plus reserve candidates** in the wider intake pipeline. The 148 within-project alternatives are replacement options within their existing projects; they do not add 148 independent projects.

### Stage 2 blocked/held candidates in the 8-count

- Earthkit-data: external GRIB fixture bytes/hash/terms and CF metadata provenance.
- Nox: 3 malformed/missing selectors in an immutable 27-selector row; 24/27 alone cannot be called a complete row pass.
- Moto: 18 selectors, only one issue-specific ECR selector; remaining IoT selectors make the row mixed-scope/invalid.
- DataComPy: frozen selectors do not cleanly isolate the empty-NumPy-array issue.
- Werkzeug: one of two frozen parameterized selectors is malformed/not found.
- WeasyPrint: test scope and Pyphen dictionary provenance remain unresolved.
- Parcels: static issue/patch scope hold.
- Trimesh: static issue/patch scope hold.

### Technical-pass caution

The 15 Stage 2 passes are not 15 accepted cases. CTAPIpe #2732 is retained as an engineering/feasibility pilot but excluded from model evaluation because the project lead recorded candidate-specific prior pipeline/debug exposure as `some`. Modin remains on a scope hold because the issue title says AutoSwitchBackend ON while the PR/frozen selectors test OFF/False. Napalm has a Cisco fixture provenance/license hold. PyThaiNLP has native/dependency license and human adjudication gates. Amaranth has a temporal exposure review. Other technically passing cases still need Stage 3, provenance/license and final acceptance.

## 3. Shortest defensible route to reduce the blockers

1. **Use Dishka #435 as the first acceptance candidate.** Stage 2 passed; Stage 3 gold/alternatives/E1-E2-E3 was approved; the project lead has acknowledged its full researcher-source exposure and single-human-adjudicator limitations. The remaining formal work is the complete case record, required artifact/timestamp/license fields, JSON Schema validation, registry validation and a separate final project-lead acceptance. Do not mark it accepted before those checks and that separate decision.
2. **In parallel, finish candidate provenance/licensing.** Start with the candidate actually intended for acceptance, then continue per candidate. Preserve exact source, changed-file, test fixture, dependency/native notice and timestamp evidence. A package's license metadata being present is not legal clearance.
3. **Continue technical intake sequentially.** PSyclone #2755 has successful row discovery and Python 3.13 environment lock, but its manual Stage 2 base-fail/fixed-pass workflow still has not run. Nox, Moto and Werkzeug stay held; never delete or rewrite frozen selectors just to make CI green.
4. **Complete governance before generating outputs.** Confirm Rater B or amend the protocol before outcomes; finish calibration; freeze the five named design/review documents and generation manifest.
5. **Then complete exact model-license and runtime verification.** Only the exact frozen model revision and authorized operations are in scope. The present audit authorizes neither load nor generation.
6. **Keep model training separate.** The secondary LoRA plan proposes 80 accepted independent projects with a project-disjoint 60/10/10 train/validation/locked-test split. It is a separate hypothesis and training authorization; the 15-case primary target or one-case feasibility minimum does not authorize training.

## 4. What must not be done to make the counters green

- Do not change frozen dataset rows or silently remove selectors.
- Do not count multiple selectors, repeat runs or same-project alternatives as independent cases.
- Do not treat an Actions job PASS as a case-acceptance decision.
- Do not infer human consent, legal approval, exposure clearance or gold/tier approval from missing records.
- Do not load, generate with, fine-tune or train the model while the relevant gate is closed.
- Do not claim confirmatory efficacy, general model self-awareness, or universal hallucination reduction from this exploratory design.

**Latest inspected status:** 14 readiness messages; 0 accepted cases; 65 broad primary candidates; 17 distinct-project reserves; no model operation performed.


## 5. Human review team now proposed by the project lead

The project lead has said that Hasan and Batuhan can be presented with the project's research and asked to make explicit yes/no decisions on scientifically relevant approvals. This is recorded as **proposed reviewer availability**, not as consent or completed review.

- Mahmut remains student project lead and final decision-maker.
- Two reviewers are proposed under repository pseudonyms Reviewer H and Reviewer B. Their participation, scope of expertise, case-specific prior exposure, independence, and consent must be recorded individually.
- ChatGPT remains advisory only and is not a human panel member.
- A reviewer who sees an issue, patch, hidden gold, or tier adjudication for a case cannot later be described as blind to those items when scoring that case's model output.
- If reviewers make documentary license recommendations, those are not formal legal opinions. Unresolved legal scope remains open.
- The yes/no review instrument is `HUMAN_REVIEW_PANEL_DECISION_PACKET_V0_1_2026-11-19.md`.

Thus the former single “Rater B not confirmed” blocker is now assigned an actionable review route, but it is not yet closed. Explicit agreement, role selection, per-case exposure declarations, calibration, and protocol/human-review amendment are still required.

## 6. Two second-pass exclusions: internal decision and controlled reconsideration

The earlier two exclusions were produced by the project's own internal second-pass technical/oracle screen. They were **not** decisions made by TÜBİTAK, an external jury, Hasan, or Batuhan.

- Databricks dbt-databricks #994/#995: original PR tests are defect-insensitive and omit session-close cleanup. It may be reconsidered only with a separately authored issue-specific reproducer, preserving the original frozen selectors and transparently classifying any approved path as supplemental or protocol-amended.
- SimPEG #1609/PR #1633: the original issue itself acknowledges that the expected survey-level `components` value is undefined for heterogeneous receivers; the PR deprecates the misleading property. This may be a defensible API-contract resolution, so the previous “integer-return mismatch” exclusion is reopened for independent human scope review. It still needs exact row/selector and base/fix validation.

The frozen 96-row cohort and original second-pass entries are unchanged. Until a documented human decision and evidence-based protocol amendment, the two remain outside the 65 strict primary shortlist. Funnel labels:
- Strict primary shortlist: 65.
- Additional conditional re-review records: 2.
- Separate project reserves: 17.
- Total tracked candidate pathways when reconsideration is shown separately: 84 (not 84 accepted or currently eligible cases).
