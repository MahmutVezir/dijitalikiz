import json
from pathlib import Path
from rscbench.io import read_jsonl
from rscbench.prompts import PromptBuilder
from rscbench.schemas import CCDG, Case
from rscbench.validator import base_input_sha256

ROOT = Path(__file__).resolve().parents[1]


def test_standard_and_ccdg_share_identical_base_input_hash():
    cases = read_jsonl(ROOT / "dataset/pilot/cases.jsonl", Case)
    graphs = {g.case_id: g for g in read_jsonl(ROOT / "dataset/pilot/ccdg.jsonl", CCDG)}
    builder = PromptBuilder(ROOT)
    for case in cases:
        ccdg = graphs[case.case_id]
        standard_system, standard_user = builder.render("standard", case)
        ccdg_system, ccdg_user = builder.render("ccdg", case, ccdg)
        canonical_base = json.dumps(case.I_base, ensure_ascii=False, sort_keys=True, indent=2)
        assert base_input_sha256(case) == ccdg.base_input_sha256
        assert canonical_base in standard_user
        assert canonical_base in ccdg_user
        assert standard_system == ccdg_system
