from scripts.power_mcnemar import exact_mcnemar_power, required_n


def test_power_is_zero_without_discordant_probability():
    assert exact_mcnemar_power(100, 0.0, 0.0) == 0.0


def test_power_increases_with_sample_size_for_fixed_effect():
    small = exact_mcnemar_power(20, 0.25, 0.05)
    large = exact_mcnemar_power(100, 0.25, 0.05)
    assert large >= small


def test_required_n_meets_target():
    n = required_n(0.25, 0.05, target_power=0.80, max_n=1000)
    assert n is not None
    assert exact_mcnemar_power(n, 0.25, 0.05) >= 0.80
    if n > 2:
        assert exact_mcnemar_power(n - 1, 0.25, 0.05) < 0.80


def test_symmetric_discordance_does_not_claim_power():
    power = exact_mcnemar_power(200, 0.10, 0.10)
    assert power < 0.20
