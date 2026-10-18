import csv
import json

import pytest

from scripts.audit_rater_reliability import (
    CHALLENGE_CLASSES,
    LABELS,
    RESPONSE_ORIGINS,
    compute_rater_reliability,
    load_ratings_csv,
    main,
)


def expected_items():
    items = []
    challenge_classes = CHALLENGE_CLASSES * 4
    for index, challenge_class in enumerate(challenge_classes):
        if index < 7:
            origin = "independent_model_output"
            source_case_id = f"model-case-{index + 1}"
        else:
            origin = (
                "human_authored_control"
                if index % 2 == 0
                else "synthetic_adversarial_control"
            )
            source_case_id = f"control-case-{index + 1}"
        items.append({
            "item_id": f"opaque-item-{index + 1:03d}",
            "challenge_class": challenge_class,
            "source_case_id": source_case_id,
            "response_origin": origin,
        })
    return items


def rows_with_full_agreement(items):
    return [
        {
            "item_id": item["item_id"],
            "rater_a": LABELS[index % len(LABELS)],
            "rater_b": LABELS[index % len(LABELS)],
        }
        for index, item in enumerate(items)
    ]


def test_reliability_passes_with_full_agreement_and_valid_composition():
    items = expected_items()
    rows = rows_with_full_agreement(items)
    report = compute_rater_reliability(rows, items)

    assert report["status"] == "pass"
    assert report["gate_passed"] is True
    assert report["exact_agreement"] == 1.0
    assert report["cohen_kappa"] == 1.0
    assert report["rating_count"] == 28
    assert report["calibration_only"] is True
    assert report["model_inference_permitted"] is False
    assert report["gate_reasons"] == []
    composition = report["calibration_composition"]
    assert set(composition["challenge_class_counts"].values()) == {4}
    assert composition["distinct_model_output_cases"] == 7
    assert composition["control_example_count"] >= 7


def test_reliability_blocks_below_both_preregistered_thresholds():
    items = expected_items()
    pattern = (
        ("correct", "correct"),
        ("correct", "partially_correct"),
        ("partially_correct", "partially_correct"),
        ("incorrect", "incorrect"),
    )
    rows = [
        {
            "item_id": item["item_id"],
            "rater_a": pattern[index % 4][0],
            "rater_b": pattern[index % 4][1],
        }
        for index, item in enumerate(items)
    ]
    report = compute_rater_reliability(rows, items)

    assert report["status"] == "blocked"
    assert report["exact_agreement"] == 0.75
    assert report["cohen_kappa"] == pytest.approx(0.636364, abs=1e-6)
    assert report["gate_reasons"] == [
        "exact_agreement_below_threshold",
        "cohen_kappa_below_threshold",
    ]


def test_undefined_kappa_blocks_even_when_exact_agreement_is_perfect():
    items = expected_items()
    rows = [
        {"item_id": item["item_id"], "rater_a": "correct", "rater_b": "correct"}
        for item in items
    ]
    report = compute_rater_reliability(rows, items)

    assert report["exact_agreement"] == 1.0
    assert report["cohen_kappa"] is None
    assert report["status"] == "blocked"
    assert "cohen_kappa_undefined" in report["gate_reasons"]


def test_rating_rows_must_match_preregistered_item_ids_exactly():
    items = expected_items()
    rows = [{
        "item_id": items[0]["item_id"],
        "rater_a": "correct",
        "rater_b": "correct",
    }]

    with pytest.raises(ValueError, match="do not match"):
        compute_rater_reliability(rows, items)


def test_duplicate_items_and_invalid_labels_are_rejected():
    items = expected_items()
    duplicate = [
        {"item_id": items[0]["item_id"], "rater_a": "correct", "rater_b": "correct"},
        {"item_id": items[0]["item_id"], "rater_a": "incorrect", "rater_b": "incorrect"},
    ]
    with pytest.raises(ValueError, match="duplicate item IDs"):
        compute_rater_reliability(duplicate, items)

    invalid = [
        {"item_id": items[0]["item_id"], "rater_a": "agree", "rater_b": "correct"}
    ]
    with pytest.raises(ValueError, match="invalid rater_a label"):
        compute_rater_reliability(invalid, items)


def test_calibration_metadata_rejects_underrepresented_challenge_class():
    items = expected_items()
    items[0]["challenge_class"] = "canonical_correct"
    with pytest.raises(ValueError, match="class composition is below"):
        compute_rater_reliability(rows_with_full_agreement(items), items)


def test_calibration_metadata_requires_seven_distinct_model_output_cases():
    items = expected_items()
    model_items = [
        item for item in items
        if item["response_origin"] == "independent_model_output"
    ]
    model_items[-1]["source_case_id"] = model_items[0]["source_case_id"]
    with pytest.raises(ValueError, match="seven distinct defect cases"):
        compute_rater_reliability(rows_with_full_agreement(items), items)


def test_calibration_metadata_requires_seven_control_examples():
    items = expected_items()
    for item in items:
        item["response_origin"] = "independent_model_output"
        item["source_case_id"] = f"unique-case-{item['item_id']}"
    with pytest.raises(ValueError, match="at least seven control examples"):
        compute_rater_reliability(rows_with_full_agreement(items), items)


def test_csv_loader_requires_only_opaque_id_and_two_labels(tmp_path):
    ratings_path = tmp_path / "ratings.csv"
    with ratings_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["item_id", "rater_a", "rater_b"])
        writer.writeheader()
        writer.writerow({
            "item_id": "opaque-001", "rater_a": "correct", "rater_b": "correct"
        })
    rows = load_ratings_csv(ratings_path)

    assert rows == [{
        "item_id": "opaque-001", "rater_a": "correct", "rater_b": "correct"
    }]


def test_csv_loader_rejects_extra_or_reordered_columns(tmp_path):
    ratings_path = tmp_path / "ratings.csv"
    ratings_path.write_text(
        "item_id,rater_b,rater_a\nx,correct,correct\n", encoding="utf-8"
    )

    with pytest.raises(ValueError, match="CSV header must be exactly"):
        load_ratings_csv(ratings_path)


def test_cli_rejects_attempt_to_lower_preregistered_thresholds(tmp_path):
    items = expected_items()
    ratings_path = tmp_path / "ratings.csv"
    ratings_path.write_text(
        "item_id,rater_a,rater_b\nopaque-001,incorrect,incorrect\n",
        encoding="utf-8",
    )
    expected_path = tmp_path / "expected_item_metadata.json"
    expected_path.write_text(json.dumps(items), encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        main([
            "--ratings-csv", str(ratings_path),
            "--expected-item-metadata", str(expected_path),
            "--min-exact-agreement", "0",
            "--min-kappa", "-1",
        ])

    assert exc_info.value.code == 2
