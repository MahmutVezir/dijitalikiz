# Scoring-calibration data gate

This directory defines the *future* calibration gate. It deliberately does not contain fabricated annotations or claim that a semantic evaluator has been validated.

## Required source-grounded examples

Create `examples.jsonl` from defects and response examples that are independent of every frozen pilot and confirmatory case. Every row must meet `schemas/scoring_calibration_example.schema.json`, including a source URL, fixed revision, supporting evidence URLs, a short case summary, a gold root-cause rationale, response text, challenge class, and the legacy matcher's accept/reject result.

The draft manifest requires at least four examples of each challenge class (28 total minimum): canonical correct answer, correct paraphrase, wrong mechanism, negated mention of the correct phrase, multiple unresolved hypotheses, partial diagnosis, and unscorable output. These are a minimum design safeguard, not a claim that 28 examples guarantee general validity. Include multiple independent defect cases, not 28 variants of a single bug.

Do **not** use any response from the frozen 40-run pilot or 160-run confirmatory experiment to calibrate the score. The audit rejects overlap between calibration source case IDs and the pilot/confirmatory manifests.

## Blinded review workflow

1. Build the two review packets and an unblinding key. Keep the key outside version control and do not share it yet:

   ```bash
   python scripts/build_scoring_calibration_review_packets.py \
     --examples data/calibration/examples.jsonl \
     --reviewer-a-output /tmp/scoring-calibration/reviewer_a_packet.jsonl \
     --reviewer-b-output /tmp/scoring-calibration/reviewer_b_packet.jsonl \
     --key-output /tmp/scoring-calibration/review_key_private.json
   ```

2. Give reviewers only their own packet, not the examples file or private key. Each reviewer independently returns JSONL rows with `review_id`, `reviewer_id`, `label`, `rationale` (at least 20 characters), `evidence_urls`, and the three boolean attestations `condition_blinded`, `challenge_class_blinded`, and `matcher_result_blinded`, all set to true. Allowed labels are listed below.
3. After both independent review files are locked, reveal the key to the adjudicator. Resolve disagreements against source evidence and produce `adjudication.jsonl`; each row must include `review_id`, `adjudicator_id`, final `label`, evidence-backed `rationale`, `evidence_urls`, all three blinding attestations, and `disagreement_resolved: true`.
4. Update the manifest to `status: "adjudicated"`, set `frozen: true`, and record the UTC freeze time, rubric version, and commit that contains the frozen protocol. Do not set these fields before the annotations and disagreements are actually complete.
5. Run the validator with the private key located at the path used during packet generation:

   ```bash
   python scripts/validate_scoring_calibration.py \
     --key /tmp/scoring-calibration/review_key_private.json \
     --output /tmp/scoring-calibration/calibration_audit.json
   ```

The output must say `status: "pass"` and `ready_for_new_confirmatory_inference: true`. Any error or missing annotation keeps the gate blocked.

## Review labels

- `correct`: identifies the underlying root-cause mechanism and is supported by case evidence.
- `partially_correct`: captures a relevant symptom/component but omits or materially misstates the root cause or a necessary dependency.
- `incorrect`: identifies the wrong mechanism, conflicts with evidence, or only lists hypotheses without selecting a justified diagnosis.
- `unscorable`: insufficient/ambiguous evidence or response to make a fair determination.

Only `correct` maps to the strict binary target. Partial and incorrect labels are reported separately; unscorable items are excluded from matcher sensitivity/specificity. Do not label an answer correct merely because it contains a gold phrase: negation and unsupported multi-hypothesis answers are explicit challenge types. The validator reports initial reviewer agreement (exact agreement and Cohen's kappa), an adjudicated confusion matrix, sensitivity, specificity, predictive values and class-level counts. These are finite-set diagnostics with uncertainty, not proof of universal semantic validity.

## Privacy and frozen-study integrity

Private/blinded material is ignored by Git in `.gitignore`. Never commit the private key or share it before both reviews are locked. The audit only characterizes the scoring instrument on the separate calibration set; it does not change the archived 40-run pilot or 160-run confirmatory result. Those historical scores remain immutable, and any review of those outputs remains exploratory.

## Current status

The repository contains the schema and fail-closed tooling, but it intentionally does not contain real calibration examples, reviewer annotations, adjudication, or a private key. The gate is therefore **blocked** until real source-grounded examples are assembled and independently reviewed. Tooling and synthetic software tests must not be misrepresented as completed human validation.
