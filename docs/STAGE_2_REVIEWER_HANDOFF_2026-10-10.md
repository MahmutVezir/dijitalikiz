# Stage 2 reviewer handoff — source review and scoring calibration

**Status (2026-10-10): BLOCKED pending real independent reviews.**  
**Purpose:** Make the next human-dependent research step executable without changing or rescoring the historical study.

This handoff is operational guidance only. It is not a completed review, an adjudication, or evidence that the CCDG hypothesis is supported. Do not change any readiness flag to bypass missing evidence.

## Why outside review is required

The current seven cases have source URLs, exact pre-fix/fixed revisions, and regression-test evidence. These establish provenance and reproducer behavior; they do not independently establish that every proposed root-cause statement or CCDG edge is correct. The existing source audit is preliminary desk review only.

The reviewers should be independent of each other and should not see the provisional root-cause labels, CCDG edges, scoring rubric classifications, or the other reviewer's responses before their own review is locked. A separate adjudicator must resolve disagreements.

## Reviewer qualifications and scope

Seek two reviewers with demonstrable Java/source-debugging experience (for example, a software engineering teacher, university researcher, maintainer, or experienced Java developer) and a third person who can adjudicate disagreements independently. A reviewer should disclose any authorship, employment, collaboration, or other conflict relating to a candidate repository.

The review is about source-grounded research validity, not whether a change is popular or whether an LLM produced a convincing sentence. For each assigned case, reviewers must inspect the exact pinned pre-fix and fixed revisions, inspect the named regression test, identify the causal mechanism from source evidence, and include only dependency edges supported by source. They must decide whether the record describes one coherent defect and whether it is suitable for the intended cross-component dependency experiment. Ambiguity must lead to revise/exclude, not a forced positive decision.

All seven candidates are reserved for **scoring calibration only**. They must never be included in the future held-out confirmatory set. Public exposure means training-data contamination is possible but not proven; reviewers must not claim that model exposure is known.

## Generate the blinded source-review packets

From the repository root, run:

```bash
python scripts/build_case_ground_truth_review_packets.py \
  --output-dir /tmp/dijitalikiz-case-ground-truth-review
```

The script writes:
- `reviewer_a_packet.jsonl`
- `reviewer_b_packet.jsonl`
- `review_key_private.json`
- `packet_manifest.json`
- `REVIEWER_INSTRUCTIONS.md`

Give Reviewer A only A's packet and Reviewer B only B's packet. The packets use different random orderings and omit provisional root-cause labels, component labels, `I_base`, CCDG edges, and the selection rationale. Keep `review_key_private.json` outside version control and inaccessible to both reviewers until both independent submissions are locked. Do not place response files in the repository while review is in progress.

Each reviewer response must be a JSONL file with one record per `review_id`, containing at minimum these fields:
- `review_id`, `reviewer_id`
- `decision`: `keep`, `revise`, or `exclude`
- `root_cause_rationale`
- `components`
- `dependency_edges` (each edge must record source, relation, target, and evidence URLs)
- `is_single_coherent_defect` (boolean)
- `ccdg_suitability`: `strong`, `moderate`, `weak`, or `ineligible`
- `contamination_risk`: `low`, `medium`, `high`, or `unknown`
- `evidence_urls` and `limitations`

Use line-specific source URLs, revision links, and regression-test evidence where possible. Preserve the original submitted files unchanged and calculate SHA-256 hashes before adjudication.

## Adjudication and case-pool gate

After both submissions are locked, a distinct adjudicator compares the review records and the private key, resolves each disagreement using revision-bound source/test evidence, and records a rationale for each final decision. If a case is excluded, keep the exclusion reason and do not silently replace its label or graph.

Run the case-pool validator only after the source-review audit and its hashes have been created:

```bash
python scripts/validate_calibration_case_pool.py \
  --output /tmp/dijitalikiz-case-ground-truth-review/case-pool-audit.json
```

The exact manifest must show seven genuinely adjudicated eligible cases if the existing minimum remains unchanged. If reviewers exclude candidates, do not mark them eligible to meet the count; source and review replacement candidates first. The validator's pass is a structural/readiness result, not a substitute for reading the evidence.

## Scoring-calibration stage follows source adjudication

Do not build a completed calibration audit before real calibration data exists. Once eligible calibration cases are frozen, create a separate calibration-only model-output set plus clearly marked human-authored/synthetic controls. The planned challenge classes are:
- canonical correct diagnosis;
- correct paraphrase;
- wrong mechanism;
- negated correct phrase;
- multiple competing hypotheses;
- partial diagnosis;
- unscorable output.

The existing rubric requires at least four examples per challenge class, at least three distinct source cases per class, at least seven genuine model outputs spanning seven independent source cases, and at least seven human-authored or synthetic controls. No example may reuse outputs from the frozen historical experiment. Controls must be labelled by their true origin; synthetic controls must never be represented as model outputs.

Build separately shuffled scoring-review packets using `scripts/build_scoring_calibration_review_packets.py`. Again, the private answer key must remain private until two independent blind labels and a separate adjudication are locked. Then run `scripts/validate_scoring_calibration.py`. The declared minimum reliability is exact agreement >= 0.80 and Cohen's kappa >= 0.70. Report the finite-set sensitivity/specificity of the literal matcher honestly; even a high result on this finite sample would not establish universal semantic validity. The primary endpoint for the new study remains blinded, source-grounded human adjudication.

## What this does *not* authorize

- It does not authorize new v2 confirmatory inference.
- It does not alter the old 40-record pilot or 160-output confirmatory archive.
- It does not make preliminary AI/desk review count as independent human review.
- It does not permit model-generated labels to stand in for adjudication.
- It does not justify weakening the predeclared reviewer-reliability thresholds after seeing labels.

When the human evidence is returned, continue with source adjudication, scoring calibration, independent held-out case sourcing, tokenizer/runtime checks, and a final protocol freeze. Only the readiness validator's evidence-backed `ready` result can permit the next inference run.
