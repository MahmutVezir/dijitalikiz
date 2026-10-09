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
- Cases: MATH-927, MATH-950, MATH-949, MATH-988

## Frozen runtime compatibility lock

`requirements-pilot.txt` is checksum-locked by `data/pilot/pilot_manifest.json`.
The legacy GPTQ stack explicitly pins NumPy 1.26.4, PyArrow 15.0.2,
datasets 2.21.0, fsspec 2024.6.1 and PEFT 0.11.1 alongside the existing
Torch/Transformers/AutoGPTQ versions. This prevents the dependency resolver from
silently choosing the observed NumPy 1.x / PyArrow 26 incompatible combination.
The Kaggle launcher runs `pip check` before preflight; model-load preflight then
imports and version-checks the pinned data stack before loading the checkpoint.

## Execution rule

İlk inference başlamadan önce model, revision, temperature, seeds, prompt, case records ve context renderer frozen durumdadır. İlk inference sonrasında bunlardan hiçbiri değiştirilemez.

Runner fail-closed'dur: mevcut run kayıtlarını ezmez. Interrupted execution için `--resume` yalnızca eksik kayıtları tamamlamak amacıyla kullanılır.

## Kaggle Frozen Pilot

Desteklenen workflow adı: **Kaggle Frozen Pilot**.

- Workflow manual-only ve opt-in'dir.
- `execute_inference=true` olmadan job çalışmaz.
- GitHub Actions exact Git commit'i `git archive` ile private Kaggle kernel paketine koyar.
- Kaggle kernel; environment capture, CUDA preflight, model-load preflight, frozen audit, 40 inference ve finalization zincirini çalıştırır.
- Finalization sırası: integrity audit → evaluation → case-level analysis → QA → JSONL → artifact manifest.
- İndirilen artifact manifest workflow tarafından ayrıca SHA-256 doğrulanır.
- Deney çıktısı `main` branch'e otomatik commit edilmez.

Kaggle tarafında doğrudan private GitHub clone yapılmaz; gerekli kaynak exact bundle olarak taşınır.

## Local execution

```bash
pip install -r requirements-pilot.txt
python scripts/pilot_preflight.py --require-cuda
python scripts/model_load_preflight.py
python scripts/capture_environment.py
python scripts/run_pilot.py
```

Expected:
`4 cases × 2 conditions × 5 seeds = 40 records`

Sonrasında:

```bash
python scripts/finalize_pilot.py
```

Final artifacts:

```
data/pilot/pilot_records.jsonl
data/pilot/pilot_evaluation.json
data/pilot/case_level_analysis.json
data/pilot/pilot_qa_report.json
data/pilot/artifact_manifest.json
```

## Artifact integrity

`artifact_manifest.json` canonical pilot output listesini ve SHA-256 bütünlük bilgisini taşır.

Bağımsız doğrulama:

```bash
python scripts/validate_pilot_artifact_manifest.py
```

## Scientific gate

Pilot tamamlanmadan main benchmark freeze edilmez. Pilot çıktıları sadece execution integrity ve predeclared pilot analysis için kullanılır; confirmatory benchmark case selection sonuçlara göre geriye dönük yapılmaz.
