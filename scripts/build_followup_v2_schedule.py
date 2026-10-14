from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "followup_v2" / "protocol_manifest.json"
DEFAULT_OUTPUT = ROOT / "data" / "followup_v2" / "randomized_schedule.json"


def build_schedule(case_ids: list[str], seeds: list[int], randomization_seed: int = 20261010) -> dict[str, Any]:
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("Schedule needs a non-empty, unique held-out case list.")
    if len(seeds) != len(set(seeds)) or not seeds:
        raise ValueError("Schedule needs a non-empty, unique seed list.")
    cells = [
        {"case_id": case_id, "condition_id": condition, "seed": seed}
        for case_id in case_ids
        for condition in ("A", "B", "C")
        for seed in seeds
    ]
    random.Random(randomization_seed).shuffle(cells)
    for index, cell in enumerate(cells, start=1):
        cell["order_index"] = index
    return {
        "protocol_version": "followup-v2-randomized-schedule-1.0",
        "status": "frozen",
        "randomization_seed": randomization_seed,
        "case_ids_sha256": hashlib.sha256(
            json.dumps(case_ids, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        ).hexdigest(),
        "condition_order": ["A", "B", "C"],
        "seeds": seeds,
        "cell_count": len(cells),
        "cells": cells,
        "model_inference_started": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and hash the randomized v2 schedule; does not run inference.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=20261010)
    args = parser.parse_args()
    manifest_path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if manifest.get("status") != "draft" or manifest.get("model_inference_permitted") is not False:
        raise SystemExit("Schedule preparation is allowed only before protocol freeze and before inference.")
    pool = manifest["case_pool"]
    case_ids = pool["case_ids"]
    minimum = int(pool["minimum_independent_case_count"])
    if len(case_ids) < minimum:
        raise SystemExit(f"Held-out case pool has {len(case_ids)} cases; at least {minimum} are required.")

    for case_id in case_ids:
        case_path = ROOT / pool["case_directory"] / f"{case_id}.json"
        if not case_path.is_file():
            raise SystemExit(f"Missing held-out case file: {case_path}")
        case = json.loads(case_path.read_text(encoding="utf-8"))
        if case.get("split") != pool["split_name"]:
            raise SystemExit(f"Wrong split for {case_id}; expected {pool['split_name']!r}.")

    schedule = build_schedule(case_ids, list(manifest["generation"]["seeds"]), args.seed)
    payload = json.dumps(schedule, indent=2, ensure_ascii=False) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(output_path.read_bytes()).hexdigest()
    print(json.dumps({
        "status": "prepared",
        "schedule_path": str(output_path),
        "sha256": digest,
        "case_count": len(case_ids),
        "condition_count": 3,
        "seed_count": len(schedule["seeds"]),
        "cell_count": schedule["cell_count"],
        "model_inference_started": False
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
