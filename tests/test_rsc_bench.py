import json
from pathlib import Path

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.evaluation import evaluate_output
from dijitalikiz.models import DiagnosticOutput, ResearchCase


def _load_case() -> ResearchCase:
    sample = Path(__file__).resolve().parents[1] / "data" / "sample_cases" / "supabase_rls_case.json"
    with sample.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return ResearchCase.from_dict(payload)


def test_standard_context_includes_error_details():
    case = _load_case()
    rendered = render_standard_context(case)
    assert "Error description:" in rendered
    assert "The profile list shows rows from other users" in rendered
    assert "I_base:" in rendered


def test_ccdg_context_includes_dependencies():
    case = _load_case()
    rendered = render_ccdg_context(case)
    assert "React ProfileList" in rendered
    assert "calls" in rendered
    assert "protected_by" in rendered
    assert "auth.uid" in rendered


def test_evaluation_accepts_matching_output():
    case = _load_case()
    output = DiagnosticOutput(
        diagnosed_component="RLS",
        root_cause_class="policy_condition_mismatch",
        affected_entity="profiles",
        explanation="The SELECT bug happens because authenticated_user must match profiles.id and auth.uid semantics are incorrect.",
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
