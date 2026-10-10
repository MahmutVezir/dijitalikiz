from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from dijitalikiz.context_v2 import (
    render_ccdg_context_v2,
    render_dependency_prose_context_v2,
    render_standard_context_v2,
)
from dijitalikiz.models import ResearchCase

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "followup_v2" / "protocol_manifest.json"
RENDERERS = {
    "A": render_standard_context_v2,
    "B": render_dependency_prose_context_v2,
    "C": render_ccdg_context_v2,
}


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _validate_manifest_shape(manifest: dict[str, Any], root: Path) -> None:
    schema_path = root / "schemas" / "followup_v2_protocol.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(manifest),
        key=lambda error: list(error.path),
    )
    if errors:
        details = "; ".join(
            f"{'/'.join(map(str, error.path))}: {error.message}"
            for error in errors[:8]
        )
        raise ValueError(f"Follow-up v2 manifest schema errors: {details}")


def build_token_audit(
    *,
    manifest: dict[str, Any],
    root: Path,
    tokenizer: Any,
    transformers_version: str,
) -> dict[str, Any]:
    model = manifest["model"]
    prompts = manifest["prompts"]
    case_pool = manifest["case_pool"]
    generation = manifest["generation"]
    context_limit = int(prompts["max_context_tokens"])
    reserve = int(prompts["generation_reserve_tokens"])
    case_ids = list(case_pool["case_ids"])

    if len(case_ids) < int(case_pool["minimum_independent_case_count"]):
        raise ValueError(
            "Held-out case pool is below its required minimum; tokenizer audit is blocked."
        )
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("Held-out case IDs must be unique.")
    if list(RENDERERS) != ["A", "B", "C"]:
        raise RuntimeError("The audited A/B/C renderer order is not canonical.")

    system_path = root / prompts["system_prompt_path"]
    task_path = root / prompts["task_prompt_path"]
    system_bytes = system_path.read_bytes()
    task_bytes = task_path.read_bytes()
    if sha256_bytes(system_bytes) != prompts["system_prompt_sha256"]:
        raise ValueError("System-prompt SHA-256 does not match the protocol manifest.")
    if sha256_bytes(task_bytes) != prompts["task_prompt_sha256"]:
        raise ValueError("Task-prompt SHA-256 does not match the protocol manifest.")
    system_prompt = system_bytes.decode("utf-8")
    task_prompt = task_bytes.decode("utf-8")

    tokenizer_template = getattr(tokenizer, "chat_template", None) or ""
    special_tokens_map = getattr(tokenizer, "special_tokens_map", {}) or {}
    tokenizer_name = getattr(tokenizer, "name_or_path", model["model_id"])
    tokenizer_class = tokenizer.__class__.__name__

    results: list[dict[str, Any]] = []
    failures: list[str] = []
    for case_id in case_ids:
        case_path = root / case_pool["case_directory"] / f"{case_id}.json"
        if not case_path.is_file():
            failures.append(f"missing_case_file:{case_id}")
            continue
        payload = json.loads(case_path.read_text(encoding="utf-8"))
        if payload.get("case_id") != case_id:
            failures.append(f"case_id_mismatch:{case_id}")
            continue
        if payload.get("split") != case_pool["split_name"]:
            failures.append(f"wrong_split:{case_id}")
            continue
        if not isinstance(payload.get("software_twin_snapshot"), dict):
            failures.append(f"missing_version_bound_snapshot:{case_id}")
            continue

        case = ResearchCase.from_dict(payload)
        contexts = {key: renderer(case) for key, renderer in RENDERERS.items()}
        base_contexts = {
            "A": contexts["A"],
            "B": contexts["B"].split("Dependency relations in sentences:", 1)[0].rstrip(),
            "C": contexts["C"].split("Dependency relations as directed triples:", 1)[0].rstrip(),
        }
        if not (base_contexts["A"].strip() == base_contexts["B"] == base_contexts["C"]):
            failures.append(f"shared_base_facts_mismatch:{case_id}")
            continue
        if not case.ccdg:
            failures.append(f"missing_dependency_edges:{case_id}")
            continue
        for condition, context in contexts.items():
            if case.ground_truth.root_cause and case.ground_truth.root_cause.casefold() in context.casefold():
                failures.append(f"ground_truth_leakage:{case_id}:{condition}")
                continue
            prompt = task_prompt + "\n\n" + context
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
            rendered_chat = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            encoded = tokenizer([rendered_chat], return_tensors=None)
            token_ids = encoded["input_ids"][0]
            token_count = len(token_ids)
            fits = token_count + reserve <= context_limit
            if not fits:
                failures.append(
                    f"context_overflow:{case_id}:{condition}:{token_count}+{reserve}>{context_limit}"
                )
            results.append({
                "case_id": case_id,
                "condition_id": condition,
                "context_sha256": sha256_text(context),
                "task_prompt_plus_context_sha256": sha256_text(prompt),
                "rendered_chat_input_sha256": sha256_text(rendered_chat),
                "token_ids_sha256": sha256_bytes(canonical_json([int(x) for x in token_ids])),
                "context_character_count": len(context),
                "rendered_chat_character_count": len(rendered_chat),
                "input_token_count": token_count,
                "generation_reserve_tokens": reserve,
                "total_context_budget": token_count + reserve,
                "model_context_limit": context_limit,
                "fits_context_limit": fits,
            })

    expected_records = len(case_ids) * len(RENDERERS)
    if len(results) != expected_records:
        failures.append(f"expected_{expected_records}_prompt_cells_got_{len(results)}")
    keys = [(item["case_id"], item["condition_id"]) for item in results]
    if len(keys) != len(set(keys)):
        failures.append("duplicate_case_condition_prompt_cell")

    report = {
        "audit_version": "followup-v2-tokenizer-audit-1.0",
        "status": "blocked" if failures else "pass",
        "model_id": model["model_id"],
        "model_revision": model["revision"],
        "tokenizer_name_or_path": str(tokenizer_name),
        "tokenizer_class": tokenizer_class,
        "transformers_version": transformers_version,
        "python_version": platform.python_version(),
        "chat_template_sha256": sha256_text(tokenizer_template),
        "special_tokens_map_sha256": sha256_bytes(canonical_json(special_tokens_map)),
        "system_prompt_sha256": sha256_bytes(system_bytes),
        "task_prompt_sha256": sha256_bytes(task_bytes),
        "case_count": len(case_ids),
        "condition_count": len(RENDERERS),
        "expected_prompt_cell_count": expected_records,
        "actual_prompt_cell_count": len(results),
        "all_prompts_fit_context_budget": not any(
            not item["fits_context_limit"] for item in results
        ) and not failures,
        "all_expected_cells_present": len(results) == expected_records and len(keys) == len(set(keys)),
        "tokenization_matches_inference_call_shape": "tokenizer([rendered_chat], return_tensors=None) with default special-token policy; must be rechecked against the runner before freeze",
        "failures": failures,
        "prompts": results,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Hash and count final chat-template prompt tokens; never runs model inference."
    )
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    _validate_manifest_shape(manifest, root)

    if manifest.get("model_inference_permitted") is not False:
        raise ValueError("Tokenizer audit requires model_inference_permitted=false.")
    if manifest.get("status") != "draft":
        raise ValueError("Prompt token auditing must happen before the protocol freeze.")

    from transformers import AutoTokenizer, __version__ as transformers_version

    model = manifest["model"]
    tokenizer = AutoTokenizer.from_pretrained(
        model["model_id"],
        revision=model["revision"],
        trust_remote_code=False,
    )
    report = build_token_audit(
        manifest=manifest,
        root=root,
        tokenizer=tokenizer,
        transformers_version=transformers_version,
    )
    payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output_path = args.output if args.output.is_absolute() else root / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload, encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "model_id": report["model_id"],
        "model_revision": report["model_revision"],
        "case_count": report["case_count"],
        "prompt_cell_count": report["actual_prompt_cell_count"],
        "all_prompts_fit_context_budget": report["all_prompts_fit_context_budget"],
        "failure_count": len(report["failures"]),
        "output": str(args.output) if args.output else None,
    }, indent=2))
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
