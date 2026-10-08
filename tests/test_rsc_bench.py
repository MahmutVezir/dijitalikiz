import json
from pathlib import Path

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.evaluation import evaluate_output
from dijitalikiz.models import DiagnosticOutput, ResearchCase


def _load_case() -> ResearchCase:
    path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "pilot"
        / "commons-math-defects4j-MATH-927.json"
    )
    with path.open("r", encoding="utf-8") as handle:
        return ResearchCase.from_dict(json.load(handle))


def test_standard_context_includes_error_details():
    case = _load_case()
    rendered = render_standard_context(case)
    assert "Error description:" in rendered
    assert "GammaDistribution cloning failed" in rendered
    assert "I_base:" in rendered


def test_ccdg_context_includes_dependencies():
    case = _load_case()
    rendered = render_ccdg_context(case)
    assert "GammaDistribution" in rendered
    assert "inherits_from" in rendered
    assert "BitsStreamGenerator" in rendered


def test_evaluation_accepts_matching_output():
    case = _load_case()
    output = DiagnosticOutput(
        diagnosed_component="BitsStreamGenerator",
        root_cause_class="non_serializable_dependency_in_inheritance_chain",
        affected_entity="GammaDistribution",
        explanation=(
            "The serialization/cloning operation fails because the "
            "GammaDistribution dependency chain reaches BitsStreamGenerator."
        ),
    )
    result = evaluate_output(output, case.ground_truth)
    assert result["passed"] is True


def test_evaluation_rejects_mismatched_output():
    case = _load_case()
    output = DiagnosticOutput(
        diagnosed_component="Frontend",
        root_cause_class="timeout",
        affected_entity="users",
        explanation="The UI is slow because the API request is delayed.",
    )
    result = evaluate_output(output, case.ground_truth)
    assert result["passed"] is False
