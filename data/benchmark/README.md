# Main Benchmark Intake

The main benchmark must not be populated with model-generated results until the pilot has been executed and reviewed.

## Frozen experimental unit

One independent software case is evaluated under both conditions:

- Standard: base evidence only.
- CCDG: the same base evidence plus explicit structured cross-component dependency representation.

Each case therefore produces a paired Standard/CCDG observation.

## Required case fields

Each benchmark case must contain:

- `case_id`
- `source`
- `source_url`
- `publication_date`
- `technology`
- `error_description`
- `i_base`
- `ccdg`
- `ground_truth`
- provenance/evidence metadata
- contamination-audit metadata
- split designation

## Ground-truth rules

Ground truth is annotated independently of model outputs. It must never be rendered into either experimental condition.

The root cause, affected entity, operation, and required relations must be supported by primary issue/fix evidence or another explicitly documented authoritative source.

## Split rules

Pilot cases are not automatically part of the final benchmark. If pilot cases remain in the final analysis, this must be justified before the main benchmark is frozen; otherwise they should be retained as a separate pilot split.

No benchmark case may be added solely because its model output is favorable.

## Power analysis

The primary inferential comparison is paired Standard versus CCDG accuracy. The planned confirmatory test is exact McNemar's test on case-level binary correctness, with alpha=0.05.

Required sample size must be determined from an explicitly documented expected discordant-pair pattern before the main benchmark is run. The pilot is used to estimate feasibility and inform that assumption, not to retroactively choose a favorable sample size.
