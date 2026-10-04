from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
CANDIDATES=ROOT/"data/candidates"
ASSESSMENTS=ROOT/"data/assessments"

def main():
    candidates=sorted(CANDIDATES.glob("*.json")) if CANDIDATES.exists() else []
    print(f"candidates={len(candidates)}")
    for p in candidates:
        a=ASSESSMENTS/p.name
        if not a.exists():
            print(f"{p.stem}: assessment=missing")
            continue
        d=json.loads(a.read_text(encoding="utf-8"))
        print(f"{p.stem}: eligible={d.get('eligible_for_pilot',False)} IC4={d.get('IC4','unknown')} dependency={d.get('dependency_strength','unknown')} ccdg={d.get('ccdg_suitability','unknown')}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
