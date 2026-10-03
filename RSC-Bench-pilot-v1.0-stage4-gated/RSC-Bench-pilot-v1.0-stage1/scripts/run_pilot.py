from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rscbench.io import read_jsonl
from rscbench.model_client import MockModelClient
from rscbench.runner import run_one
from rscbench.schemas import CCDG, Case, GroundTruth

CASES = ROOT / "dataset/pilot/cases.jsonl"
TRUTH = ROOT / "dataset/pilot/ground_truth.jsonl"
GRAPHS = ROOT / "dataset/pilot/ccdg.jsonl"
OUTPUT = ROOT / "outputs/pilot_mock.jsonl"


def main() -> None:
    cases = read_jsonl(CASES, Case)
    truths = {item.case_id: item for item in read_jsonl(TRUTH, GroundTruth)}
    graphs = {item.case_id: item for item in read_jsonl(GRAPHS, CCDG)}

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as handle:
        for case in cases:
            if case.case_id not in truths or case.case_id not in graphs:
                raise ValueError(f"Pilot case is missing ground truth or CCDG: {case.case_id}")
            for replicate in range(1, 6):
                for condition in ("standard", "ccdg"):
                    record = run_one(
                        root=ROOT,
                        case=case,
                        truth=truths[case.case_id],
                        ccdg=graphs[case.case_id],
                        condition=condition,
                        replicate=replicate,
                        client=MockModelClient(output_payload={
                            "diagnosed_component": truths[case.case_id].component,
                            "root_cause_class": truths[case.case_id].root_cause,
                            "affected_entity": truths[case.case_id].entity,
                            "explanation": "mock",
                        }),
                        experiment_id="PILOT-MOCK-001",
                        require_frozen_prompts=False,
                    )
                    handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    print(f"Wrote {len(cases) * 5 * 2} mock pilot runs to {OUTPUT}")


if __name__ == "__main__":
    main()
