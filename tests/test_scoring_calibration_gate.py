import hashlib
import json
from pathlib import Path

from scripts.build_scoring_calibration_review_packets import build_packets
from scripts.validate_scoring_calibration import audit_calibration


ROOT = Path(__file__).resolve().parents[1]
CHALLENGE_CLASSES = [
    "canonical_correct",
    "correct_paraphrase",
    "wrong_mechanism",
    "negated_correct_phrase",
    "multiple_hypotheses",
    "partial_diagnosis",
    "unscorable_output",
]
LABEL_BY_CLASS = {
    "canonical_correct": "correct",
    "correct_paraphrase": "correct",
    "wrong_mechanism": "incorrect",
    "negated_correct_phrase": "incorrect",
    "multiple_hypotheses": "incorrect",
    "partial_diagnosis": "partially_correct",
    "unscorable_output": "unscorable",
}
MATCHER_BY_CLASS = {
    "canonical_correct": True,
    "correct_paraphrase": False,
    "wrong_mechanism": False,
    "negated_correct_phrase": True,
    "multiple_hypotheses": True,
    "partial_diagnosis": False,
    "unscorable_output": False,
}


def _write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row) + "\n" for row in rows),
        encoding="utf-8",
    )


def _complete_fixture(root: Path):
    (root / "schemas").mkdir(parents=True, exist_ok=True)
    _write_json(
        root / "schemas" / "scoring_calibration_example.schema.json",
        json.loads((ROOT / "schemas" / "scoring_calibration_example.schema.json").read_text(encoding="utf-8")),
    )
    _write_json(root / "data" / "pilot" / "pilot_manifest.json", {"cases": ["pilot-case"]})
    _write_json(root / "data" / "benchmark" / "benchmark_manifest.json", {"case_ids": ["confirmatory-case"]})

    examples = []
    for i, challenge_class in enumerate(CHALLENGE_CLASSES, start=1):
        examples.append({
            "schema_version": "1.0",
            "example_id": f"CAL-{i:03d}",
            "source_case_id": f"independent-case-{i}",
            "source_url": f"https://example.org/issues/{i}",
            "fixed_revision": f"{i:040x}",
            "evidence_urls": [f"https://example.org/issues/{i}", f"https://example.org/commit/{i}"],
            "case_summary": "A documented software defect whose root-cause mechanism is independently supported by issue and fix evidence.",
            "ground_truth_root_cause": f"verified mechanism {i}",
            "ground_truth_rationale": "The issue report, failing test, and fixed revision jointly support this root-cause explanation.",
            "root_cause_aliases": [f"verified mechanism {i}"],
            "response_text": (
                json.dumps({
                    "canonical_correct": {
                        "diagnosed_component": f"Component {i}",
                        "root_cause_class": f"verified mechanism {i}",
                        "affected_entity": f"Entity {i}",
                        "explanation": f"The source evidence supports verified mechanism {i}.",
                    },
                    "correct_paraphrase": {
                        "diagnosed_component": f"Component {i}",
                        "root_cause_class": "boundary branch excludes the required endpoint",
                        "affected_entity": f"Entity {i}",
                        "explanation": "The branch condition violates the endpoint contract.",
                    },
                    "wrong_mechanism": {
                        "diagnosed_component": f"Component {i}",
                        "root_cause_class": "stale cache entry",
                        "affected_entity": f"Entity {i}",
                        "explanation": "The cached result was not invalidated.",
                    },
                    "negated_correct_phrase": {
                        "diagnosed_component": f"Component {i}",
                        "root_cause_class": "unrelated cause",
                        "affected_entity": f"Entity {i}",
                        "explanation": f"The cause is not verified mechanism {i}; the evidence rules it out.",
                    },
                    "multiple_hypotheses": {
                        "diagnosed_component": f"Component {i}",
                        "root_cause_class": "uncertain cause",
                        "affected_entity": f"Entity {i}",
                        "explanation": f"Possible causes include verified mechanism {i} or a resource leak, but the answer does not decide.",
                    },
                    "partial_diagnosis": {
                        "diagnosed_component": f"Component {i}",
                        "root_cause_class": "incorrect public API value",
                        "affected_entity": f"Entity {i}",
                        "explanation": f"The public API returns a wrong value, but the underlying cause is not identified in case {i}.",
                    },
                }[challenge_class], ensure_ascii=False, sort_keys=True)
                if challenge_class != "unscorable_output"
                else "I cannot determine the cause from the available evidence."
            ),
            "response_origin": (
                "independent_model_output" if i in {1, 3, 5, 7}
                else "human_authored_control"
            ),
            "generation_metadata": ({
                "model_id": "calibration/test-model",
                "model_revision": f"{i:040x}",
                "seed": i,
                "prompt_sha256": "a" * 64,
                "raw_output_sha256": "b" * 64,
            } if i in {1, 3, 5, 7} else None),
            "challenge_class": challenge_class,
            "legacy_matcher_accepts": MATCHER_BY_CLASS[challenge_class],
            "is_from_frozen_study_output": False,
        })
    for example in examples:
        if example["response_origin"] == "independent_model_output":
            example["generation_metadata"]["raw_output_sha256"] = hashlib.sha256(
                example["response_text"].encode("utf-8")
            ).hexdigest()
    _write_jsonl(root / "data" / "calibration" / "examples.jsonl", examples)

    packet_a, packet_b, key = build_packets(examples)
    key_path = root / "private" / "review_key_private.json"
    _write_json(key_path, key)

    reviewer_a = []
    reviewer_b = []
    adjudications = []
    for key_row in key["items"]:
        review_id = key_row["review_id"]
        label = LABEL_BY_CLASS[key_row["challenge_class"]]
        common = {
            "review_id": review_id,
            "label": label,
            "rationale": "The cited issue and fix evidence support this independent label decision.",
            "evidence_urls": ["https://example.org/issue", "https://example.org/fix"],
            "condition_blinded": True,
            "challenge_class_blinded": True,
            "matcher_result_blinded": True,
        }
        reviewer_a.append({**common, "reviewer_id": "reviewer-A"})
        reviewer_b.append({**common, "reviewer_id": "reviewer-B"})
        adjudications.append({
            **common,
            "adjudicator_id": "adjudicator-C",
            "disagreement_resolved": True,
        })

    _write_jsonl(root / "data" / "calibration" / "reviewer_a.jsonl", reviewer_a)
    _write_jsonl(root / "data" / "calibration" / "reviewer_b.jsonl", reviewer_b)
    _write_jsonl(root / "data" / "calibration" / "adjudication.jsonl", adjudications)

    manifest = {
        "schema_version": "1.0",
        "status": "adjudicated",
        "frozen": True,
        "minimum_examples_per_challenge_class": 1,
        "minimum_independent_model_output_examples": 4,
        "minimum_independent_model_output_source_cases": 4,
        "minimum_human_authored_or_synthetic_control_examples": 3,
        "minimum_distinct_source_cases": 7,
        "minimum_distinct_cases_per_challenge_class": 1,
        "required_challenge_classes": CHALLENGE_CLASSES,
        "readiness_policy": {
            "minimum_initial_reviewer_exact_agreement": 0.8,
            "minimum_initial_reviewer_cohen_kappa": 0.7,
        },
        "files": {
            "examples": "data/calibration/examples.jsonl",
            "reviewer_a": "data/calibration/reviewer_a.jsonl",
            "reviewer_b": "data/calibration/reviewer_b.jsonl",
            "adjudication": "data/calibration/adjudication.jsonl",
        },
        "freeze_metadata": {
            "frozen_at_utc": "2026-10-10T00:00:00Z",
            "rubric_version": "test-1.0",
            "adjudication_commit": "test-commit",
        },
    }
    manifest_path = root / "data" / "calibration" / "manifest.json"
    _write_json(manifest_path, manifest)
    return manifest_path, key_path


def test_packet_builder_masks_gold_and_matcher_metadata():
    examples = [{
        "example_id": "CAL-001",
        "source_case_id": "independent-case",
        "source_url": "https://example.org/issue",
        "evidence_urls": ["https://example.org/issue"],
        "case_summary": "An independently documented software defect with a stable fix.",
        "ground_truth_root_cause": "verified cause",
        "ground_truth_rationale": "Issue and fix evidence establish the cause.",
        "root_cause_aliases": ["verified cause"],
        "response_text": "Candidate response.",
        "response_origin": "human_authored_control",
        "generation_metadata": None,
        "challenge_class": "correct_paraphrase",
        "legacy_matcher_accepts": False,
        "is_from_frozen_study_output": False,
    }]
    packet_a, packet_b, key = build_packets(examples)
    for packet in (packet_a, packet_b):
        assert len(packet) == 1
        item = packet[0]
        assert "response_text" in item
        assert "response_origin" not in item
        assert "generation_metadata" not in item
        assert "challenge_class" not in item
        assert "legacy_matcher_accepts" not in item
        assert "ground_truth_root_cause" not in item
        assert "source_case_id" not in item
    assert key["key_status"] == "PRIVATE_DO_NOT_SHARE_BEFORE_REVIEWS_LOCKED"
    assert key["items"][0]["challenge_class"] == "correct_paraphrase"


def test_calibration_gate_blocks_when_annotation_files_are_missing(tmp_path):
    manifest_path = tmp_path / "data" / "calibration" / "manifest.json"
    _write_json(manifest_path, {
        "schema_version": "1.0",
        "status": "draft",
        "frozen": False,
        "minimum_examples_per_challenge_class": 4,
        "required_challenge_classes": CHALLENGE_CLASSES,
        "files": {
            "examples": "data/calibration/examples.jsonl",
            "reviewer_a": "data/calibration/reviewer_a.jsonl",
            "reviewer_b": "data/calibration/reviewer_b.jsonl",
            "adjudication": "data/calibration/adjudication.jsonl",
        },
    })
    report = audit_calibration(
        manifest_path=manifest_path,
        key_path=tmp_path / "private" / "missing_key.json",
        pilot_manifest_path=tmp_path / "data" / "pilot" / "missing.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "missing.json",
    )
    assert report["status"] == "blocked"
    assert report["ready_for_new_confirmatory_inference"] is False
    assert report["issue_count"] > 0


def test_complete_fixture_reports_matcher_errors_and_reviewer_agreement(tmp_path):
    manifest_path, key_path = _complete_fixture(tmp_path)
    report = audit_calibration(
        manifest_path=manifest_path,
        key_path=key_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )
    assert report["status"] == "pass"
    assert report["ready_for_new_confirmatory_inference"] is True
    metrics = report["metrics"]
    assert metrics["initial_review_exact_agreement"] == 1.0
    assert metrics["initial_review_cohen_kappa"] == 1.0
    matcher = metrics["matcher_diagnostics"]
    assert matcher["confusion_matrix"] == {
        "true_positive": 1,
        "false_positive": 2,
        "true_negative": 2,
        "false_negative": 1,
    }
    assert matcher["n_unscorable_excluded"] == 1
    assert metrics["response_origin_counts"] == {
        "independent_model_output": 4,
        "human_authored_control": 3,
    }
    by_origin = metrics["matcher_diagnostics_by_response_origin"]
    assert by_origin["independent_model_output"]["n_total"] == 4
    assert by_origin["human_authored_control"]["n_total"] == 3


def test_calibration_gate_rejects_matcher_flag_not_supported_by_aliases(tmp_path):
    manifest_path, key_path = _complete_fixture(tmp_path)
    examples_path = tmp_path / "data" / "calibration" / "examples.jsonl"
    examples = [json.loads(line) for line in examples_path.read_text(encoding="utf-8").splitlines()]
    examples[0]["legacy_matcher_accepts"] = not examples[0]["legacy_matcher_accepts"]
    _write_jsonl(examples_path, examples)
    report = audit_calibration(
        manifest_path=manifest_path,
        key_path=key_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )
    assert report["status"] == "blocked"
    assert any("legacy_matcher_result_mismatch" in issue for issue in report["issues"])



def test_calibration_gate_rejects_raw_output_hash_mismatch(tmp_path):
    manifest_path, key_path = _complete_fixture(tmp_path)
    examples_path = tmp_path / "data" / "calibration" / "examples.jsonl"
    examples = [json.loads(line) for line in examples_path.read_text(encoding="utf-8").splitlines()]
    examples[0]["response_text"] = json.dumps({
        "diagnosed_component": "Component 1",
        "root_cause_class": "verified mechanism 1",
        "affected_entity": "Entity 1",
        "explanation": "Changed response content.",
    }, ensure_ascii=False, sort_keys=True)
    # Deliberately retain the original raw_output_sha256 to simulate a tampered record.
    _write_jsonl(examples_path, examples)
    report = audit_calibration(
        manifest_path=manifest_path,
        key_path=key_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )
    assert report["status"] == "blocked"
    assert any("raw_output_sha256_mismatch" in issue for issue in report["issues"])



def test_calibration_gate_uses_only_root_cause_and_explanation_fields(tmp_path):
    manifest_path, key_path = _complete_fixture(tmp_path)
    examples_path = tmp_path / "data" / "calibration" / "examples.jsonl"
    examples = [json.loads(line) for line in examples_path.read_text(encoding="utf-8").splitlines()]
    # An alias in another structured field must not count; the frozen matcher
    # inspects only root_cause_class plus explanation.
    examples[0]["response_text"] = json.dumps({
        "diagnosed_component": "verified mechanism 1",
        "root_cause_class": "different cause",
        "affected_entity": "verified mechanism 1",
        "explanation": "No alias phrase in the scoring fields.",
    }, ensure_ascii=False, sort_keys=True)
    examples[0]["generation_metadata"]["raw_output_sha256"] = hashlib.sha256(
        examples[0]["response_text"].encode("utf-8")
    ).hexdigest()
    examples[0]["legacy_matcher_accepts"] = False
    _write_jsonl(examples_path, examples)
    report = audit_calibration(
        manifest_path=manifest_path,
        key_path=key_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )
    assert report["status"] == "pass"
    assert report["ready_for_new_confirmatory_inference"] is True



def test_calibration_gate_rejects_overlap_with_frozen_cases(tmp_path):
    manifest_path, key_path = _complete_fixture(tmp_path)
    examples_path = tmp_path / "data" / "calibration" / "examples.jsonl"
    examples = [json.loads(line) for line in examples_path.read_text(encoding="utf-8").splitlines()]
    examples[0]["source_case_id"] = "confirmatory-case"
    _write_jsonl(examples_path, examples)
    report = audit_calibration(
        manifest_path=manifest_path,
        key_path=key_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )
    assert report["status"] == "blocked"
    assert any("overlaps_frozen_case" in issue for issue in report["issues"])


def test_calibration_gate_rejects_blinding_leaks(tmp_path):
    manifest_path, key_path = _complete_fixture(tmp_path)
    reviewer_path = tmp_path / "data" / "calibration" / "reviewer_a.jsonl"
    rows = [json.loads(line) for line in reviewer_path.read_text(encoding="utf-8").splitlines()]
    rows[0]["challenge_class"] = "correct_paraphrase"
    _write_jsonl(reviewer_path, rows)
    report = audit_calibration(
        manifest_path=manifest_path,
        key_path=key_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )
    assert report["status"] == "blocked"
    assert any("leaks_blinding_field_challenge_class" in issue for issue in report["issues"])

def test_calibration_gate_blocks_low_independent_reviewer_agreement(tmp_path):
    manifest_path, key_path = _complete_fixture(tmp_path)
    reviewer_path = tmp_path / "data" / "calibration" / "reviewer_b.jsonl"
    rows = [json.loads(line) for line in reviewer_path.read_text(encoding="utf-8").splitlines()]
    for row in rows:
        row["label"] = "incorrect"
    _write_jsonl(reviewer_path, rows)
    report = audit_calibration(
        manifest_path=manifest_path,
        key_path=key_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )
    assert report["status"] == "blocked"
    assert report["ready_for_new_confirmatory_inference"] is False
    assert any("below_threshold" in issue for issue in report["issues"])



def test_calibration_gate_rejects_manifest_thresholds_below_protocol_floors(tmp_path):
    manifest_path, key_path = _complete_fixture(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    # The fixture has perfect synthetic agreement; lowering both manifest
    # thresholds must not turn that fixture into a valid protocol pass.
    manifest["readiness_policy"]["minimum_initial_reviewer_exact_agreement"] = 0.0
    manifest["readiness_policy"]["minimum_initial_reviewer_cohen_kappa"] = 0.0
    _write_json(manifest_path, manifest)

    report = audit_calibration(
        manifest_path=manifest_path,
        key_path=key_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )

    assert report["status"] == "blocked"
    assert report["ready_for_new_confirmatory_inference"] is False
    assert any(
        "minimum_initial_reviewer_exact_agreement_below_protocol_floor" in issue
        for issue in report["issues"]
    )
    assert any(
        "minimum_initial_reviewer_cohen_kappa_below_protocol_floor" in issue
        for issue in report["issues"]
    )


def test_calibration_gate_rejects_boolean_values_as_reliability_thresholds(tmp_path):
    manifest_path, key_path = _complete_fixture(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["readiness_policy"]["minimum_initial_reviewer_exact_agreement"] = True
    manifest["readiness_policy"]["minimum_initial_reviewer_cohen_kappa"] = False
    _write_json(manifest_path, manifest)

    report = audit_calibration(
        manifest_path=manifest_path,
        key_path=key_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )

    assert report["status"] == "blocked"
    assert report["ready_for_new_confirmatory_inference"] is False
    assert "invalid_minimum_initial_reviewer_exact_agreement" in report["issues"]
    assert "invalid_minimum_initial_reviewer_cohen_kappa" in report["issues"]
