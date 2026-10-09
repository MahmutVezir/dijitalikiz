# Confirmatory Analysis Plan — Frozen Endpoint and Observed Result

## Version and chronology

The initial plan specified case-level complete-diagnostic correctness. The completed four-case pilot exposed a construct-validity concern in the exact canonical matching rules: explanations that were substantively close could fail the literal label checks. On 2026-10-09, before confirmatory outputs were examined, the primary confirmatory endpoint was amended to case-level root-cause correctness using a fixed, case-specific string-alias rubric. Pilot outputs were consulted to diagnose this scoring issue; this chronology is a disclosed protocol amendment, not a claim of complete preregistration before any model output existed.

The alias rubric was derived from case ground truth and source evidence, not model outputs, and its SHA-256 is bound to the frozen benchmark manifest. It cannot be altered after confirmatory outputs are seen. The original exact complete-diagnostic score is retained as a secondary endpoint without rewriting pilot or confirmatory run records.

## Primary question

Does explicit Cross-Component Dependency Graph (CCDG) representation improve root-cause diagnosis accuracy compared with Standard Context when all other experimental inputs are held constant?

## Frozen primary endpoint

At run level, concatenate `root_cause_class` and `explanation`, normalize to lowercase alphanumeric tokens, and search for any fixed case-specific alias as a contiguous phrase. A match is a pass. Non-matches, parse failures, and schema failures are failures. This is a deterministic phrase matcher, not a semantic judge.

A condition passes at case level if at least 3 of 5 fixed seeds pass the primary endpoint. The independent statistical unit is the software case, not the seed.

## Paired statistical analysis

Use an exact two-sided McNemar test on the paired case-level outcomes.

- Null hypothesis: Standard and CCDG have equal marginal case-level primary-endpoint success probabilities.
- Research direction: CCDG may improve root-cause correctness.
- Alpha: 0.05.
- Unit of inference: independent software case.
- Effect: P(CCDG correct, Standard incorrect) - P(Standard correct, CCDG incorrect).
- Confidence interval: predeclared Newcombe-style paired risk-difference interval using Wilson score bounds for the discordant proportions.
- Seeds: 42, 43, 44, 45, 46.
- Conditions: `standard`, `ccdg`.

## Secondary endpoints

Report the original strict complete-diagnostic score unchanged, including component, affected entity, operation evidence, canonical root cause, and required-dependency relations. Also report parse failure rate, per-component metric, and within-case repeated-output diagnostics. Unless otherwise frozen, secondary descriptive metrics must not be presented as independently confirmatory inferential tests.

## Missing data and integrity

A missing seed file blocks a complete primary case outcome. Do not silently impute a missing replication. Parse/schema failures are failed observations, and are reported separately. Each run record must have frozen model/revision, condition, seed, generation settings, context/prompt/system hashes, raw output/hash, and source commit. The artifact's entire file inventory and SHA-256 checksums are independently validated.

## Pilot and benchmark split

Pilot cases are excluded from the confirmatory benchmark. Confirmatory case membership was selected independently of model outputs. All 16 confirmatory cases carry a conservative high public-exposure contamination-risk label; this does not prove membership in training data.

## Power assumption

The 16-case plan was selected using the predeclared directional McNemar design assumptions stored in `data/benchmark/benchmark_manifest.json`, target power 0.80 and alpha 0.05. These are design assumptions, not estimates inferred from the pilot or confirmatory outcomes; no sample-size retuning is permitted after result inspection.

## Observed confirmatory result (not a protocol change)

The completed 16-case experiment yielded zero primary alias matches in both conditions: Standard 0/80, CCDG 0/80, and 0/16 case-level majority passes in each condition. Exact two-sided McNemar p=1.00, risk difference 0.00, 95% interval [-0.1936, 0.1936], zero discordant cases. This is a floor-effect outcome. It does not prove equivalence or absence of a CCDG effect; the semantic hypothesis remains unresolved by the literal matcher. The frozen score and rubric must not be retrospectively changed.

## Authoritative artifacts

- Frozen pilot: GitHub Actions run `37968099402`, source commit `d50adaf9b6d0b017a5d30c9ebd9dd404988dbfb5`.
- Frozen confirmatory run: GitHub Actions run `37976682761`, source commit `e1e083f5400432b98143bdb35ff2c5b435ea8f6e`.
- Result document: `docs/CONFIRMATORY_RESULTS_2026-10-09.md`.
- Machine-readable metrics: `data/benchmark/confirmatory_result_summary.json`.
