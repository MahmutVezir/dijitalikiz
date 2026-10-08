from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/pilot/pilot_manifest.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_version(package: str) -> str | None:
    try:
        module = __import__(package.replace("-", "_"))
        return getattr(module, "__version__", None)
    except Exception:
        return None


def check(ok: bool, name: str, detail: str) -> dict:
    return {"ok": ok, "name": name, "detail": detail}


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed local preflight for the frozen TÜBİTAK pilot.")
    parser.add_argument("--require-cuda", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    results: list[dict] = []

    results.append(check(
        manifest.get("status") == "model_frozen",
        "manifest_frozen",
        f"status={manifest.get('status')!r}",
    ))

    for rel, key in (
        ("data/pilot/PROMPT_TEMPLATE.txt", "prompt"),
        ("data/pilot/SYSTEM_PROMPT.txt", "system_prompt"),
    ):
        path = ROOT / rel
        exists = path.is_file()
        digest = sha256_file(path) if exists else None
        expected = manifest[key]["sha256"]
        results.append(check(
            exists and digest == expected,
            f"{key}_hash",
            f"expected={expected}, actual={digest}",
        ))

    expected_cases = len(manifest["cases"]) * len(manifest["conditions"]) * len(manifest["generation"]["seeds"])
    results.append(check(
        manifest["replications"] == len(manifest["generation"]["seeds"]),
        "replication_seed_match",
        f"replications={manifest['replications']} seeds={len(manifest['generation']['seeds'])}",
    ))

    for case_id in manifest["cases"]:
        path = ROOT / "data/pilot" / f"{case_id}.json"
        results.append(check(path.is_file(), f"case_{case_id}", str(path)))

    results.append(check(
        shutil.which("git") is not None,
        "git_available",
        shutil.which("git") or "not found",
    ))

    for package in ("torch", "transformers", "accelerate", "optimum", "auto_gptq", "jsonschema"):
        installed = importlib.util.find_spec(package) is not None
        results.append(check(installed, f"python_package_{package}", "installed" if installed else "missing"))

    expected_runtime = manifest.get("runtime", {})
    requirements_path = expected_runtime.get("requirements_path")
    requirements_sha = expected_runtime.get("requirements_sha256")
    if requirements_path and requirements_sha:
        requirements_file = ROOT / requirements_path
        actual_requirements_sha = sha256_file(requirements_file) if requirements_file.is_file() else None
        results.append(check(
            actual_requirements_sha == requirements_sha,
            "requirements_frozen",
            f"expected={requirements_sha}, actual={actual_requirements_sha}",
        ))
    expected_python = expected_runtime.get("python")
    if expected_python:
        actual_python = f"{sys.version_info.major}.{sys.version_info.minor}"
        results.append(check(
            actual_python == expected_python,
            "python_version_frozen",
            f"expected={expected_python}, actual={actual_python}",
        ))

    for package_key in ("torch", "transformers", "accelerate", "optimum", "auto_gptq", "jsonschema"):
        expected = expected_runtime.get(package_key)
        if expected:
            actual = package_version(package_key)
            results.append(check(
                actual == expected,
                f"{package_key}_version_frozen",
                f"expected={expected}, actual={actual}",
            ))

    cuda_available = False
    cuda_detail = "torch unavailable"
    try:
        import torch
        cuda_available = bool(torch.cuda.is_available())
        if cuda_available:
            cuda_detail = f"{torch.cuda.get_device_name(0)}; VRAM={torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GiB"
        else:
            cuda_detail = "CUDA unavailable"
    except Exception as exc:
        cuda_detail = f"{type(exc).__name__}: {exc}"

    results.append(check(cuda_available or not args.require_cuda, "cuda", cuda_detail))

    # Verify that the exact revision can be resolved without changing the frozen manifest.
    revision_ok = False
    revision_detail = "not checked"
    try:
        from huggingface_hub import model_info
        info = model_info(
            manifest["model"]["model_id"],
            revision=manifest["model"]["revision"],
        )
        revision_ok = info.sha == manifest["model"]["revision"]
        revision_detail = f"resolved_sha={info.sha}"
    except Exception as exc:
        revision_detail = f"{type(exc).__name__}: {exc}"

    results.append(check(revision_ok, "exact_model_revision", revision_detail))

    payload = {
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "expected_records": expected_cases,
        "results": results,
    }

    failed = [r for r in results if not r["ok"]]
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if failed:
        print(f"\nPREFLIGHT FAILED: {len(failed)} check(s). Do not start inference.")
        return 1

    print(f"\nPREFLIGHT PASSED: local environment is eligible to start the frozen {expected_cases}-record pilot.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
