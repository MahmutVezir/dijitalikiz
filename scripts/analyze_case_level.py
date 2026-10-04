from __future__ import annotations
import argparse, json
from pathlib import Path
from math import comb
CONDITIONS=("standard","ccdg")
SEEDS=(42,43,44,45,46)
MAJORITY_REQUIRED=3
def exact_mcnemar_pvalue(standard_only:int, ccdg_only:int)->float:
    d=standard_only+ccdg_only
    if d==0:return 1.0
    lower=sum(comb(d,k) for k in range(0,min(standard_only,ccdg_only)+1))
    return min(1.0,2.0*lower/(2**d))
def load_case_outcomes(runs_dir:Path,case_ids:list[str]):
    outcomes={}
    for case_id in case_ids:
        outcomes[case_id]={}
        for condition in CONDITIONS:
            scores=[]
            for seed in SEEDS:
                path=runs_dir/f"{case_id}__{condition}__seed{seed}.json"
                if not path.exists(): raise FileNotFoundError(path)
                record=json.loads(path.read_text(encoding="utf-8"))
                if record.get("parse_error") is not None or record.get("parsed_output") is None:
                    raise ValueError(f"Non-evaluable run: {path}")
                if "score" not in record: raise ValueError(f"Missing stored score in {path}")
                scores.append(bool(record["score"]["passed"]))
            outcomes[case_id][condition]=sum(scores)>=MAJORITY_REQUIRED
    return outcomes
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--runs-dir",required=True); p.add_argument("--case-ids",nargs="+",required=True); p.add_argument("--output",required=True)
    a=p.parse_args(); outcomes=load_case_outcomes(Path(a.runs_dir),a.case_ids)
    standard_only=sum(outcomes[c]["standard"] and not outcomes[c]["ccdg"] for c in a.case_ids)
    ccdg_only=sum(outcomes[c]["ccdg"] and not outcomes[c]["standard"] for c in a.case_ids)
    both_pass=sum(outcomes[c]["standard"] and outcomes[c]["ccdg"] for c in a.case_ids)
    both_fail=sum(not outcomes[c]["standard"] and not outcomes[c]["ccdg"] for c in a.case_ids)
    n=len(a.case_ids); s=sum(outcomes[c]["standard"] for c in a.case_ids); g=sum(outcomes[c]["ccdg"] for c in a.case_ids)
    result={"n_cases":n,"majority_rule":"at least 3 of 5 seeds","contingency_table":{"standard_pass_ccdg_pass":both_pass,"standard_pass_ccdg_fail":standard_only,"standard_fail_ccdg_pass":ccdg_only,"standard_fail_ccdg_fail":both_fail},"standard_accuracy":s/n,"ccdg_accuracy":g/n,"accuracy_difference_ccdg_minus_standard":(g-s)/n,"exact_two_sided_mcnemar_p":exact_mcnemar_pvalue(standard_only,ccdg_only),"case_outcomes":outcomes}
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=="__main__": main()
