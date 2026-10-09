from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_report(
    evaluation: dict,
    manifest: dict,
    assessments: dict[str, dict],
    review: dict | None = None,
) -> dict:
    by_condition = evaluation.get("by_condition", {})
    duplicate_groups = evaluation.get("duplicate_output_groups", [])
    case_level = evaluation.get("case_level", {})

    flags: list[str] = []
    for condition, payload in by_condition.items():
        if payload.get("parse_failure_rate", 0) not in (0, None):
            flags.append(f"parse_failures_present:{condition}")
    if duplicate_groups:
        flags.append("identical_parsed_outputs_across_seeds_present")

    review_risk = {
        item.get("case_id"): item.get("contamination_risk", "unknown")
        for item in (review or {}).get("decisions", [])
        if item.get("case_id") and item.get("decision") == "include"
    }
    contamination = {}
    for case_id in manifest["cases"]:
        risk = assessments.get(case_id, {}).get("contamination_risk")
        if risk in (None, "unknown"):
            risk = review_risk.get(case_id, "unknown")
        contamination[case_id] = risk
    unresolved_contamination = sorted(
        case_id for case_id, risk in contamination.items() if risk == "unknown"
    )
    if unresolved_contamination:
        flags.append("pilot_contamination_risk_unresolved:" + ",".join(unresolved_contamination))

    return {
        "report_type": "pilot_qa",
        "status": evaluation.get("status", "incomplete"),
        "scientific_result_claims": "none",
        "expected_records": evaluation.get("expected_records"),
        "found_records": evaluation.get("found_records"),
        "by_condition": by_condition,
        "case_level": case_level,
        "duplicate_output_groups": duplicate_groups,
        "contamination_risk": contamination,
        "flags": flags,
        "interpretation": (
            "QA report describes execution integrity only. It is not a confirmatory effectiveness claim."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a non-inferential pilot QA report.")
    parser.add_argument("--evaluation", default="data/pilot/pilot_evaluation.json")
    parser.add_argument("--manifest", default="data/pilot/pilot_manifest.json")
    parser.add_argument("--assessments-dir", default="data/assessments")
    parser.add_argument("--output", default="data/pilot/pilot_qa_report.json")
    args = parser.parse_args()

    evaluation = json.loads(Path(args.evaluation).read_text(encoding="utf-8"))
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    assessments: dict[str, dict] = {}
    for case_id in manifest["cases"]:
        path = Path(args.assessments_dir) / f"{case_id}.json"
        if path.is_file():
            assessments[case_id] = json.loads(path.read_text(encoding="utf-8"))

    review: dict | None = None
    review_path = Path(
        manifest.get("selection_review", {}).get(
            "review_path",
            "data/pilot/final_candidate_review_2026-10-08.json",
        )
    )
    if review_path.is_file():
        review = json.loads(review_path.read_text(encoding="utf-8"))

    report = build_report(evaluation, manifest, assessments, review)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
