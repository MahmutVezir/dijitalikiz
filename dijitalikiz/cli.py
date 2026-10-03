from __future__ import annotations

import argparse
import json
from pathlib import Path

from .context import render_ccdg_context, render_standard_context
from .evaluation import evaluate_output
from .models import DiagnosticOutput, ResearchCase


def load_case(case_path: str | Path) -> ResearchCase:
    with Path(case_path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return ResearchCase.from_dict(payload)


def _print_case_summary(case: ResearchCase) -> None:
    print(render_standard_context(case))
    print("\n" + "=" * 80 + "\n")
    print(render_ccdg_context(case))


def _evaluate_demo(case: ResearchCase) -> None:
    expected = case.ground_truth
    predicted = DiagnosticOutput(
        diagnosed_component=expected.component,
        root_cause_class=expected.root_cause,
        affected_entity=expected.entity,
        explanation=(
            "The issue is caused by a policy condition mismatch: "
            f"authenticated_user must be compared with {expected.entity} using the correct {expected.operation} semantics. "
            f"Required relation: {', '.join(expected.required_relations)}"
        ),
    )
    result = evaluate_output(predicted, expected)
    print("\n" + "=" * 80)
    print("Evaluation result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="RSC-Bench CCDG research scaffold")
    parser.add_argument("--case", type=str, help="Path to a JSON case file")
    parser.add_argument(
        "--mode",
        choices=["render", "evaluate"],
        default="render",
        help="Render either standard and CCDG prompts or evaluate a matching output.",
    )
    args = parser.parse_args()

    if not args.case:
        parser.error("--case is required for this tool")

    case = load_case(args.case)
    if args.mode == "render":
        _print_case_summary(case)
    else:
        _evaluate_demo(case)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
