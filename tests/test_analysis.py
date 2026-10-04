from scripts.analyze_case_level import exact_mcnemar_pvalue
def test_mcnemar_is_one_when_no_discordant_cases():
    assert exact_mcnemar_pvalue(0,0)==1.0
def test_mcnemar_is_symmetric():
    assert exact_mcnemar_pvalue(2,5)==exact_mcnemar_pvalue(5,2)
def test_mcnemar_extreme_discordance_is_small():
    assert exact_mcnemar_pvalue(0,8)<0.01
