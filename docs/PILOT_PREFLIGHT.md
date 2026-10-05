# Pilot Preflight

This document is the execution gate for the frozen 30-run pilot.

## 1. Install the frozen pilot environment

From the repository root:

```bash
python -m pip install -r requirements-pilot.txt
```

## 2. Run the fail-closed preflight

```bash
python scripts/pilot_preflight.py --require-cuda
```

Do not start inference if this command fails.

The preflight checks:
- frozen manifest status;
- prompt and system-prompt SHA-256 hashes;
- replication/seed consistency;
- all three pilot case files;
- required Python packages;
- CUDA availability;
- exact Hugging Face checkpoint revision resolution;
- expected pilot size (30 records).

## 3. Capture the actual inference environment

```bash
python scripts/capture_environment.py
```

Preserve `data/pilot/environment.json` with the pilot artifacts. It records Python, platform, pip freeze, and relevant ML package versions.

## 4. Run the frozen pilot

```bash
python scripts/run_pilot.py
```

Expected output: exactly 30 JSON records under `data/pilot/runs/`.

The runner must not be modified after the pilot starts. If it fails part-way through, keep the generated records and document the interruption; do not silently rerun or overwrite an existing seed record without preserving provenance.

## 5. Evaluate

```bash
python scripts/evaluate_pilot.py
```

Then:

```bash
python scripts/analyze_case_level.py \
  --evaluation data/pilot/pilot_evaluation.json \
  --case-ids commons-math-defects4j-MATH-927 commons-math-defects4j-MATH-950 commons-math-defects4j-MATH-988 \
  --output data/pilot/case_level_analysis.json
```

## 6. Integrity gate

```bash
python scripts/audit_pilot_integrity.py
```

A successful audit is required before interpreting pilot results.

## 7. Immutable evidence

Before any interpretation, preserve:
- raw run JSON files;
- `pilot_manifest.json`;
- prompt/system prompt files;
- `environment.json`;
- `pilot_evaluation.json`;
- `case_level_analysis.json`;
- preflight output;
- integrity-audit output.

Do not change the frozen model, prompts, seeds, evaluation rule, or pilot cases because of observed outcomes.

## Current boundary

Repository-side Phase 1 preparation is complete. Actual environment capture, checkpoint availability verification on the inference machine, and the 30 real model calls must be executed on the machine that will perform the experiment. Those results cannot be fabricated or simulated in the repository.
