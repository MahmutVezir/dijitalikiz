import pytest
from rscbench.io import parse_model_output
from rscbench.schemas import ModelOutput


def test_valid_model_output_parses():
    raw = '{"diagnosed_component":"RLS","root_cause_class":"policy_condition_mismatch","affected_entity":"profiles","explanation":"x"}'
    parsed = parse_model_output(raw, ModelOutput)
    assert parsed.diagnosed_component == "RLS"


def test_non_json_response_is_rejected():
    with pytest.raises(ValueError, match="not valid JSON"):
        parse_model_output("not json", ModelOutput)


def test_extra_output_field_is_rejected():
    raw = '{"diagnosed_component":"RLS","root_cause_class":"x","affected_entity":"profiles","explanation":"x","extra":"no"}'
    with pytest.raises(Exception):
        parse_model_output(raw, ModelOutput)
