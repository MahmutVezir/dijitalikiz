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


def check(ok: bool, name: str, detail: str) -> dict:
    return {"ok": ok, "name": name, "detail": detail}


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed local preflight for the frozen TÜBİTAK pilot.")
    parser.add_argument("--require-cuda", action="store_true")
    parser.add_argument("--output", default="data/pilot/preflight.json")
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
    results.append(check(
        expected_cases == 30,
        "expected_pilot_size",
        f"expected_records={expected_cases}",
    ))

    for case_id in manifest["cases"]:
        path = ROOT / "data/pilot" / f"{case_id}.json"
        results.append(check(path.is_file(), f"case_{case_id}", str(path)))

    results.append(check(
        shutil.which("git") is not None,
        "git_available",
        shutil.which("git") or "not found",
    ))

    for package in ("torch", "transformers", "accelerate", "optimum"):
        installed = importlib.util.find_spec(package) is not None
        results.append(check(installed, f"python_package_{package}", "installed" if installed else "missing"))

    cuda_available = False
    cuda_detail = "torch unavailable"
    try:
        import torch
        cuda_available = bool(torch.cuda.is_available())
        if cuda_available:
            props = torch.cuda.get_device_properties(0)
            cuda_detail = (
                f"{torch.cuda.get_device_name(0)}; "
                f"VRAM={props.total_memory / (1024**3):.2f} GiB; "
                f"CUDA={torch.version.cuda}"
            )
        else:
            cuda_detail = "CUDA unavailable"
    except Exception as exc:
        cuda_detail = f"{type(exc).__name__}: {exc}"

    results.append(check(cuda_available or not args.require_cuda, "cuda", cuda_detail))

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
        "status": "pending",
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "expected_records": expected_cases,
        "results": results,
    }

    failed = [r for r in results if not r["ok"]]
    payload["status"] = "passed" if not failed else "failed"
    payload["failed_checks"] = [r["name"] for r in failed]

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if failed:
        print(f"\nPREFLIGHT FAILED: {len(failed)} check(s). Do not start inference.")
        return 1

    print("\nPREFLIGHT PASSED: local environment is eligible to start the frozen 30-run pilot.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
