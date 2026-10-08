from __future__ import annotations
import argparse, json
from pathlib import Path
from scripts.analyze_case_level import load_evaluation, build_result

def main()->int:
    p=argparse.ArgumentParser(description="Run the predeclared primary paired confirmatory analysis.")
    p.add_argument("--evaluation",default="data/benchmark/confirmatory_evaluation.json")
    p.add_argument("--output",default="data/benchmark/primary_analysis.json")
    a=p.parse_args()
    manifest=json.loads(Path("data/benchmark/benchmark_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status")!="frozen":
        raise RuntimeError("Confirmatory benchmark must be frozen before primary analysis.")
    case_ids=list(manifest["case_ids"])
    result=build_result(load_evaluation(Path(a.evaluation),case_ids),case_ids)
    table=result["contingency_table"]
    result.update({
        "analysis_type":"predeclared_primary_confirmatory",
        "alpha":manifest["analysis"]["alpha"],
        "test":"exact two-sided McNemar",
        "unit":"independent software case",
        "decision_rule":"reject H0 when exact two-sided McNemar p <= alpha",
        "effect_size_definition":"P(CCDG correct, Standard incorrect) - P(Standard correct, CCDG incorrect)",
        "power_assumption":manifest["power_assumption"],
        "interpretation":"Interpretation is generated only from completed observed case outcomes; no benchmark membership or protocol parameter is changed post hoc.",
    })
    result["discordant_pairs"]={
        "standard_only":table["standard_pass_ccdg_fail"],
        "ccdg_only":table["standard_fail_ccdg_pass"],
    }
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
