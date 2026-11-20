# Candidate portfolio review — Dishka-equivalent v0.2 exploratory standard

**Review date:** 20 November 2026  
**Research branch:** research/2026-11-16-followup-evidence-validation  
**Scope:** all currently recorded Stage 2 technical passes plus active row/oracle/fixture holds in the primary cohort.  
**Authority:** advisory triage only. The project lead makes all gold/tier and final acceptance decisions.

## 1. Executive decision

Dishka #435 is the sole accepted v0.2 exploratory/feasibility case. Its standard is the comparison baseline; no later candidate is accepted merely because its CI passed.

The active Stage 2 ledger contains **15 distinct upstream projects with technical base-fail/fixed-pass evidence**, including Dishka. CTAPIPE #2732 is technically reproducible but must be **excluded from the model-evaluation sample** because the project lead declared prior candidate-specific pipeline/debug exposure as 'some'; it may remain a technical-development pilot only.

That leaves **14 additional Stage 2-passed projects** beyond Dishka; after excluding CTAPIPE from the model-evaluation sample, **13 additional technical candidates** remain worth Stage 3 review, subject to their case-specific gates below. If all 13 survived, the exploratory cohort would contain 14 projects including Dishka, still one short of the 15-project primary target. If Modin is not accepted under its unresolved issue-title/PR-scope discrepancy, the current candidate pool would be 12 additional projects plus Dishka (13), and at least two further independent projects would be required.

This is not a reason to relax thresholds. The target is 15; the minimum feasibility sample is one; below 15 we report the achieved sample and do not claim that the preferred analysis threshold has been met.

## 2. The common acceptance rule

Every candidate must pass the same sequential gates. A pass on one gate never implies a pass on the next.

1. **Identity and provenance:** exact upstream repository, issue, PR, base/fixed commits, frozen dataset row, timestamp resource (issue vs PR), canonical row hash, and selector identity.
2. **Defect-specific reproduction:** each frozen selector must execute and fail on the exact buggy base for the reported defect, then the identical selector must pass on the exact fixed revision. A collection/import/setup failure is not a base failure. An independent issue reproducer is valuable corroboration, but it cannot silently replace a mismatched frozen selector.
3. **Scope and independence:** one accepted case maximum per upstream project; multiple selectors/reproducers are not separate cases. Related issues are clustered and counted once. The issue/PR/selector contract must be coherent.
4. **Bounded documentary license/provenance screen:** exact upstream root/changed-file licenses, direct/transitive and bundled/native notices, dataset license/attribution, and external fixture terms. This is a bounded research-scope acknowledgement, not legal advice, legal clearance, or redistribution permission.
5. **Exposure:** full source exposure is disclosed. The v0.2 sample eligibility rule requires candidate-specific prior pipeline/debug/test-oracle/prompt-calibration exposure to be 'none'. A truthful 'some' excludes the candidate from the model-evaluation sample; it cannot be changed to none for convenience.
6. **Human technical decision:** under the v0.2 exploratory route used for Dishka, the project lead is the single source-aware human adjudicator for the gold mechanism, plausible alternatives and E1/E2/E3 tier membership/sufficiency. ChatGPT is advisory only. Hasan may be recorded as project-lead-reported supplementary source-aware technical input, not as a second signed independent adjudication, blind review or inter-rater statistic. Full exposure and the single-adjudicator limitation are reported.
7. **Case acceptance:** complete schema-conformant case record, fail-closed registry validation, and a separate final project-lead YES/NO. Until then, the candidate is not accepted.

**Important role distinction:** two human scorers remain required for the separate later task of independently scoring raw model responses for evidence support (Rater A and eligible, consented, case-unexposed Rater B). This does not create a two-reviewer or third-adjudicator requirement for source-aware gold/E1/E2/E3 construction. Rater B consent, exposure screening and calibration are still required before response scoring. Neither ChatGPT nor Hasan is represented as a blinded rater for cases whose source/design they have seen.

## 3. Stage 2-passed candidates — current advisory triage

**Evidence audit boundary:** the Stage 2 pass statuses for the 13 older candidate rows are carried forward from their canonical review records and the current project ledger; I did not re-download and recalculate every historical artifact for all 13 in this review. NumPyro #1916 and Dymos #1166 were freshly repeated in this turn on the current branch head, and their latest archives were individually downloaded and re-verified. Before any candidate's final acceptance, its own canonical artifact and license/source manifests must be checked again as part of that candidate's acceptance packet.

| Cohort rank | Upstream project / case | Stage 2 evidence | Advisory disposition | Main remaining gate |
|---:|---|---|---|---|
| 2 | reagento/dishka #435 / PR #436 | 8/8 frozen selectors and independent issue reproducer: exact base failure / fixed pass; locally verified artifact | **Accepted v0.2 exploratory baseline** | Global readiness blockers remain; no inference authorized |
| 12 | pyro-ppl/numpyro #1916 / PR #1918 | 2/2 AIES/ESS frozen selectors plus separate 100-chain AIES warmup→run reproducer: base failure / fixed pass; artifacts locally hash-verified | **Advance first — strong candidate** | Project-lead source-aware gold/E1-E2/E3 decision; bounded NumPy/JAX dependency scope acknowledgement; prior pipeline/debug exposure declaration |
| 15 | OpenMDAO/dymos #1166 / PR #1165 | Exact dataset selector plus fresh Brachistochrone public-API reproducer: base failure / fixed pass; both artifacts locally hash-verified | **Advance second — strong candidate** | Project-lead gold/tier decision; NumPy/SciPy bundled notices and exact pinned dataset-card license; prior exposure declaration |
| 16 | CS-SI/eodag #1530 / PR #1536 | 2/2 issue-specific selectors plus independent YAML duplicate-key reproducer: base failure / fixed pass | **Advance early — strong candidate** | Full dependency license scope; related-issue/project screen; source-aware gold/tier; exposure declaration |
| 17 | skypilot-org/skypilot #5981 / PR #5985 | Exact SSH selector: base failure / fixed pass; pinned 85-package lock and artifact checks | **Keep — strong candidate** | Large direct/transitive dependency scope; issue-family/exposure; gold/tier decision |
| 19 | napalm-automation/napalm #2151 / PR #2152 | Exact selector plus a synthetic parser reproducer: base failure / fixed pass | **Conditional hold — technically good, fixture rights unresolved** | Cisco fixture provenance/terms/retention and bounded license scope; do not circulate the raw fixture or noncanonical artifacts |
| 21 | PyThaiNLP/pythainlp #1004 / PR #1046 | Exact selector plus two one-word support reproducers: base failure / fixed pass | **Keep — strong candidate** | PyICU/native ICU and bundled NumPy/SciPy license scope; model/exposure assessment; related-defect screen |
| 22 | modin-project/modin #7553 / PR #7554 | Both DataFrameGroupBy and SeriesGroupBy frozen selectors: base failure / fixed pass | **Conditional hold — user scope decision needed** | Issue title says AutoSwitchBackend “on”; PR description and frozen selectors test “off/False”; issue body is empty. Do not silently rewrite the contract |
| 24 | MarketSquare/robotframework-robocop #1371 / PR #1374 | Exact CLI exit-code selector: base failure / fixed pass | **Advance early — strong candidate** | Refresh stale review summary; complete source/fixture/license and issue-family record; gold/tier and exposure |
| 26 | meltano/sdk #3090 / PR #3091 | Exact repeated-sibling-$ref selector plus independent schema reproducer: base failure / fixed pass | **Advance early — strong candidate** | Refresh stale review summary; complete dependency/license and related-defect review; gold/tier and exposure |
| 30 | amaranth-lang/amaranth #1518 / PR #1519 | Exact RTLIL brace selector plus independent RTLIL reproducer: base failure / fixed pass | **Keep — strong but date-sensitive** | Issue/PR are one day after the model family's public release window; training-data cutoff is not proven. Treat as exposure caveat, not a proven leak or automatic rejection |
| 31 | cta-observatory/ctapipe #2730 / PR #2732 | Exact selector and direct DataWriter/HDF5 call-path reproducer: base failure / fixed pass | **Exclude from model-evaluation sample** | Project lead declared prior candidate-specific pipeline/debug exposure 'some'; keep only as engineering/feasibility pilot. Also preserve the unresolved published YAML vs reporter-traceback configuration discrepancy |
| 35 | python-control/python-control #1144 / PR #1145 | 3/3 exact selectors plus independent Nyquist axes reproducer: base failure / fixed pass | **Keep — strong candidate with scope note** | PR also fixes related Nichols/describing-function axes issues. Treat all as one project/case; explicitly adjudicate the broader issue-family relationship |
| 39 | qutip/qutip #2646 / PR #2694 | Exact coefficient-argument selector plus independent public coefficient reproducer: base failure / fixed pass; repeat artifact verified | **Keep — conditional on exact scope** | Issue's example is through QobjEvo; test/reproducer exercise the underlying coefficient API more narrowly. Project lead must decide whether this is the same sufficient defect contract; retain caveat |
| 90 | pyfar/pyfar #721 / PR #722 | 23/23 exact frozen selectors: base failure / fixed pass; later corrected lock and successful repeat supersede the old collection failure | **Advance — strong numerical candidate** | Refresh stale candidate-review text; complete full pinned dependency and native/bundled license review; source-aware gold/tier and exposure |

### Notes on the matrix

- A row with many selectors is still one case. For example, QuTiP's one selector, NumPyro's two variants, python-control's three related plot tests, and PyFar's 23 parameter cases do not multiply the project count.
- The issue-level independent reproducer strengthens the technical evidence but is not a substitute for the frozen row/selector contract.
- “Keep” means suitable for Stage 3 review under the unchanged standard, not accepted. No case other than Dishka is in the accepted registry.
- Several earlier candidate review files still contain pre-Stage-2 “pending” wording. The ledger and this dated portfolio review supersede those historical status lines; addenda should be used rather than silently rewriting audit history.

## 4. Blocked or unsuitable frozen rows — disposition

| Candidate | What is known | Recommendation |
|---|---|---|
| ecmwf/earthkit-data #571 / PR #592 (rank 4) | Static code path is plausible, but the regression test depends on a remote ECMWF GRIB fixture with no frozen bytes/hash/terms record. The new cf_attrs.yaml also lacks a pinned CF source revision/attribution/provenance record. No Stage 2 execution is admissible yet. | **Hold, do not execute/download the fixture** until exact fixture provenance, hash, retention/license terms, CF source version and exact frozen row/selector are resolved. High-value fallback if those gates close. |
| wntrblm/nox #919 / PR #922 (rank 6) | Independent local uv-shim reproducer failed on base as expected, but the immutable dataset row has three selector/source mismatches; one exact selector method is absent in both pinned base and fix. Earlier dataset result used a full PR diff and shell splitting and is inadmissible. | **Hold.** Do not drop, rewrite or silently replace the frozen selectors. Reconcile row/oracle through a documented, protocol-compliant path or exclude this row. |
| getmoto/moto #8269 / PR #8296 (rank 9) | ECR issue has a clean, promising independent reproducer design, but the frozen row mixes one ECR selector with 17 unrelated IoT selectors; some pass on buggy base and others are invalid. Candidate job also previously failed before runner allocation. | **Exclude this frozen row for issue #8269.** Do not trim the row to make it pass. A distinct, separately frozen issue from Moto would be a new candidate search, not a rescue of this row. |
| pallets/werkzeug #2955 / PR #2956 (rank 32) | The empty Authorization parameter/IndexError mechanism is clear. The initial run stopped during collection because ephemeral-port-reserve was absent; later lock pins it. One of two frozen selectors is truncated or does not resolve to a valid test node. | **Hold.** Verify exact row bytes and selector serialization; no guessed node IDs. If the immutable selector cannot be recovered, do not count it. |
| capitalone/datacompy #58 / PR #404 (rank 27) | The issue is specifically equality of two empty NumPy arrays. The frozen NumPy test first fails on non-empty arrays before reaching the empty-array assertions; two other selectors test Python/Polars lists, not the issue. | **Exclude this frozen row for issue #58.** A minimal empty-array reproducer may be supporting diagnosis only; it cannot replace the frozen selectors. |

These are not five technical failures. They are provenance, test-oracle, fixture or execution blockers. A blocker does not become a pass, and a non-specific failure does not become evidence of the reported defect.

## 5. Recommended work order

The goal is to finish cases that already have independent, exact technical evidence before spending time rescuing broken rows.

### Batch A — finish the two Stage 3 packages already prepared

1. **NumPyro #1916** — project lead gold/alternatives/E1-E2/E3 decision; bounded license acknowledgement; prior pipeline/debug exposure declaration; acceptance record and registry.
2. **Dymos #1166** — same sequence. Preserve issue-vs-PR timestamp distinction and the #531 related-family cluster (one case only).

These two have exact dataset reproduction, separate public-API reproductions, prepared nested packets and passing structural CI.

### Batch B — low-friction, clear defect contracts

3. **EODAG #1530** — duplicate YAML key and 2/2 aligned selectors.
4. **Robocop #1371** — direct CLI exit-code contract.
5. **Meltano SDK #3090** — repeated sibling JSON Schema references.
6. **PyFar #721** — unusually strong numeric oracle and 23/23 exact selectors.

### Batch C — strong, but wider or more expensive scope

7. **SkyPilot #5981** — clear string-prefix semantics, but large dependency inventory.
8. **PyThaiNLP #1004** — clear two-word linguistic oracle; native ICU and numerical-library notices need bounded review.
9. **python-control #1144** — strong exact Axes oracle; cluster the three plotting-related changes as one project case.
10. **Amaranth #1518** — direct RTLIL contract; record the very close Qwen release chronology and do not infer training-data cutoff.
11. **QuTiP #2646** — decide whether the narrower coefficient API result sufficiently represents the QobjEvo issue example.

### Batch D — conditional decisions before spending more effort

12. **Modin #7553** — ask the project lead to decide whether the PR's explicit disabled/False contract is acceptable despite the issue title saying on. If not, hold/exclude.
13. **NAPALM #2151** — only continue if the Cisco fixture's provenance and terms can be satisfactorily scoped. Do not put fixture contents into public artifacts without a rights basis.

### Separate engineering/hold queue

- **CTAPIpe:** excluded from the study sample because prior pipeline/debug exposure is 'some'; retain as an engineering pilot only.
- **Earthkit-data:** wait for exact external fixture and CF catalogue provenance.
- **Nox:** wait for immutable selector-to-source reconciliation.
- **Werkzeug:** wait for exact truncated selector recovery.
- **Moto and DataComPy:** current frozen rows are unsuitable; do not patch around their issue/selector mismatch.

After batches A–D, screen additional independent projects from the frozen primary cohort in its predeclared rank order, then use the 17-project reserve only if needed. Do not re-rank candidates because a result looks favourable.

## 6. Sample-count forecast and implications

| Scenario | Additional current projects counted after Dishka | Total including Dishka | Primary target 15 |
|---|---:|---:|---|
| All 13 remaining eligible Stage 2 projects pass Stage 3 (CTAPIPE excluded) | 13 | 14 | One more independent project required |
| Modin also held/excluded | 12 | 13 | Two more independent projects required |
| One or more remaining candidates fail Stage 3 gates | Fewer than 12–13 | Fewer than 13–14 | Continue the frozen queue/reserve; never lower the threshold |

The 15-case target is not a permission to accept weak or mixed-scope rows. If fewer than 15 independent projects meet all unchanged criteria, report the achieved smaller feasibility sample and the uncertainty.

## 7. Decisions requested from the project lead

This review is intended to let the project lead assess the candidates rather than to pre-accept them. The next explicit decisions are:

1. For NumPyro, whether the proposed E1 initialization excerpt makes one causal mechanism sufficiently distinguishable from the alternatives.
2. For Dymos, whether the proposed explanation (the ControlInterpComp input is initialized to ones instead of the requested options['val']) is the correct gold mechanism and whether E1/E2/E3 are defensible.
3. For Modin, whether to retain the PR/frozen-selector disabled/False contract despite the issue title's “on” wording.
4. For QuTiP, whether the underlying public coefficient-argument reproducer adequately supports the issue's QobjEvo report, with the scope limitation explicitly preserved.
5. For NAPALM, whether the project is willing to keep it conditional until the Cisco fixture provenance/rights question is resolved; no relaxation of that gate is recommended.

For each candidate, the project lead must separately declare prior pipeline/debug exposure and record the bounded documentary license-scope acknowledgement. A response about one candidate must not be copied to another.

## 8. Global boundary

At this review point:

- Accepted exploratory cases: **1 (Dishka only)**.
- Technical Stage 2 passes in distinct upstream projects: **15 including Dishka**.
- Additional Stage 2 projects still potentially eligible after excluding CTAPIPE: **13**, before Stage 3 review.
- Model loading, inference, fine-tuning and training: **not authorized and not performed**.
- Latest no-inference preflight: run 44741767911, successful; readiness ready_for_inference=false, 13 global blockers, accepted-case count 1.
- This document is a dated advisory triage, not human gold/tier adjudication, legal clearance, case acceptance or inference authorization.

---

## 9. Project-lead portfolio decision — 20 November 2026

The project lead reviewed the advisory triage above and explicitly approved the following portfolio dispositions. This section records portfolio selection only; it does not substitute for candidate-specific gold/tier adjudication, license-scope acknowledgement, exposure declaration, or final case acceptance.

### Approved Stage 3 order

**First group — advance to Stage 3 review, in this order:**
1. NumPyro #1916
2. Dymos #1166
3. EODAG #1530
4. Robocop #1371
5. Meltano SDK #3090
6. PyFar #721

**Second group — retain for the next evaluation round, in this order:**
1. SkyPilot #5981
2. PyThaiNLP #1004
3. python-control #1144
4. Amaranth #1518
5. QuTiP #2646

The second group is retained as a later candidate queue, not promoted ahead of the first group. Existing candidate-specific scope caveats remain in force.

### Not selected by the project lead

- **Modin #7553:** not accepted as a candidate for this study portfolio. Preserve the technical review and the issue-title versus PR/frozen-selector discrepancy as audit history; do not spend further Stage 3 effort on this row.
- **NAPALM #2151:** not accepted as a candidate for this study portfolio. Preserve the technical reproduction and Cisco fixture provenance/rights concern as audit history; do not spend further effort on this row.

These are portfolio-selection decisions, not findings that the technical reproductions were false.

### Exclusions and holds confirmed

- **CTAPIpe #2732:** excluded from the v0.2 model-evaluation sample due to the already recorded prior candidate-specific pipeline/debug exposure='some'; retain only as an engineering/feasibility pilot.
- **Moto #8269 and DataComPy #58:** exclude the current frozen rows; do not trim or replace their selectors to rescue them.
- **Earthkit-data #571, Nox #919 and Werkzeug #2955:** hold. Make only a bounded attempt to resolve the exact fixture/provenance or immutable selector issue; if it cannot be resolved efficiently and with admissible evidence, leave the row out and move on.

### Work order

Proceed with NumPyro first, then Dymos. Next process EODAG, Robocop, Meltano SDK and PyFar. Only after that batch, process the second group in its approved order. Then continue through the frozen primary cohort in its predeclared rank order and use the reserve group only if required. Do not reorder based on favourable outcomes.

### Approval boundary

The project lead considers the technical evidence for NumPyro and Dymos sufficiently clear to proceed with their source-aware scientific review. This portfolio approval does **not** yet approve either candidate's proposed gold mechanism, alternatives, or E1/E2/E3 tier membership. Those decisions must be recorded candidate by candidate. The single source-aware project-lead adjudication route remains the v0.2 standard; ChatGPT's role is advisory. No model loading, inference, fine-tuning, or training is authorized by this portfolio decision.
---

## 10. Conditional project-lead authorization and exposure-rule correction — 20 November 2026

The project lead stated that the first proposed group may be accepted as study cases where they are genuinely eligible under the unchanged Dishka-equivalent v0.2 standard, and asked that the group be evaluated in the previously proposed order. This is authorization to complete case-specific assessment and accept only candidates that satisfy every existing gate. It does not waive a gate, turn a technical Stage 2 pass into case acceptance, or authorize model inference.

### First-group eligibility correction

The previously listed first group included Robocop #1371. A historical project audit, however, explicitly records Robocop #1371 (together with pdoc #812) as having been used for technical debugging and excluded under the predeclared source-exposure/debugging rule. That exclusion predates the current portfolio decision and cannot be reversed merely because the later controlled reproduction passed.

Accordingly:
- Robocop #1371 is removed from the v0.2 model-evaluation sample. Preserve its successful technical reproduction as engineering/feasibility evidence only.
- The remaining first-group case-assessment order is NumPyro → Dymos → EODAG → Meltano SDK → PyFar.
- The order reflects the project lead's previously approved sequence with Robocop removed for the existing exposure rule; it does not re-rank based on favorable outcomes.

### Current assessment boundary for the remaining five

All five have Stage 2 technical base-fail/fixed-pass evidence recorded. Their eligibility for case acceptance is not yet established by that fact alone:

- NumPyro #1916: proposed v0.2 evidence packets and structural validation exist; the added E1 initialization excerpt addresses a key alternative. The source-aware gold/E1-E2-E3 decision, candidate-specific prior pipeline/debug declaration, bounded license-scope acknowledgement (including the pinned dataset-card license issue), and final case record remain open.
- Dymos #1166: proposed gold/tier packet exists and its structural tests pass. Preserve #531 as related history, not another case. The source-aware gold/tier decision, candidate-specific prior pipeline/debug declaration, and bounded license-scope acknowledgement (including bundled NumPy/SciPy notices and the pinned dataset-card license issue) remain open.
- EODAG #1530: exact dataset selectors and an independent YAML reproducer pass base-fail/fixed-pass. Keep the scope limitation visible: PR #1536 also contains a separate StacListAssets change, while the issue-specific selectors and reproducer isolate the duplicate geodes/geodes_s3 configuration-key defect. Related-issue/lineage, source-aware gold/tier, exposure and bounded dependency-scope review remain open.
- Meltano SDK #3090: exact dataset selector and independent repeated-sibling-reference reproducer pass base-fail/fixed-pass. The source-aware gold/tier, related-issue/lineage, candidate-specific exposure, and bounded dependency-scope review remain open.
- PyFar #721: the corrected environment and latest recorded Stage 2 run pass all 23 frozen selectors base-fail/fixed-pass. The older candidate review and assignment files contain superseded pre-rerun statements; those statements must be preserved as history and superseded by a dated addendum. Complete current source/issue-family, exposure, independent-reproducer parity (if required by the case standard), and bounded dependency/native-notice scope review before acceptance.

No candidate is declared accepted by this addendum. Each case must have one coherent issue/PR/dataset-row contract, source-aware gold and E1/E2/E3 rationale under the Dishka-equivalent single-human project-lead route, truthful prior_pipeline_debug_exposure=none, bounded documentary license-scope acknowledgement, a complete proposed v0.2 case record, schema/fail-closed registry validation, and the authorized separate final acceptance record. Full researcher source exposure remains disclosed. No blind-panel requirement is imposed for gold/tier construction; two human scorers remain required later for blind raw model-output evidence-support scoring.

### Decision record boundary

The project lead's conditional acceptance instruction is recorded as a portfolio-level authorization. It is not copied as a case-specific final YES for any of the five candidates. The accepted registry remains unchanged until each case's record is complete and the separate decision is written.
