from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from scripts.build_confirmatory_artifact_manifest import build_payload


ROOT = Path(__file__).resolve().parents[1]


def test_confirmatory_artifact_manifest_hashes_all_delivered_files(tmp_path):
    artifact_root = tmp_path / "benchmark"
    runs = artifact_root / "runs"
    runs.mkdir(parents=True)
    case_ids = ["fixture-case"]
    conditions = ["standard", "ccdg"]
    seeds = [42, 43, 44, 45, 46]

    (artifact_root / "benchmark_manifest.json").write_text(
        json.dumps({"status": "frozen", "case_ids": case_ids}),
        encoding="utf-8",
    )
    (artifact_root / "pilot_manifest.json").write_text(
        json.dumps({"conditions": conditions, "generation": {"seeds": seeds}}),
        encoding="utf-8",
    )
    for name in (
        "environment.json",
        "confirmatory_evaluation.json",
        "case_level_analysis.json",
        "primary_analysis.json",
        "confirmatory_qa_report.json",
    ):
        (artifact_root / name).write_text("{}", encoding="utf-8")
    (artifact_root / "confirmatory_records.jsonl").write_text(
        "".join(json.dumps({"record": i}) + "\n" for i in range(10)),
        encoding="utf-8",
    )

    support_file = artifact_root / "assessments" / "fixture-case.json"
    support_file.parent.mkdir()
    support_file.write_text('{"contamination_risk":"high"}', encoding="utf-8")
    case_file = artifact_root / "cases" / "fixture-case.json"
    case_file.parent.mkdir()
    case_file.write_text('{"case_id":"fixture-case"}', encoding="utf-8")

    for case_id in case_ids:
        for condition in conditions:
            for seed in seeds:
                (runs / f"{case_id}__{condition}__seed{seed}.json").write_text(
                    "{}", encoding="utf-8"
                )

    output = artifact_root / "artifact_manifest.json"
    payload = build_payload(
        artifact_root, runs, output, case_ids, conditions, seeds
    )
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    paths = {item["path"]: item for item in payload["files"]}
    for path in (
        "assessments/fixture-case.json",
        "cases/fixture-case.json",
        "pilot_manifest.json",
        "confirmatory_records.jsonl",
        "runs/fixture-case__ccdg__seed46.json",
    ):
        assert path in paths
    assert paths["assessments/fixture-case.json"]["sha256"] == hashlib.sha256(
        support_file.read_bytes()
    ).hexdigest()
    assert payload["run_record_count"] == 10
    assert payload["file_count"] == len(payload["files"])

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_confirmatory_artifact_manifest.py"),
            "--artifact-root",
            str(artifact_root),
            "--manifest",
            str(output),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def test_confirmatory_artifact_manifest_rejects_missing_run(tmp_path):
    artifact_root = tmp_path / "benchmark"
    runs = artifact_root / "runs"
    runs.mkdir(parents=True)
    with_expected = ["fixture-case"]
    try:
        build_payload(
            artifact_root,
            runs,
            artifact_root / "artifact_manifest.json",
            with_expected,
            ["standard", "ccdg"],
            [42, 43, 44, 45, 46],
        )
    except RuntimeError as exc:
        assert "run set differs from the frozen design" in str(exc)
    else:
        raise AssertionError("Incomplete run set must fail closed.")
