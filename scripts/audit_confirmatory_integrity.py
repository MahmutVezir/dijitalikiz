from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.models import DiagnosticOutput, ResearchCase


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed audit for frozen confirmatory inference.")
    parser.add_argument("--runs-dir", default="data/benchmark/runs")
    parser.add_argument("--manifest", default="data/benchmark/benchmark_manifest.json")
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    root = Path(".")
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    pilot_manifest = json.loads((root / "data" / "pilot" / "pilot_manifest.json").read_text(encoding="utf-8"))
    prompt = (root / "data" / "pilot" / "PROMPT_TEMPLATE.txt").read_text(encoding="utf-8")
    system_prompt = (root / "data" / "pilot" / "SYSTEM_PROMPT.txt").read_text(encoding="utf-8")

    assert manifest["status"] == "frozen"
    assert manifest["contamination_audit_completed"] is True
    assert manifest["case_ids"]
    cases = tuple(manifest["case_ids"])
    conditions = tuple(pilot_manifest["conditions"])
    seeds = tuple(pilot_manifest["generation"]["seeds"])
    assert conditions == ("standard", "ccdg")
    assert seeds == (42, 43, 44, 45, 46)
    assert sha256(prompt) == pilot_manifest["prompt"]["sha256"]
    assert sha256(system_prompt) == pilot_manifest["system_prompt"]["sha256"]

    expected_paths = {
        Path(args.runs_dir) / f"{case_id}__{condition}__seed{seed}.json"
        for case_id in cases for condition in conditions for seed in seeds
    }
    checked = 0
    commits: set[str] = set()

    for case_id in cases:
        case = ResearchCase.from_dict(json.loads(
            (root / "data" / "benchmark" / "cases" / f"{case_id}.json").read_text(encoding="utf-8")
        ))
        for condition in conditions:
            context = render_standard_context(case) if condition == "standard" else render_ccdg_context(case)
            assert case.ground_truth.root_cause.lower() not in context.lower()
            assert "ground_truth" not in context.lower()
            expected_prompt_sha = sha256(prompt + "\n\n" + context)
            expected_context_sha = sha256(context)
            for seed in seeds:
                path = Path(args.runs_dir) / f"{case_id}__{condition}__seed{seed}.json"
                if not path.exists():
                    continue
                record = json.loads(path.read_text(encoding="utf-8"))
                commits.add(record["source_commit"])
                assert record["source_commit"]
                assert record["case_id"] == case_id
                assert record["condition"] == condition
                assert record["seed"] == seed
                assert record["model_id"] == pilot_manifest["model"]["model_id"]
                assert record["model_revision"] == pilot_manifest["model"]["revision"]
                assert record["temperature"] == pilot_manifest["generation"]["temperature"]
                assert record["top_p"] == pilot_manifest["generation"]["top_p"]
                assert record["max_new_tokens"] == pilot_manifest["generation"]["max_new_tokens"]
                assert record["prompt_sha256"] == expected_prompt_sha
                assert record["context_sha256"] == expected_context_sha
                assert record["system_prompt_sha256"] == pilot_manifest["system_prompt"]["sha256"]
                assert record["raw_output_sha256"] == sha256(record["raw_output"])
                if record.get("parsed_output") is not None:
                    DiagnosticOutput.from_dict(record["parsed_output"])
                checked += 1

    unexpected = sorted(str(p) for p in (set(Path(args.runs_dir).glob("*.json")) if Path(args.runs_dir).exists() else set()) - expected_paths)
    expected = len(cases) * len(conditions) * len(seeds)
    if len(commits) > 1:
        raise RuntimeError(f"Confirmatory records span multiple source commits: {sorted(commits)}")
    if args.require_complete and checked != expected:
        raise RuntimeError(f"Confirmatory inference incomplete: {checked}/{expected}.")
    if args.require_complete and unexpected:
        raise RuntimeError(f"Unexpected run records: {unexpected}")

    print(json.dumps({
        "status":"pass",
        "expected_records":expected,
        "checked_existing_records":checked,
        "missing_records":expected-checked,
        "unexpected_records":unexpected,
        "source_commits":sorted(commits),
        "complete":checked == expected and not unexpected
    },indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
