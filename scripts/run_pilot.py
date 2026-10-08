from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.models import DiagnosticOutput, ResearchCase

MANIFEST = Path("data/pilot/pilot_manifest.json")
PROMPT_TEMPLATE = Path("data/pilot/PROMPT_TEMPLATE.txt")
SYSTEM_PROMPT = Path("data/pilot/SYSTEM_PROMPT.txt")
RUN_RECORD_SCHEMA = Path("schemas/pilot_run_record.schema.json")
DIAGNOSTIC_OUTPUT_SCHEMA = Path("schemas/diagnostic_output.schema.json")


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _source_commit() -> str:
    bundle_path = Path("data/pilot/kaggle_source_commit.txt")
    if bundle_path.is_file():
        return bundle_path.read_text(encoding="utf-8").strip()
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model output")
    return json.loads(match.group(0))


def validate_schema(instance: object, schema_path: Path, label: str) -> None:\n    schema = json.loads(schema_path.read_text(encoding="utf-8"))\n    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.path))\n    if errors:\n        detail = "; ".join(f"{label}: {e.message}" for e in errors[:5])\n        raise ValueError(detail)\n\n\ndef load_model(model_id: str, revision: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        torch_dtype="auto",
        device_map="auto",
    )
    return tokenizer, model


def generate(
    tokenizer,
    model,
    prompt: str,
    seed: int,
    *,
    system_prompt: str,
    temperature: float,
    top_p: float,
    max_new_tokens: int,
) -> str:
    import torch

    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    output_ids = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        do_sample=True,
    )
    generated = output_ids[0][inputs.input_ids.shape[-1]:]
    return tokenizer.decode(generated, skip_special_tokens=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="data/pilot/runs")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Preserve existing frozen records and generate only missing records.",
    )
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("status") != "model_frozen":
        raise RuntimeError("Pilot manifest is not frozen.")

    model_id = manifest["model"]["model_id"]
    revision = manifest["model"]["revision"]
    seeds = tuple(manifest["generation"]["seeds"])
    temperature = manifest["generation"]["temperature"]
    top_p = manifest["generation"]["top_p"]
    max_new_tokens = manifest["generation"]["max_new_tokens"]
    cases = tuple(manifest["cases"])
    conditions = tuple(manifest["conditions"])

    if conditions != ("standard", "ccdg"):
        raise ValueError("Pilot runner only supports the frozen Standard/CCDG conditions.")
    if manifest["replications"] != len(seeds):
        raise ValueError("Manifest replication count does not match seed count.")
    if manifest["generation"]["do_sample"] is not True:
        raise ValueError("Frozen pilot requires do_sample=true.")

    prompt_template = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    system_prompt = SYSTEM_PROMPT.read_text(encoding="utf-8")
    expected_prompt_hash = manifest["prompt"]["sha256"]
    expected_system_prompt_hash = manifest["system_prompt"]["sha256"]
    if _sha256(prompt_template) != expected_prompt_hash:
        raise RuntimeError("Frozen prompt hash does not match pilot manifest.")
    if _sha256(system_prompt) != expected_system_prompt_hash:
        raise RuntimeError("Frozen system prompt hash does not match pilot manifest.")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    expected_paths = [
        output_dir / f"{case_id}__{condition}__seed{seed}.json"
        for case_id in cases
        for condition in conditions
        for seed in seeds
    ]
    existing = [path for path in expected_paths if path.exists()]
    if existing and not args.resume:
        raise RuntimeError(
            f"{len(existing)} frozen run record(s) already exist. "
            "Use --resume to preserve them and generate only missing records."
        )

    tokenizer, model = load_model(model_id, revision)
    source_commit = _source_commit()

    for case_name in cases:
        payload = json.loads(
            Path("data/pilot", case_name + ".json").read_text(encoding="utf-8")
        )
        case = ResearchCase.from_dict(payload)

        for condition in conditions:
            context = (
                render_standard_context(case)
                if condition == "standard"
                else render_ccdg_context(case)
            )
            prompt = prompt_template + "\n\n" + context
            prompt_sha256 = _sha256(prompt)
            context_sha256 = _sha256(context)

            for seed in seeds:
                path = output_dir / f"{case.case_id}__{condition}__seed{seed}.json"
                if path.exists():
                    if args.resume:
                        print(f"SKIP existing frozen record: {path}", flush=True)
                        continue

                started_at = datetime.now(timezone.utc)
                raw = generate(
                    tokenizer,
                    model,
                    prompt,
                    seed,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    top_p=top_p,
                    max_new_tokens=max_new_tokens,
                )
                parsed = None
                parse_error = None
                try:\n                    parsed = _extract_json(raw)\n                    validate_schema(parsed, DIAGNOSTIC_OUTPUT_SCHEMA, "diagnostic_output_schema")\n                    DiagnosticOutput.from_dict(parsed)\n                except (ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:\n                    parse_error = f"{type(exc).__name__}: {exc}"\n
                completed_at = datetime.now(timezone.utc)
                record = {
                    "source_commit": source_commit,
                    "started_at_utc": started_at.isoformat(),
                    "completed_at_utc": completed_at.isoformat(),
                    "raw_output_sha256": _sha256(raw),
                    "case_id": case.case_id,
                    "condition": condition,
                    "seed": seed,
                    "model_id": model_id,
                    "model_revision": revision,
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_new_tokens": max_new_tokens,
                    "prompt_sha256": prompt_sha256,
                    "system_prompt_sha256": expected_system_prompt_hash,
                    "context_sha256": context_sha256,
                    "parse_error": parse_error,
                    "raw_output": raw,
                    "parsed_output": parsed,
                }
                validate_schema(record, RUN_RECORD_SCHEMA, "pilot_run_record_schema")\n                temporary = path.with_suffix(path.suffix + ".tmp")\n                temporary.write_text(
                    json.dumps(record, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                temporary.replace(path)
                print(f"WROTE {path}", flush=True)


if __name__ == "__main__":
    main()
