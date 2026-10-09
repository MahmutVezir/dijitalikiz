from __future__ import annotations

import argparse
import json
import platform
import sys
from importlib.metadata import PackageNotFoundError, version as distribution_version
from datetime import datetime, timezone
from pathlib import Path

MODEL_ID = "Qwen/Qwen2.5-3B-Instruct-GPTQ-Int4"
MODEL_REVISION = "68c4276063d1496cdf13d0b8e8221f899bfa77f7"


def package_version(name: str) -> str:
    try:
        return str(distribution_version(name.replace("_", "-")))
    except PackageNotFoundError:
        return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed load/compatibility gate for the frozen Qwen GPTQ pilot."
    )
    parser.add_argument("--output", default="data/pilot/model_load_preflight.json")
    args = parser.parse_args()

    import torch
    import transformers
    from huggingface_hub import model_info
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

    checks: list[dict] = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    check("model_revision_resolves",
          model_info(MODEL_ID, revision=MODEL_REVISION).sha == MODEL_REVISION,
          MODEL_REVISION)

    config = AutoConfig.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    qcfg = getattr(config, "quantization_config", None) or {}
    quant_method = qcfg.get("quant_method") if isinstance(qcfg, dict) else getattr(qcfg, "quant_method", None)
    bits = qcfg.get("bits") if isinstance(qcfg, dict) else getattr(qcfg, "bits", None)

    check("architecture_qwen2", getattr(config, "model_type", None) == "qwen2",
          f"model_type={getattr(config, 'model_type', None)!r}")
    check("quantization_method_gptq", str(quant_method).lower() == "gptq",
          f"quant_method={quant_method!r}")
    check("quantization_bits_4", int(bits) == 4,
          f"bits={bits!r}")
    check("transformers_version", transformers.__version__ == "4.43.2",
          f"actual={transformers.__version__}")
    check("torch_version", torch.__version__.split("+")[0] == "2.2.1",
          f"actual={torch.__version__}")
    check("auto_gptq_importable", package_version("auto_gptq") == "0.7.1",
          f"actual={package_version('auto_gptq')}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=MODEL_REVISION,
        torch_dtype="auto",
        device_map="auto",
    )
    check("tokenizer_loaded", tokenizer is not None, type(tokenizer).__name__)
    check("model_loaded", model is not None, type(model).__name__)
    check("model_class", model.__class__.__name__ == "Qwen2ForCausalLM",
          model.__class__.__name__)

    # A tiny, non-study smoke generation validates the actual GPTQ/Transformers
    # inference kernel before the 40 frozen study runs. It is not part of n=40.
    smoke = "Reply with exactly OK."
    inputs = tokenizer([smoke], return_tensors="pt").to(model.device)
    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=4,
            do_sample=False,
        )
    decoded = tokenizer.decode(
        output_ids[0][inputs.input_ids.shape[-1]:],
        skip_special_tokens=True,
    ).strip()
    check("smoke_generation", bool(decoded), f"decoded={decoded!r}")

    payload = {
        "status": "pass" if all(c["ok"] for c in checks) else "fail",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "model_id": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "checks": checks,
        "device_map": getattr(model, "hf_device_map", None),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["status"] != "pass":
        raise RuntimeError("Model load/GPTQ compatibility gate failed; frozen pilot not started.")
    print("MODEL LOAD PREFLIGHT PASSED: Qwen GPTQ checkpoint loaded and smoke generation succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
