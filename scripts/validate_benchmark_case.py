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
    if case.ground_truth.root_cause in render_standard_context(case):
        errors.append("ground-truth root cause leaked into Standard context")
    if case.ground_truth.root_cause in render_ccdg_context(case):
        errors.append("ground-truth root cause leaked into CCDG context")
    for rendered_name, rendered in (
        ("Standard", render_standard_context(case)),
        ("CCDG", render_ccdg_context(case)),
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
