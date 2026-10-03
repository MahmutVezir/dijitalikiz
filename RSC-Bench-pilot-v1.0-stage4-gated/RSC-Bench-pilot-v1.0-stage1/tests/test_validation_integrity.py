from pathlib import Path
import pytest

from rscbench.io import read_jsonl
from rscbench.schemas import CCDG, CCDGEdge, Case, GroundTruth
from rscbench.validator import base_input_sha256, validate_case_links, validate_main_dataset_exclusion

ROOT = Path(__file__).resolve().parents[1]


def test_ccdg_is_derived_from_same_base_input():
    case = read_jsonl(ROOT / "dataset/pilot/cases.jsonl", Case)[0]
    truth = read_jsonl(ROOT / "dataset/pilot/ground_truth.jsonl", GroundTruth)[0]
    ccdg = read_jsonl(ROOT / "dataset/pilot/ccdg.jsonl", CCDG)[0]
    assert ccdg.base_input_sha256 == base_input_sha256(case)
    validate_case_links(case, truth, ccdg)


def test_ccdg_wrong_base_hash_is_rejected():
    case = read_jsonl(ROOT / "dataset/pilot/cases.jsonl", Case)[0]
    truth = read_jsonl(ROOT / "dataset/pilot/ground_truth.jsonl", GroundTruth)[0]
    ccdg = read_jsonl(ROOT / "dataset/pilot/ccdg.jsonl", CCDG)[0]
    bad = ccdg.model_copy(update={"base_input_sha256": "0" * 64})
    with pytest.raises(ValueError, match="base_input_sha256"):
        validate_case_links(case, truth, bad)


def test_unknown_ccdg_relation_is_rejected():
    case = read_jsonl(ROOT / "dataset/pilot/cases.jsonl", Case)[0]
    truth = read_jsonl(ROOT / "dataset/pilot/ground_truth.jsonl", GroundTruth)[0]
    ccdg = read_jsonl(ROOT / "dataset/pilot/ccdg.jsonl", CCDG)[0]
    bad = ccdg.model_copy(update={"edges": [CCDGEdge(source=ccdg.nodes[0].id, target=ccdg.nodes[0].id, relation="invented_relation")]})
    with pytest.raises(ValueError, match="Unsupported CCDG relation"):
        validate_case_links(case, truth, bad)


def test_pilot_case_cannot_overlap_main_dataset():
    with pytest.raises(ValueError, match="cannot enter the main dataset"):
        validate_main_dataset_exclusion({"RSC-PILOT-001"}, {"RSC-PILOT-001"})


def test_duplicate_ccdg_node_ids_are_rejected():
    case = read_jsonl(ROOT / "dataset/pilot/cases.jsonl", Case)[0]
    truth = read_jsonl(ROOT / "dataset/pilot/ground_truth.jsonl", GroundTruth)[0]
    ccdg = read_jsonl(ROOT / "dataset/pilot/ccdg.jsonl", CCDG)[0]
    bad = ccdg.model_copy(update={"nodes": [ccdg.nodes[0], ccdg.nodes[0]]})
    with pytest.raises(ValueError, match="node IDs must be unique"):
        validate_case_links(case, truth, bad)
