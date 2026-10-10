import json
from pathlib import Path

from scripts.validate_followup_v2_lead_review import validate_review_responses


def _write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def _packet_rows():
    return [
        {"review_id": "REV-0123456789ABCDEF", "repository_url": "https://github.com/example/repo"},
        {"review_id": "REV-FEDCBA9876543210", "repository_url": "https://github.com/example/repo"},
    ]


def _response(review_id: str, reviewer_id: str = "reviewer-a"):
    return {
        "protocol_version": "followup-v2-lead-source-review-1.0",
        "review_id": review_id,
        "reviewer_id": reviewer_id,
        "decision": "keep",
        "root_cause_rationale": "The failure follows from a concrete mismatch between the caller contract and the callee implementation.",
        "components": [
            {
                "component_id": "ExampleCaller",
                "role": "passes the malformed value to the downstream parser",
                "evidence_urls": ["https://github.com/example/repo/blob/1111111111111111111111111111111111111111/src/Caller.java#L10"],
            }
        ],
        "dependency_edges": [
            {
                "source": "ExampleCaller",
                "relation": "passes_value_to",
                "target": "ExampleParser",
                "evidence_urls": ["https://github.com/example/repo/blob/1111111111111111111111111111111111111111/src/Caller.java#L10"],
            }
        ],
        "is_single_coherent_defect": True,
        "ccdg_suitability": "moderate",
        "license_reviewed": True,
        "contamination_risk": "unknown",
        "limitations": "The exact training data exposure of this public defect is not known.",
        "evidence_urls": [
            "https://github.com/example/repo/blob/1111111111111111111111111111111111111111/src/Caller.java#L10",
            "https://github.com/example/repo/blob/2222222222222222222222222222222222222222/src/Caller.java#L10",
        ],
    }


def test_review_response_validator_accepts_complete_blinded_response(tmp_path):
    packet = tmp_path / "packet.jsonl"
    response = tmp_path / "response.jsonl"
    _write_jsonl(packet, _packet_rows())
    _write_jsonl(response, [_response("REV-0123456789ABCDEF"), _response("REV-FEDCBA9876543210")])

    result = validate_review_responses(packet_path=packet, response_path=response)

    assert result["status"] == "pass"
    assert result["expected_response_count"] == 2
    assert result["observed_response_count"] == 2
    assert result["reviewer_id"] == "reviewer-a"
    assert result["issue_count"] == 0


def test_review_response_validator_blocks_missing_and_unknown_ids(tmp_path):
    packet = tmp_path / "packet.jsonl"
    response = tmp_path / "response.jsonl"
    _write_jsonl(packet, _packet_rows())
    _write_jsonl(response, [_response("REV-0000000000000001"), _response("REV-0123456789ABCDEF")])

    result = validate_review_responses(packet_path=packet, response_path=response)

    assert result["status"] == "blocked"
    assert "REV-FEDCBA9876543210" in result["missing_review_ids"]
    assert "REV-0000000000000001" in result["unknown_review_ids"]


def test_review_response_validator_requires_one_reviewer_identity(tmp_path):
    packet = tmp_path / "packet.jsonl"
    response = tmp_path / "response.jsonl"
    _write_jsonl(packet, _packet_rows())
    _write_jsonl(response, [
        _response("REV-0123456789ABCDEF", "reviewer-a"),
        _response("REV-FEDCBA9876543210", "reviewer-b"),
    ])

    result = validate_review_responses(packet_path=packet, response_path=response)

    assert result["status"] == "blocked"
    assert any("one_consistent_reviewer_id" in issue for issue in result["issues"])


def test_review_response_validator_blocks_schema_errors(tmp_path):
    packet = tmp_path / "packet.jsonl"
    response = tmp_path / "response.jsonl"
    _write_jsonl(packet, _packet_rows())
    invalid = _response("REV-0123456789ABCDEF")
    invalid.pop("dependency_edges")
    _write_jsonl(response, [invalid, _response("REV-FEDCBA9876543210")])

    result = validate_review_responses(packet_path=packet, response_path=response)

    assert result["status"] == "blocked"
    assert any("schema_error" in issue for issue in result["issues"])
