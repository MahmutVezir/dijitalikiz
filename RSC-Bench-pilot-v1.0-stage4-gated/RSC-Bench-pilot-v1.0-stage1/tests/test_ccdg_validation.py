from rscbench.schemas import CCDG, Case, GroundTruth
from rscbench.validator import base_input_sha256
from rscbench.validator import validate_case_links

def test_pilot_fixture_links():
    case = Case.model_validate({
        "case_id":"x",
        "source":{"type":"synthetic_fixture","url":"https://example.invalid/x","publication_date":"2026-01-01"},
        "technology":["test"],"error_description":"test","I_base":{"problem":"x"},
        "contamination":{"is_pilot":True,"excluded_from_main_dataset":True,"reason":"technical validation"}
    })
    truth = GroundTruth(case_id="x", component="RLS", entity="profiles",
                        operation="SELECT", root_cause="policy_condition_mismatch",
                        required_relation=[])
    ccdg = CCDG.model_validate({"case_id":"x","base_input_sha256":base_input_sha256(case),"nodes":[{"id":"a","type":"component","name":"A"}],"edges":[]})
    validate_case_links(case, truth, ccdg)
