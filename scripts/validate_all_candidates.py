from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dijitalikiz.candidate_assessment import CandidateAssessment
from scripts.validate_candidate import validate_candidate


ROOT = Path(__file__).resolve().parents[1]


def validate_all(candidates_dir: Path, assessments_dir: Path) -> list[str]:
    errors: list[str] = []
    candidate_files = sorted(candidates_dir.glob("*.json"))

    for candidate_path in candidate_files:
        try:
            candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{candidate_path}: unreadable candidate ({type(exc).__name__}: {exc})")
            continue

        for error in validate_candidate(candidate):
            errors.append(f"{candidate_path}: {error}")

        case_id = candidate.get("case_id")
        assessment_path = assessments_dir / f"{case_id}.json"
        if not assessment_path.is_file():
            errors.append(f"{candidate_path}: assessment missing: {assessment_path}")
            continue

        try:
            CandidateAssessment.from_dict(
                json.loads(assessment_path.read_text(encoding="utf-8"))
            )
        except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
            errors.append(f"{assessment_path}: invalid assessment ({type(exc).__name__}: {exc})")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the complete candidate/assessment intake pool.")
    parser.add_argument("--candidates-dir", default=str(ROOT / "data" / "candidates"))
    parser.add_argument("--assessments-dir", default=str(ROOT / "data" / "assessments"))
    args = parser.parse_args()

    errors = validate_all(Path(args.candidates_dir), Path(args.assessments_dir))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    count = len(list(Path(args.candidates_dir).glob("*.json")))
    print(f"VALID CANDIDATE POOL: {count} candidates with valid assessments")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
