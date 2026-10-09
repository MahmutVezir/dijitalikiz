# Frozen Pilot Execution — Completed State

**Status:** The frozen 40-inference pilot completed successfully and its artifact passed independent integrity verification on 2026-10-09. This supersedes earlier readiness notes that described execution as pending.

## Frozen configuration

- Model: Qwen/Qwen2.5-3B-Instruct
- Hugging Face revision: aa8e72537993ba99e69dfaafa59ed015b17504d1
- Quantization: none
- Load precision: FP16 (source checkpoint uses BF16 weights)
- Replications: 5
- Seeds: 42, 43, 44, 45, 46
- Temperature: 0.2
- Top-p: 1.0
- Sampling: enabled
- Maximum new tokens: 256
- Conditions: Standard and CCDG
- Cases: MATH-927, MATH-950, MATH-949, MATH-988

## Runtime compatibility lock

`requirements-pilot.txt` is checksum-locked by `data/pilot/pilot_manifest.json`. The runtime pins Torch 2.2.1, Transformers 4.43.2, Accelerate 0.33.0, NumPy 1.26.4, PyArrow 15.0.2, datasets 2.21.0 and fsspec 2024.6.1. AutoGPTQ/Optimum/PEFT are not used in this inference lane. The former GPTQ checkpoint was rejected before any study record was written because the loader reported unexpected parameter initialization and stochastic generation failed with invalid sampling probabilities.

## Execution record

- Workflow: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37968099402
- Source commit: `d50adaf9b6d0b017a5d30c9ebd9dd404988dbfb5`
- Artifact ID: `11634641753`
- Archive SHA-256: `b12594415894d5cac18442d3bd6c505e843b1a14027272c1afa398a59101aca0`
- Expected / found records: 40 / 40.
- Parse failures: 0.
- Internal artifact file inventory: 55 files, all size/hash checks passed; no missing or unexpected files.
- Original strict complete-diagnostic endpoint: Standard 0/20, CCDG 0/20; no case passed the 3-of-5 case rule.

## Artifact and interpretation

The original pilot evaluation and all raw records remain unchanged. The pilot exposed a potential construct-validity weakness in literal canonical matching. The pre-confirmatory scoring amendment is documented in `docs/CONFIRMATORY_SCORING_PROTOCOL.md`; it does not relabel pilot scores or allow the confirmatory rubric to be changed after main outputs are seen.

The pilot is feasibility/scoring-protocol evidence, not sufficient evidence that CCDG helps or does not help.
