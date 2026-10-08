from __future__ import annotations

import argparse
import json
from pathlib import Path


def main()->int:
    parser=argparse.ArgumentParser(description="Generate non-inferential confirmatory execution QA.")
    parser.add_argument("--evaluation",default="data/benchmark/confirmatory_evaluation.json")
    parser.add_argument("--manifest",default="data/benchmark/benchmark_manifest.json")
    parser.add_argument("--assessments-dir",default="data/assessments")
    parser.add_argument("--output",default="data/benchmark/confirmatory_qa_report.json")
    args=parser.parse_args()

    evaluation=json.loads(Path(args.evaluation).read_text(encoding="utf-8"))
    manifest=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    flags=[]
    for condition,payload in evaluation.get("by_condition",{}).items():
        if payload.get("parse_failure_rate") not in (0,None):
            flags.append(f"parse_failures_present:{condition}")
    if evaluation.get("duplicate_output_groups"):
        flags.append("identical_parsed_outputs_across_seeds_present")
    risks={}
    for case_id in manifest.get("case_ids",[]):
        p=Path(args.assessments_dir)/f"{case_id}.json"
        risks[case_id]=json.loads(p.read_text(encoding="utf-8")).get("contamination_risk","unknown") if p.is_file() else "unknown"
    if any(v=="unknown" for v in risks.values()):
        flags.append("confirmatory_contamination_risk_unresolved")
    report={
        "report_type":"confirmatory_qa","status":evaluation.get("status","incomplete"),
        "scientific_result_claims":"results_are_recorded_without_post_hoc_case_selection",
        "expected_records":evaluation.get("expected_records"),"found_records":evaluation.get("found_records"),
        "by_condition":evaluation.get("by_condition",{}),"case_level":evaluation.get("case_level",{}),
        "duplicate_output_groups":evaluation.get("duplicate_output_groups",[]),
        "contamination_risk":risks,"flags":flags,
        "interpretation":"This QA artifact documents execution integrity. Statistical effectiveness conclusions belong only to the frozen primary analysis."
    }
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2,ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
