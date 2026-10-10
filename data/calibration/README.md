# Scoring-calibration data gate

This directory defines the *future* calibration gate. It deliberately does not contain fabricated annotations or claim that a semantic evaluator has been validated.

## Required files

- `examples.jsonl`: source-grounded challenge examples, with their gold rationale and legacy matcher decision. These must be independent of every frozen pilot and confirmatory case.
- `reviewer_a.jsonl` and `reviewer_b.jsonl`: separate initial reviews from two reviewers. Reviewers must not see the model condition, generation seed, challenge class, or legacy matcher decision.
- `adjudication.jsonl`: final labels and evidence-backed rationales after disagreements have been resolved.

Each JSONL line is one JSON object. Field names and allowed values are checked by `scripts/validate_scoring_calibration.py`.

## Challenge coverage

At least four examples per class are required by the draft manifest: canonical correct answer, correct paraphrase, wrong mechanism, negated mention of the correct phrase, multiple unresolved hypotheses, partial diagnosis, and unscorable output. The count is a minimum design safeguard, not a claim that 28 examples guarantees general validity. The calibration set should include different independent software-defect cases and cite source evidence for each gold label.

## Review labels

- `correct`: identifies the underlying root-cause mechanism and is supported by case evidence.
- `partially_correct`: captures a relevant symptom/component but omits or materially misstates the root cause or a necessary dependency.
- `incorrect`: identifies the wrong mechanism, conflicts with evidence, or only lists hypotheses without selecting a justified diagnosis.
- `unscorable`: insufficient/ambiguous evidence or response to make a fair determination.

Only `correct` maps to the strict binary target. Partial and incorrect labels are separate in descriptive reporting; unscorable items are excluded from matcher sensitivity/specificity. Do not reclassify an answer as correct merely because it contains a gold phrase: negation and unsupported multi-hypothesis answers are explicit challenge types.

## Fail-closed gate

Run:

```bash
python scripts/validate_scoring_calibration.py
```

The script is expected to report `blocked` until all annotation files exist, each required class has enough examples, pilot/confirmatory overlap is absent, both independent reviews and adjudications cover every example, source references are present, and the manifest is explicitly frozen. A blocked status at this point is correct and must not be bypassed.

When complete, run with `--output data/calibration/calibration_audit.json` and attach the audit to the future study protocol. The audit only characterizes the scoring instrument on the separate calibration set; it does not change the archived 40-run pilot or 160-run confirmatory result. Those historical scores remain immutable and any review of those outputs is exploratory.
