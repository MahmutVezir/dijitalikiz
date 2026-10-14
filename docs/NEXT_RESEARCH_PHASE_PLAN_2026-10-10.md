# Next Research Phase: Improving Measurement and Expanding the Evidence Base

**Project:** LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi  
**Status:** Research plan; not a replacement for the frozen confirmatory results  
**Date:** 2026-10-10

## 1. Goal

Strengthen the evidence and the student's research defense for the regional stage, with a longer-term goal of reaching the national final. Awards cannot be guaranteed. The most defensible path is sound measurement, independent cases, a fair comparison, transparent limitations, and a report the student can personally explain.

## 2. Historical experiment: frozen and limited

The completed confirmatory artifact contains 160 outputs from 16 cases × 2 conditions × 5 seeds. Its frozen primary alias metric recorded Standard Context = 0/80 and CCDG Context = 0/80; case-level majority success was 0/16 in both, with exact two-sided McNemar p = 1.00. There were no parse errors or artifact hash mismatches.

This is a floor-effect result. It does **not** establish that CCDG has no effect or that the two conditions are equivalent. It indicates that the frozen literal-alias endpoint did not distinguish the conditions.

A code audit found another limitation: the legacy Standard renderer contains an explicit error-description field, whereas the legacy CCDG renderer omits that field and adds dependency edges. The historical comparison therefore does not isolate graph representation alone. See `docs/CONTEXT_INFORMATION_PARITY_AUDIT_2026-10-10.md`.

Preserve the original contexts, manifest, scoring rubric, outputs, report and statistical result unchanged. Any new analysis of the already-seen 160 outputs is post-hoc and exploratory. A blinded reviewer packet has been prepared; it has not yet been independently reviewed by humans and cannot replace the frozen endpoint.

## 3. Gate A — Validate the scoring instrument

1. Treat synthetic fixtures as software behavior tests only; they are not evidence of empirical scoring accuracy.
2. Prepare a source-grounded calibration set of unambiguous diagnoses and plausible paraphrases, plus incorrect mechanisms, negations, unresolved multiple guesses, partial answers, and unscorable outputs.
3. Have two reviewers independently label the examples before reconciling disagreements where feasible.
4. Measure matcher false-rejection and false-acceptance behavior on the adjudicated set; report uncertain examples and reviewer disagreement.
5. Freeze the scoring rubric, reviewer procedure, case-level aggregation rule and analysis script before generating any new confirmatory outputs.

**Gate A exit condition:** the measure has documented source-grounded calibration evidence and a frozen versioned rubric. Unit tests alone do not satisfy this condition.

## 4. Gate B — Improve independent case data

1. Screen new, licensed and reproducible multi-component defects. Record issue/PR provenance, fixed revision, failing test, source evidence, affected and diagnosing components, dependency path, case quality, license and contamination risk.
2. Exclude ambiguous causes, missing or irreproducible fixes, weak component relationships, likely duplicates, and cases unsuitable for CCDG. Record the exclusion reason in machine-readable form.
3. Prefer a diverse sample across projects and defect families; do not fill the sample only with cases from one repository.
4. Review exposure risk conservatively. Older public Defects4J cases may have appeared in model training data; this is a risk, not proof of model exposure. Newly public cases may reduce but cannot eliminate contamination risk.
5. Count distinct defects as the statistical unit. Five generations for one defect are repeated measurements, not five independent cases.
6. Keep a new held-out confirmatory sample separate from calibration, prompt development, and exploratory review.
7. Initial candidate expansion added three recent public fixes and one structured case draft. Commons Compress #770 passed an independent regression test on the exact pre-fix and fixed commits in [run 37993954772](https://github.com/MahmutVezir/dijitalikiz/actions/runs/37993954772). This verifies the tested failure/fix behavior but does not yet satisfy all dataset eligibility criteria; the candidate remains outside the frozen benchmark.

## 5. Gate C — Use an information-matched three-condition design

The v2 code is implemented separately in `dijitalikiz/context_v2.py`; historical renderers remain unchanged.

| Condition | Content | Research purpose |
|---|---|---|
| A. Standard baseline | Source + Technology + Error description + I_base | Baseline without an explicit edge list |
| B. Dependency-enriched prose | Exactly the same base information plus each dependency edge expressed as a sentence | Effect of explicitly adding dependency facts |
| C. CCDG triples | Exactly the same base information and same edge endpoints, relation labels and details as B, represented as directed triples | Whether graph representation adds value over equivalent prose |

The primary planned contrast is **C versus B**. Secondary contrasts are B versus A and C versus A. These contrasts and how multiple comparisons are handled must be declared before inference.

The v2 implementation has tests for shared base information, edge-field parity, neutral treatment headers and ground-truth leakage. A fail-closed parity auditor also exists at `scripts/audit_context_v2_parity.py`. The full repository validation run at [GitHub Actions #37994308924](https://github.com/MahmutVezir/dijitalikiz/actions/runs/37994308924) passed tests, the independent 160-output confirmatory artifact audit, the independent 40-record pilot artifact audit against the exact pilot source commit, and the no-inference source bundle build. The same pilot archive was independently checked as 55/55 manifest files with zero size/hash mismatches. No v2 model inference has been run. Before using v2, additionally freeze tokenizer-based prompt lengths and prompt hashes for every condition/case.

## 6. Gate D — Power and protocol freeze

Use `docs/FOLLOWUP_SAMPLE_SIZE_SENSITIVITY_2026-10-10.md` as a sensitivity illustration, not an estimate from the old result. For instance, one illustrative discordance assumption (prose-only 0.05, graph-only 0.25) requires about 61 independent paired cases to reach 80% power under an exact two-sided McNemar test at alpha 0.05. These are assumptions, not observed probabilities, and must be justified before the sample size is frozen.

Before new inference, commit a manifest with:
- independent case IDs and inclusion/exclusion rules;
- primary and secondary comparisons and multiplicity handling;
- scoring rubric and case-level aggregation rule;
- model, immutable revision, runtime, generation parameters;
- all three context versions, token counts and hashes;
- sample size and power assumptions;
- generation order/randomization, retries, missing outputs and error handling;
- statistical test, effect size and interval plan.

If the available independent case pool cannot support a justified sample, report the limitation rather than inflating the sample with repeated seeds.

## 7. Gate E — Run and interpret

1. Run all three conditions on the same eligible cases, with order randomized or balanced where practical.
2. Preserve all raw outputs and errors; validate schema, record counts, configuration, hashes and duplicate IDs.
3. Aggregate repeated outputs according to the predeclared case-level rule.
4. Report absolute performance, paired differences, uncertainty intervals, effect sizes, planned tests, limitations and missingness.
5. Report null, adverse and inconclusive results as they stand. Do not choose an alternative score after seeing the results to produce a preferred conclusion.
6. Archive the manifest, model/revision, prompts, data provenance, source commit, raw records, analysis outputs and an independent artifact audit.

## 8. Competition readiness

- Explain and cite all source datasets, software behavior, evaluation criteria and analysis methods.
- Be able to explain the research question, CCDG structure, case provenance, data leakage risks, statistics and limitations without relying on an assistant to answer judges' questions.
- Follow the official 2026–2027 TÜBİTAK template and AI transparency guidance.
- Do not claim finalist status, award likelihood, or proven practical value before an independent selection or appropriately designed empirical result.
- Submission formatting and final report remain separate work: official Word template transfer, PDF visual QA, references, authentic student/school/advisor information, and AI-use disclosure are still required.

## 9. Current status and next actions

- [x] Preserve old experiment and its conclusion unchanged.
- [x] Add synthetic matcher behavior tests and document their non-empirical status.
- [x] Implement separate v2 renderers and parity checks.
- [x] Create a masked exploratory review packet and reviewer guide.
- [x] Audit the archived pilot artifact: 55/55 manifest files and 40/40 run records; zero file hash/size mismatches. Frozen primary score remains 0/20 in each condition.
- [x] Add three source-reviewed candidate records and a structured PAX-header case draft; independently reproduce #770 pre-fix failure and fixed-revision pass.
- [ ] Complete an independent human review of the packet; report disagreement and mark the results exploratory.
- [ ] Create and adjudicate a source-grounded scoring calibration set.
- [ ] Expand and independently screen the candidate pool.
- [ ] Freeze new three-arm study protocol and tokenizer-level prompt audit.
- [ ] Only then run new confirmatory inference.
- [ ] Finish the TÜBİTAK report template and PDF QA.

**Current state:** the old experiment is complete but inconclusive for the semantic hypothesis. The new study is not yet run; no new human review/calibration has been completed. The application package is not yet submission-ready.

## Stage 1 — Mainline research-gate verification (updated 2026-10-10)

The current research-gate implementation is in draft [PR #6](https://github.com/MahmutVezir/dijitalikiz/pull/6), integrated with `main` through commit `59a043d683aa01bec44fefc367d01ac8a4cacd41`. The PR is still a draft; passing CI does not satisfy the independent human-evidence gate.

- Seven source-linked defect candidates are recorded under `data/calibration/cases/`. They are **calibration-only**, not eligible held-out confirmatory cases.
- All seven candidate case records contain revision-bound software-twin snapshot fields (repository, exact pre-fix revision, regression-test identifier, observed failure signal). This establishes provenance metadata, not truth of root-cause or CCDG labels.
- The case-pool manifest is deliberately unfrozen, has no eligible cases, and sets `model_inference_permitted=false`.
- The scoring-calibration manifest remains `draft` and `frozen=false`. No independent reviewer labels, adjudications, or scored calibration examples are claimed complete.
- Current integrated-branch validation: [run #149](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38048614525) passed on commit `0de4145741c618242a66712ad366e7a85bd25762`: 144 tests; pilot configuration/integrity gates; the archived 40-record pilot artifact audit; the 160-record confirmatory artifact audit; and source-bundle/confirmatory-launcher build. The pilot and confirmatory inference jobs were skipped. Earlier current-mainline checkpoints #140, #142, #144, and #148 also passed 144 tests; #147 temporarily caught a test assumption that classified the read-only incident auditor as an inference workflow. That test was corrected to assert that only one workflow can execute inference and the incident auditor only reads status/log/output. Run #149 then passed.
- Temporary validation-trigger edits were restored to the exact current `main` content after each check. The current PR diff contains 32 paths, including the read-only incident-audit workflow and the hash-bound incident summary, in addition to research-gate code/docs/tests.
- The mainline inference controls require the frozen-pilot and confirmatory jobs to run only on `main`; push-triggered pilot inference additionally requires explicit `[pilot]`. Normal PR updates and `[validate-only]` runs do not authorize inference.

### Incident #134 — log recovered, raw output files still unavailable

[Actions run #134](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38047007838) was unintentionally triggered before the main-only inference guard was present on the feature branch. Its Kaggle kernel reached `KernelWorkerStatus.COMPLETE`. The original workflow failed to retrieve `pilot_manifest.json`, so artifact validation/upload in that run were skipped.

A separate read-only workflow recovered and retained the existing kernel log in [audit run #1](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38048286908), artifact ID `11668148104`. The archive SHA-256 is `05a43f32bea088aa13ae3f443f29f7bc92774b4422b53308bed5eb204803bd2e`; the retrieved kernel log SHA-256 is `4ffff3b573d80bd4cc837bba85ff092065e0c07fccaac588859c40a7fe7b2cb1`. The log says 40 pilot records were exported and all 55 artifact files staged in Kaggle, but the read-only CLI retrieval returned only the log itself: no `pilot_records.jsonl`, manifest, or other expected final file was recovered.

The log's QA summary reports 20/20 parseable/scored outputs per condition, but zero passes for Standard and CCDG under the historical literal-alias matcher, with 0/4 majority-pass cases. These log-only figures are not adopted as official pilot results, not merged into the historical pilot archive, and not used as evidence for or against the CCDG hypothesis. A hash-bound incident inventory is stored at `data/incident_audits/unplanned_run_134.json`; details and missing-file inventory are in `docs/INFERENCE_TRIGGER_INCIDENT_2026-10-10.md`.

### Stage 1 exit assessment

**Technical repository validation: passed** on the current research-gate code at the cited validation-only checkpoints. Historical pilot/confirmatory artifact-integrity checks: passed. The operational run's execution log is now preserved, but its raw record JSONL and finalized artifacts remain unavailable; exclude the event from official results. The separate human review/adjudication gate remains open in Stage 2 below.

## Stage 2 — Independent case review and a real human-evidence gate (2026-10-10)

- Added `docs/CANDIDATE_SOURCE_AUDIT_2026-10-10.md`, a provisional case-by-case source/structure review. It explicitly is not represented as independent human adjudication.
- Classified every current candidate as a scoring-calibration-only candidate. The calibration set must not be reused as a future confirmatory set after the scoring instrument has been assessed on it.
- Flagged Commons Compress #803 as parallel LZ4/Snappy decoder paths rather than one causal chain, and Commons Lang #1808 as a weak single-component boundary case. These may serve as calibration controls only and must not be used to inflate the future study's strong cross-component case count.
- Aligned reproduction-status metadata in all seven records with the archived pre-fix/fixed-revision evidence. Version-bound snapshots include repository, exact pre-fix revision, regression-test target, and observed failure signal.
- Added `scripts/build_case_ground_truth_review_packets.py`. It builds separately ordered reviewer packets with provisional root-cause labels, `I_base`, and CCDG edges omitted; the unblinding map is written only to a caller-selected private path outside the repository.
- Added `schemas/case_ground_truth_review_audit.schema.json` and strengthened `scripts/validate_calibration_case_pool.py`: selected cases now require a frozen audit with two distinct reviewers, an independent adjudicator, hashes of packet/response artifacts, exact revision bindings, evidence URLs, a coherent-defect decision, and an adjudicated root-cause/dependency graph. A manifest boolean by itself cannot authorize inference.
- Added tests for packet leakage, private-key path safety, review-audit hash mismatch, and missing human-review evidence. The latest integrated validation-only run [#151](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38048719322) passed 144 tests and historical artifact integrity audits; both inference jobs were skipped. Subsequent Stage 3 draft assets are covered by the current ongoing/current-head validation sequence and must not be described as validated until that run passes. These checks validate tooling and archived artifacts, not human review or the research hypothesis.

**Current blocker:** No independent human packet responses or adjudication record exist. The review gate in `data/calibration/case_pool_manifest.json` remains `pending`, selection is not frozen, `eligible_case_ids=[]`, and `model_inference_permitted=false`. Do not modify these flags to bypass the gate. First generate the packets, obtain two genuine independent source-based reviews, adjudicate disagreement, then validate and freeze the audit. The unplanned kernel log recovery in run #134 does not satisfy any of these human-evidence requirements and its raw JSONL is not available in the retained audit artifact.


## Stage 3 — Preregistration and measurement infrastructure (2026-10-10; no inference)

**Status: preparatory implementation. The protocol is a draft; new model inference remains forbidden. Stage 2's independent human review and scoring calibration are still open.**

Added a separate prospective v2 experiment plan so the flawed historical comparison is not repeated:

- `docs/FOLLOWUP_V2_PREREGISTRATION_DRAFT_2026-10-10.md` documents the three arms A (baseline), B (dependency facts in prose), C (the same facts as CCDG triples), the single primary contrast C vs B, secondary contrasts B vs A and C vs A, human-blinded scoring, case-level McNemar analysis, and explicit null/adverse reporting.
- `data/followup_v2/protocol_manifest.json` is machine-readable and deliberately remains `status: draft`, `model_inference_permitted: false`, with an empty held-out case pool and pending gates.
- `schemas/followup_v2_protocol.schema.json` and `scripts/validate_followup_v2_protocol.py` define a fail-closed readiness gate. It rejects overlap with the historic pilot/confirmatory case IDs and the calibration pool; checks sample-size arithmetic; and requires source review, calibration, prompt-tokenizer audit, compatibility, randomized schedule, analysis hash and final freeze evidence before readiness.
- `schemas/followup_v2_heldout_case_review.schema.json` defines a two-reviewer and separate-adjudicator audit specifically for the new held-out sample. Calibration decisions are not reused as confirmatory inclusion decisions.
- `scripts/build_followup_v2_schedule.py` creates a balanced, pre-hashed case-condition-seed order from a completed held-out pool without executing the model.
- `scripts/analyze_followup_v2.py` consumes only final human-adjudicated output labels, requires complete unique case-condition-seed coverage, computes the declared exact McNemar contrasts, adjusts the secondary tests with Holm, and estimates a paired case-level risk-difference interval by preregistered bootstrap.
- `scripts/audit_followup_v2_tokenizer.py` is a no-generation prompt audit for shared context bytes, task/system prompt hashes, final chat-template rendered-input hashes, token-ID hashes and context-length budget. It must be executed after the selected held-out cases and runtime gate exist; no real token audit result is claimed yet.
- Tests were added for protocol blocking, historic/calibration case overlap, schedule reproducibility, outcome coverage, McNemar/Holm calculations, prompt hashing and context overflow. Final validation-only run [#159](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38050082147) passed **158 tests** on the trigger-restored branch; historical pilot/confirmatory artifact audits and source-bundle/launcher checks also passed, and both inference jobs were skipped. The draft manifest remains intentionally blocked, with no held-out case IDs and no model inference authorization.

### Prospective sample-size assumption

The draft plans 61 distinct defects × 3 conditions × 5 generations = 915 outputs, using the existing exact-McNemar sensitivity calculation with assumed prose-only discordance 0.05 and graph-only discordance 0.25 (estimated power 0.8052). These are design assumptions, not observations from the historic data. The target cannot be reduced just because a smaller pool is convenient; if 61 defensible held-out cases cannot be sourced and reviewed, record the limitation and revise only before any v2 confirmatory outputs exist.

### Stage 3 exit gates (all currently pending)

1. Complete the two independent source reviews and separate adjudication for the seven calibration candidates.
2. Build and independently adjudicate the separate scoring-calibration examples; pass at least 0.80 initial reviewer exact agreement and Cohen's kappa ≥ 0.70. Keep the literal alias matcher diagnostic rather than the semantic primary endpoint.
3. Source at least 61 new eligible defects, with exact pre-fix/fixed revisions, regression tests, license/provenance, coherent root cause, cross-component edge review, contamination assessment and reviewer evidence. Exclude every old pilot/confirmatory/calibration case.
4. Run a no-inference tokenizer/runtime audit on the actual new held-out contexts and verify all 183 case-condition prompts plus generation reserve fit the model context; for 61 cases the expected total is 183 prompts and 915 generation cells.
5. Freeze the sample, exact prompt/context hashes, model and runtime, randomized schedule, rating rubric, missing-output/retry policy, analysis code and one primary test before v2 inference.
6. Run inference only after the gate validator reports `ready` and the independent human gates are true. New records must live in `data/followup_v2/`; never mutate the historical artifacts.

**Decision:** Stage 3 protocol/analysis preparation has started, but the study is not ready for inference. A draft manifest is not a completed experiment and must not be presented as a positive result in the TÜBİTAK application.

## Current implementation addendum — 2026-10-10

The following is an updated operational snapshot; it does not replace the frozen historic results or authorize new model inference.

- The latest pull-request validation-only workflow [#38053377558](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38053377558) completed successfully: **163 tests passed**, repository/case/benchmark checks passed, historic pilot and confirmatory artifact integrity checks passed, and no model inference was run.
- Seven discovery leads have completed red/green evidence in [screening run #38053125548](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38053125548). Every named regression test failed on its pinned pre-fix revision and passed on the fixed revision; all seven downloaded artifact ZIP digests were checked against GitHub-reported SHA-256 values. The structured evidence is in `data/followup_v2/discovery_screening_audit.json`. These seven leads remain screening candidates only, with zero human adjudications and zero held-out-eligible cases.
- The reviewer packet builder and its tests were changed to reduce priming: the blind packets no longer include the PR URL/body, reproduction-log URL or observed-failure synopsis. Reviewers receive the repository and pinned source-tree links plus regression-test targets and are instructed to inspect source/test evidence before opening public discussion or prior logs.
- The design-only sensitivity audit shows that 61 cases reach ~80% power only under the strong assumed B-only/C-only discordance probabilities 0.05/0.25. More modest illustrative assumptions require 92, 129, 168 or 249 independent cases depending on the assumed effect. These are hypothetical power scenarios, not empirical estimates. The student/reviewer must justify the assumption before freezing the preregistration.
- **Eligibility remains unchanged:** six leads have technically reproducible tests; that does not make them held-out cases. Independent human source review, separate adjudication, scoring calibration, and 61 or otherwise justified independent held-out cases remain incomplete. The v2 manifest remains draft with `model_inference_permitted=false`; historical pilot/confirmatory results remain untouched.

Next: finish the seven-case screening archive audit, keep only cases that independent reviewers judge to have coherent, defensible cross-component dependencies, and then source enough diverse new candidates. Do not move leads into the held-out manifest solely to reach the target count.

## Operational resumption snapshot — 2026-10-14

This addendum records repository state only. It does not change any historical experiment, endpoint, model result, or scientific conclusion.

### Frozen study and newly merged calibration control

- The historical pilot remains 40/40 records and the historical confirmatory study remains 160/160 records with their prior hash audits; no new inference was run during this resumption.
- Main includes merge commit `99f685567a9486c9aae395f426e093b19cf22afd` and the scoring-calibration matcher change merged through PR #10.
- Calibration examples now require a per-example `root_cause_aliases` list. The calibration auditor recomputes the literal whole-token match from `response_text` and blocks records whose stored `legacy_matcher_accepts` value disagrees. Aliases are not shown in reviewer packets and are retained in the private unblinding key. This is a reproducibility control for the literal matcher, not evidence of semantic-validity and not a replacement for human adjudication.
- The duplicate schema-description-only PR #11 was closed; no research records or frozen metrics were changed by that PR.

### Validation status — inconclusive, not pass

- Validation attempts on PR #10 / PR #11 are visible as GitHub Actions runs [#38581325214](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38581325214) and [#38581406321](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38581406321).
- GitHub's job records contain no executed step summaries, and the exposed job logs are unavailable. A rerun of #38581325214 also failed without step summaries. Therefore these outcomes do **not** establish that pytest or the integrity scripts passed or failed. A successful validation run is still required before claiming current-main test verification.
- This status note is not a substitute for a CI pass. Do not convert the current job-level failure into a scientific result.

### Calibration and follow-up gates remain blocked

- `data/calibration/examples.jsonl`, reviewer annotations, adjudication, and a private review key have not been created. The calibration gate remains blocked.
- The seven calibration case drafts still require independent source/revision/test review and a separate adjudicator; technical red/green reproduction alone does not confer eligibility.
- `data/followup_v2/protocol_manifest.json` remains `status: "draft"`, `model_inference_permitted: false`, with an empty held-out case list and pending gates. No v2 confirmatory inference is authorised.
- Preserve the 40/160 historic artifacts, original renderer, alias rubric, p-value, risk difference and confidence interval unchanged.

### Next actions, in order

1. Obtain a successful no-inference CI run on the current mainline after the matcher-calibration change; if runner setup continues to fail without steps, resolve repository Actions/runner availability rather than editing research code blindly.
2. Have two independent reviewers inspect the seven calibration-case source revisions and regression tests; a separate adjudicator must record decisions. Exclude unsuitable cases rather than promoting them automatically.
3. Only after case-source review passes, freeze the calibration-case set and run the separately authorised calibration-output workflow with complete model/revision, prompt hash, seed and raw-output SHA-256 metadata.
4. Build and independently review the source-grounded calibration controls; report inter-reviewer agreement, Cohen's kappa, false acceptances and false rejections. Do not freeze if the prespecified thresholds fail.
5. Continue sourcing and reviewing new held-out cases, run the tokenizer/context audit, calculate and justify prospective sample size, and freeze the three-condition protocol before any v2 confirmatory inference.


### Source-review packets prepared — 2026-10-14

A separate packet set was prepared outside version control for the **12 held-out-discovery leads** in strict screening run #86. This is distinct from the seven-case scoring-calibration candidate pool.

- Packet provenance and distribution rules: `docs/LEAD_SOURCE_REVIEW_PACKET_MANIFEST_2026-10-14.md`.
- Reviewer A ZIP SHA-256: `c088cf249e5d8122dee0e4fa7e2146a7ea196627ffe18880b9a2ddc1b9d1b632`.
- Reviewer B ZIP SHA-256: `49f0571a25d9f2d27ae8acc36d664c0568680b1edcede5f04f68a403a646f47f`.
- Both packages contain the same 12 opaque review IDs in different orders; case IDs, PR details, preliminary labels and screening logs are omitted. The coordinator key is stored separately and must not be sent to either reviewer.
- Packet integrity/blinding checks passed locally. **Human source review and adjudication remain pending; no lead has been promoted and no inference is authorized.**


### Calibration-candidate source-review packets prepared — 2026-10-14

A second, independent packet set is prepared for the **seven scoring-calibration source cases**; it is not the same pool as the 12 held-out-discovery leads above.

- Packet manifest: `docs/CALIBRATION_CASE_SOURCE_REVIEW_PACKET_MANIFEST_2026-10-14.md`.
- Reviewer A ZIP SHA-256: `67416cc2496390b9cb77b06b49e6c91a0cfe7b8fa386d209f6284c7a126d92de`.
- Reviewer B ZIP SHA-256: `3d6ef06d6859092ecac252798efa6ec3a2db59797caad072809a5c481cf08ca0`.
- Both archives contain the same seven opaque review IDs in different orders and omit proposed causes, public PR URLs, suitability labels and screening logs. The coordinator key is separate.
- Local structural/blinding checks passed. Human source review and separate adjudication are still pending, so the case pool remains `screening_pending` and inference remains prohibited.

The unchanged research decision is: the historic endpoint had a floor effect and cannot resolve the semantic CCDG hypothesis. A future run may support, contradict, or leave the hypothesis unresolved; no desired result is assumed.
