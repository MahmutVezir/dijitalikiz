import hashlib
import json
from pathlib import Path

from scripts.validate_calibration_case_pool import audit_case_pool


ROOT = Path(__file__).resolve().parents[1]
CASE_IDS = [
    "commons-compress-github-pr-770-tar-pax-header-memory-bound",
    "commons-compress-github-pr-803-empty-framed-stream-recursion",
    "commons-collections-github-pr-694-passive-expiring-map-synchronized-views",
    "commons-collections-github-pr-731-transformed-multivalued-map-null-transformer",
    "commons-lang-github-pr-1783-methodutils-nonpublic-class-accessible-method",
    "commons-codec-github-pr-443-git-identifiers-utf8-tree-order",
    "commons-lang-github-pr-1808-randomstringutils-tilde-exclusive-upper-bound",
]


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _complete_fixture(root: Path):
    shutil_schema = ROOT / "schemas" / "research_case.schema.json"
    _write_json(
        root / "schemas" / "research_case.schema.json",
        json.loads(shutil_schema.read_text(encoding="utf-8")),
    )
    _write_json(root / "data" / "pilot" / "pilot_manifest.json", {"cases": []})
    _write_json(root / "data" / "benchmark" / "benchmark_manifest.json", {"case_ids": []})

    case_id = "independent-calibration-case-1"
    fix = "a" * 40
    before = "b" * 40
    record = {
        "case_id": case_id,
        "software_twin_snapshot": {
            "repository_url": "https://github.com/example/project",
            "snapshot_revision": before,
            "regression_test": "ExampleRegressionTest#failsOnPreFixRevision",
            "observed_failure_signal": "The regression assertion failed on the pinned snapshot revision.",
        },
        "source": "Independent test fixture",
        "source_url": "https://example.org/pr/1",
        "publication_date": "2026-01-01",
        "technology": "Example runtime",
        "error_description": "A documented operation exhibits a repeatable defect at the boundary.",
        "i_base": [
            "The operation receives a value from a caller-facing method.",
            "A helper determines whether the boundary value is accepted.",
        ],
        "ccdg": [
            {
                "source": "caller-facing method",
                "target": "boundary helper",
                "relation": "delegates_validation",
                "details": "The method relies on the helper's boundary semantics.",
            }
        ],
        "ground_truth": {
            "component": "boundary helper",
            "entity": "inclusive range endpoint",
            "operation": "validate endpoint",
            "root_cause": "missing_return_value_validation",
            "required_relations": ["caller-facing method", "boundary helper"],
        },
        "split": "candidates",
        "provenance": {"fix_commit": fix, "pre_fix_revision": before},
    }
    record_path = root / "data" / "calibration" / "cases" / f"{case_id}.json"
    _write_json(record_path, record)

    manifest = {
        "schema_version": "1.0",
        "manifest_version": "test",
        "status": "frozen",
        "model_inference_permitted": True,
        "rules": {"minimum_calibration_case_count": 1},
        "candidates": [{
            "case_id": case_id,
            "case_record_path": f"data/calibration/cases/{case_id}.json",
            "source_url": "https://example.org/pr/1",
            "repository_url": "https://github.com/example/project",
            "regression_test_targets": ["ExampleRegressionTest#failsOnPreFixRevision"],
            "fix_revision": fix,
            "pre_fix_revision": before,
            "reproduction_status": "independent_pre_fix_failure_and_fixed_revision_pass",
            "reproduction_evidence_url": "https://example.org/actions/1",
            "ground_truth_adjudication_status": "independently_adjudicated",
            "inference_allowed": True,
        }],
        "selection_freeze": {
            "frozen": True,
            "date_utc": "2026-10-10T00:00:00Z",
            "eligible_case_ids": [case_id],
        },
    }
    audit_path = root / "data" / "calibration" / "case_ground_truth_review_audit.json"
    audit = {
        "protocol_version": "case-ground-truth-review-v1",
        "status": "adjudicated",
        "frozen": True,
        "review_packet_manifest_sha256": "c" * 64,
        "reviewers": [
            {
                "reviewer_id": "reviewer-a",
                "independent_review_attestation": True,
                "source_revision_review_attestation": True,
                "reviewed_packet_sha256": "a" * 64,
                "response_sha256": "b" * 64,
            },
            {
                "reviewer_id": "reviewer-b",
                "independent_review_attestation": True,
                "source_revision_review_attestation": True,
                "reviewed_packet_sha256": "d" * 64,
                "response_sha256": "e" * 64,
            },
        ],
        "adjudicator": {
            "reviewer_id": "adjudicator-c",
            "source_evidence_reviewed": True,
            "completed_at_utc": "2026-10-10T00:00:00Z",
        },
        "case_decisions": [
            {
                "case_id": case_id,
                "pre_fix_revision": before,
                "fixed_revision": fix,
                "review_a_decision": "keep",
                "review_b_decision": "keep",
                "final_decision": "keep_for_scoring_calibration",
                "root_cause_adjudicated": True,
                "dependency_edges_adjudicated": True,
                "single_coherent_defect": True,
                "disagreement_resolved": True,
                "ccdg_suitability": "moderate",
                "rationale": "Both revisions and the test support the same bounded root cause and dependency path.",
                "evidence_urls": [
                    "https://github.com/example/project/blob/" + before + "/src/A.java",
                    "https://github.com/example/project/blob/" + fix + "/src/A.java",
                ],
            }
        ],
    }
    _write_json(audit_path, audit)
    manifest["review_gate"] = {
        "status": "adjudicated",
        "frozen": True,
        "audit_path": "data/calibration/case_ground_truth_review_audit.json",
        "audit_sha256": hashlib.sha256(audit_path.read_bytes()).hexdigest(),
    }

    manifest_path = root / "data" / "calibration" / "case_pool_manifest.json"
    _write_json(manifest_path, manifest)
    return manifest_path, case_id


def test_live_calibration_pool_is_blocked_until_reproduction_and_adjudication():
    report = audit_case_pool(manifest_path=ROOT / "data" / "calibration" / "case_pool_manifest.json")
    assert report["status"] == "blocked"
    assert report["model_inference_permitted"] is False
    assert report["candidate_count"] == 7
    assert report["selected_count"] == 0
    assert "case_pool_manifest_not_frozen" in report["issues"]
    assert "case_pool_manifest_model_inference_not_permitted" in report["issues"]


def test_all_candidate_case_records_validate_without_ground_truth_label_leakage():
    report = audit_case_pool(manifest_path=ROOT / "data" / "calibration" / "case_pool_manifest.json")
    assert report["candidate_count"] == 7
    assert not any("case_record_id_mismatch" in issue for issue in report["issues"])
    assert not any("research_case_schema_error" in issue for issue in report["issues"])
    assert not any("ground_truth_root_cause_label_leaked_into_context" in issue for issue in report["issues"])

    manifest = json.loads((ROOT / "data" / "calibration" / "case_pool_manifest.json").read_text(encoding="utf-8"))
    assert manifest["model_inference_permitted"] is False
    assert manifest["selection_freeze"]["frozen"] is False
    assert manifest["selection_freeze"]["eligible_case_ids"] == []
    for candidate in manifest["candidates"]:
        case_path = ROOT / candidate["case_record_path"]
        record = json.loads(case_path.read_text(encoding="utf-8"))
        snapshot = record.get("software_twin_snapshot")
        assert isinstance(snapshot, dict), candidate["case_id"]
        assert snapshot["repository_url"] == candidate["repository_url"]
        assert snapshot["snapshot_revision"] == candidate["pre_fix_revision"]
        assert snapshot["regression_test"] in candidate["regression_test_targets"]
        assert len(snapshot["observed_failure_signal"].strip()) >= 15
        assert record["provenance"]["fix_commit"] == candidate["fix_revision"]
        assert record["provenance"]["pre_fix_revision"] == candidate["pre_fix_revision"]
        assert record["provenance"]["reproduction_status"] == candidate["reproduction_status"]
        assert record["provenance"]["reproduction_status"] == "independent_pre_fix_failure_and_fixed_revision_pass"
        assert record["provenance"]["ground_truth_adjudication_status"] == "pending_independent_review"
        assert record["provenance"]["role"] == "scoring_calibration_candidate_only"

    by_id = {candidate["case_id"]: candidate for candidate in manifest["candidates"]}
    parallel_case = by_id["commons-compress-github-pr-803-empty-framed-stream-recursion"]
    assert parallel_case["ccdg_suitability"] == "weak_for_single_cross_component_chain_parallel_decoder_paths"
    assert parallel_case["role"] == "calibration_only_parallel_decoder_paths"
    weak_control = by_id["commons-lang-github-pr-1808-randomstringutils-tilde-exclusive-upper-bound"]
    assert weak_control["ccdg_suitability"] == "weak_single_component_boundary_control"

def test_qualified_and_frozen_case_pool_can_pass_gate(tmp_path):
    manifest_path, _ = _complete_fixture(tmp_path)
    report = audit_case_pool(
        manifest_path=manifest_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )
    assert report["status"] == "pass"
    assert report["model_inference_permitted"] is True
    assert report["selected_count"] == 1


def test_case_pool_gate_rejects_historical_case_overlap(tmp_path):
    manifest_path, case_id = _complete_fixture(tmp_path)
    _write_json(tmp_path / "data" / "benchmark" / "benchmark_manifest.json", {"case_ids": [case_id]})
    report = audit_case_pool(
        manifest_path=manifest_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )
    assert report["status"] == "blocked"
    assert report["model_inference_permitted"] is False
    assert f"{case_id}_overlaps_frozen_historical_cases" in report["issues"]


def test_case_pool_gate_rejects_missing_pre_fix_reproduction(tmp_path):
    manifest_path, case_id = _complete_fixture(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["candidates"][0]["reproduction_status"] = "pending"
    _write_json(manifest_path, manifest)
    report = audit_case_pool(
        manifest_path=manifest_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )
    assert report["status"] == "blocked"
    assert report["model_inference_permitted"] is False
    assert f"{case_id}_independent_red_green_reproduction_not_complete" in report["issues"]


def test_case_pool_gate_rejects_selected_cases_without_review_audit(tmp_path):
    manifest_path, _ = _complete_fixture(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    audit_path = tmp_path / manifest["review_gate"]["audit_path"]
    audit_path.unlink()

    report = audit_case_pool(
        manifest_path=manifest_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )
    assert report["status"] == "blocked"
    assert report["model_inference_permitted"] is False
    assert "missing_case_ground_truth_review_audit" in report["issues"]


def test_case_pool_gate_rejects_tampered_review_audit_hash(tmp_path):
    manifest_path, _ = _complete_fixture(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["review_gate"]["audit_sha256"] = "f" * 64
    _write_json(manifest_path, manifest)

    report = audit_case_pool(
        manifest_path=manifest_path,
        pilot_manifest_path=tmp_path / "data" / "pilot" / "pilot_manifest.json",
        benchmark_manifest_path=tmp_path / "data" / "benchmark" / "benchmark_manifest.json",
    )
    assert report["status"] == "blocked"
    assert report["model_inference_permitted"] is False
    assert "case_ground_truth_review_audit_sha256_mismatch" in report["issues"]
