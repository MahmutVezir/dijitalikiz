from rscbench.matcher import deterministic_match
from rscbench.schemas import GroundTruth, ModelOutput

def truth():
    return GroundTruth(case_id="x", component="RLS", entity="profiles",
                        operation="SELECT", root_cause="policy_condition_mismatch",
                        required_relation=["a", "b"])

def test_exact_primary_match():
    out = ModelOutput(diagnosed_component="RLS",
                      root_cause_class="policy_condition_mismatch",
                      affected_entity="profiles", explanation="x")
    assert deterministic_match(out, truth()).primary_accuracy == 1

def test_wrong_root_cause_is_incorrect():
    out = ModelOutput(diagnosed_component="RLS", root_cause_class="other",
                      affected_entity="profiles", explanation="x")
    assert deterministic_match(out, truth()).primary_accuracy == 0
