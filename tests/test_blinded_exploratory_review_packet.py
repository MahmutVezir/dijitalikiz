import hashlib
import json
from collections import Counter
from pathlib import Path

from scripts.build_blinded_exploratory_review_packet import build_packet


def _write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def _small_artifact(root: Path) -> None:
    _write_json(root / "benchmark_manifest.json", {"case_ids": ["case-private-1"]})
    _write_json(
        root / "cases" / "case-private-1.json",
        {
            "case_id": "case-private-1",
            "source": "Synthetic test fixture",
            "source_url": "https://example.invalid/issue/1",
            "publication_date": "2026-01-01",
            "technology": "Python",
            "error_description": "A synthetic multi-component test defect.",
            "i_base": ["Component A calls Component B."],
            "ccdg": [{"source": "A", "target": "B", "relation": "calls", "details": "synthetic"}],
            "ground_truth": {
                "component": "Component B",
                "entity": "test entity",
                "operation": "run()",
                "root_cause": "synthetic_root_cause",
                "required_relations": ["Component A", "Component B"],
            },
        },
    )
    for condition in ("standard", "ccdg"):
        for seed in (42, 43, 44, 45, 46):
            _write_json(
                root / "runs" / f"case-private-1__{condition}__seed{seed}.json",
                {
                    "case_id": "case-private-1",
                    "condition": condition,
                    "seed": seed,
                    "source_commit": "test-commit",
                    "prompt_sha256": f"prompt-{condition}-{seed}",
                    "context_sha256": f"context-{condition}-{seed}",
                    "raw_output": json.dumps({
                        "diagnosis": "opaque-" + hashlib.sha256(f"{condition}:{seed}".encode()).hexdigest()[:12]
                    }),
                    "parsed_output": {
                        "diagnosed_component": "Component B",
                        "root_cause_class": "candidate mechanism",
                        "affected_entity": "test entity",
                        "explanation": "A synthetic candidate explanation.",
                    },
                },
            )


def test_review_packet_masks_case_condition_and_seed(tmp_path):
    root = tmp_path / "artifact"
    _small_artifact(root)
    packet, key = build_packet(root, "0" * 64)
    assert packet[0]["n_records"] == 10
    assert packet[0]["condition_labels_and_seeds_in_reviewer_rows"] is False
    rows = packet[1:]
    assert len(rows) == 10
    for row in rows:
        assert "case-private-1" not in json.dumps(row, ensure_ascii=False)
        assert "condition" not in row
        assert "seed" not in row
        assert "reference" not in row
        serialized = json.dumps(row, ensure_ascii=False)
        assert "synthetic_root_cause" not in serialized
        assert "example.invalid" not in serialized
        assert "source_url" not in row["source_evidence"]
        assert "source" not in row["source_evidence"]
        assert "publication_date" not in row["source_evidence"]
        assert set(row["source_evidence"]) == {"technical_domain", "reported_problem", "base_facts"}
        assert all("evidence_id" in fact and "text" in fact for fact in row["source_evidence"]["base_facts"])
        assert set(row["review"]) == {
            "root_cause_correctness",
            "component_localization",
            "evidence_consistency",
            "dependency_reasoning",
            "overall_diagnostic_status",
            "reviewer_notes_with_evidence",
        }
    assert all("condition" in item and "seed" in item for item in key)
    assert {item["condition"] for item in key} == {"standard", "ccdg"}
    assert {item["seed"] for item in key} == {42, 43, 44, 45, 46}
    assert {item["review_id"] for item in key} == {row["review_id"] for row in rows}


def test_review_packet_is_deterministic_for_same_artifact_hash(tmp_path):
    root = tmp_path / "artifact"
    _small_artifact(root)
    packet1, key1 = build_packet(root, "f" * 64)
    packet2, key2 = build_packet(root, "f" * 64)
    assert packet1 == packet2
    assert key1 == key2


def test_review_packet_rejects_missing_run_records(tmp_path):
    root = tmp_path / "artifact"
    _small_artifact(root)
    (root / "runs" / "case-private-1__ccdg__seed46.json").unlink()
    try:
        build_packet(root, "0" * 64)
    except ValueError as exc:
        assert "Expected 10 run records" in str(exc)
    else:
        raise AssertionError("Missing run records must fail closed.")


def test_reviewer_packets_have_independent_order_and_stable_case_refs(tmp_path):
    root = tmp_path / "artifact"
    _small_artifact(root)
    packet_a, key_a = build_packet(root, "f" * 64, "A")
    packet_b, key_b = build_packet(root, "f" * 64, "B")

    rows_a = packet_a[1:]
    rows_b = packet_b[1:]
    assert packet_a[0]["reviewer_code"] == "A"
    assert packet_b[0]["reviewer_code"] == "B"
    assert packet_a[0]["ground_truth_and_answer_key_hidden_from_reviewer_rows"] is True
    assert packet_b[0]["source_urls_and_project_identifiers_hidden_from_reviewer_rows"] is True
    assert packet_a[0]["perfect_condition_blinding_guaranteed"] is False
    assert all(row["review_id"].startswith("REVIEW-A-") for row in rows_a)
    assert all(row["review_id"].startswith("REVIEW-B-") for row in rows_b)

    refs_a = {item["source_case_id"]: item["case_ref"] for item in key_a}
    refs_b = {item["source_case_id"]: item["case_ref"] for item in key_b}
    assert refs_a == refs_b == {"case-private-1": refs_a["case-private-1"]}

    def without_review_id(row):
        return {key: value for key, value in row.items() if key != "review_id"}

    import collections
    a_content = collections.Counter(
        json.dumps(without_review_id(row), sort_keys=True) for row in rows_a
    )
    b_content = collections.Counter(
        json.dumps(without_review_id(row), sort_keys=True) for row in rows_b
    )
    assert a_content == b_content
    sequence_a = [(row["case_ref"], hashlib.sha256(row["response"]["raw_output"].encode()).hexdigest()) for row in rows_a]
    sequence_b = [(row["case_ref"], hashlib.sha256(row["response"]["raw_output"].encode()).hexdigest()) for row in rows_b]
    assert sequence_a != sequence_b
    assert Counter(sequence_a) == Counter(sequence_b)
    assert {item["reviewer_code"] for item in key_a} == {"A"}
    assert {item["reviewer_code"] for item in key_b} == {"B"}
    assert all(len(item["raw_output_sha256"]) == 64 for item in key_a + key_b)

