from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "data" / "candidates"
ASSESSMENTS = ROOT / "data" / "assessments"


def main() -> int:
    candidate_files = sorted(CANDIDATES.glob("*.json")) if CANDIDATES.exists() else []
    assessment_files = sorted(ASSESSMENTS.glob("*.json")) if ASSESSMENTS.exists() else []

    print(f"candidates={len(candidate_files)}")
    print(f"assessments={len(assessment_files)}")

    for path in candidate_files:
        case_id = path.stem
        assessment_path = ASSESSMENTS / path.name
        if not assessment_path.exists():
            print(f"{case_id}: assessment=missing")
            continue
        data = json.loads(assessment_path.read_text(encoding="utf-8"))
        print(
            f"{case_id}: "
            f"IC1-IC7={','.join(str(data.get(f'IC{i}', 'unknown')) for i in range(1, 8))}; "
            f"dependency={data.get('dependency_strength', 'unknown')}; "
            f"ccdg={data.get('ccdg_suitability', 'unknown')}; "
            f"contamination={data.get('contamination_risk', 'unknown')}; "
            f"eligible={data.get('eligible_for_pilot', False)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
