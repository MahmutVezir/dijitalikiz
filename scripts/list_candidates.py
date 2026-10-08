from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def collect(candidates_dir: Path, assessments_dir: Path) -> list[dict]:
    rows = []
    for candidate_path in sorted(candidates_dir.glob("*.json")):
        candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        case_id = candidate.get("case_id", candidate_path.stem)
        assessment_path = assessments_dir / f"{case_id}.json"
        assessment = (
            json.loads(assessment_path.read_text(encoding="utf-8"))
            if assessment_path.is_file()
            else {}
        )
        rows.append({
            "case_id": case_id,
            "split": candidate.get("split"),
            "annotation_status": candidate.get("annotation_status"),
            "provenance_verification_status": candidate.get(
                "provenance_verification_status"
            ),
            "dependency_strength": assessment.get("dependency_strength", "unassessed"),
            "ccdg_suitability": assessment.get("ccdg_suitability", "unassessed"),
            "contamination_risk": assessment.get("contamination_risk", "unassessed"),
            "eligible_for_pilot": assessment.get("eligible_for_pilot", False),
            "eligible_for_main": assessment.get("eligible_for_main", False),
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="List candidate/assessment status.")
    parser.add_argument("--candidates-dir", default="data/candidates")
    parser.add_argument("--assessments-dir", default="data/assessments")
    parser.add_argument("--eligible-for-main", action="store_true")
    args = parser.parse_args()

    rows = collect(ROOT / args.candidates_dir, ROOT / args.assessments_dir)
    if args.eligible_for_main:
        rows = [row for row in rows if row["eligible_for_main"]]
    print(json.dumps({"count": len(rows), "candidates": rows},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
