import json
import sys
from pathlib import Path

import scripts.evaluate_pilot as evaluate_pilot


def test_parse_failure_is_counted_as_failed_run(monkeypatch, tmp_path):
    case_id = "commons-math-defects4j-MATH-927"
    case_dir = tmp_path / "data" / "pilot"
    runs_dir = tmp_path / "runs"
    case_dir.mkdir(parents=True)
    runs_dir.mkdir()

    manifest = {
        "status": "model_frozen",
        "cases": [case_id],
        "conditions": ["standard", "ccdg"],
        "replications": 5,
        "generation": {"seeds": [42, 43, 44, 45, 46]},
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

    for condition in evaluate_pilot.CONDITIONS if hasattr(evaluate_pilot, "CONDITIONS") else ("standard", "ccdg"):
        for seed in (42, 43, 44, 45, 46):
            (runs_dir / f"{case_id}__{condition}__seed{seed}.json").write_text(
                json.dumps({
                    "case_id": case_id,
                    "condition": condition,
                    "seed": seed,
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
