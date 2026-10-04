from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from pathlib import Path

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.models import DiagnosticOutput, ResearchCase

MANIFEST = Path("data/pilot/pilot_manifest.json")
PROMPT_TEMPLATE = Path("data/pilot/PROMPT_TEMPLATE.txt")


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model output")
    return json.loads(match.group(0))


def load_model(model_id: str, revision: str):
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
        {
            "role": "system",
            "content": "You are a controlled research benchmark model. Follow the requested JSON schema exactly.",
        },
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
    tokenizer, model = load_model(model_id, revision)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

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
                raw = generate(
                    tokenizer,
                    model,
                    prompt,
                    seed,
                    temperature=temperature,
                    top_p=top_p,
                    max_new_tokens=max_new_tokens,
                )
                parsed = None
                parse_error = None
                try:
                    parsed = _extract_json(raw)
                    DiagnosticOutput.from_dict(parsed)
                except (ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
                    parse_error = f"{type(exc).__name__}: {exc}"

                record = {
                    "case_id": case.case_id,
                    "condition": condition,
                    "seed": seed,
                    "model_id": model_id,
                    "model_revision": revision,
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_new_tokens": max_new_tokens,
                    "prompt_sha256": prompt_sha256,
                    "context_sha256": context_sha256,
                    "parse_error": parse_error,
                    "raw_output": raw,
                    "parsed_output": parsed,
                }
                path = output_dir / f"{case.case_id}__{condition}__seed{seed}.json"
                path.write_text(
                    json.dumps(record, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )


if __name__ == "__main__":
    main()
