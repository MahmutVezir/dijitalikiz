import json
from pathlib import Path

import pytest

from scripts.build_case_ground_truth_review_packets import build_packets


def _write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _fixture_manifest(root: Path) -> Path:
    candidates = []
    for index in range(4):
        case_id = f"private-case-{index}"
        pre_fix = f"{index + 1:040x}"
        fixed = f"{index + 11:040x}"
        source_url = f"https://github.com/example/project/pull/{index + 1}"
        case_path = f"data/calibration/cases/{case_id}.json"
        record = {
            "case_id": case_id,
            "source_url": source_url,
            "source": "Example project source history",
            "publication_date": "2026-10-10",
            "technology": "Java",
            "error_description": "Private ground-truth clue that must not be leaked.",
            "i_base": ["Private base fact that must not be leaked."],
            "ccdg": [{"source": "A", "relation": "calls", "target": "B"}],
            "ground_truth": {
                "component": "PrivateComponent",
                "entity": "PrivateEntity",
                "operation": "privateOperation",
                "root_cause": "private_root_cause_secret",
                "required_relations": ["A", "B"],
            },
            "software_twin_snapshot": {
                "repository_url": "https://github.com/example/project",
                "snapshot_revision": pre_fix,
                "regression_test": "ExampleTest#failsBeforeFix",
                "observed_failure_signal": "An assertion fails in the pre-fix revision.",
            },
            "provenance": {"pre_fix_revision": pre_fix, "fix_commit": fixed},
        }
        _write_json(root / case_path, record)
        candidates.append({
            "case_id": case_id,
            "source_url": source_url,
            "repository_url": "https://github.com/example/project",
            "pre_fix_revision": pre_fix,
            "fix_revision": fixed,
            "regression_test_targets": ["ExampleTest#failsBeforeFix"],
            "case_record_path": case_path,
            "reproduction_evidence_url": f"https://github.com/example/project/actions/runs/{index + 1}",
        })
    manifest_path = root / "data" / "calibration" / "case_pool_manifest.json"
    _write_json(manifest_path, {
        "schema_version": "1.0",
        "status": "screening_pending",
        "model_inference_permitted": False,
        "candidates": candidates,
        "selection_freeze": {"frozen": False, "eligible_case_ids": []},
    })
    return manifest_path


def test_packets_mask_case_ids_and_provisional_annotations_and_keep_private_key_outside_repo(tmp_path):
    manifest = _fixture_manifest(tmp_path)
    output = tmp_path / "private-review"
    result = build_packets(
        manifest_path=manifest,
        reviewer_a_output=output / "reviewer_a.jsonl",
        reviewer_b_output=output / "reviewer_b.jsonl",
        key_output=output / "private_key.json",
        manifest_output=output / "packet_manifest.json",
    )

    reviewer_a = [json.loads(line) for line in (output / "reviewer_a.jsonl").read_text(encoding="utf-8").splitlines()]
    reviewer_b = [json.loads(line) for line in (output / "reviewer_b.jsonl").read_text(encoding="utf-8").splitlines()]
    key = json.loads((output / "private_key.json").read_text(encoding="utf-8"))
    serialized_packets = (output / "reviewer_a.jsonl").read_text() + (output / "reviewer_b.jsonl").read_text()

    assert result["case_count"] == 4
    assert result["reviewer_packets_contain_provisional_ground_truth"] is False
    assert result["human_review_completed"] is False
    assert len(reviewer_a) == len(reviewer_b) == 4
    assert {row["review_id"] for row in reviewer_a} == {row["review_id"] for row in reviewer_b}
    assert all("private-case-" not in serialized_packets for _ in [0])
    assert "private_root_cause_secret" not in serialized_packets
    assert "PrivateComponent" not in serialized_packets
    assert "Private base fact" not in serialized_packets
    assert "ground_truth" not in serialized_packets.lower()
    assert all(isinstance(entry, dict) for entry in key["mapping"].values())
    assert {entry["case_id"] for entry in key["mapping"].values()} == {f"private-case-{i}" for i in range(4)}
    assert result["reviewer_a_packet_sha256"]
    assert result["reviewer_b_packet_sha256"]
    assert (output / "REVIEWER_INSTRUCTIONS.md").is_file()


def test_builder_rejects_private_outputs_inside_repository(tmp_path):
    manifest = _fixture_manifest(tmp_path)
    with pytest.raises(ValueError, match="outside the repository"):
        build_packets(
            manifest_path=manifest,
            reviewer_a_output=tmp_path / "a.jsonl",
            reviewer_b_output=tmp_path / "b.jsonl",
            key_output=Path(__file__).resolve().parents[1] / "data" / "calibration" / "private_key.json",
            manifest_output=tmp_path / "packet_manifest.json",
        )


def test_packet_has_only_source_revision_evidence_not_provisional_graph_labels(tmp_path):
    manifest = _fixture_manifest(tmp_path)
    output = tmp_path / "private-review"
    build_packets(
        manifest_path=manifest,
        reviewer_a_output=output / "reviewer_a.jsonl",
        reviewer_b_output=output / "reviewer_b.jsonl",
        key_output=output / "private_key.json",
        manifest_output=output / "packet_manifest.json",
    )
    row = json.loads((output / "reviewer_a.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert set(row) == {
        "review_id", "repository_url", "pre_fix_revision", "fixed_revision",
        "source_tree_urls", "regression_test_targets", "review_task",
    }
    assert row["source_tree_urls"]["pre_fix"].endswith(row["pre_fix_revision"])
    assert row["source_tree_urls"]["fixed"].endswith(row["fixed_revision"])
    assert row["review_task"]["identify_actual_root_cause_from_source"] is True
    assert row["review_task"]["do_not_open_public_pr_body_or_reproduction_logs_before_initial_review_locked"] is True
    assert "root_cause" not in row
    assert "ccdg" not in row
    assert "case_id" not in row
    assert "source_url" not in row
    assert "reproduction_evidence_url" not in row
    assert "observed_failure_signal" not in row
