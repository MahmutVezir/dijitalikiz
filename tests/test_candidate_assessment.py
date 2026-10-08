from dijitalikiz.candidate_assessment import (
    CandidateAssessment,
    CCDGSuitability,
    ContaminationRisk,
    CriterionState,
    DependencyStrength,
)


def test_default_not_eligible():
    assessment = CandidateAssessment(case_id="X")
    assert assessment.recompute_eligibility() is False
    assert assessment.eligible_for_main is False


def test_complete_case_eligible_for_pilot_but_main_requires_contamination_audit():
    assessment = CandidateAssessment(
        case_id="X",
        IC1=CriterionState.PASS,
        IC2=CriterionState.PASS,
        IC3=CriterionState.PASS,
        IC4=CriterionState.PASS,
        IC5=CriterionState.PASS,
        IC6=CriterionState.PASS,
        IC7=CriterionState.PASS,
        dependency_strength=DependencyStrength.STRONG,
        ccdg_suitability=CCDGSuitability.STRONG,
    )
    assert assessment.recompute_eligibility() is True
    assert assessment.eligible_for_main is False

    assessment.contamination_risk = ContaminationRisk.MEDIUM
    assert assessment.recompute_eligibility() is True
    assert assessment.eligible_for_main is True


def test_eligible_field_rejects_non_boolean():
    payload = CandidateAssessment(case_id="X").to_dict()
    payload["eligible_for_pilot"] = "false"
    try:
        CandidateAssessment.from_dict(payload)
    except TypeError:
        pass
    else:
        raise AssertionError("eligible_for_pilot must be a boolean")


def test_main_eligibility_rejects_false_frozen_value():
    assessment = CandidateAssessment(
        case_id="X",
        IC1=CriterionState.PASS,
        IC2=CriterionState.PASS,
        IC3=CriterionState.PASS,
        IC4=CriterionState.PASS,
        IC5=CriterionState.PASS,
        IC6=CriterionState.PASS,
        IC7=CriterionState.PASS,
        dependency_strength=DependencyStrength.STRONG,
        ccdg_suitability=CCDGSuitability.STRONG,
        contamination_risk=ContaminationRisk.LOW,
    )
    payload = assessment.to_dict()
    payload["eligible_for_main"] = False
    try:
        CandidateAssessment.from_dict(payload)
    except ValueError:
        pass
    else:
        raise AssertionError("eligible_for_main must match deterministic eligibility")
