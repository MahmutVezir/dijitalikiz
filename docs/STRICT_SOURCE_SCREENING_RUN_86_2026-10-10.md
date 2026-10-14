# Strict source-screening report — 10 October 2026

## Result

The strict no-model-inference workflow completed successfully: [GitHub Actions run #86](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38057613670). It screened **12 public defect leads across 22 named regression-test targets**. Every named target failed on the pinned pre-fix revision and passed on the pinned fixed revision. All 12 downloaded artifact ZIP SHA-256 values matched the corresponding GitHub artifact digests. Every artifact included a regression-test patch hash and identical test-file hashes for the pre-fix and fixed runs.

The machine-readable record is [discovery_screening_audit_run_38057613670.json](../data/followup_v2/discovery_screening_audit_run_38057613670.json). It records the exact source revisions, test targets, artifact IDs/digests, per-file fixture hashes, patch hashes, and the remaining review gates.

The separate [repository validation run #57](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38057613640) also passed without model inference.

## Method correction

An earlier screening implementation copied whole test files from fixed revisions into pre-fix snapshots. This risked bringing unrelated helper/test changes into the pre-fix run, so those earlier screens are retained only as historical diagnostics and are **not** the evidence used by this strict audit.

The strict workflow instead applies only the test-file diff between the pinned revisions, records the patch SHA-256, then verifies identical test-file hashes before and after resetting the source to the fixed revision. This controls the regression-test fixture across the red/green comparison.

### Spring Framework fixture adaptation

The Spring candidate's upstream test patch calls `createRequest("files.multipart", ...)`, while the test helper requires a `Resource`. The screening workflow applies a narrow, documented test-fixture adaptation to use `ClassPathResource` on both the pre-fix and fixed snapshots. It does not modify production source. The adjustment and its reason are recorded in the artifact metadata and machine-readable audit. The candidate remains subject to independent review of this adaptation.

## Interpretation and restrictions

This is **technical reproducibility evidence only**. It is not a ground-truth adjudication. Passing a regression test does not by itself establish that a case has complete root-cause evidence, a meaningful cross-component dependency path, acceptable provenance, or low contamination risk.

- Strict technical screening: **12/12 leads passed**; **22/22 named tests** showed the intended red/green behavior.
- Independent human source reviews: **0 completed**.
- Separate adjudications: **0 completed**.
- Cases accepted into the held-out confirmatory set: **0/61**.
- New model inference or scoring calibration: **not performed**.
- V2 protocol: **draft; model inference remains unauthorized**.

No case from this report may be moved into the confirmatory set until two independent reviewers assess the pinned source and test semantics, and a separate adjudicator records the final decision. Calibration and prompt-development cases must remain separate from held-out confirmation.
