from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Load-only smoke test for the frozen pilot model.")
    parser.add_argument("--manifest", default="data/pilot/pilot_manifest.json")
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    if manifest.get("status") != "model_frozen":
        raise RuntimeError("Pilot manifest is not frozen.")

    model_id = manifest["model"]["model_id"]
    revision = manifest["model"]["revision"]

    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        torch_dtype="auto",
        device_map="auto",
    )

    device = str(getattr(model, "device", "unknown"))
    quantization_config = getattr(getattr(model, "config", None), "quantization_config", None)

    print(json.dumps({
        "status": "pass",
        "model_id": model_id,
        "revision": revision,
        "model_class": type(model).__name__,
        "tokenizer_class": type(tokenizer).__name__,
        "device": device,
        "quantization_config_type": type(quantization_config).__name__ if quantization_config is not None else None,
        "parameter_count": sum(parameter.numel() for parameter in model.parameters()),
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
