from pathlib import Path
from rscbench.io import read_jsonl
from rscbench.model_client import MockModelClient
from rscbench.runner import run_one
from rscbench.schemas import CCDG, Case, GroundTruth, RunRecord

ROOT = Path(__file__).resolve().parents[1]


def test_run_record_contains_model_generation_and_input_provenance():
    case = read_jsonl(ROOT / "dataset/pilot/cases.jsonl", Case)[0]
    truth = read_jsonl(ROOT / "dataset/pilot/ground_truth.jsonl", GroundTruth)[0]
    ccdg = read_jsonl(ROOT / "dataset/pilot/ccdg.jsonl", CCDG)[0]
    result = run_one(root=ROOT, case=case, truth=truth, ccdg=ccdg,
                     condition="standard", replicate=1, client=MockModelClient())
    record = RunRecord.model_validate(result)
    assert record.model["model_id"] == "mock-v0"
    assert record.generation["temperature"] == 0.0
    assert len(record.input_hashes["I_base_sha256"]) == 64
    assert len(record.prompt_hashes["user_sha256"]) == 64


def test_ccdg_run_records_include_ccdg_input_hashes():
    case = read_jsonl(ROOT / "dataset/pilot/cases.jsonl", Case)[0]
    truth = read_jsonl(ROOT / "dataset/pilot/ground_truth.jsonl", GroundTruth)[0]
    ccdg = read_jsonl(ROOT / "dataset/pilot/ccdg.jsonl", CCDG)[0]
    result = run_one(root=ROOT, case=case, truth=truth, ccdg=ccdg,
                     condition="ccdg", replicate=1, client=MockModelClient())
    record = RunRecord.model_validate(result)
    assert record.input_hashes["CCDG_base_input_sha256"] == ccdg.base_input_sha256
    assert len(record.input_hashes["CCDG_canonical_sha256"]) == 64
