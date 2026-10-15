from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.models import ResearchCase

EXPLICIT_FIX_CUE = re.compile(
    r"\b(?:the fix|fix(?:es|ed)?|fixed|corrected|correction|before the fix|after the fix)\b",
    re.IGNORECASE,
)
SECONDARY_REMEDIATION_CUE = re.compile(
    r"\b(?:previously|restoration|restore|restores|restored|instead of|introduces|introduced|removes|removed|applies|applied|changes|changed)\b",
    re.IGNORECASE,
)


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def normalize_phrase(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _phrase_hits(text: str, phrases: list[str]) -> list[str]:
    normalized_text = f" {normalize_phrase(text)} "
    return [
        phrase
        for phrase in phrases
        if normalize_phrase(phrase)
        and f" {normalize_phrase(phrase)} " in normalized_text
    ]


def _cue_facts(items: list[str], matcher: re.Pattern[str]) -> list[dict[str, Any]]:
    flagged = []
    for index, item in enumerate(items, start=1):
        matches = [match.group(0) for match in matcher.finditer(item)]
        if matches:
            flagged.append({
                "fact_id": f"B{index}",
                "matched_cue_text": matches,
                "text": item,
            })
    return flagged


def analyze_case(payload: dict[str, Any], aliases: list[str]) -> dict[str, Any]:
    """Inspect the exact legacy renderers without changing their input or output."""
    case = ResearchCase.from_dict(payload)
    standard = render_standard_context(case)
    ccdg = render_ccdg_context(case)
    root_cause = case.ground_truth.root_cause
    i_base_lines = [f"- {item}" for item in case.i_base]

    standard_alias_hits = _phrase_hits(standard, aliases)
    ccdg_alias_hits = _phrase_hits(ccdg, aliases)

    return {
        "case_id": case.case_id,
        "standard_context_has_explicit_error_description": (
            "Error description:" in standard and case.error_description in standard
        ),
        "ccdg_context_has_explicit_error_description": (
            "Error description:" in ccdg and case.error_description in ccdg
        ),
        "standard_context_has_dependency_section": "Dependencies:" in standard,
        "ccdg_context_has_dependency_section": "Dependencies:" in ccdg,
        "source_and_technology_shared": (
            f"Source: {case.source}" in standard
            and f"Source: {case.source}" in ccdg
            and f"Technology: {case.technology}" in standard
            and f"Technology: {case.technology}" in ccdg
        ),
        "all_i_base_facts_shared_verbatim": all(
            line in standard and line in ccdg for line in i_base_lines
        ),
        "canonical_root_cause_literal_hit_standard": bool(
            normalize_phrase(root_cause)
            and f" {normalize_phrase(root_cause)} " in f" {normalize_phrase(standard)} "
        ),
        "canonical_root_cause_literal_hit_ccdg": bool(
            normalize_phrase(root_cause)
            and f" {normalize_phrase(root_cause)} " in f" {normalize_phrase(ccdg)} "
        ),
        "case_alias_literal_hits_standard": standard_alias_hits,
        "case_alias_literal_hits_ccdg": ccdg_alias_hits,
        "explicit_fix_cue_facts_in_shared_i_base": _cue_facts(
            case.i_base, EXPLICIT_FIX_CUE
        ),
        "secondary_remediation_cue_facts_in_shared_i_base": _cue_facts(
            case.i_base, SECONDARY_REMEDIATION_CUE
        ),
        "error_description": case.error_description,
        "i_base": case.i_base,
        "ccdg_edge_count": len(case.ccdg),
    }


def audit_project(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root).resolve()
    benchmark_dir = root / "data" / "benchmark"
    manifest = _read_json(benchmark_dir / "benchmark_manifest.json")
    rubric = _read_json(benchmark_dir / "evaluation_rubric.json")

    if manifest.get("status") != "frozen":
        raise ValueError("Historical benchmark manifest is not frozen.")
    case_ids = manifest.get("case_ids")
    rubric_cases = rubric.get("cases")
    if not isinstance(case_ids, list) or not case_ids:
        raise ValueError("Benchmark manifest case_ids must be a non-empty list.")
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("Benchmark manifest has duplicate case IDs.")
    if not isinstance(rubric_cases, list):
        raise ValueError("Scoring rubric cases must be a list.")
    if [item.get("case_id") for item in rubric_cases] != case_ids:
        raise ValueError("Rubric case IDs/order differ from frozen benchmark manifest.")

    aliases_by_case = {
        item["case_id"]: item.get("root_cause_aliases", [])
        for item in rubric_cases
    }
    cases_dir = benchmark_dir / "cases"
    case_json_ids = {
        path.stem for path in cases_dir.glob("*.json")
        if path.name != "README.json"
    }
    active_ids = set(case_ids)
    missing = sorted(active_ids - case_json_ids)
    unlisted = sorted(case_json_ids - active_ids)
    if missing:
        raise ValueError(f"Manifest-listed cases missing from case directory: {missing}")

    case_rows = []
    for case_id in case_ids:
        payload = _read_json(cases_dir / f"{case_id}.json")
        if payload.get("case_id") != case_id:
            raise ValueError(f"Case ID mismatch in {case_id}.json")
        case_rows.append(analyze_case(payload, aliases_by_case[case_id]))

    n = len(case_rows)
    standard_error_count = sum(
        row["standard_context_has_explicit_error_description"] for row in case_rows
    )
    ccdg_error_count = sum(
        row["ccdg_context_has_explicit_error_description"] for row in case_rows
    )
    standard_dependency_count = sum(
        row["standard_context_has_dependency_section"] for row in case_rows
    )
    ccdg_dependency_count = sum(
        row["ccdg_context_has_dependency_section"] for row in case_rows
    )
    common_base_count = sum(row["all_i_base_facts_shared_verbatim"] for row in case_rows)
    common_metadata_count = sum(row["source_and_technology_shared"] for row in case_rows)
    explicit_fix_case_ids = [
        row["case_id"]
        for row in case_rows
        if row["explicit_fix_cue_facts_in_shared_i_base"]
    ]
    secondary_remediation_case_ids = [
        row["case_id"]
        for row in case_rows
        if row["secondary_remediation_cue_facts_in_shared_i_base"]
    ]
    literal_alias_standard = [
        row["case_id"] for row in case_rows if row["case_alias_literal_hits_standard"]
    ]
    literal_alias_ccdg = [
        row["case_id"] for row in case_rows if row["case_alias_literal_hits_ccdg"]
    ]

    return {
        "audit_version": "1.0",
        "audit_type": "retrospective, non-mutating historical design audit",
        "model_inference_performed": False,
        "historical_results_modified": False,
        "manifest_status": manifest["status"],
        "active_case_count": n,
        "manifest_listed_case_ids": case_ids,
        "case_json_files_not_in_active_manifest": unlisted,
        "legacy_context_parity": {
            "cases_with_source_and_technology_identical": common_metadata_count,
            "cases_with_all_I_base_facts_identical": common_base_count,
            "standard_explicit_error_description_count": standard_error_count,
            "ccdg_explicit_error_description_count": ccdg_error_count,
            "standard_dependency_section_count": standard_dependency_count,
            "ccdg_dependency_section_count": ccdg_dependency_count,
            "interpretation": (
                "The historical renderers do not isolate representation format: Standard "
                "includes the explicit error-description section, while CCDG includes "
                "dependency edges and omits that section. I_base/source/technology are shared."
            ),
        },
        "input_cue_screen": {
            "case_count_with_literal_alias_occurring_in_standard_context": len(literal_alias_standard),
            "case_ids_with_literal_alias_in_standard_context": literal_alias_standard,
            "case_count_with_literal_alias_occurring_in_ccdg_context": len(literal_alias_ccdg),
            "case_ids_with_literal_alias_in_ccdg_context": literal_alias_ccdg,
            "case_count_with_explicit_fix_or_corrected_cue_in_I_base": len(explicit_fix_case_ids),
            "case_ids_with_explicit_fix_or_corrected_cue_in_I_base": explicit_fix_case_ids,
            "case_count_with_secondary_remediation_cue_in_I_base": len(secondary_remediation_case_ids),
            "case_ids_with_secondary_remediation_cue_in_I_base": secondary_remediation_case_ids,
            "cue_screen_warning": (
                "These regex flags are triage signals, not semantic ground-truth judgments. "
                "A flagged statement may still be legitimate evidence; a missing flag does not "
                "mean the case is free of diagnosis hints. Review case-level text manually."
            ),
        },
        "cases": case_rows,
        "interpretation_constraints": [
            "This audit does not rescore historical model outputs.",
            "No inference or human rating was performed.",
            "Case-specific context information differences remain a historical design limitation.",
            "Input-level cause/fix clues are not proof of LLM training-set contamination.",
            "Unlisted case files are reported but do not become active experiment cases unless present in the frozen manifest and rubric.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit historical context parity and input-cue risks without inference or mutation."
    )
    parser.add_argument(
        "--project-root", type=Path, default=ROOT,
        help="Repository root containing data/benchmark and the dijitalikiz package.",
    )
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON report path.")
    args = parser.parse_args()

    report = audit_project(args.project_root)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(json.dumps({
            "status": "audit_completed",
            "active_case_count": report["active_case_count"],
            "output": str(args.output),
            "model_inference_performed": False,
            "historical_results_modified": False,
        }, indent=2))
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
