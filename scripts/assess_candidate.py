from __future__ import annotations

import argparse
import json
from pathlib import Path

from dijitalikiz.candidate_assessment import CandidateAssessment


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "data" / "candidates"
ASSESSMENTS = ROOT / "data" / "assessments"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create/update a researcher-entered candidate assessment.")
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--input", required=True, help="JSON file containing assessment fields.")
    args = parser.parse_args()

    candidate = CANDIDATES / f"{args.case_id}.json"
    if not candidate.exists():
        raise SystemExit(f"Candidate not found: {candidate}")

    with Path(args.input).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    payload["case_id"] = args.case_id
    assessment = CandidateAssessment.from_dict(payload)
    ASSESSMENTS.mkdir(parents=True, exist_ok=True)
    destination = ASSESSMENTS / f"{args.case_id}.json"
    destination.write_text(
        json.dumps(assessment.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(destination)
    print(f"eligible_for_pilot={assessment.eligible_for_pilot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
