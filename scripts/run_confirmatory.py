from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.models import DiagnosticOutput, ResearchCase

ROOT = Path(".")
MANIFEST = ROOT / "data" / "benchmark" / "benchmark_manifest.json"
PILOT_MANIFEST = ROOT / "data" / "pilot" / "pilot_manifest.json"
PROMPT_TEMPLATE = ROOT / "data" / "pilot" / "PROMPT_TEMPLATE.txt"
SYSTEM_PROMPT = ROOT / "data" / "pilot" / "SYSTEM_PROMPT.txt"


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def source_commit() -> str:
    path = ROOT / "data" / "benchmark" / "kaggle_source_commit.txt"
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model output")
    return json.loads(match.group(0))


def load_model(model_id: str, revision: str):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        torch_dtype=torch.float16,
        device_map="auto",
        low_cpu_mem_usage=True,
    )
    quantization = getattr(model.config, "quantization_config", None)
    if quantization:
        raise RuntimeError("Frozen confirmatory lane requires the native unquantized checkpoint.")
    if any(parameter.dtype != torch.float16 for parameter in model.parameters()):
        raise RuntimeError("Frozen confirmatory model parameters are not all FP16.")
    return tokenizer, model


def generate(tokenizer, model, prompt: str, seed: int, *, system_prompt: str,
             temperature: float, top_p: float, max_new_tokens: int) -> str:
    import torch

    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    rendered = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer([rendered], return_tensors="pt").to(model.device)
    output_ids = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        do_sample=True,
    )
    generated = output_ids[0][inputs.input_ids.shape[-1]:]
    return tokenizer.decode(generated, skip_special_tokens=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Frozen confirmatory Standard-vs-CCDG runner.")
    parser.add_argument("--output-dir", default="data/benchmark/runs")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pilot_manifest = json.loads(PILOT_MANIFEST.read_text(encoding="utf-8"))

    if manifest.get("status") != "frozen":
        raise RuntimeError("Confirmatory benchmark manifest is not frozen.")
    if manifest.get("contamination_audit_completed") is not True:
        raise RuntimeError("Confirmatory contamination audit is not complete.")
    cases = tuple(manifest["case_ids"])
    if not cases:
        raise RuntimeError("Confirmatory benchmark contains no cases.")
    if len(cases) != len(set(cases)):
        raise RuntimeError("Confirmatory benchmark case IDs must be unique.")
    scoring = manifest.get("scoring_rubric", {})
    rubric_path = ROOT / scoring.get("path", "data/benchmark/evaluation_rubric.json")
    rubric_bytes = rubric_path.read_bytes()
    rubric_sha256 = hashlib.sha256(rubric_bytes).hexdigest()
    if rubric_sha256 != scoring.get("sha256"):
        raise RuntimeError(
            f"Scoring rubric SHA-256 mismatch: expected {scoring.get('sha256')}, got {rubric_sha256}"
        )
    rubric = json.loads(rubric_bytes.decode("utf-8"))
    if scoring.get("primary_endpoint") != rubric.get("primary_endpoint"):
        raise RuntimeError("Scoring endpoint does not match the rubric.")
    rubric_cases = [item.get("case_id") for item in rubric.get("cases", [])]
    if rubric_cases != list(cases):
        raise RuntimeError("Rubric case IDs/order do not match confirmatory manifest.")
    if not all(
        isinstance(item.get("root_cause_aliases"), list) and item["root_cause_aliases"]
        for item in rubric.get("cases", [])
    ):
        raise RuntimeError("Every case must have predeclared root-cause aliases.")
    if set(cases) & set(manifest.get("pilot_case_ids", [])):
        raise RuntimeError("Confirmatory benchmark overlaps pilot cases.")

    model = pilot_manifest["model"]
    generation = pilot_manifest["generation"]
    conditions = tuple(pilot_manifest["conditions"])
    seeds = tuple(generation["seeds"])
    if conditions != ("standard", "ccdg"):
        raise ValueError("Frozen confirmatory runner requires Standard/CCDG conditions.")
    if len(seeds) != 5 or tuple(seeds) != (42, 43, 44, 45, 46):
        raise ValueError("Frozen confirmatory runner requires seeds 42..46.")
    if pilot_manifest["replications"] != len(seeds):
        raise ValueError("Replication count does not match seed count.")
    if generation["do_sample"] is not True:
        raise ValueError("Frozen confirmatory run requires sampling enabled.")
    prompt_template = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    system_prompt = SYSTEM_PROMPT.read_text(encoding="utf-8")
    if sha256(prompt_template) != pilot_manifest["prompt"]["sha256"]:
        raise RuntimeError("Frozen prompt hash mismatch.")
    if sha256(system_prompt) != pilot_manifest["system_prompt"]["sha256"]:
        raise RuntimeError("Frozen system prompt hash mismatch.")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    expected_paths = [
        output_dir / f"{case_id}__{condition}__seed{seed}.json"
        for case_id in cases for condition in conditions for seed in seeds
    ]
    existing = [p for p in expected_paths if p.exists()]
    if existing and not args.resume:
        raise RuntimeError(
            f"{len(existing)} confirmatory records already exist; use --resume only to complete missing records."
        )

    tokenizer, model_obj = load_model(model["model_id"], model["revision"])
    commit = source_commit()

    for case_id in cases:
        payload = json.loads((ROOT / "data" / "benchmark" / "cases" / f"{case_id}.json").read_text(encoding="utf-8"))
        case = ResearchCase.from_dict(payload)

        for condition in conditions:
            context = render_standard_context(case) if condition == "standard" else render_ccdg_context(case)
            if case.ground_truth.root_cause.lower() in context.lower() or "ground_truth" in context.lower():
                raise RuntimeError(f"Ground-truth leakage detected in rendered {case_id}/{condition} context.")
            prompt = prompt_template + "\n\n" + context
            prompt_sha256 = sha256(prompt)
            context_sha256 = sha256(context)

            for seed in seeds:
                path = output_dir / f"{case_id}__{condition}__seed{seed}.json"
                if path.exists():
                    if args.resume:
                        print(f"SKIP existing frozen record: {path}", flush=True)
                        continue
                started = datetime.now(timezone.utc)
                raw = generate(
                    tokenizer, model_obj, prompt, seed,
                    system_prompt=system_prompt,
                    temperature=generation["temperature"],
                    top_p=generation["top_p"],
                    max_new_tokens=generation["max_new_tokens"],
                )
                parsed = None
                parse_error = None
                try:
                    parsed = extract_json(raw)
                    DiagnosticOutput.from_dict(parsed)
                except (ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
                    parse_error = f"{type(exc).__name__}: {exc}"
                completed = datetime.now(timezone.utc)
                record = {
                    "source_commit": commit,
                    "started_at_utc": started.isoformat(),
                    "completed_at_utc": completed.isoformat(),
                    "raw_output_sha256": sha256(raw),
                    "case_id": case.case_id,
                    "condition": condition,
                    "seed": seed,
                    "model_id": model["model_id"],
                    "model_revision": model["revision"],
                    "model_dtype": "float16",
                    "quantization": "none",
                    "temperature": generation["temperature"],
                    "top_p": generation["top_p"],
                    "max_new_tokens": generation["max_new_tokens"],
                    "prompt_sha256": prompt_sha256,
                    "system_prompt_sha256": pilot_manifest["system_prompt"]["sha256"],
                    "context_sha256": context_sha256,
                    "parse_error": parse_error,
                    "raw_output": raw,
                    "parsed_output": parsed,
                }
                tmp = path.with_suffix(path.suffix + ".tmp")
                tmp.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                tmp.replace(path)
                print(f"WROTE {path}", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
