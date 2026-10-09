# Next Research Phase: Improving Measurement and Expanding the Evidence Base

**Project:** LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi  
**Status:** Research plan; not a replacement for the frozen confirmatory results  
**Date:** 2026-10-10

## 1. Purpose

The goal is to strengthen the scientific quality and competition readiness of the project, first for the regional evaluation and then for the national final. More records alone do not guarantee stronger evidence. The next phase must improve measurement validity, case diversity, independence, reproducibility, and interpretation.

## 2. What the completed confirmatory experiment currently says

The frozen primary alias metric recorded Standard Context = 0/80 and CCDG Context = 0/80; case-level majority success was 0/16 in both conditions, with exact two-sided McNemar p = 1.00. This is a floor-effect result. It does **not** establish that CCDG has no effect, and it does **not** establish equivalence. It indicates that the frozen metric/model/task combination did not distinguish the conditions on the primary endpoint.

These frozen results and their original analysis must remain unchanged. Any new scoring analysis applied to the same confirmatory responses must be marked exploratory and must not be presented as a preregistered confirmatory result.

## 3. Work sequence

### Gate A — Diagnose the measurement system before collecting more confirmatory data

1. Inspect the output schema, prompt, parser, ground-truth labels, and alias matching as separate layers.
2. Construct a small, manually adjudicated calibration set with cases whose expected root causes are unambiguous and whose accepted aliases are defined before model outputs are reviewed.
3. Test the scoring rubric against both correct and deliberately incorrect examples. Record false acceptance and false rejection.
4. Have a second reviewer independently label a subset if feasible; resolve disagreements before freezing the rubric.
5. Keep schema validity, component identification, root-cause correctness, evidence quality, and abstention as separate measures. Do not combine them into one score without a predeclared rule.
6. Decide in advance whether the primary endpoint is exact root-cause identification, a rubric-based correctness label, or another defensible metric. State its limitations.

**Gate A exit condition:** scoring code passes tests, manual examples behave as expected, and the rubric and primary endpoint are versioned and frozen before new confirmatory inference.

### Gate B — Improve and expand the benchmark

1. Continue screening real, licensed, reproducible cross-component bugs from suitable repositories, preserving issue provenance, fixed revision, failing test, component boundaries, and ground-truth evidence.
2. Exclude cases with ambiguous root causes, weak dependency evidence, unavailable reproduction steps, likely benchmark contamination, or insufficient CCDG suitability; record reasons in machine-readable form.
3. Track unique bugs and repositories separately from repeated inference records. Repeats estimate output variability; they do not increase the number of independent software defects.
4. Inspect whether multiple candidate cases derive from the same underlying defect, duplicated patch, or closely related test. Group or exclude dependent cases as appropriate.
5. Keep a held-out confirmatory case set that is not used to develop prompts, aliases, scoring rules, or CCDG construction guidelines.
6. Before selecting the final sample size, estimate the expected paired outcome pattern and conduct a power/sample-size analysis for the predeclared paired comparison. Do not choose sample size based on which size is likely to produce statistical significance.

### Gate C — Freeze a new independent confirmatory protocol

Before running any new confirmatory inference, commit a manifest containing:
- inclusion/exclusion criteria and case identifiers;
- model ID and immutable revision, quantization/backend, environment, and generation settings;
- exact Standard Context and CCDG Context templates;
- primary and secondary endpoints, scoring rubric, and analysis code version;
- number of cases, repetitions, randomization/order policy, and missing/error handling;
- planned paired statistical test, effect-size estimate, confidence interval, and multiplicity policy;
- prompt, input, and artifact hashes.

Any changes after the freeze must be logged and, if they affect the protocol, treated as a new version rather than silently overwriting the frozen one.

### Gate D — Run, audit, and interpret

1. Run both conditions on the same eligible cases, with order randomized or balanced where technically practical.
2. Preserve every raw response and error; never delete an inconvenient outcome.
3. Validate record count, schema, prompt hash, model/config metadata, duplicate IDs, missing records, and artifact integrity.
4. Report absolute performance in both conditions, paired differences, uncertainty intervals, effect size, and the planned statistical test.
5. Report failures and null results, not only favorable metrics. If both conditions remain at floor, treat the experiment as inconclusive for the intended comparison and investigate task/model suitability without claiming CCDG success.
6. Separate confirmatory results from any exploratory analyses, alternative metrics, or later model comparisons.

## 4. Hypothesis discipline

The research hypothesis is not a result that must be made true. The defensible hypothesis is that explicit cross-component dependency representation may improve root-cause diagnosis compared with an information-matched standard context. The null or an inconclusive result remains possible. Evidence should determine the conclusion, not the desired award outcome.

## 5. Competition-readiness principles

- The student must understand and be able to explain the research question, CCDG construction, dataset provenance, code, analysis, limitations, and conclusions.
- Cite sources for benchmark cases, software versions, methods, and claims.
- Follow the applicable TÜBİTAK 2026–2027 template and instructions; transparently disclose AI assistance as required by the applicable guidance and rules.
- Do not claim that the project has won, is a finalist, or proves a general result before independent evaluation.
- Keep an immutable archive of the report, manifests, raw results, analysis outputs, source commit, and integrity-audit report.

## 6. Immediate next actions

- [ ] Inspect and test the current scoring/alias matcher against manually adjudicated examples.
- [ ] Prepare a rubric and calibration dataset without changing frozen confirmatory outcomes.
- [ ] Audit the existing candidate pool for independence, ground-truth strength, and contamination risk.
- [ ] Estimate sample size after the primary endpoint and expected paired effect are justified.
- [ ] Freeze a new protocol before collecting any new confirmatory outputs.
- [ ] Continue report-template and submission-format checks in parallel.

## 7. Validation status

On 2026-10-10, GitHub Actions run [37991100854](https://github.com/MahmutVezir/dijitalikiz/actions/runs/37991100854) completed successfully in validate-only mode. Repository tests/integrity checks, independent confirmatory-artifact audit, and source-bundle/launcher build passed. The pilot and confirmatory inference jobs were skipped by design; this run did not generate new model outputs.
