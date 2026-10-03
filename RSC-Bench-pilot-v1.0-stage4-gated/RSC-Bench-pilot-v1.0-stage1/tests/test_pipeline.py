import json
import subprocess
import sys
from pathlib import Path
from rscbench.io import read_jsonl
from rscbench.model_client import MockModelClient
from rscbench.runner import run_one
from rscbench.schemas import CCDG, Case, GroundTruth

ROOT = Path(__file__).resolve().parents[1]


def test_end_to_end_mock_pipeline():
    cases = read_jsonl(ROOT / "dataset/pilot/cases.jsonl", Case)
    truths = {x.case_id: x for x in read_jsonl(ROOT / "dataset/pilot/ground_truth.jsonl", GroundTruth)}
    graphs = {x.case_id: x for x in read_jsonl(ROOT / "dataset/pilot/ccdg.jsonl", CCDG)}
    for case in cases:
        result = run_one(root=ROOT, case=case, truth=truths[case.case_id], ccdg=graphs[case.case_id],
                         condition="ccdg", replicate=1, client=MockModelClient(output_payload={
            "diagnosed_component": truths[case.case_id].component,
            "root_cause_class": truths[case.case_id].root_cause,
            "affected_entity": truths[case.case_id].entity,
            "explanation": "mock",
        }))
        assert result["case_id"] == case.case_id
        assert result["condition"] == "ccdg"
        assert result["match"]["primary_accuracy"] == 1
        json.dumps(result)


def test_pilot_script_produces_r5_both_conditions_for_all_cases(tmp_path):
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/run_pilot.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    cases = read_jsonl(ROOT / "dataset/pilot/cases.jsonl", Case)
    expected = len(cases) * 5 * 2
    assert f"{expected} mock pilot runs" in result.stdout
    output = ROOT / "outputs/pilot_mock.jsonl"
    lines = output.read_text(encoding="utf-8").splitlines()
    assert len(lines) == expected
    output.unlink()
