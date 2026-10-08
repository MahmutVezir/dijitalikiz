from __future__ import annotations

import argparse
import json
from pathlib import Path

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.models import ResearchCase


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    case = ResearchCase.from_dict(json.loads(path.read_text(encoding="utf-8")))

    if not case.case_id:
        errors.append("case_id is empty")
    if not case.source_url:
        errors.append("source_url is empty")
    if not case.i_base:
        errors.append("i_base is empty")
    if not case.ccdg:
        errors.append("ccdg is empty")
    if not case.ground_truth.component:
        errors.append("ground_truth.component is empty")
    if not case.ground_truth.entity:
        errors.append("ground_truth.entity is empty")
    if not case.ground_truth.operation:
        errors.append("ground_truth.operation is empty")
    if not case.ground_truth.root_cause:
        errors.append("ground_truth.root_cause is empty")
    if not case.ground_truth.required_relations:
        errors.append("ground_truth.required_relations is empty")
    for index, edge in enumerate(case.ccdg):
        if not edge.source or not edge.target or not edge.relation:
            errors.append(f"ccdg edge {index} is incomplete")
    if case.ground_truth.root_cause in render_standard_context(case):
        errors.append("ground-truth root cause leaked into Standard context")
    if case.ground_truth.root_cause in render_ccdg_context(case):
        errors.append("ground-truth root cause leaked into CCDG context")
    standard = render_standard_context(case)
    ccdg = render_ccdg_context(case)
    if standard == ccdg:
        errors.append("Standard and CCDG contexts are identical")
    for base_item in case.i_base:
        if base_item not in standard:
            errors.append("I_base item missing from Standard context")
        if base_item not in ccdg:
            errors.append("I_base item missing from CCDG context")
    for rendered_name, rendered in (
        ("Standard", standard),
        ("CCDG", ccdg),
    ):
        if "ground_truth" in rendered.lower():
            errors.append(f"ground_truth field leaked into {rendered_name} context")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    path = Path(args.path)
    errors = validate(path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print(f"VALID: {path}")


if __name__ == "__main__":
    main()
