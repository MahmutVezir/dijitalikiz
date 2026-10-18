# V2 independent-rater reliability audit

**Status:** The audit tool is implemented and unit-tested; no real reviewer ratings have been received or analyzed. This tool does not create human ratings, adjudicate cases, or authorize model inference.

## Purpose

The V2 preregistration draft requires at least **0.80 exact agreement** and **Cohen's kappa >= 0.70** on a predeclared calibration subset. If exact agreement misses its threshold, kappa is below threshold, or kappa is undefined, the gate remains blocked. Do not relax thresholds after viewing confirmatory outputs.

The script `scripts/audit_rater_reliability.py` computes these metrics from actual, paired human ratings. It also outputs the complete 4-by-4 contingency table, rater marginals, expected agreement, thresholds and reasons a gate did not pass. It requires exact one-to-one coverage of the preregistered item IDs, rejects duplicate IDs and invalid labels, and does not include answer text or reviewer identity in the aggregate result.

## Required input

A UTF-8 CSV with exactly these columns, and no response text or personal identity fields:

```csv
item_id,rater_a,rater_b
opaque-item-001,correct,correct
opaque-item-002,partially_correct,correct
```

The labels are exactly: `correct`, `partially_correct`, `incorrect`, `unscorable`. Each `item_id` must be an opaque, predeclared identifier. The two ratings must come from independent, locked submissions for the same item, and the item set must be the declared calibration subset—not historical exploratory outputs or the future held-out confirmatory set.

A JSON file with the preregistered item IDs is required, for example `["opaque-item-001", "opaque-item-002"]`. The list and rubric must be frozen before the ratings are analyzed. Store identifiable reviewer records and original submissions in a suitable private location; do not commit personal data or private reviewer submissions to this public repository.

## Run only after real ratings arrive

```bash
python scripts/audit_rater_reliability.py \
  --ratings-csv /private/path/locked_ratings.csv \
  --expected-item-ids /private/path/calibration_item_ids.json \
  --output-json /private/path/reliability_summary.json
```

Exit code 0 means both preregistered thresholds passed for the declared calibration subset. Exit code 1 means the statistical gate is blocked. Exit code 2 means input/provenance validation failed. A blocked result is not a reason to change the thresholds; improve and refreeze the rubric before confirmatory outputs exist, then collect ratings on a fresh predeclared subset.

## Separation of roles

This metric assesses answer-rater agreement only. It does not replace the two independent source-review decisions or the separate adjudicator's ground-truth decision. Agreement alone does not prove that the shared decision is correct. No model inference may begin until every other manifest gate is also closed with auditable evidence.

## Current state

- No genuine human rater data are present in this repository.
- Unit tests use clearly synthetic examples only to check the calculation and blocking behavior.
- The V2 manifest remains `status: draft`, `model_inference_permitted: false`; case IDs remain empty and calibration/review/freeze gates are still pending.
