from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version as distribution_version
from pathlib import Path

MODEL_ID = "Qwen/Qwen2.5-3B-Instruct-GPTQ-Int4"
MODEL_REVISION = "68c4276063d1496cdf13d0b8e8221f899bfa77f7"
FROZEN_PACKAGES = {
    "torch": "2.2.1",
    "transformers": "4.43.2",
    "accelerate": "0.33.0",
    "optimum": "1.17.1",
    "auto_gptq": "0.7.1",
    "jsonschema": "4.23.0",
    "numpy": "1.26.4",
    "datasets": "2.21.0",
    "pyarrow": "15.0.2",
    "fsspec": "2024.6.1",
}


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

    def write_report(device_map=None) -> dict:
        payload = {
            "status": "pass" if all(c["ok"] for c in checks) else "fail",
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "model_id": MODEL_ID,
            "model_revision": MODEL_REVISION,
            "checks": checks,
            "device_map": device_map,
        }
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return payload

    for package, expected in FROZEN_PACKAGES.items():
        actual = package_version(package)
        check(
            f"{package}_version",
            actual == expected,
            f"expected={expected}, actual={actual}",
        )

    # Import the transitive data stack explicitly before attempting GPTQ model load.
    # This catches NumPy/PyArrow ABI mismatches at the preflight boundary.
    try:
        import numpy
        import datasets
        import pyarrow
        import fsspec

        stack_detail = (
            f"numpy={numpy.__version__}; datasets={datasets.__version__}; "
            f"pyarrow={pyarrow.__version__}; fsspec={fsspec.__version__}"
        )
        check(
            "gptq_data_stack_imports",
            numpy.__version__ == FROZEN_PACKAGES["numpy"]
            and datasets.__version__ == FROZEN_PACKAGES["datasets"]
            and pyarrow.__version__ == FROZEN_PACKAGES["pyarrow"]
            and fsspec.__version__ == FROZEN_PACKAGES["fsspec"],
            stack_detail,
        )
    except Exception as exc:
        check(
            "gptq_data_stack_imports",
            False,
            f"{type(exc).__name__}: {exc}",
        )

    check(
        "torch_runtime_version",
        torch.__version__.split("+")[0] == FROZEN_PACKAGES["torch"],
        f"actual={torch.__version__}",
    )
    check(
        "transformers_runtime_version",
        transformers.__version__ == FROZEN_PACKAGES["transformers"],
        f"actual={transformers.__version__}",
    )

    try:
        resolved_sha = model_info(MODEL_ID, revision=MODEL_REVISION).sha
        check(
            "model_revision_resolves",
            resolved_sha == MODEL_REVISION,
            f"expected={MODEL_REVISION}, resolved={resolved_sha}",
        )
    except Exception as exc:
        check(
            "model_revision_resolves",
            False,
            f"{type(exc).__name__}: {exc}",
        )

    config = AutoConfig.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    qcfg = getattr(config, "quantization_config", None) or {}
    quant_method = (
        qcfg.get("quant_method")
        if isinstance(qcfg, dict)
        else getattr(qcfg, "quant_method", None)
    )
    bits = qcfg.get("bits") if isinstance(qcfg, dict) else getattr(qcfg, "bits", None)

    check(
        "architecture_qwen2",
        getattr(config, "model_type", None) == "qwen2",
        f"model_type={getattr(config, 'model_type', None)!r}",
    )
    check(
        "quantization_method_gptq",
        str(quant_method).lower() == "gptq",
        f"quant_method={quant_method!r}",
    )
    check(
        "quantization_bits_4",
        str(bits) == "4",
        f"bits={bits!r}",
    )

    # Persist diagnostics and stop before downloading/loading the large model if
    # any pinned runtime dependency failed its explicit compatibility checks.
    if not all(c["ok"] for c in checks):
        write_report()
        raise RuntimeError(
            "Model/data-stack compatibility gate failed; frozen pilot not started."
        )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=MODEL_REVISION,
        torch_dtype="auto",
        device_map="auto",
    )
    check("tokenizer_loaded", tokenizer is not None, type(tokenizer).__name__)
    check("model_loaded", model is not None, type(model).__name__)
    check(
        "model_class",
        model.__class__.__name__ == "Qwen2ForCausalLM",
        model.__class__.__name__,
    )

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

    payload = write_report(getattr(model, "hf_device_map", None))
    if payload["status"] != "pass":
        raise RuntimeError(
            "Model load/GPTQ compatibility gate failed; frozen pilot not started."
        )
    print(
        "MODEL LOAD PREFLIGHT PASSED: Qwen GPTQ checkpoint loaded and smoke generation succeeded."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
