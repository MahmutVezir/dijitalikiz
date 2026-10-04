# Pilot Execution Readiness

Status: model configuration frozen; local inference execution pending.

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

The selected Hugging Face model is the official Qwen2.5 3B Instruct GPTQ-Int4 checkpoint. The model repository documents 3.09B parameters, 32,768-token context, 4-bit GPTQ quantization, and Transformers loading. The exact revision is pinned in the pilot manifest.

## Execution rule

Do not change model, revision, temperature, seeds, prompt template, case records, or context renderer after the first pilot inference.

## Local execution

Install:

    pip install -r requirements-pilot.txt

Then from the repository root:

    python scripts/run_pilot.py

Outputs are written to:

    data/pilot/runs/

Expected inference records:

    3 cases x 2 conditions x 5 seeds = 30 records.

No accuracy claim should be made from the pilot alone. Pilot results must first be inspected for parse failures, repeated identical generations, condition contamination, and obvious schema violations before proceeding to the main benchmark.
