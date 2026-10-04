from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def command_output(command: list[str]) -> str:
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.STDOUT).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        return f"UNAVAILABLE: {exc}"


def main() -> None:
    parser_path = Path("data/pilot/environment.json")
    parser_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "pip_freeze": command_output([sys.executable, "-m", "pip", "freeze"]),
        "torch_version": None,
        "transformers_version": None,
        "accelerate_version": None,
        "optimum_version": None,
        "auto_gptq_version": None,
    }

    for package in (
        "torch",
        "transformers",
        "accelerate",
        "optimum",
        "auto_gptq",
    ):
        try:
            module = __import__(package.replace("-", "_"))
            payload[f"{package.replace('-', '_')}_version"] = getattr(module, "__version__", "unknown")
        except Exception as exc:
            payload[f"{package.replace('-', '_')}_version"] = f"UNAVAILABLE: {type(exc).__name__}: {exc}"

    parser_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {parser_path}")


if __name__ == "__main__":
    main()
