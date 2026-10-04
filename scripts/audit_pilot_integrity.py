from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.models import DiagnosticOutput, ResearchCase


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Fail-closed integrity audit for the frozen pilot.")
    parser.add_argument("--runs-dir", default="data/pilot/runs")
    parser.add_argument("--manifest", default="data/pilot/pilot_manifest.json")
    parser.add_argument("--prompt", default="data/pilot/PROMPT_TEMPLATE.txt")
    parser.add_argument("--system-prompt", default="data/pilot/SYSTEM_PROMPT.txt")
    args = parser.parse_args()

    root = Path(".")
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    prompt_template = Path(args.prompt).read_text(encoding="utf-8")
    system_prompt = Path(args.system_prompt).read_text(encoding="utf-8")
    assert manifest["prompt"]["path"] == args.prompt
    assert manifest["prompt"]["sha256"] == sha256_text(prompt_template)
    assert manifest["system_prompt"]["path"] == args.system_prompt
    assert manifest["system_prompt"]["sha256"] == sha256_text(system_prompt)
    model = manifest["model"]
    generation = manifest["generation"]
    cases = manifest["cases"]
    conditions = tuple(manifest["conditions"])
    seeds = tuple(generation["seeds"])

    assert manifest["status"] == "model_frozen"
    assert conditions == ("standard", "ccdg")
    assert manifest["replications"] == len(seeds)
    assert generation["do_sample"] is True

    checked = 0
    for case_id in cases:
        case = ResearchCase.from_dict(
            json.loads((root / "data/pilot" / f"{case_id}.json").read_text(encoding="utf-8"))
        )
        for condition in conditions:
            context = (
                render_standard_context(case)
                if condition == "standard"
                else render_ccdg_context(case)
            )
            assert case.ground_truth.root_cause.lower() not in context.lower()
            assert "ground_truth" not in context.lower()
            expected_prompt_hash = sha256_text(prompt_template + "\n\n" + context)
            expected_context_hash = sha256_text(context)

            for seed in seeds:
                path = Path(args.runs_dir) / f"{case_id}__{condition}__seed{seed}.json"
                if not path.exists():
                    continue
                record = json.loads(path.read_text(encoding="utf-8"))
                assert record["case_id"] == case_id
                assert record["condition"] == condition
                assert record["seed"] == seed
                assert record["model_id"] == model["model_id"]
                assert record["model_revision"] == model["revision"]
                assert record["temperature"] == generation["temperature"]
                assert record["top_p"] == generation["top_p"]
                assert record["max_new_tokens"] == generation["max_new_tokens"]
                assert record["prompt_sha256"] == expected_prompt_hash
                assert record["system_prompt_sha256"] == manifest["system_prompt"]["sha256"]
                assert record["context_sha256"] == expected_context_hash
                if record.get("parsed_output") is not None:
                    DiagnosticOutput.from_dict(record["parsed_output"])
                checked += 1

    expected = len(cases) * len(conditions) * len(seeds)
    print(json.dumps({
        "status": "pass",
        "expected_records": expected,
        "checked_existing_records": checked,
        "missing_records": expected - checked,
        "configuration_only": checked == 0,
        "message": (
            "Frozen configuration passed; no inference records exist yet."
            if checked == 0
            else "Frozen configuration and all existing run records passed integrity checks."
        )
    }, indent=2))


if __name__ == "__main__":
    main()
