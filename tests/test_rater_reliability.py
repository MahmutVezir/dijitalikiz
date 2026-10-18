import csv

import pytest

from scripts.audit_rater_reliability import (
    LABELS,
    compute_rater_reliability,
    load_ratings_csv,
    main,
)


def rows_with_full_agreement():
    return [
        {"item_id": label, "rater_a": label, "rater_b": label}
        for label in LABELS
    ]


def test_reliability_passes_with_full_agreement_across_all_labels():
    rows = rows_with_full_agreement()
    report = compute_rater_reliability(rows, [row["item_id"] for row in rows])

    assert report["status"] == "pass"
    assert report["gate_passed"] is True
    assert report["exact_agreement"] == 1.0
    assert report["cohen_kappa"] == 1.0
    assert report["rating_count"] == 4
    assert report["calibration_only"] is True
    assert report["model_inference_permitted"] is False
    assert report["gate_reasons"] == []


def test_reliability_blocks_below_both_preregistered_thresholds():
    rows = [
        {"item_id": "1", "rater_a": "correct", "rater_b": "correct"},
        {"item_id": "2", "rater_a": "correct", "rater_b": "partially_correct"},
        {"item_id": "3", "rater_a": "partially_correct", "rater_b": "partially_correct"},
        {"item_id": "4", "rater_a": "incorrect", "rater_b": "incorrect"},
    ]
    report = compute_rater_reliability(rows, ["1", "2", "3", "4"])

    assert report["status"] == "blocked"
    assert report["exact_agreement"] == 0.75
    assert report["cohen_kappa"] == pytest.approx(0.636364, abs=1e-6)
    assert report["gate_reasons"] == [
        "exact_agreement_below_threshold",
        "cohen_kappa_below_threshold",
    ]


def test_undefined_kappa_blocks_even_when_exact_agreement_is_perfect():
    rows = [
        {"item_id": "1", "rater_a": "correct", "rater_b": "correct"},
        {"item_id": "2", "rater_a": "correct", "rater_b": "correct"},
    ]
    report = compute_rater_reliability(rows, ["1", "2"])

    assert report["exact_agreement"] == 1.0
    assert report["cohen_kappa"] is None
    assert report["status"] == "blocked"
    assert "cohen_kappa_undefined" in report["gate_reasons"]


def test_rating_rows_must_match_preregistered_item_ids_exactly():
    rows = [{"item_id": "item-1", "rater_a": "correct", "rater_b": "correct"}]

    with pytest.raises(ValueError, match="do not match"):
        compute_rater_reliability(rows, ["item-1", "item-2"])


def test_duplicate_items_and_invalid_labels_are_rejected():
    duplicate = [
        {"item_id": "item-1", "rater_a": "correct", "rater_b": "correct"},
        {"item_id": "item-1", "rater_a": "incorrect", "rater_b": "incorrect"},
    ]
    with pytest.raises(ValueError, match="duplicate item IDs"):
        compute_rater_reliability(duplicate, ["item-1", "item-2"])

    invalid = [{"item_id": "item-1", "rater_a": "agree", "rater_b": "correct"}]
    with pytest.raises(ValueError, match="invalid rater_a label"):
        compute_rater_reliability(invalid, ["item-1"])


def test_csv_loader_requires_only_opaque_id_and_two_labels(tmp_path):
    ratings_path = tmp_path / "ratings.csv"
    with ratings_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["item_id", "rater_a", "rater_b"])
        writer.writeheader()
        writer.writerow({"item_id": "opaque-1", "rater_a": "correct", "rater_b": "correct"})
    rows = load_ratings_csv(ratings_path)

    assert rows == [{"item_id": "opaque-1", "rater_a": "correct", "rater_b": "correct"}]


def test_csv_loader_rejects_extra_or_reordered_columns(tmp_path):
    ratings_path = tmp_path / "ratings.csv"
    ratings_path.write_text("item_id,rater_b,rater_a\nx,correct,correct\n", encoding="utf-8")

    with pytest.raises(ValueError, match="CSV header must be exactly"):
        load_ratings_csv(ratings_path)



def test_cli_rejects_attempt_to_lower_preregistered_thresholds(tmp_path):
    ratings_path = tmp_path / "ratings.csv"
    ratings_path.write_text(
        "item_id,rater_a,rater_b\nopaque-1,incorrect,incorrect\n",
        encoding="utf-8",
    )
    expected_ids_path = tmp_path / "expected_ids.json"
    expected_ids_path.write_text('["opaque-1"]', encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        main([
            "--ratings-csv", str(ratings_path),
            "--expected-item-ids", str(expected_ids_path),
            "--min-exact-agreement", "0",
            "--min-kappa", "-1",
        ])

    assert exc_info.value.code == 2
