# Inference Trigger Incident — 2026-10-10

**Status at last check:** The workflow was still running; the kernel could not be cancelled through the available GitHub connector. Operator cancellation is required.

## Event record

- Workflow: [GitHub Actions run #134](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38047007838)
- Workflow ID: `38047007838`
- Branch: `research/scoring-calibration-mainline-v2`
- Triggering commit: `c8b6f8f2e9647f1ab696387ccc9962051900102b`
- Triggering commit message: `Port research gate update: .github/kaggle-pilot-trigger`
- Job: `run-frozen-pilot`
- Last observed step state: `Push immutable Kaggle frozen pilot` succeeded; `Wait for Kaggle frozen pilot` was still in progress.
- Predicted kernel slug from the checked-in launcher convention: `mahmutvezir/dijitalikiz-frozen-pilot-c8b6f8f2-38047007838-1`.

The event occurred because the trigger file was committed to the research branch before the main-only inference guard had been ported into that branch. The push event therefore matched the older condition, which started the frozen-pilot job. This was an operator/tooling error and must not be hidden.

## Immediate containment

1. Manually cancel [run #134](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38047007838) in GitHub Actions.
2. Inspect the named Kaggle kernel. If it remains active after the GitHub workflow is cancelled, stop/cancel it in Kaggle as well.
3. If an artifact was already finalized or uploaded, preserve it for audit and label it as an unintended operational run. **Do not merge its records into the frozen pilot or confirmatory datasets and do not use it to alter any reported score.**
4. Do not claim the kernel was cancelled or that no inference occurred until the Actions and Kaggle states are checked by an operator.

## Corrective changes now present on `main`

- Both frozen-pilot and confirmatory inference jobs require `github.ref == 'refs/heads/main'`.
- Push-triggered pilot inference now additionally requires the explicit `[pilot]` commit marker; a normal merge commit or generic trigger-file edit is no longer sufficient.
- `tests/test_kaggle_workflow_safety.py` checks the main-branch guard and explicit pilot marker.
- Research-only review and calibration work stays on a separate branch. New validation runs use `[validate-only]` and should skip both inference jobs.

The latest source review/calibration PR remains a draft. The historical pilot and confirmatory artifacts must remain unchanged. The inadvertent workflow run, if completed, is a separate operational incident and is not part of the study.
