from dijitalikiz.candidate_assessment import CandidateAssessment, CriterionState, DependencyStrength, CCDGSuitability

def test_default_not_eligible():
    assert CandidateAssessment(case_id="X").recompute_eligibility() is False

def test_complete_case_eligible():
    a=CandidateAssessment(case_id="X",IC1=CriterionState.PASS,IC2=CriterionState.PASS,IC3=CriterionState.PASS,IC4=CriterionState.PASS,IC5=CriterionState.PASS,IC6=CriterionState.PASS,IC7=CriterionState.PASS,dependency_strength=DependencyStrength.STRONG,ccdg_suitability=CCDGSuitability.STRONG)
    assert a.recompute_eligibility() is True
