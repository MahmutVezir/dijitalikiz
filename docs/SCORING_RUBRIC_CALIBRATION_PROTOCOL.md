# Scoring Rubric Calibration Protocol

**Project:** LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi  
**Status:** Protocol design; not a reanalysis of the frozen confirmatory outputs  
**Date:** 2026-10-10

## 1. Why this protocol is needed

The completed confirmatory study has 160 valid JSON outputs but zero primary-endpoint alias matches in either condition. The frozen result must remain unchanged. Because the endpoint is a deterministic contiguous-phrase matcher rather than a semantic judge, zero matches alone cannot distinguish genuinely incorrect diagnoses from semantically plausible paraphrases. In calibration records, preserve the full raw answer in `response_text`; the auditor must parse the exact frozen four-field output schema and derive the matcher surface internally as `root_cause_class + " " + explanation`. Do not accept a separately hand-entered matcher surface.

This protocol defines how to evaluate the measurement instrument independently of the already-observed confirmatory outcomes. It does not declare any existing response correct or incorrect, and it does not permit retrospective changes to the frozen result.

## 2. Separate the measurement layers

Evaluate the following separately; do not collapse them into one score without a frozen rule.

1. **Transport/record integrity:** expected case, condition, seed, model/configuration, prompt hash and output artifact are present and consistent.
2. **Output validity:** response parses and meets the JSON schema.
3. **Component localization:** named component matches independently documented ground truth.
4. **Root-cause correctness:** diagnosis identifies the underlying defect mechanism, not merely a symptom or affected method.
5. **Evidence consistency:** the explanation is consistent with source code, issue report, failing test and fixed revision.
6. **Cross-component reasoning:** the diagnosis correctly describes the relevant dependency or propagation path when the case requires one.
7. **Abstention/uncertainty:** unsupported confident claims are distinguished from a justified uncertainty response.

A syntactically valid output is not necessarily a correct diagnosis. A plausible explanation is not enough unless it matches the case's evidence.

## 3. Calibration set design

Before any new confirmatory inference, assemble a separate calibration set with manually adjudicated examples. It should contain:

- clear correct diagnoses using the canonical term;
- clear correct paraphrases that do not contain the canonical term;
- incorrect diagnoses naming the affected component but not the root cause;
- incorrect diagnoses that name a related but distinct mechanism;
- explanations that mention the correct phrase only to deny it (negation);
- explanations that quote or list multiple possible causes without selecting the actual one;
- empty, malformed, ambiguous, and partially correct responses;
- cases requiring a specific dependency path, with plausible but incorrect paths.

For each example, store the input example ID, ground-truth rationale, expected component/root-cause status, evidence references, adjudication status, and the version of the rubric. Calibration examples must not be drawn from or tuned against the held-out confirmatory outcome set.

## 4. Adjudication procedure

1. Two reviewers independently label each calibration response as **correct**, **partially correct**, **incorrect**, or **unscorable**, using a written rubric and source evidence.
2. Reviewers must not see the Standard/CCDG condition labels during adjudication when feasible.
3. Record each reviewer's decision and rationale before reconciliation.
4. Resolve disagreements through documented adjudication. If a second reviewer is unavailable, label single-reviewer calibration as a limitation rather than implying inter-rater reliability.
5. Freeze the rubric and calibration decisions before confirmatory inference. If the rubric changes later, increment its version and treat analyses under the new rubric as a distinct analysis.

## 5. Required scoring-instrument diagnostics

For the deterministic alias matcher and any proposed rubric, report at minimum:

- true acceptance and false rejection on the adjudicated calibration examples;
- false acceptance, especially negated mentions and lists of candidate causes;
- agreement between the deterministic matcher and adjudicated labels;
- reviewer agreement before reconciliation, when two reviewers are available;
- number of examples and uncertainty around each reported rate;
- cases for which the rubric is unable to decide.

Do not claim that the calibration set validates semantic correctness if it only tests punctuation normalization or contiguous-string matching. Unit tests can validate software behavior; only adjudicated source-grounded examples can provide evidence about the validity of the scoring instrument.

## 6. Predeclared primary endpoint for a future study

Before the new confirmatory run, choose one primary endpoint. A defensible option is case-level root-cause correctness under the frozen, source-grounded adjudication rubric, with the independent software defect as the statistical unit. Define in advance:

- what counts as a correct root cause;
- how paraphrases, partial diagnoses, negation, multiple guesses, and abstentions are treated;
- whether the primary endpoint is binary or ordinal;
- how two reviewers' disagreements are resolved;
- the rule for aggregating repeated generations within each case-condition;
- the paired statistical test, effect size, confidence interval, and missing-output policy.

Do not select the endpoint based on which one produces the most favorable Standard-versus-CCDG difference.

## 7. Data and inference separation

- Preserve docs/CONFIRMATORY_RESULTS_2026-10-09.md, the frozen manifest, scoring rubric, raw output archive, and prior summaries unchanged.
- Do not add aliases to the existing rubric after viewing the confirmatory outputs and then describe the resulting scores as confirmatory.
- A blinded semantic review of existing outputs, if later performed, must be labeled exploratory and must document its review procedure.
- The next confirmatory test must use an independently selected case set and the rubric frozen before its outputs are generated.
- Keep model-output repetitions distinct from the number of independent cases; five seeds for one defect do not equal five independent defects.

## 8. Exit criteria before new confirmatory inference

- [ ] Calibration set has source evidence and independently adjudicated labels.
- [ ] Correct paraphrases, wrong mechanisms, negation, and multi-hypothesis examples are represented.
- [ ] Matcher and rubric diagnostics are reported, including false-acceptance and false-rejection behavior.
- [ ] Primary endpoint and case-level aggregation rule are versioned and frozen.
- [ ] Independent case selection and sample-size/power plan are documented.
- [ ] Model, prompt, environment, generation settings, and analysis code are frozen.
- [ ] The new confirmatory protocol is committed before inference starts.

## 9. Current state

This document is a protocol specification only. The calibration set has not yet been adjudicated, no new semantic correctness labels have been assigned to the frozen confirmatory responses, and no new inference has been run. The existing confirmatory result remains zero primary passes in both conditions, with a floor effect and unresolved semantic hypothesis.
