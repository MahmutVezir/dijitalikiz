from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rscbench.io import load_jsonl  # noqa: E402
from rscbench.model_client import OpenAIResponsesClient  # noqa: E402
from rscbench.runner import run_one  # noqa: E402
from rscbench.schemas import CCDG, Case, GroundTruth  # noqa: E402


def main() -> int:
    if os.getenv("RSCBENCH_ALLOW_REAL_PILOT") != "1":
        raise SystemExit(
            "Refusing real model calls. Set RSCBENCH_ALLOW_REAL_PILOT=1 explicitly after reviewing the pilot protocol."
        )

    with (ROOT / "configs/model.yaml").open(encoding="utf-8") as f:
        model_cfg = yaml.safe_load(f)
    with (ROOT / "configs/experiment.yaml").open(encoding="utf-8") as f:
        experiment_cfg = yaml.safe_load(f)

    model_id = model_cfg.get("model_id")
    if not model_id or model_id == "REPLACE_ME":
        raise SystemExit("Set an exact fixed model_id in configs/model.yaml before real execution.")

    cases = {x.case_id: x for x in (Case.model_validate(v) for v in load_jsonl(ROOT / "dataset/pilot/cases.jsonl"))}
    truths = {x.case_id: x for x in (GroundTruth.model_validate(v) for v in load_jsonl(ROOT / "dataset/pilot/ground_truth.jsonl"))}
    graphs = {x.case_id: x for x in (CCDG.model_validate(v) for v in load_jsonl(ROOT / "dataset/pilot/ccdg.jsonl"))}

    client = OpenAIResponsesClient(
        model_id=model_id,
        api_version=model_cfg.get("api_version"),
        temperature=model_cfg["generation"]["temperature"],
        top_p=model_cfg["generation"]["top_p"],
        max_output_tokens=model_cfg["generation"]["max_output_tokens"],
        seed=model_cfg["generation"].get("seed"),
    )

    output_path = ROOT / "outputs" / "real_pilot_runs.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as out:
        for case_id in sorted(cases):
            for condition in experiment_cfg["conditions"]:
                for replicate in range(1, int(experiment_cfg["replicates"]) + 1):
                    record = run_one(
                        root=ROOT,
                        case=cases[case_id],
                        truth=truths[case_id],
                        ccdg=graphs[case_id],
                        condition=condition,
                        replicate=replicate,
                        client=client,
                        experiment_id=experiment_cfg["experiment_id"],
                        require_frozen_prompts=False,
                    )
                    out.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
                    out.flush()
                    print(f"completed {case_id} {condition} R{replicate}")

    print(f"Wrote real pilot records to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
