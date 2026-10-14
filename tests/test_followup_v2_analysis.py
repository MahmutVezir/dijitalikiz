from scripts.analyze_followup_v2 import analyze_adjudicated_ratings, exact_mcnemar_pvalue, holm_adjust
from scripts.build_followup_v2_schedule import build_schedule


SEEDS = (42, 43, 44, 45, 46)


def make_rows(case_ids):
    rows = []
    for case_id in case_ids:
        for condition, correct_count in (("A", 3), ("B", 2), ("C", 4)):
            for index, seed in enumerate(SEEDS):
                rows.append({
                    "case_id": case_id,
                    "condition_id": condition,
                    "seed": seed,
                    "final_label": "correct" if index < correct_count else "incorrect",
                    "adjudicated": True,
                    "adjudicator_id": "adjudicator-1",
                })
    return rows


def test_exact_mcnemar_exact_symmetric_binomial_probability():
    assert exact_mcnemar_pvalue(0, 0) == 1.0
    assert exact_mcnemar_pvalue(5, 0) == 0.0625
    assert exact_mcnemar_pvalue(0, 5) == 0.0625
    assert exact_mcnemar_pvalue(3, 3) == 1.0


def test_holm_adjustment_is_monotone_and_bounded():
    adjusted = holm_adjust({"B_vs_A": 0.01, "C_vs_A": 0.04})
    assert adjusted == {"B_vs_A": 0.02, "C_vs_A": 0.04}
    assert all(0 <= value <= 1 for value in adjusted.values())


def test_v2_analysis_uses_final_human_labels_and_case_as_unit():
    cases = ["new-case-1", "new-case-2"]
    report = analyze_adjudicated_ratings(make_rows(cases), cases, bootstrap_resamples=1000)
    assert report["status"] == "pass"
    assert report["case_count"] == 2
    assert report["output_count"] == 30
    assert report["case_level_pass_counts"] == {"A": 2, "B": 0, "C": 2}
    assert report["primary_contrast"]["x_pass_y_fail"] == 2
    assert report["primary_contrast"]["y_pass_x_fail"] == 0
    assert report["primary_contrast"]["exact_two_sided_mcnemar_p"] == 0.5
    assert report["primary_contrast"]["risk_difference_x_minus_y"] == 1.0
    assert report["unscorable_handling"].startswith("counts as not-correct")


def test_v2_analysis_blocks_missing_or_duplicated_ratings():
    cases = ["new-case-1"]
    rows = make_rows(cases)
    assert analyze_adjudicated_ratings(rows[:-1], cases)["status"] == "blocked"
    duplicate = rows + [rows[0]]
    result = analyze_adjudicated_ratings(duplicate, cases)
    assert result["status"] == "blocked"
    assert any(item.startswith("duplicate_rating:") for item in result["issues"])


def test_schedule_is_deterministic_and_covers_every_cell():
    first = build_schedule(["case-a", "case-b"], list(SEEDS), randomization_seed=1201)
    second = build_schedule(["case-a", "case-b"], list(SEEDS), randomization_seed=1201)
    assert first == second
    assert first["status"] == "frozen"
    assert first["model_inference_started"] is False
    assert first["cell_count"] == 30
    assert len({
        (row["case_id"], row["condition_id"], row["seed"])
        for row in first["cells"]
    }) == 30
    assert [row["order_index"] for row in first["cells"]] == list(range(1, 31))


def test_schedule_refuses_duplicate_case_or_seed_ids():
    import pytest
    with pytest.raises(ValueError):
        build_schedule(["case-a", "case-a"], list(SEEDS))
    with pytest.raises(ValueError):
        build_schedule(["case-a"], [1, 1, 2, 3, 4])
