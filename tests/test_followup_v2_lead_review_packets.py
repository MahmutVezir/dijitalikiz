import json
from pathlib import Path

import pytest

from scripts.build_followup_v2_lead_review_packets import build_packets


def _write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _fixture_audit(path: Path) -> Path:
    candidates = []
    for index in range(4):
        case_id = f"private-lead-{index}"
        candidates.append({
            "case_id": case_id,
            "pull_request_url": f"https://github.com/example/project/pull/{index + 1}",
            "repository_url": "https://github.com/example/project",
            "pre_fix_sha": f"{index + 1:040x}",
            "fixed_sha": f"{index + 11:040x}",
            "regression_tests": [{"target": f"ExampleTest#regression{index}"}],
            "artifact_id": index + 101,
            "artifact_sha256": f"{index + 1:064x}",
            "reproduction_status": "ci_red_green_pass",
            "human_review_status": "pending",
            "heldout_confirmatory_eligible": False,
            "cross_component_suitability": "private provisional label",
            "contamination_risk": "medium_public_source_exposure",
        })
    _write_json(path, {
        "status": "technical_screening_pass",
        "workflow": {
            "conclusion": "success",
            "run_url": "https://github.com/example/project/actions/runs/123",
        },
        "candidates": candidates,
    })
    return path


def test_builder_creates_blinded_packets_and_private_unblinding_key(tmp_path):
    audit = _fixture_audit(tmp_path / "audit.json")
    output = tmp_path / "private-review"
    result = build_packets(
        audit_path=audit,
        reviewer_a_output=output / "reviewer_a_packet.jsonl",
        reviewer_b_output=output / "reviewer_b_packet.jsonl",
        key_output=output / "private_key_do_not_share.json",
        manifest_output=output / "packet_manifest.json",
    )

    packet_a = [json.loads(line) for line in (output / "reviewer_a_packet.jsonl").read_text(encoding="utf-8").splitlines()]
    packet_b = [json.loads(line) for line in (output / "reviewer_b_packet.jsonl").read_text(encoding="utf-8").splitlines()]
    key = json.loads((output / "private_key_do_not_share.json").read_text(encoding="utf-8"))
    serialized_packets = (output / "reviewer_a_packet.jsonl").read_text() + (output / "reviewer_b_packet.jsonl").read_text()

    assert result["status"] == "packets_created_review_pending"
    assert result["candidate_count"] == 4
    assert result["model_inference_authorized"] is False
    assert len(packet_a) == len(packet_b) == 4
    assert {row["review_id"] for row in packet_a} == {row["review_id"] for row in packet_b}
    assert [row["review_id"] for row in packet_a] != [row["review_id"] for row in packet_b]
    assert all("private-lead-" not in serialized_packets for _ in [0])
    assert "pull/1" not in serialized_packets
    assert "private provisional label" not in serialized_packets
    assert "medium_public_source_exposure" not in serialized_packets
    assert "artifact_sha256" not in serialized_packets
    assert all("case_id" not in row for row in packet_a + packet_b)
    assert all("pull_request_url" not in row for row in packet_a + packet_b)
    assert {item["case_id"] for item in key["mapping"].values()} == {f"private-lead-{i}" for i in range(4)}
    assert result["reviewer_a_packet_sha256"]
    assert result["reviewer_b_packet_sha256"]
    assert result["private_key_sha256"]
    assert (output / "REVIEWER_INSTRUCTIONS.md").is_file()


def test_builder_rejects_private_outputs_inside_repository(tmp_path):
    audit = _fixture_audit(tmp_path / "audit.json")
    private_path = Path(__file__).resolve().parents[1] / "data" / "followup_v2" / "_test_private_key_should_not_exist.json"
    with pytest.raises(ValueError, match="outside the repository"):
        build_packets(
            audit_path=audit,
            reviewer_a_output=tmp_path / "reviewer_a.jsonl",
            reviewer_b_output=tmp_path / "reviewer_b.jsonl",
            key_output=private_path,
            manifest_output=tmp_path / "manifest.json",
        )
    assert not private_path.exists()


def test_builder_refuses_audit_that_already_admits_candidate_to_confirmatory_sample(tmp_path):
    audit = json.loads(_fixture_audit(tmp_path / "audit.json").read_text(encoding="utf-8"))
    audit["candidates"][0]["heldout_confirmatory_eligible"] = True
    audit_path = tmp_path / "admitted-audit.json"
    _write_json(audit_path, audit)
    output = tmp_path / "private-review"

    with pytest.raises(ValueError, match="must not already be marked eligible"):
        build_packets(
            audit_path=audit_path,
            reviewer_a_output=output / "a.jsonl",
            reviewer_b_output=output / "b.jsonl",
            key_output=output / "key.json",
            manifest_output=output / "manifest.json",
        )


def test_builder_fails_closed_when_screening_artifact_hash_is_missing(tmp_path):
    audit = json.loads(_fixture_audit(tmp_path / "audit.json").read_text(encoding="utf-8"))
    audit["candidates"][1]["artifact_sha256"] = "not-a-hash"
    audit_path = tmp_path / "bad-audit.json"
    _write_json(audit_path, audit)
    output = tmp_path / "private-review"

    with pytest.raises(ValueError, match="invalid screening artifact SHA-256"):
        build_packets(
            audit_path=audit_path,
            reviewer_a_output=output / "a.jsonl",
            reviewer_b_output=output / "b.jsonl",
            key_output=output / "key.json",
            manifest_output=output / "manifest.json",
        )
