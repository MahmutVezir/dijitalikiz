from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from scripts.pilot_config import expected_pilot_record_count
from scripts.validate_benchmark_manifest import validate_manifest
from scripts.validate_pilot_artifact_manifest import (
    REQUIRED_FINAL_FILES,
    validate as validate_pilot_artifact,
)


ROOT = Path(".")
REQUIRED_PILOT_FILES = tuple(sorted(REQUIRED_FINAL_FILES | {"artifact_manifest.json"}))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Freeze the preselected confirmatory benchmark after pilot completion."
    )
    parser.add_argument(
        "--pilot-artifact-root",
        required=True,
        help="Directory containing the complete, finalized pilot artifact.",
    )
    parser.add_argument("--manifest", default="data/benchmark/benchmark_manifest.json")
    args = parser.parse_args()

    pilot_root = Path(args.pilot_artifact_root)
    missing = [
        str(pilot_root / name)
        for name in REQUIRED_PILOT_FILES
        if not (pilot_root / name).is_file()
    ]
    if missing:
        raise SystemExit("Pilot finalization artifacts missing: " + ", ".join(missing))

    artifact_errors = validate_pilot_artifact(
        pilot_root, pilot_root / "artifact_manifest.json"
    )
    if artifact_errors:
        raise SystemExit(
            "Pilot artifact validation failed; confirmatory benchmark cannot freeze: "
            + " | ".join(artifact_errors)
        )

    pilot_manifest = json.loads(
        (pilot_root / "pilot_manifest.json").read_text(encoding="utf-8")
    )
    try:
        expected_records = expected_pilot_record_count(
            pilot_manifest, require_declared=True
        )
    except (TypeError, ValueError) as exc:
        raise SystemExit(f"Frozen pilot configuration is invalid: {exc}") from exc

    pilot_eval = json.loads(
        (pilot_root / "pilot_evaluation.json").read_text(encoding="utf-8")
    )
    if (
        pilot_eval.get("status") != "complete"
        or pilot_eval.get("found_records") != expected_records
        or pilot_eval.get("expected_records") != expected_records
    ):
        raise SystemExit(
            "Pilot artifact is incomplete or its record count disagrees with the frozen manifest; "
            "confirmatory benchmark cannot freeze."
        )

    path = Path(args.manifest)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("status") != "draft":
        raise SystemExit("Benchmark manifest is already frozen or invalid.")

    errors = validate_manifest(manifest, ROOT)
    if errors:
        raise SystemExit("Benchmark draft validation failed: " + " | ".join(errors))

    if len(manifest.get("case_ids", [])) != manifest["power_assumption"]["required_case_count"]:
        raise SystemExit("Confirmatory case count does not match predeclared power requirement.")

    frozen_candidate = dict(manifest)
    frozen_candidate["status"] = "frozen"
    frozen_errors = validate_manifest(frozen_candidate, ROOT)
    if frozen_errors:
        raise SystemExit("Frozen benchmark validation failed: " + " | ".join(frozen_errors))

    manifest["status"] = "frozen"
    manifest["freeze_metadata"] = {
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "pilot_completion_verified": True,
        "case_selection_model_outputs_consulted": False,
    }
    path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"status": "frozen", "case_count": len(manifest["case_ids"])},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
