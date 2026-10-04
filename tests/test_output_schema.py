import pytest

from dijitalikiz.models import DiagnosticOutput


def valid_payload():
    return {
        "diagnosed_component": "Component",
        "root_cause_class": "root_cause",
        "affected_entity": "Entity",
        "explanation": "Operation explanation",
    }


def test_diagnostic_output_accepts_exact_frozen_schema():
    output = DiagnosticOutput.from_dict(valid_payload())
    assert output.diagnosed_component == "Component"


def test_diagnostic_output_rejects_extra_fields():
    payload = valid_payload()
    payload["confidence"] = "high"
    with pytest.raises(ValueError):
        DiagnosticOutput.from_dict(payload)


def test_diagnostic_output_rejects_missing_fields():
    payload = valid_payload()
    del payload["explanation"]
    with pytest.raises(ValueError):
        DiagnosticOutput.from_dict(payload)


def test_diagnostic_output_rejects_non_string_fields():
    payload = valid_payload()
    payload["affected_entity"] = 123
    with pytest.raises(TypeError):
        DiagnosticOutput.from_dict(payload)
