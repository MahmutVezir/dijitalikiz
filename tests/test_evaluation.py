from dijitalikiz.evaluation import evaluate_output
from dijitalikiz.models import DiagnosticOutput, GroundTruth


def test_evaluation_checks_are_boolean():
    truth = GroundTruth(
        component="C",
        entity="E",
        operation="SELECT",
        root_cause="R",
        required_relations=["A"],
    )
    output = DiagnosticOutput(
        diagnosed_component="C",
        root_cause_class="R",
        affected_entity="E",
        explanation="SELECT uses A",
    )
    result = evaluate_output(output, truth)
    assert all(isinstance(value, bool) for value in result["checks"].values())
    assert result["passed"] is True
