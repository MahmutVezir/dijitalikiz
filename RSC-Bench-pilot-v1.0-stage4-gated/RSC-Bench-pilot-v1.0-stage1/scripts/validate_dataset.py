from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rscbench.io import read_jsonl
from rscbench.schemas import CCDG, Case, GroundTruth
from rscbench.validator import validate_case_links


def main() -> None:
    cases = read_jsonl(ROOT / "dataset/pilot/cases.jsonl", Case)
    truths = {x.case_id: x for x in read_jsonl(ROOT / "dataset/pilot/ground_truth.jsonl", GroundTruth)}
    graphs = {x.case_id: x for x in read_jsonl(ROOT / "dataset/pilot/ccdg.jsonl", CCDG)}

    for case in cases:
        if case.case_id not in truths or case.case_id not in graphs:
            raise ValueError(f"Incomplete pilot case bundle: {case.case_id}")
        validate_case_links(case, truths[case.case_id], graphs[case.case_id])

    print(f"Validated {len(cases)} pilot case(s).")


if __name__ == "__main__":
    main()
