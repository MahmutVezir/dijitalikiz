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

The current research-gate implementation is in draft [PR #6](https://github.com/MahmutVezir/dijitalikiz/pull/6), based on the latest `main` commit `e46174504f82238297f4bb9abd107d91367ce7a9`. The PR is still a draft; passing CI does not satisfy the independent human-evidence gate.

- Seven source-linked defect candidates are recorded under `data/calibration/cases/`. They are **calibration-only**, not eligible held-out confirmatory cases.
- All seven candidate case records contain revision-bound software-twin snapshot fields (repository, exact pre-fix revision, regression-test identifier, observed failure signal). This establishes provenance metadata, not truth of root-cause or CCDG labels.
- The case-pool manifest is deliberately unfrozen, has no eligible cases, and sets `model_inference_permitted=false`.
- The scoring-calibration manifest remains `draft` and `frozen=false`. No independent reviewer labels, adjudications, or scored calibration examples are claimed complete.
- The current PR head `1b1467c77390f6a277637638b65aec19f959ff2f` passed [validation-only run #140](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38047908557): 144 tests; pilot-configuration integrity gate; independent audit of the archived 40-record pilot artifact; independent audit of all 160 confirmatory records; source-bundle and confirmatory-launcher build. Both inference jobs were skipped.
- The temporary trigger-file edit used to run validation was restored to the exact same content as `main`; the PR diff is again limited to 29 research-gate files.
- The mainline inference controls require the frozen-pilot and confirmatory jobs to run only on `main`; push-triggered pilot inference additionally requires explicit `[pilot]`. Normal PR updates and `[validate-only]` runs do not authorize inference.

### Incident that remains under audit

[Actions run #134](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38047007838) was unintentionally triggered before the main-only guard was present on the feature branch. Its Kaggle kernel reached `KernelWorkerStatus.COMPLETE`, but output retrieval failed because `pilot_manifest.json` was missing; artifact validation and upload were skipped. The exact kernel is [`mahmutvezir/dijitalikiz-frozen-pilot-c8b6f8f2-38047007838-1`](https://www.kaggle.com/code/mahmutvezir/dijitalikiz-frozen-pilot-c8b6f8f2-38047007838-1). The actual Kaggle log and any persisted outputs still require operator inspection. Do not assert that no inference occurred, do not count this run as a valid study result, and do not merge recovered records into the historical frozen datasets.

### Stage 1 exit assessment

**Technical repository validation: passed.** Historical artifact-integrity checks: passed. Operational-run audit: **pending** because the unintended Kaggle output has not been independently inspected. The remaining human review gate is tracked in Stage 2 below.

## Stage 2 — Independent case review and a real human-evidence gate (2026-10-10)

- Added `docs/CANDIDATE_SOURCE_AUDIT_2026-10-10.md`, a provisional case-by-case source/structure review. It explicitly is not represented as independent human adjudication.
- Classified every current candidate as a scoring-calibration-only candidate. The calibration set must not be reused as a future confirmatory set after the scoring instrument has been assessed on it.
- Flagged Commons Compress #803 as parallel LZ4/Snappy decoder paths rather than one causal chain, and Commons Lang #1808 as a weak single-component boundary case. These may serve as calibration controls only and must not be used to inflate the future study's strong cross-component case count.
- Aligned reproduction-status metadata in all seven records with the archived pre-fix/fixed-revision evidence. Version-bound snapshots include repository, exact pre-fix revision, regression-test target, and observed failure signal.
- Added `scripts/build_case_ground_truth_review_packets.py`. It builds separately ordered reviewer packets with provisional root-cause labels, `I_base`, and CCDG edges omitted; the unblinding map is written only to a caller-selected private path outside the repository.
- Added `schemas/case_ground_truth_review_audit.schema.json` and strengthened `scripts/validate_calibration_case_pool.py`: selected cases now require a frozen audit with two distinct reviewers, an independent adjudicator, hashes of packet/response artifacts, exact revision bindings, evidence URLs, a coherent-defect decision, and an adjudicated root-cause/dependency graph. A manifest boolean by itself cannot authorize inference.
- Added tests for packet leakage, private-key path safety, review-audit hash mismatch, and missing human-review evidence. The current PR-head validation-only workflow [run #140](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38047908557) passed 144 tests, validated the frozen pilot configuration, audited the 40-record archived pilot artifact and 160-record confirmatory artifact, and built the source bundle/confirmatory launcher. Both inference jobs were skipped. These checks validate the tooling and stored artifacts, not the human review or the research hypothesis.

**Current blocker:** No independent human packet responses or adjudication record exist. The review gate in `data/calibration/case_pool_manifest.json` remains `pending`, selection is not frozen, `eligible_case_ids=[]`, and `model_inference_permitted=false`. Do not modify these flags to bypass the gate. First generate the packets, obtain two genuine independent source-based reviews, adjudicate disagreement, then validate and freeze the audit.
