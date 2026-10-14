from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data/pilot/pilot_manifest.json"
REPORT_PATH = ROOT / "data/pilot/compatibility_report.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def main() -> int:
    checks: list[dict] = []
    model = None
    tokenizer = None
    manifest: dict = {}
    device_map = None

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "status": "pass" if ok else "fail", "detail": detail})

    def run_check(name: str, fn) -> None:
        try:
            detail = fn()
            check(name, True, str(detail))
        except Exception as exc:
            check(name, False, f"{type(exc).__name__}: {exc}")

    def report() -> dict:
        payload = {
            "schema_version": 1,
            "status": "pass" if checks and all(c["status"] == "pass" for c in checks) else "fail",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_commit": _source_commit(),
            "python": sys.version,
            "platform": platform.platform(),
            "model_id": manifest.get("model", {}).get("model_id"),
            "model_revision": manifest.get("model", {}).get("revision"),
            "quantization": manifest.get("model", {}).get("quantization"),
            "precision": manifest.get("model", {}).get("precision"),
            "expected_records": manifest.get("expected_records"),
            "pilot_authorized": bool(checks) and all(c["status"] == "pass" for c in checks),
            "checks": checks,
        }
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(payload, indent=2, ensure_ascii=False), flush=True)
        return payload

    def _load_manifest() -> str:
        nonlocal manifest
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        if manifest.get("status") != "model_frozen":
            raise ValueError(f"manifest status is {manifest.get('status')!r}")
        if manifest.get("model", {}).get("model_id") != "Qwen/Qwen2.5-3B-Instruct":
            raise ValueError("This frozen gate only authorizes the non-quantized Qwen2.5-3B-Instruct lane.")
        if manifest.get("model", {}).get("quantization") != "none":
            raise ValueError("Quantization must be 'none'; GPTQ lane is not authorized for this pilot.")
        if manifest.get("model", {}).get("precision") != "float16":
            raise ValueError("Frozen precision must be float16.")
        if manifest.get("runtime", {}).get("python") != "3.11":
            raise ValueError("Frozen runtime must use Python 3.11.")
        if manifest.get("runtime", {}).get("requirements_path") != "requirements-pilot.txt":
            raise ValueError("Unexpected requirements file.")
        cases = manifest.get("cases", [])
        conditions = manifest.get("conditions", [])
        seeds = manifest.get("generation", {}).get("seeds", [])
        expected = len(cases) * len(conditions) * len(seeds)
        if not cases or conditions != ["standard", "ccdg"] or not seeds:
            raise ValueError("Invalid frozen case/condition/seed contract.")
        if manifest.get("replications") != len(seeds) or manifest.get("expected_records") != expected:
            raise ValueError(f"Record count contract mismatch: calculated={expected}, declared={manifest.get('expected_records')}")
        return f"frozen manifest valid; expected_records={expected}"

    def _source_commit() -> str:
        marker = ROOT / "data/pilot/kaggle_source_commit.txt"
        if marker.is_file():
            return marker.read_text(encoding="utf-8").strip()
        try:
            import subprocess
            return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        except Exception:
            return "unknown"

    run_check("frozen_manifest_and_record_contract", _load_manifest)
    if not manifest:
        report()
        return 1

    runtime = manifest["runtime"]
    for package in ("torch", "transformers", "accelerate", "jsonschema", "numpy", "datasets", "pyarrow", "fsspec"):
        actual = package_version(package)
        expected = runtime.get(package)
        check(f"package_version_{package}", actual == expected, f"expected={expected!r}; actual={actual!r}")

    try:
        import torch
        import transformers
        import jsonschema
        from huggingface_hub import model_info
        from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

        check("transformers_runtime_version", transformers.__version__ == runtime["transformers"],
              f"expected={runtime['transformers']}; actual={transformers.__version__}")
        check("torch_runtime_version", torch.__version__.split("+")[0] == runtime["torch"],
              f"expected={runtime['torch']}; actual={torch.__version__}")
    except Exception as exc:
        check("critical_imports", False, f"{type(exc).__name__}: {exc}")
        report()
        return 1

    for rel, key in (
        ("data/pilot/PROMPT_TEMPLATE.txt", "prompt"),
        ("data/pilot/SYSTEM_PROMPT.txt", "system_prompt"),
    ):
        path = ROOT / rel
        try:
            actual = sha256_file(path)
            expected = manifest[key]["sha256"]
            check(f"{key}_sha256", actual == expected, f"expected={expected}; actual={actual}")
        except Exception as exc:
            check(f"{key}_sha256", False, f"{type(exc).__name__}: {exc}")

    req_path = ROOT / runtime["requirements_path"]
    try:
        actual = sha256_file(req_path)
        expected = runtime["requirements_sha256"]
        check("requirements_sha256", actual == expected, f"expected={expected}; actual={actual}")
    except Exception as exc:
        check("requirements_sha256", False, f"{type(exc).__name__}: {exc}")

    try:
        import subprocess
        pip_check = subprocess.run([sys.executable, "-m", "pip", "check"], capture_output=True, text=True)
        check("pip_dependency_consistency", pip_check.returncode == 0,
              (pip_check.stdout + pip_check.stderr).strip() or f"exit={pip_check.returncode}")
    except Exception as exc:
        check("pip_dependency_consistency", False, f"{type(exc).__name__}: {exc}")

    cuda_ok = bool(torch.cuda.is_available()) and torch.cuda.device_count() >= 1
    if cuda_ok:
        devices = [
            {
                "index": i,
                "name": torch.cuda.get_device_name(i),
                "capability": ".".join(map(str, torch.cuda.get_device_capability(i))),
                "memory_gib": round(torch.cuda.get_device_properties(i).total_memory / 1024**3, 2),
            }
            for i in range(torch.cuda.device_count())
        ]
        cuda_detail = json.dumps({"cuda_version": torch.version.cuda, "devices": devices})
    else:
        cuda_detail = f"cuda_available={torch.cuda.is_available()}; device_count={torch.cuda.device_count()}"
    check("cuda_gpu_visibility", cuda_ok, cuda_detail)

    model_id = manifest["model"]["model_id"]
    revision = manifest["model"]["revision"]
    try:
        info = model_info(model_id, revision=revision)
        revision_ok = info.sha == revision
        check("exact_model_revision", revision_ok, f"expected={revision}; resolved={info.sha}")
    except Exception as exc:
        check("exact_model_revision", False, f"{type(exc).__name__}: {exc}")

    # Do not attempt model loading when any static/runtime prerequisite has failed.
    static_failed = [c for c in checks if c["status"] == "fail"]
    if static_failed:
        check("model_loading_and_smoke_inference", False, "not run because one or more prerequisite checks failed")
        check("diagnostic_output_schema", False, "not run because model inference was blocked")
        payload = report()
        return 0 if payload["status"] == "pass" else 1

    try:
        config = AutoConfig.from_pretrained(model_id, revision=revision)
        check("model_architecture", getattr(config, "model_type", None) == "qwen2",
              f"model_type={getattr(config, 'model_type', None)!r}")
        qcfg = getattr(config, "quantization_config", None)
        check("quantization_backend", not qcfg and manifest["model"].get("quantization") == "none",
              f"manifest_quantization={manifest['model'].get('quantization')!r}; config_quantization={qcfg!r}")
        if any(c["status"] == "fail" for c in checks):
            raise RuntimeError("Model configuration or quantization profile failed.")

        tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
        model, loading_info = AutoModelForCausalLM.from_pretrained(
            model_id,
            revision=revision,
            torch_dtype=torch.float16,
            device_map="auto",
            output_loading_info=True,
        )
        missing = list(loading_info.get("missing_keys", []))
        if getattr(model.config, "tie_word_embeddings", False):
            missing = [k for k in missing if k != "lm_head.weight"]
        unexpected = list(loading_info.get("unexpected_keys", []))
        mismatched = list(loading_info.get("mismatched_keys", []))
        errors = list(loading_info.get("error_msgs", []))
        if missing or unexpected or mismatched or errors:
            raise RuntimeError(f"checkpoint weight mismatch: missing={missing[:8]}, unexpected={unexpected[:8]}, mismatched={mismatched[:8]}, errors={errors[:3]}")
        if next(model.parameters()).dtype != torch.float16:
            raise RuntimeError(f"model dtype mismatch: {next(model.parameters()).dtype}")
        device_map = getattr(model, "hf_device_map", None)

        smoke_messages = [
            {"role": "system", "content": "Return exactly one JSON object with string fields diagnosed_component, root_cause_class, affected_entity, explanation. No Markdown."},
            {"role": "user", "content": "A test-only synthetic defect exists in component Parser: malformed input is accepted. Return a concise JSON diagnosis with exactly those four string fields."},
        ]
        smoke_text = tokenizer.apply_chat_template(smoke_messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer([smoke_text], return_tensors="pt").to(model.device)
        with torch.inference_mode():
            logits = model(**inputs, use_cache=False).logits
            if not bool(torch.isfinite(logits).all().item()):
                raise RuntimeError("smoke logits contain NaN or infinity")
            generated = model.generate(
                **inputs,
                max_new_tokens=96,
                do_sample=False,
            )
        raw = tokenizer.decode(generated[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True).strip()
        check("model_loading_and_smoke_inference", bool(raw), f"dtype={next(model.parameters()).dtype}; device_map={device_map}; output_chars={len(raw)}")
        parsed = json.loads(raw)
        schema_path = ROOT / "schemas/diagnostic_output.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        errors = list(jsonschema.Draft202012Validator(schema).iter_errors(parsed))
        check("diagnostic_output_schema", not errors, f"output={parsed!r}; schema_errors={[e.message for e in errors[:5]]}")
    except Exception as exc:
        if not any(c["name"] == "model_loading_and_smoke_inference" for c in checks):
            check("model_loading_and_smoke_inference", False, f"{type(exc).__name__}: {exc}")
        elif checks[-1]["name"] != "diagnostic_output_schema":
            check("diagnostic_output_schema", False, f"{type(exc).__name__}: {exc}")
        elif checks[-1]["status"] == "pass":
            check("post-inference_exception", False, f"{type(exc).__name__}: {exc}")

    payload = report()
    if payload["status"] != "pass":
        print("COMPATIBILITY GATE FAILED: pilot must not start.", file=sys.stderr, flush=True)
        return 1
    print("COMPATIBILITY GATE PASSED: frozen pilot is authorized to start.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
