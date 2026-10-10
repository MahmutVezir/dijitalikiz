# Inference Trigger Incident — 2026-10-10

**Status:** GitHub Actions run #134 completed with failure after its Kaggle kernel reached `KernelWorkerStatus.COMPLETE`. This was not a successful cancellation. Required result artifacts were not retrieved; therefore the scientific contents and whether any model inferences were persisted remain unverified.

## Event record

- Workflow: [GitHub Actions run #134](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38047007838)
- Workflow run ID: `38047007838`
- Branch: `research/scoring-calibration-mainline-v2`
- Triggering commit: `c8b6f8f2e9647f1ab696387ccc9962051900102b`
- Triggering commit message: `Port research gate update: .github/kaggle-pilot-trigger`
- Job: `run-frozen-pilot` (job ID `114198449581`)
- Exact kernel: [`mahmutvezir/dijitalikiz-frozen-pilot-c8b6f8f2-38047007838-1`](https://www.kaggle.com/code/mahmutvezir/dijitalikiz-frozen-pilot-c8b6f8f2-38047007838-1)
- Kernel source commit embedded by the launcher: `c8b6f8f2e9647f1ab696387ccc9962051900102b`
- Generated launcher SHA-256: `0a39fe1e5844e94a525400af599cdd7a8e3930ab3de63b147ae6e39092f2a9b1`
- Generated kernel metadata SHA-256: `54decd7fde182ff142f1077b02f6988e377a17277bfcfe51f507cbeb238dc6bc`
- GitHub log records Kaggle state `QUEUED` at 11:03:06 UTC, `RUNNING` from 11:04:07 through 11:11:13 UTC, and `COMPLETE` at 11:12:14 UTC on 2026-10-10.
- The subsequent `Download finalized pilot output` step downloaded only `dijitalikiz-frozen-pilot-c8b6f8f2-38047007838-1.log`; it failed with `Missing finalized Kaggle artifact: pilot_manifest.json`. Artifact validation and GitHub artifact upload were skipped.
- The CI runner's downloaded Kaggle log file was in its temporary workspace and was not uploaded as an artifact. This audit cannot establish whether inference records were created inside Kaggle.

The event occurred because the trigger file was committed to the research branch before that branch contained the main-only inference guard. This was an operator/tooling error and is documented rather than hidden.

## Required audit and containment

1. Inspect the exact Kaggle kernel above and retrieve its complete output/logs. Record the execution status, whether model loading and inference occurred, output files, timestamps, and hashes. The GitHub Actions run's failure alone does not prove that no inference occurred.
2. If records or outputs exist, preserve them separately with this incident identifier. Do not append them to, replace, or score them as part of the historical frozen pilot or confirmatory dataset.
3. Mark the run as an unplanned operational execution. Exclude it from all confirmatory analyses and TÜBİTAK result claims. Do not interpret missing downloaded artifacts as zero records or a model failure without inspecting the actual Kaggle log.
4. Keep the historical pilot/confirmatory records and reported scores unchanged.

## Corrective changes present on `main` at the audit check

- Both frozen-pilot and confirmatory inference jobs require `github.ref == 'refs/heads/main'`.
- Push-triggered pilot inference additionally requires the explicit `[pilot]` commit marker; a normal merge commit or generic trigger-file edit is not enough.
- `tests/test_kaggle_workflow_safety.py` checks the main-branch guard and explicit pilot marker.
- Validation-only runs use `[validate-only]` and should skip inference jobs.

## Scientific status

- This operational run is **not** a valid pilot result: no required output manifest was retrieved, validated, or archived.
- Existing historical results remain unchanged. The historic endpoint's Standard 0/80 and CCDG 0/80 outcome is still a floor-effect/inconclusive result, not proof of no effect or equivalence.
- PR #6 stays a draft pending current-head CI validation and independent human review. No case labels, adjudications, calibration examples, or experiment results may be fabricated to close those gates.
