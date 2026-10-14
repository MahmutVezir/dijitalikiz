# Inference Trigger Incident — 2026-10-10

**Status:** The unintended Kaggle kernel completed and its execution log was recovered through a separate read-only audit. The log states that 40 pilot records were exported and all required pilot outputs were staged inside the Kaggle runtime, but the Kaggle CLI exposed only the execution log to the GitHub runner. The raw `pilot_records.jsonl` and finalized artifact files were not recovered. Treat this as an unplanned operational execution, **not a valid official pilot or confirmatory result**.

## Event record

- GitHub Actions workflow: [run #134](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38047007838), run ID `38047007838`.
- Triggering branch/commit: `research/scoring-calibration-mainline-v2` / `c8b6f8f2e9647f1ab696387ccc9962051900102b`.
- Triggering commit message: `Port research gate update: .github/kaggle-pilot-trigger`.
- Exact Kaggle kernel: [`mahmutvezir/dijitalikiz-frozen-pilot-c8b6f8f2-38047007838-1`](https://www.kaggle.com/code/mahmutvezir/dijitalikiz-frozen-pilot-c8b6f8f2-38047007838-1).
- Generated launcher SHA-256: `0a39fe1e5844e94a525400af599cdd7a8e3930ab3de63b147ae6e39092f2a9b1`.
- Generated kernel metadata SHA-256: `54decd7fde182ff142f1077b02f6988e377a17277bfcfe51f507cbeb238dc6bc`.
- GitHub's kernel-wait log records `QUEUED`, then `RUNNING`, then `KernelWorkerStatus.COMPLETE` at 2026-10-10 11:12:14 UTC.
- The original Actions job then failed at `Download finalized pilot output` because `pilot_manifest.json` was missing. Validation and archival by run #134 were skipped.
- The kernel log nevertheless contains `EXPORTED PILOT JSONL: 40 records -> data/pilot/pilot_records.jsonl`, `PILOT FINALIZATION COMPLETE`, a pilot artifact manifest reporting `run_record_count: 40` and `file_count: 55`, and `Pilot artifacts staged at /kaggle/working/pilot-output`.
- The log's execution-QA summary reports 20 expected/found/parsed/scored outputs per condition, 0 passes out of 20 for Standard and 0/20 for CCDG, parse-failure rate 0, four case IDs (MATH-927, MATH-950, MATH-949, MATH-988) with five runs per condition each, zero majority-pass cases, no duplicate-output groups, and no QA flags. The log explicitly describes this as execution-integrity QA, not a confirmatory effectiveness claim.
- These logged counts are evidence that the unintended kernel executed its pilot plan; they are **not being adopted as the official frozen pilot result**, because the raw record JSONL and manifest were not retrieved and cannot be independently audited here.

## Read-only recovery audit

A dedicated workflow, [audit run #1](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38048286908), was added and run against the existing kernel. It only read status, logs, and existing kernel output; it did not push or execute a kernel.

GitHub Actions artifact:
- Name: `unplanned-kaggle-run-134-audit-38048286908`
- Artifact ID: `11668148104`
- [Audit workflow run / downloadable artifact](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38048286908)
- Artifact SHA-256 digest: `05a43f32bea088aa13ae3f443f29f7bc92774b4422b53308bed5eb204803bd2e`
- Artifact was created 2026-10-10 and is retained by GitHub until 2026-11-09.
- Recovered kernel log SHA-256: `4ffff3b573d80bd4cc837bba85ff092065e0c07fccaac588859c40a7fe7b2cb1`.
- Downloaded raw-output log SHA-256: `e899f5f297b372df7097d396f070536025aa614b1a85aafd639dd5d4903dec92`.
- Kernel status response SHA-256: `e1dd3bd4d4802439f03411103290656727f7baa2e63ab697f6f3b676a83b8b26`.
- The read-only audit could retrieve only the existing kernel log; all ten expected finalized files were missing from the downloaded output, including `pilot_records.jsonl`, `pilot_manifest.json`, QA/evaluation files, prompt files, and `artifact_manifest.json`. Kaggle CLI exit codes were zero but the returned file list contained only the log. The archive therefore proves the log was preserved, **not** that the raw records were recovered.

## Handling and scope

1. Keep this operational run separate from the official 40-record pilot archive and the 160-record confirmatory artifact. Never append or substitute its records, and never use the logged 0/20 and 0/20 figures to change official scores.
2. Do not represent it as confirmatory evidence, a successful hypothesis test, or proof of no CCDG effect. The historical frozen score remains Standard 0/80 vs CCDG 0/80 on the literal-alias endpoint and remains an inconclusive floor-effect result.
3. Keep the read-only audit artifact as the incident evidence. If complete raw files later become accessible in Kaggle, retrieve them separately, hash them, and preserve them under this incident identifier before any further analysis. Do not merge them into the research dataset.
4. The temporary trigger used for the audit should be removed once recovery is documented; keep the reusable read-only audit workflow and preserve the run artifact.

## Cause and corrective controls

The early feature-branch commit changed `.github/kaggle-pilot-trigger` before the main-only inference guard was present on that branch. That tooling error caused the unintended run. Current `main` controls:
- require both pilot and confirmatory inference jobs to run only on `main`;
- require the explicit `[pilot]` commit marker for push-triggered pilot inference;
- allow `[validate-only]` checks to run tests and integrity audits while skipping both inference jobs.

The current PR's latest validation-only runs passed 144 tests and historical artifact audits; no inference was launched by those validation jobs. This corrects the workflow guard, but does not erase the incident.

## Research stage status after the incident

- Technical repository validation: passed.
- Historical archived pilot/confirmatory artifact integrity: passed.
- Incident status/log recovery and retention: completed; raw JSONL recovery: unresolved.
- Independent source review, separate adjudication, and source-grounded scoring calibration: **still pending**.
- Calibration manifest remains draft/unfrozen, case pool remains unfrozen with `eligible_case_ids=[]`, and `model_inference_permitted=false`.
- Do not merge this draft PR, start calibration inference, or run a new confirmatory experiment before the human-evidence gates are genuinely complete.
