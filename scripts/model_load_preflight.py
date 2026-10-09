from __future__ import annotations

import json
import platform
import random
import sys
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version as distribution_version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "pilot" / "pilot_manifest.json"
FROZEN_PACKAGE_KEYS = (
    "torch",
    "transformers",
    "accelerate",
    "jsonschema",
    "numpy",
    "datasets",
    "pyarrow",
    "fsspec",
)


def package_version(name: str) -> str:
    try:
        return str(distribution_version(name.replace("_", "-")))
    except PackageNotFoundError:
        return "unknown"


def main() -> int:
    import torch
    import transformers
    import numpy
    import datasets
    import pyarrow
    import fsspec
    from huggingface_hub import model_info
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    model_spec = manifest["model"]
    runtime = manifest["runtime"]
    generation = manifest["generation"]
    model_id = model_spec["model_id"]
    revision = model_spec["revision"]
    precision = model_spec["precision"]

    checks: list[dict] = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    def write_report(device_map=None) -> dict:
        payload = {
            "status": "pass" if all(item["ok"] for item in checks) else "fail",
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "model_id": model_id,
            "model_revision": revision,
            "precision": precision,
            "quantization": model_spec.get("quantization"),
            "checks": checks,
            "device_map": device_map,
        }
        output = ROOT / "data" / "pilot" / "model_load_preflight.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return payload

    # Freeze and verify the complete runtime before loading model weights.
    for package_key in FROZEN_PACKAGE_KEYS:
        expected = runtime.get(package_key)
        actual = package_version(package_key)
        check(
            f"{package_key}_version",
            bool(expected) and actual == expected,
            f"expected={expected}, actual={actual}",
        )

    check(
        "data_stack_imports",
        all(
            [
                numpy.__version__ == runtime["numpy"],
                datasets.__version__ == runtime["datasets"],
                pyarrow.__version__ == runtime["pyarrow"],
                fsspec.__version__ == runtime["fsspec"],
            ]
        ),
        (
            f"numpy={numpy.__version__}; datasets={datasets.__version__}; "
            f"pyarrow={pyarrow.__version__}; fsspec={fsspec.__version__}"
        ),
    )
    check(
        "torch_runtime_version",
        torch.__version__.split("+")[0] == runtime["torch"],
        f"actual={torch.__version__}",
    )
    check(
        "transformers_runtime_version",
        transformers.__version__ == runtime["transformers"],
        f"actual={transformers.__version__}",
    )

    try:
        resolved_sha = model_info(model_id, revision=revision).sha
        check(
            "model_revision_resolves",
            resolved_sha == revision,
            f"expected={revision}, resolved={resolved_sha}",
        )
    except Exception as exc:
        check(
            "model_revision_resolves",
            False,
            f"{type(exc).__name__}: {exc}",
        )

    config = AutoConfig.from_pretrained(model_id, revision=revision)
    quantization_config = getattr(config, "quantization_config", None)
    check(
        "architecture_qwen2",
        getattr(config, "model_type", None) == "qwen2",
        f"model_type={getattr(config, 'model_type', None)!r}",
    )
    check(
        "quantization_disabled",
        not quantization_config,
        f"quantization_config={quantization_config!r}",
    )
    check(
        "frozen_precision_fp16",
        precision == "float16",
        f"manifest_precision={precision!r}",
    )
    check(
        "cuda_available",
        torch.cuda.is_available(),
        "CUDA available" if torch.cuda.is_available() else "CUDA unavailable",
    )

    # A failed dependency/config check must stop before model load or study inference.
    if not all(item["ok"] for item in checks):
        write_report()
        raise RuntimeError("Frozen model/runtime compatibility gate failed.")

    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    model, loading_info = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        torch_dtype=torch.float16,
        device_map="auto",
        output_loading_info=True,
    )

    check("tokenizer_loaded", tokenizer is not None, type(tokenizer).__name__)
    check(
        "model_class",
        model.__class__.__name__ == "Qwen2ForCausalLM",
        model.__class__.__name__,
    )
    model_dtype = str(next(model.parameters()).dtype)
    check(
        "loaded_model_dtype_fp16",
        next(model.parameters()).dtype == torch.float16,
        model_dtype,
    )

    tied_output_weight = bool(getattr(model.config, "tie_word_embeddings", False))
    missing_keys = list(loading_info.get("missing_keys", []))
    if tied_output_weight:
        missing_keys = [key for key in missing_keys if key != "lm_head.weight"]
    unexpected_keys = list(loading_info.get("unexpected_keys", []))
    mismatched_keys = list(loading_info.get("mismatched_keys", []))
    error_messages = list(loading_info.get("error_msgs", []))
    check(
        "checkpoint_weights_match_model",
        not missing_keys and not unexpected_keys and not mismatched_keys and not error_messages,
        (
            f"missing_keys={missing_keys[:10]}; unexpected_keys={unexpected_keys[:10]}; "
            f"mismatched_keys={mismatched_keys[:10]}; error_msgs={error_messages[:3]}"
        ),
    )

    # Test finite logits before running the same sampling mode used by the frozen pilot.
    smoke = "Reply with exactly OK."
    inputs = tokenizer([smoke], return_tensors="pt").to(model.device)
    finite_logits = False
    logits_detail = "not evaluated"
    try:
        with torch.inference_mode():
            logits = model(**inputs, use_cache=False).logits
            finite_logits = bool(torch.isfinite(logits).all().item())
        logits_detail = f"finite={finite_logits}; shape={tuple(logits.shape)}; dtype={logits.dtype}"
    except Exception as exc:
        logits_detail = f"{type(exc).__name__}: {exc}"
    check("smoke_logits_finite", finite_logits, logits_detail)

    sampled_ok = False
    sampled_detail = "not evaluated"
    try:
        random.seed(42)
        torch.manual_seed(42)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(42)
        with torch.inference_mode():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=min(4, int(generation["max_new_tokens"])),
                do_sample=bool(generation["do_sample"]),
                temperature=float(generation["temperature"]),
                top_p=float(generation["top_p"]),
            )
        decoded = tokenizer.decode(
            output_ids[0][inputs.input_ids.shape[-1]:],
            skip_special_tokens=True,
        ).strip()
        sampled_ok = bool(decoded)
        sampled_detail = f"decoded={decoded!r}"
    except Exception as exc:
        sampled_detail = f"{type(exc).__name__}: {exc}"
    check("pilot_sampling_smoke", sampled_ok, sampled_detail)

    payload = write_report(getattr(model, "hf_device_map", None))
    if payload["status"] != "pass":
        raise RuntimeError(
            "Model loading or pilot-mode sampling preflight failed; study inference not started."
        )
    print(
        "MODEL LOAD PREFLIGHT PASSED: exact checkpoint weights match, FP16 logits are finite, "
        "and frozen sampling-mode smoke generation succeeded."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
