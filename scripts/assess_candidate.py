from pathlib import Path
import argparse
import json
from dijitalikiz.candidate_assessment import CandidateAssessment

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--case-id",required=True)
    parser.add_argument("--input",required=True)
    args=parser.parse_args()
    if not (ROOT/"data/candidates"/f"{args.case_id}.json").exists():
        raise SystemExit("candidate not found")
    payload=json.loads(Path(args.input).read_text(encoding="utf-8"))
    payload["case_id"]=args.case_id
    assessment=CandidateAssessment.from_dict(payload)
    out=ROOT/"data/assessments"/f"{args.case_id}.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(assessment.to_dict(),indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(out)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
