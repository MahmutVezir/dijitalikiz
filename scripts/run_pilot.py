from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.models import DiagnosticOutput, ResearchCase

MODEL_ID = "Qwen/Qwen2.5-3B-Instruct-GPTQ-Int4"
MODEL_REVISION = "68c4276063d1496cdf13d0b8e8221f899bfa77f7"
SEEDS = (42, 43, 44, 45, 46)
TEMPERATURE = 0.2
TOP_P = 1.0
MAX_NEW_TOKENS = 256
PROMPT_TEMPLATE = Path("data/pilot/PROMPT_TEMPLATE.txt")
CASES = (
    "commons-math-defects4j-MATH-927",
    "commons-math-defects4j-MATH-950",
    "commons-math-defects4j-MATH-988",
)


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model output")
    return json.loads(match.group(0))


def load_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=MODEL_REVISION,
        torch_dtype="auto",
        device_map="auto",
    )
    return tokenizer, model


def generate(tokenizer, model, prompt: str, seed: int) -> str:
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
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        do_sample=True,
    )
    generated = output_ids[0][inputs.input_ids.shape[-1]:]
    return tokenizer.decode(generated, skip_special_tokens=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="data/pilot/runs")
    args = parser.parse_args()

    prompt_template = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    tokenizer, model = load_model()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for case_name in CASES:
        payload = json.loads(
            Path("data/pilot", case_name + ".json").read_text(encoding="utf-8")
        )
        case = ResearchCase.from_dict(payload)

        for condition in ("standard", "ccdg"):
            context = (
                render_standard_context(case)
                if condition == "standard"
                else render_ccdg_context(case)
            )
            prompt = prompt_template + "\n\n" + context

            for seed in SEEDS:
                raw = generate(tokenizer, model, prompt, seed)
                parsed = _extract_json(raw)
                DiagnosticOutput.from_dict(parsed)

                record = {
                    "case_id": case.case_id,
                    "condition": condition,
                    "seed": seed,
                    "model_id": MODEL_ID,
                    "model_revision": MODEL_REVISION,
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "max_new_tokens": MAX_NEW_TOKENS,
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
