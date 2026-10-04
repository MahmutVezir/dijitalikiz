def majority_pass(values: list[bool], required: int = 3) -> bool:
    return len(values) == 5 and sum(values) >= required


def test_majority_rule_requires_five_seeds():
    assert majority_pass([True, True, True, False, False])
    assert not majority_pass([True, True, False, False])


def test_majority_rule_rejects_two_of_five():
    assert not majority_pass([True, True, False, False, False])


def test_majority_rule_accepts_four_or_five():
    assert majority_pass([True, True, True, True, False])
    assert majority_pass([True, True, True, True, True])
