from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from dijitalikiz.candidate_assessment import CandidateAssessment


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promote one independently assessed candidate into the confirmatory benchmark."
    )
    parser.add_argument("--case-id", required=True)
    args = parser.parse_args()

    candidate_path = ROOT / "data" / "candidates" / f"{args.case_id}.json"
    assessment_path = ROOT / "data" / "assessments" / f"{args.case_id}.json"
    output_path = ROOT / "data" / "benchmark" / "cases" / f"{args.case_id}.json"
    pilot_manifest = json.loads(
        (ROOT / "data" / "pilot" / "pilot_manifest.json").read_text(encoding="utf-8")
    )

    if not candidate_path.is_file():
        raise SystemExit(f"candidate not found: {candidate_path}")
    if not assessment_path.is_file():
        raise SystemExit(f"assessment not found: {assessment_path}")
    if args.case_id in set(pilot_manifest["cases"]):
        raise SystemExit("pilot case cannot be promoted to confirmatory benchmark")

    assessment = CandidateAssessment.from_dict(
        json.loads(assessment_path.read_text(encoding="utf-8"))
    )
    if not assessment.eligible_for_main:
        raise SystemExit("candidate is not eligible_for_main; contamination risk and structural criteria must be resolved first")

    payload = json.loads(candidate_path.read_text(encoding="utf-8"))
    required = {"case_id", "source", "source_url", "publication_date", "technology", "error_description", "i_base", "ccdg", "ground_truth"}
    missing = sorted(required - set(payload))
    if missing:
        raise SystemExit(f"candidate lacks complete ResearchCase fields: {missing}")

    if payload["case_id"] != args.case_id:
        raise SystemExit("candidate case_id does not match requested case")
    if output_path.exists():
        raise SystemExit(f"confirmatory case already exists: {output_path}")

    payload["split"] = "confirmatory"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"PROMOTED: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
