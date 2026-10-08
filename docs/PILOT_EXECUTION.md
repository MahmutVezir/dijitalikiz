# Pilot Execution Readiness

Status: model configuration frozen; local/Kaggle inference execution pending.

## Frozen configuration

- Model: Qwen/Qwen2.5-3B-Instruct-GPTQ-Int4
- Hugging Face revision: 68c4276063d1496cdf13d0b8e8221f899bfa77f7
- Quantization: GPTQ 4-bit
- Replications: 5
- Seeds: 42, 43, 44, 45, 46
- Temperature: 0.2
- Top-p: 1.0
- Sampling: enabled
- Maximum new tokens: 256
- Conditions: Standard and CCDG
- Cases: MATH-927, MATH-950, MATH-988

The selected Hugging Face model is the official Qwen2.5 3B Instruct GPTQ-Int4 checkpoint. The model card documents direct Transformers loading with `device_map="auto"`; the exact revision is pinned in the pilot manifest.

## Execution rule

Do not change model, revision, temperature, seeds, prompt template, case records, or context renderer after the first pilot inference.

The runner is fail-closed: if frozen run files already exist, a normal invocation stops rather than overwriting them. Use `--resume` only to preserve existing records and generate missing records after an interrupted execution.

## Kaggle execution

The supported automated route is the GitHub Actions workflow:

1. Open **Actions → Kaggle Pilot**.
2. Select **Run workflow**.
3. Keep `run_pilot=true`.
4. The workflow checks out the exact Git commit and packages that source tree into the private Kaggle kernel.
5. Kaggle runs the CUDA preflight, environment capture, frozen integrity audit, 30 inferences, second integrity audit, evaluator, and case-level analysis.
6. The workflow waits for completion and downloads the Kaggle output as a GitHub Actions artifact named with the source commit.

The workflow is intentionally **manual-only**. A normal push to `main` must never launch a 30-run scientific inference automatically.

This packaging design is required because the research repository is private; the Kaggle kernel must not attempt an unauthenticated `git clone` of the repository.

## Local execution

Install:

    pip install -r requirements-pilot.txt

Before inference, verify the environment:

    python scripts/pilot_preflight.py --require-cuda

The preflight now checks the exact runtime versions declared in `data/pilot/pilot_manifest.json`.

Then perform the load-only model smoke test (no experimental generation is performed):

    python scripts/model_load_preflight.py

Capture the environment:

    python scripts/capture_environment.py

Then run:

    python scripts/run_pilot.py

For an interrupted run, preserve existing records:

    python scripts/run_pilot.py --resume

Outputs are written to:

    data/pilot/runs/

Expected inference records:

    3 cases x 2 conditions x 5 seeds = 30 records.

No accuracy claim should be made from the pilot alone. Pilot results must first be inspected for parse failures, repeated identical generations, condition contamination, and obvious schema violations before proceeding to the main benchmark.

## Automated pilot evaluation

After inference completes, run:

    python scripts/evaluate_pilot.py

This reads the stored inference records without calling the model again and writes:

    data/pilot/pilot_evaluation.json

Then run:

    python scripts/analyze_case_level.py \
      --evaluation data/pilot/pilot_evaluation.json \
      --case-ids commons-math-defects4j-MATH-927 commons-math-defects4j-MATH-950 commons-math-defects4j-MATH-988 \
      --output data/pilot/case_level_analysis.json

The evaluator reports, separately for Standard and CCDG:

- number of expected/found records
- parse success and parse-failure rate
- deterministic diagnostic pass count and pass rate
- repeated identical parsed outputs across different seeds

It also records per-run scoring details. Missing inference records make the evaluation status `incomplete`.

The evaluation uses the frozen deterministic matcher in `dijitalikiz/evaluation.py`. Do not change that matcher after pilot inference has started; otherwise the pilot would no longer be scored under a frozen analysis rule.
