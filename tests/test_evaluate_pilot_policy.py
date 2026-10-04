import hashlib
import json
import sys
from pathlib import Path

import scripts.evaluate_pilot as evaluate_pilot
from dijitalikiz.context import render_standard_context
from dijitalikiz.models import ResearchCase


def test_parse_failure_is_counted_as_failed_run(monkeypatch, tmp_path):
    case_id = "commons-math-defects4j-MATH-927"
    case_dir = tmp_path / "data" / "pilot"
    runs_dir = tmp_path / "data" / "pilot" / "runs"
    case_dir.mkdir(parents=True)
    runs_dir.mkdir()

    prompt = "frozen prompt\n"
    system_prompt = "frozen system\n"
    (case_dir / "PROMPT_TEMPLATE.txt").write_text(prompt, encoding="utf-8")
    (case_dir / "SYSTEM_PROMPT.txt").write_text(system_prompt, encoding="utf-8")

    manifest = {
        "status": "model_frozen",
        "cases": [case_id],
        "conditions": ["standard", "ccdg"],
        "replications": 5,
        "generation": {"seeds": [42, 43, 44, 45, 46], "temperature": 0.2, "top_p": 1.0, "max_new_tokens": 256},
        "prompt": {"path": "data/pilot/PROMPT_TEMPLATE.txt", "sha256": hashlib.sha256(prompt.encode()).hexdigest()},
        "system_prompt": {"path": "data/pilot/SYSTEM_PROMPT.txt", "sha256": hashlib.sha256(system_prompt.encode()).hexdigest()},
        "model": {"model_id": "test/model", "revision": "test-revision"},
    }
    (case_dir / "pilot_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    case_payload = {
        "case_id": case_id,
        "source": "test",
        "source_url": "https://example.invalid/case",
        "publication_date": "2026-01-01",
        "technology": "test",
        "error_description": "test",
        "i_base": ["evidence"],
        "ccdg": [],
        "ground_truth": {
            "component": "C",
            "entity": "E",
            "operation": "O",
            "root_cause": "R",
            "required_relations": [],
        },
    }
    (case_dir / f"{case_id}.json").write_text(json.dumps(case_payload), encoding="utf-8")
    case = ResearchCase.from_dict(case_payload)
    context = render_standard_context(case)
    prompt_hash = hashlib.sha256((prompt + "\n\n" + context).encode()).hexdigest()
    context_hash = hashlib.sha256(context.encode()).hexdigest()

    for condition in evaluate_pilot.CONDITIONS if hasattr(evaluate_pilot, "CONDITIONS") else ("standard", "ccdg"):
        for seed in (42, 43, 44, 45, 46):
            (runs_dir / f"{case_id}__{condition}__seed{seed}.json").write_text(
                json.dumps({
                    "case_id": case_id,
                    "condition": condition,
                    "seed": seed,
                    "model_id": "test/model",
                    "model_revision": "test-revision",
                    "temperature": 0.2,
                    "top_p": 1.0,
                    "max_new_tokens": 256,
                    "prompt_sha256": prompt_hash,
                    "context_sha256": context_hash,
                    "system_prompt_sha256": hashlib.sha256(system_prompt.encode()).hexdigest(),
                    "parse_error": "invalid JSON" if seed == 42 else None,
                    "parsed_output": None if seed == 42 else {
                        "diagnosed_component": "C",
                        "root_cause_class": "R",
                        "affected_entity": "E",
                        "explanation": "O",
                    },
                }),
                encoding="utf-8",
            )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(evaluate_pilot, "MANIFEST", Path("data/pilot/pilot_manifest.json"))
    monkeypatch.setattr(sys, "argv", ["evaluate_pilot"])
    evaluate_pilot.main()

    result = json.loads((tmp_path / "data" / "pilot" / "pilot_evaluation.json").read_text())
    standard = [r for r in result["records"] if r["condition"] == "standard"]
    assert len(standard) == 5
    failed = next(r for r in standard if r["seed"] == 42)
    assert failed["parse_ok"] is False
    assert failed["score"]["passed"] is False
    assert result["case_level"]["standard"][case_id]["pass_count"] == 4
