from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.evaluation import evaluate_output
from dijitalikiz.models import DiagnosticOutput, ResearchCase

ROOT=Path(".")
MAJORITY_REQUIRED=3
RUBRIC_PATH=ROOT/"data/benchmark/evaluation_rubric.json"


def sha256_text(v:str)->str:
    return hashlib.sha256(v.encode("utf-8")).hexdigest()


def normalize_phrase(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def root_cause_alias_match(output, aliases: list[str]) -> bool:
    haystack = " " + normalize_phrase(output.root_cause_class + " " + output.explanation) + " "
    return any(
        (" " + normalized + " ") in haystack
        for normalized in (normalize_phrase(alias) for alias in aliases)
        if normalized
    )


def sha256_json(v:object)->str:
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()


def main()->int:
    parser=argparse.ArgumentParser(description="Evaluate frozen confirmatory inference records.")
    parser.add_argument("--runs-dir",default="data/benchmark/runs")
    parser.add_argument("--output",default="data/benchmark/confirmatory_evaluation.json")
    args=parser.parse_args()

    manifest=json.loads((ROOT/"data/benchmark/benchmark_manifest.json").read_text(encoding="utf-8"))
    pilot=json.loads((ROOT/"data/pilot/pilot_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status")!="frozen":
        raise RuntimeError("Confirmatory benchmark manifest is not frozen.")
    cases=tuple(manifest["case_ids"]); conditions=tuple(pilot["conditions"]); seeds=tuple(pilot["generation"]["seeds"])
    scoring=manifest.get("scoring_rubric",{})
    rubric_bytes=RUBRIC_PATH.read_bytes()
    rubric_sha256=hashlib.sha256(rubric_bytes).hexdigest()
    if rubric_sha256 != scoring.get("sha256"):
        raise RuntimeError("Scoring rubric SHA-256 mismatch.")
    rubric=json.loads(rubric_bytes.decode("utf-8"))
    if scoring.get("primary_endpoint") != rubric.get("primary_endpoint"):
        raise RuntimeError("Scoring endpoint mismatch.")
    if [item.get("case_id") for item in rubric.get("cases",[])] != list(cases):
        raise RuntimeError("Scoring rubric case IDs/order mismatch.")
    aliases_by_case={item["case_id"]:item["root_cause_aliases"] for item in rubric["cases"]}
    if conditions!=("standard","ccdg") or seeds!=(42,43,44,45,46):
        raise RuntimeError("Frozen confirmatory configuration mismatch.")

    prompt_template=(ROOT/"data/pilot/PROMPT_TEMPLATE.txt").read_text(encoding="utf-8")
    expected_system_sha=pilot["system_prompt"]["sha256"]
    runs=Path(args.runs_dir)
    records=[]; missing=[]
    for case_id in cases:
        case=ResearchCase.from_dict(json.loads((ROOT/"data/benchmark/cases"/f"{case_id}.json").read_text(encoding="utf-8")))
        for condition in conditions:
            context=render_standard_context(case) if condition=="standard" else render_ccdg_context(case)
            for seed in seeds:
                path=runs/f"{case_id}__{condition}__seed{seed}.json"
                if not path.exists():
                    missing.append(str(path)); continue
                record=json.loads(path.read_text(encoding="utf-8"))
                expected_prompt=sha256_text(prompt_template+"\n\n"+context)
                frozen={
                    "case_id":case_id,"condition":condition,"seed":seed,
                    "model_id":pilot["model"]["model_id"],"model_revision":pilot["model"]["revision"],
                    "temperature":pilot["generation"]["temperature"],"top_p":pilot["generation"]["top_p"],
                    "max_new_tokens":pilot["generation"]["max_new_tokens"],
                    "prompt_sha256":expected_prompt,"context_sha256":sha256_text(context),
                    "system_prompt_sha256":expected_system_sha
                }
                for field,expected in frozen.items():
                    if record.get(field)!=expected:
                        raise ValueError(f"Frozen field mismatch in {path}: {field}")
                parse_ok=record.get("parse_error") is None and record.get("parsed_output") is not None
                if parse_ok:
                    output=DiagnosticOutput.from_dict(record["parsed_output"])
                    legacy_score=evaluate_output(output,case.ground_truth)
                    primary_pass=root_cause_alias_match(output,aliases_by_case[case_id])
                    score={"passed":primary_pass,"checks":{"root_cause_alias":primary_pass},"primary_endpoint":"root_cause_correctness_with_predeclared_aliases","complete_diagnostic_passed":legacy_score["passed"],"secondary_checks":legacy_score["checks"]}
                else:
                    score={"passed":False,"checks":{"component":False,"entity":False,"operation":False,"root_cause":False,"required_relations":False}}
                records.append({"case_id":case_id,"condition":condition,"seed":seed,"parse_ok":parse_ok,"parse_error":record.get("parse_error"),"score":score})

    by_condition={}
    for condition in conditions:
        subset=[r for r in records if r["condition"]==condition]
        parse_ok=sum(r["parse_ok"] for r in subset); passed=sum(r["score"]["passed"] for r in subset)
        by_condition[condition]={
            "n_expected":len(cases)*len(seeds),"n_found":len(subset),"n_parse_ok":parse_ok,
            "parse_failure_rate":1-(parse_ok/len(subset)) if subset else None,
            "n_scored":len(subset),"n_passed":passed,"pass_rate":passed/len(subset) if subset else None
        }

    duplicates=[]
    for case_id in cases:
        for condition in conditions:
            grouped={}
            for seed in seeds:
                p=runs/f"{case_id}__{condition}__seed{seed}.json"
                if not p.exists(): continue
                rec=json.loads(p.read_text(encoding="utf-8"))
                if rec.get("parsed_output") is None: continue
                grouped.setdefault(sha256_json(rec["parsed_output"]),[]).append(seed)
            for h,ss in grouped.items():
                if len(ss)>1: duplicates.append({"case_id":case_id,"condition":condition,"output_sha256":h,"seeds":ss})

    case_level={}
    for condition in conditions:
        case_level[condition]={}
        for case_id in cases:
            subset=[r for r in records if r["case_id"]==case_id and r["condition"]==condition]
            if len(subset)!=len(seeds):
                case_level[condition][case_id]={"n_runs_found":len(subset),"n_runs_expected":len(seeds),"majority_pass":None,"status":"missing_replication"}
            else:
                pc=sum(bool(r["score"]["passed"]) for r in subset)
                case_level[condition][case_id]={"n_runs_found":len(subset),"pass_count":pc,"majority_pass":pc>=MAJORITY_REQUIRED,"status":"complete"}

    summary={
        "status":"complete" if not missing else "incomplete",
        "expected_records":len(cases)*len(conditions)*len(seeds),"found_records":len(records),
        "missing_files":missing,"by_condition":by_condition,
        "case_level_majority_rule":"at least 3 of 5 seeds; parse/schema failures count as failed runs",
        "case_level":case_level,"duplicate_output_groups":duplicates,"records":records,
        "case_ids":list(cases)
    }
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":summary["status"],"expected_records":summary["expected_records"],"found_records":summary["found_records"],"missing_files":len(missing),"duplicate_output_groups":len(duplicates),"output":str(out)},indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
