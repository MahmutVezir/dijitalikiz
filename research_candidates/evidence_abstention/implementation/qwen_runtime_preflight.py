import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


EXPECTED_MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"
EXPECTED_REVISION = "aa8e72537993ba99e69dfaafa59ed015b17504d1"


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def canonical_sha256(value: Any) -> str:
    content = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(content)


def validate_configuration(manifest: Mapping[str, Any], runtime_lock: Mapping[str, Any]) -> list[str]:
    blockers = []
    model = manifest.get("model")
    locked_model = runtime_lock.get("model")
    if not isinstance(model, Mapping) or not isinstance(locked_model, Mapping):
        return ["Model configuration is missing."]
    for field, expected in (
        ("id", EXPECTED_MODEL_ID),
        ("revision", EXPECTED_REVISION),
        ("tokenizer_id", EXPECTED_MODEL_ID),
        ("tokenizer_revision", EXPECTED_REVISION),
    ):
        if model.get(field) != expected or locked_model.get(field) != expected:
            blockers.append(f"Model/tokenizer {field} does not match the pinned checkpoint.")

    generation = manifest.get("generation")
    locked_generation = runtime_lock.get("generation")
    if not isinstance(generation, Mapping) or not isinstance(locked_generation, Mapping):
        blockers.append("Generation policy is missing.")
    else:
        for field in ("candidate_count", "do_sample", "temperature", "top_p", "top_k", "max_new_tokens", "seed_policy", "selected_output_policy"):
            if generation.get(field) != locked_generation.get(field):
                blockers.append(f"Runtime lock differs from experiment manifest: generation.{field}.")

    if model.get("dtype") != locked_model.get("dtype") or model.get("quantization", "none") != locked_model.get("quantization", "none"):
        blockers.append("Model precision/quantization differs between manifest and runtime lock.")
    if locked_model.get("trust_remote_code") is not False:
        blockers.append("Pinned runtime must explicitly disable trust_remote_code.")
    if locked_generation.get("generation_performed_during_preflight") is not False:
        blockers.append("Runtime lock does not explicitly prohibit generation during preflight.")
    return blockers


def installed_versions() -> dict[str, str | None]:
    versions = {"python": platform.python_version()}
    for distribution in ("torch", "transformers", "accelerate"):
        try:
            versions[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            versions[distribution] = None
    return versions


def validate_versions(actual: Mapping[str, str | None], expected: Mapping[str, str]) -> list[str]:
    blockers = []
    for key in ("python", "torch", "transformers", "accelerate"):
        if actual.get(key) != expected.get(key):
            blockers.append(f"Runtime version mismatch for {key}: expected {expected.get(key)}, observed {actual.get(key)}.")
    return blockers


def run_no_output_preflight(manifest_path: Path, runtime_lock_path: Path, output_path: Path) -> dict:
    manifest_bytes = manifest_path.read_bytes()
    lock_bytes = runtime_lock_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    runtime_lock = json.loads(lock_bytes)
    blockers = validate_configuration(manifest, runtime_lock)

    expected_environment = runtime_lock.get("proposed_environment")
    if not isinstance(expected_environment, Mapping):
        blockers.append("Candidate runtime versions are missing.")
        expected_environment = {}

    observed_versions = installed_versions()
    version_blockers = validate_versions(observed_versions, expected_environment)
    blockers.extend(version_blockers)
    if blockers:
        report = {
            "record_type": "no_output_runtime_preflight",
            "status": "blocked_before_model_download",
            "blockers": blockers,
            "observed_versions": observed_versions,
            "manifest_sha256": sha256_bytes(manifest_bytes),
            "runtime_lock_sha256": sha256_bytes(lock_bytes),
            "model_generation_called": False,
            "model_output_generated": False,
            "model_inference_performed": False,
        }
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return report

    import torch
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

    if runtime_lock.get("proposed_environment", {}).get("requires_cuda") is True and not torch.cuda.is_available():
        report = {
            "record_type": "no_output_runtime_preflight",
            "status": "blocked_no_cuda",
            "blockers": ["The candidate runtime requires CUDA, but torch.cuda.is_available() is false."],
            "observed_versions": observed_versions,
            "manifest_sha256": sha256_bytes(manifest_bytes),
            "runtime_lock_sha256": sha256_bytes(lock_bytes),
            "model_generation_called": False,
            "model_output_generated": False,
            "model_inference_performed": False,
        }
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return report

    model_cfg = runtime_lock["model"]
    config = AutoConfig.from_pretrained(
        model_cfg["id"],
        revision=model_cfg["revision"],
        trust_remote_code=False,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_cfg["tokenizer_id"],
        revision=model_cfg["tokenizer_revision"],
        trust_remote_code=False,
    )
    model, loading_info = AutoModelForCausalLM.from_pretrained(
        model_cfg["id"],
        revision=model_cfg["revision"],
        torch_dtype=torch.float16,
        device_map=runtime_lock["proposed_environment"].get("device_map", "auto"),
        low_cpu_mem_usage=True,
        trust_remote_code=False,
        output_loading_info=True,
    )
    model.eval()

    tokenizer_commit = getattr(tokenizer, "_commit_hash", None)
    if not tokenizer_commit and hasattr(tokenizer, "init_kwargs"):
        tokenizer_commit = tokenizer.init_kwargs.get("_commit_hash")
    config_commit = getattr(config, "_commit_hash", None)
    model_commit = getattr(model.config, "_commit_hash", None)
    devices = []
    for index in range(torch.cuda.device_count()):
        properties = torch.cuda.get_device_properties(index)
        devices.append({
            "index": index,
            "name": properties.name,
            "total_memory_bytes": properties.total_memory,
            "compute_capability": f"{properties.major}.{properties.minor}",
        })

    chat_template = getattr(tokenizer, "chat_template", None)
    loading_issues = {
        "missing_keys": loading_info.get("missing_keys", []),
        "unexpected_keys": loading_info.get("unexpected_keys", []),
        "mismatched_keys": loading_info.get("mismatched_keys", []),
        "error_messages": loading_info.get("error_msgs", []),
    }
    revision_checks = {
        "config_commit_matches_pin": config_commit == model_cfg["revision"],
        "tokenizer_commit_matches_pin": tokenizer_commit == model_cfg["tokenizer_revision"],
        "model_commit_matches_pin": model_commit == model_cfg["revision"],
    }
    loading_clean = not any(loading_issues.values())
    revisions_clean = all(revision_checks.values())
    parameter_count = sum(parameter.numel() for parameter in model.parameters())
    dtype_ok = all(parameter.dtype == torch.float16 for parameter in model.parameters())
    device_map = getattr(model, "hf_device_map", {})

    fingerprint_payload = {
        "model_id": model_cfg["id"],
        "revision": model_cfg["revision"],
        "config_commit": config_commit,
        "tokenizer_commit": tokenizer_commit,
        "model_commit": model_commit,
        "model_class": model.__class__.__name__,
        "config_class": config.__class__.__name__,
        "tokenizer_class": tokenizer.__class__.__name__,
        "vocab_size": len(tokenizer),
        "chat_template_sha256": sha256_bytes((chat_template or "").encode("utf-8")),
        "parameter_count": parameter_count,
        "all_parameters_fp16": dtype_ok,
        "device_map": device_map,
        "observed_versions": observed_versions,
        "cuda_version": torch.version.cuda,
        "devices": devices,
        "loading_issues": loading_issues,
        "revision_checks": revision_checks,
    }
    report = {
        "record_type": "no_output_runtime_preflight",
        "status": "passed" if revisions_clean and loading_clean and parameter_count > 0 and dtype_ok else "failed_validation",
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_sha256": sha256_bytes(manifest_bytes),
        "runtime_lock_sha256": sha256_bytes(lock_bytes),
        "runtime_fingerprint_sha256": canonical_sha256(fingerprint_payload),
        "runtime_fingerprint": fingerprint_payload,
        "blockers": [],
        "model_generation_called": False,
        "model_output_generated": False,
        "model_inference_performed": False,
        "note": "This verifies a pinned model/tokenizer load only. It does not generate a response, calibrate confidence, authorize inference, or change the manifest.",
    }
    if not revisions_clean:
        report["blockers"].append("The loaded config/model/tokenizer did not all resolve to the pinned commit.")
    if not loading_clean:
        report["blockers"].append("The checkpoint reported missing, unexpected, mismatched keys or loading errors.")
    if parameter_count <= 0:
        report["blockers"].append("The loaded model has no parameters.")
    if not dtype_ok:
        report["blockers"].append("One or more model parameters are not float16.")
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    del model, tokenizer, config
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Pinned Qwen model/tokenizer load check; never generates a response.")
    parser.add_argument("--manifest", type=Path, default=Path("research_candidates/evidence_abstention/UNCERTAINTY_EXPERIMENT_MANIFEST.json"))
    parser.add_argument("--runtime-lock", type=Path, default=Path("research_candidates/evidence_abstention/UNCERTAINTY_RUNTIME_LOCK.json"))
    parser.add_argument("--output", type=Path, default=Path("runtime_preflight.json"))
    parser.add_argument("--load-pinned-model-no-output", action="store_true", help="Explicitly download/load the pinned checkpoint without generating text.")
    args = parser.parse_args(argv)
    if not args.load_pinned_model_no_output:
        parser.error("No model download/load will occur unless --load-pinned-model-no-output is supplied.")
    report = run_no_output_preflight(args.manifest, args.runtime_lock, args.output)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    sys.exit(main())

