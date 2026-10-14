# Scoring-calibration data gate

This directory defines the *future* calibration gate. It deliberately does not contain fabricated annotations or claim that a semantic evaluator has been validated.

## Required source-grounded examples

Create `examples.jsonl` from defects and response examples that are independent of every frozen pilot and confirmatory case. Every row must meet `schemas/scoring_calibration_example.schema.json`, including a source URL, fixed revision, supporting evidence URLs, a short case summary, a gold root-cause rationale, response text, challenge class, and the legacy matcher's accept/reject result. Each row must include a predeclared `root_cause_aliases` list and a separate `matcher_text` field. `response_text` is the full diagnostic response shown to reviewers. `matcher_text` must be exactly the historical evaluator's match surface: `root_cause_class + " " + explanation`; do not substitute the entire JSON or unrelated fields. The `legacy_matcher_accepts` value is recomputed from `matcher_text` using the same normalization and whole-token substring rule, and inconsistent flags are blocked. Case-specific aliases must be frozen before the corresponding response is inspected or generated. This characterizes literal matching only; it does not make the matcher a semantic judge.

Record response origin explicitly. Genuine new model responses use `response_origin: "independent_model_output"` and must retain model ID, immutable model revision, seed, prompt SHA-256, and raw-output SHA-256 in `generation_metadata`. Human-authored and synthetic adversarial controls use their respective origin labels and `generation_metadata: null`. Do not relabel a hand-written response as model-generated. The manifest requires at least seven independent model-output examples from seven distinct defect cases and seven control examples; the class and diversity thresholds apply as additional requirements.

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

The reliability gate is declared in `data/calibration/manifest.json` before annotation: at least 0.80 exact initial-review agreement and Cohen's `kappa >= 0.70`. If either is not reached (or kappa is undefined), do not start a confirmatory study; clarify the rubric, retrain/calibrate reviewers using examples outside the held-out sample, and version the revised protocol before repeating calibration. Do not relax thresholds after seeing labels merely to pass the gate.

The validator also reports the legacy alias matcher's sensitivity and specificity. These diagnostics do not authorize the old alias matcher to be the semantic primary endpoint. The future primary endpoint is blinded, source-grounded human adjudication at case level; any automated primary endpoint would require a distinct protocol and prior justification.

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


## Independent ground-truth / CCDG review before case-pool freeze

The scoring-case manifest has a separate `review_gate`. The current status is `pending`; there is no adjudication artifact and no model inference is authorized. Do not manually switch the flags to make the gate pass.

Build two separately ordered review packets locally:

```bash
python scripts/build_case_ground_truth_review_packets.py \
  --manifest data/calibration/case_pool_manifest.json \
  --output-dir /tmp/dijitalikiz-case-ground-truth-review
```

The two packets intentionally omit the provisional root-cause label, component labels, `I_base`, and CCDG edges. Reviewers receive only the source PR, repository, pre-fix/fixed revisions, regression-test targets, reproduction evidence, and observed failure signal. They must inspect the exact source/test revisions and independently identify the mechanism and dependency relations.

Keep `review_key_private.json`, both reviewer packets, and the two raw review responses outside Git and do not give the private key to either reviewer. Once both reviews are complete, compare decisions against source evidence and document the resolution. The review audit must comply with `schemas/case_ground_truth_review_audit.schema.json`, include hashes of the exact packets/responses, distinct reviewer IDs, an independent adjudicator, exact revisions, evidence URLs, and case-level decisions.

Only after genuine review and adjudication are complete may a frozen `data/calibration/case_ground_truth_review_audit.json` be committed and its SHA-256 recorded in `review_gate.audit_sha256`. The case-pool validator checks this audit file and its schema; setting candidate booleans alone is insufficient. Never fabricate reviewer identities, labels, response hashes, or adjudication timestamps.
