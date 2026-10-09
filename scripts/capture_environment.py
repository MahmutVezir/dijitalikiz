from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version as distribution_version
from pathlib import Path


def command_output(command: list[str]) -> str:
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.STDOUT).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        return f"UNAVAILABLE: {exc}"


def gpu_snapshot() -> dict:
    try:
        import torch

        available = bool(torch.cuda.is_available())
        if not available:
            return {
                "cuda_available": False,
                "device_count": 0,
                "devices": [],
            }

        devices = []
        for index in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(index)
            devices.append({
                "index": index,
                "name": props.name,
                "total_memory_gib": round(props.total_memory / (1024**3), 3),
                "capability": f"{props.major}.{props.minor}",
            })
        return {
            "cuda_available": True,
            "device_count": len(devices),
            "devices": devices,
        }
    except Exception as exc:
        return {
            "cuda_available": False,
            "device_count": 0,
            "devices": [],
            "error": f"{type(exc).__name__}: {exc}",
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture the execution environment.")
    parser.add_argument("--output", default="data/pilot/environment.json")
    args = parser.parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": command_output(["git", "rev-parse", "HEAD"]),
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "gpu": gpu_snapshot(),
        "nvidia_smi": command_output(["nvidia-smi"]),
        "pip_freeze": command_output([sys.executable, "-m", "pip", "freeze"]),
    }

    for package in (
        "torch",
        "transformers",
        "accelerate",
        "optimum",
        "auto-gptq",
        "peft",
        "jsonschema",
        "numpy",
        "datasets",
        "pyarrow",
        "fsspec",
    ):
        key = package.replace("-", "_")
        try:
            payload[f"{key}_version"] = distribution_version(package)
        except PackageNotFoundError:
            payload[f"{key}_version"] = "UNAVAILABLE: PackageNotFoundError"
        try:
            module = __import__(key)
            payload[f"{key}_runtime_version"] = getattr(module, "__version__", "unknown")
        except Exception as exc:
            payload[f"{key}_runtime_version"] = (
                f"UNAVAILABLE: {type(exc).__name__}: {exc}"
            )

    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
