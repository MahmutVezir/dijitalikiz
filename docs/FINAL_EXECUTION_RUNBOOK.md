# Final Execution Runbook

## 1. Frozen pilot — 30 inference records

GitHub Actions -> Kaggle Frozen Pilot -> Run workflow -> set execute_inference=true.

The workflow:
- checks KAGGLE_API_TOKEN;
- resolves the Kaggle account automatically;
- packages the exact Git commit;
- runs preflight + model-load preflight on a private GPU kernel;
- executes 3 cases × 2 conditions × 5 seeds = 30 records;
- evaluates, aggregates 3/5 seed majority, builds QA and SHA-256 artifact manifest;
- returns the immutable pilot artifact to GitHub Actions.

Do not change model, revision, temperature, seeds, prompts, case IDs, or renderer after the pilot starts.

## 2. Confirmatory benchmark — 160 inference records

After a successful pilot artifact exists for the exact same commit, run:

GitHub Actions -> Kaggle Frozen Confirmatory -> Run workflow -> set execute_inference=true.

This workflow first verifies the pilot artifact checksum, then freezes the already-preselected 16-case manifest in the execution workspace. It then runs 16 cases × 2 conditions × 5 seeds = 160 records and produces:
- actual inference-machine environment metadata;
- raw run records and deterministic JSONL;
- confirmatory evaluation;
- case-level 3/5 aggregation;
- exact two-sided McNemar primary analysis;
- paired CCDG-minus-Standard effect and CI from the existing analysis pipeline;
- non-inferential QA;
- immutable SHA-256 artifact manifest.

## 3. What remains outside the repository

The repository cannot impersonate a user's GitHub Actions workflow_dispatch click. No secret is written to the repository and no automatic trigger is enabled.

Everything after the two manual starts is fail-closed and automated. The benchmark is intentionally not called scientifically complete until both inference stages finish successfully.

## 4. Final report gate

Only after the confirmatory artifact is complete should the Turkish TÜBİTAK report be populated with observed results. No numerical result, hypothesis decision, or effect estimate is stored in advance.
