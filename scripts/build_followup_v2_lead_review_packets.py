from __future__ import annotations

import argparse
import hashlib
import json
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIT = ROOT / "data" / "followup_v2" / "discovery_screening_audit_run_38054680670.json"
DEFAULT_OUTPUT_DIR = Path("/tmp/dijitalikiz-heldout-source-review")
SHA40 = re.compile(r"^[0-9a-fA-F]{40}$")
SHA64 = re.compile(r"^[0-9a-fA-F]{64}$")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read JSON object at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object at {path}")
    return value


def _valid_sha256(value: Any) -> bool:
    return isinstance(value, str) and SHA64.fullmatch(value) is not None


def _validate_audit(audit: dict[str, Any]) -> list[dict[str, Any]]:
    if audit.get("status") != "technical_screening_pass":
        raise ValueError("Discovery audit is not marked technical_screening_pass.")
    if audit.get("workflow", {}).get("conclusion") != "success":
        raise ValueError("Source-screening workflow did not complete successfully.")
    candidates = audit.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("Discovery audit must contain a non-empty candidates array.")

    seen: set[str] = set()
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ValueError("Each candidate must be a JSON object.")
        case_id = candidate.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip() or case_id in seen:
            raise ValueError(f"Missing or duplicate case_id: {case_id!r}")
        seen.add(case_id)
        if candidate.get("heldout_confirmatory_eligible") is not False:
            raise ValueError(f"{case_id}: discovery lead must not already be marked eligible.")
        if candidate.get("human_review_status") != "pending":
            raise ValueError(f"{case_id}: this builder expects human review to remain pending.")
        if candidate.get("reproduction_status") not in {"ci_red_green_pass", "red_green_pass"}:
            raise ValueError(f"{case_id}: no completed red/green status.")
        if not _valid_sha256(candidate.get("artifact_sha256")):
            raise ValueError(f"{case_id}: missing or invalid screening artifact SHA-256.")
        if not isinstance(candidate.get("pre_fix_sha"), str) or SHA40.fullmatch(candidate["pre_fix_sha"]) is None:
            raise ValueError(f"{case_id}: invalid pre-fix commit SHA.")
        if not isinstance(candidate.get("fixed_sha"), str) or SHA40.fullmatch(candidate["fixed_sha"]) is None:
            raise ValueError(f"{case_id}: invalid fixed commit SHA.")
        if not isinstance(candidate.get("repository_url"), str) or not candidate["repository_url"].startswith("https://github.com/"):
            raise ValueError(f"{case_id}: repository URL is missing or unsupported.")
        tests = candidate.get("regression_tests")
        if not isinstance(tests, list) or not tests or any(
            not isinstance(row, dict) or not isinstance(row.get("target"), str) or not row["target"].strip()
            for row in tests
        ):
            raise ValueError(f"{case_id}: named regression test targets are missing.")
    return candidates


def _blind_row(candidate: dict[str, Any], review_id: str) -> dict[str, Any]:
    repository_url = candidate["repository_url"].rstrip("/")
    pre_fix = candidate["pre_fix_sha"]
    fixed = candidate["fixed_sha"]
    return {
        "review_id": review_id,
        "repository_url": repository_url,
        "pre_fix_revision": pre_fix,
        "fixed_revision": fixed,
        "source_tree_urls": {
            "pre_fix": f"{repository_url}/tree/{pre_fix}",
            "fixed": f"{repository_url}/tree/{fixed}",
        },
        "regression_test_targets": [row["target"] for row in candidate["regression_tests"]],
        "review_task": {
            "inspect_both_pinned_revisions": True,
            "inspect_tests_before_issue_discussion": True,
            "identify_actual_root_cause_from_source": True,
            "identify_affected_and_interacting_components": True,
            "draw_only_evidence_supported_dependency_edges": True,
            "decide_whether_this_is_one_coherent_defect": True,
            "decide_cross_component_dependency_graph_suitability": True,
            "assess_license_and_provenance": True,
            "assess_contamination_risk_without_claiming_known_training_exposure": True,
            "record_line_specific_evidence_and_limitations": True,
        },
    }


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> bytes:
    raw = b"".join(
        (json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        for row in rows
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return raw


def build_packets(
    *,
    audit_path: Path = DEFAULT_AUDIT,
    reviewer_a_output: Path,
    reviewer_b_output: Path,
    key_output: Path,
    manifest_output: Path,
) -> dict[str, Any]:
    audit_path = audit_path.resolve()
    audit = _read_json(audit_path)
    candidates = _validate_audit(audit)
    root = ROOT.resolve()
    destinations = {
        "reviewer_a_output": reviewer_a_output.resolve(),
        "reviewer_b_output": reviewer_b_output.resolve(),
        "key_output": key_output.resolve(),
        "manifest_output": manifest_output.resolve(),
    }
    if destinations["reviewer_a_output"] == destinations["reviewer_b_output"]:
        raise ValueError("Reviewer A and Reviewer B outputs must be distinct.")
    if len(set(destinations.values())) != len(destinations):
        raise ValueError("All output paths must be distinct.")
    for field in ("reviewer_a_output", "reviewer_b_output", "key_output", "manifest_output"):
        try:
            destinations[field].relative_to(root)
        except ValueError:
            continue
        raise ValueError(f"{field} must be outside the repository; choose a private /tmp or local directory.")

    rows_by_id: dict[str, dict[str, Any]] = {}
    private_mapping: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        review_id = "REV-" + secrets.token_hex(8).upper()
        while review_id in rows_by_id:
            review_id = "REV-" + secrets.token_hex(8).upper()
        rows_by_id[review_id] = _blind_row(candidate, review_id)
        private_mapping[review_id] = {
            "case_id": candidate["case_id"],
            "pull_request_url": candidate.get("pull_request_url"),
            "screening_run_url": audit["workflow"]["run_url"],
            "screening_artifact_id": candidate.get("artifact_id"),
            "screening_artifact_sha256": candidate["artifact_sha256"],
            "preliminary_suitability_private_do_not_share": candidate.get("cross_component_suitability"),
            "contamination_risk_private_do_not_share": candidate.get("contamination_risk"),
        }

    order_a = list(rows_by_id.values())
    order_b = list(rows_by_id.values())
    secrets.SystemRandom().shuffle(order_a)
    secrets.SystemRandom().shuffle(order_b)
    if [row["review_id"] for row in order_a] == [row["review_id"] for row in order_b]:
        order_b.reverse()
    reviewer_a_bytes = _write_jsonl(destinations["reviewer_a_output"], order_a)
    reviewer_b_bytes = _write_jsonl(destinations["reviewer_b_output"], order_b)

    audit_bytes = audit_path.read_bytes()
    private_key = {
        "key_version": "followup-v2-lead-review-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_audit_path": str(audit_path),
        "source_audit_sha256": _sha256_bytes(audit_bytes),
        "warning": "PRIVATE. Never commit this key or share it before both independent reviews are locked.",
        "mapping": private_mapping,
    }
    private_key_bytes = _json_bytes(private_key)
    destinations["key_output"].parent.mkdir(parents=True, exist_ok=True)
    destinations["key_output"].write_bytes(private_key_bytes)

    packet_manifest = {
        "status": "packets_created_review_pending",
        "human_review_completed": False,
        "adjudication_completed": False,
        "model_inference_authorized": False,
        "candidate_count": len(candidates),
        "screening_run_url": audit["workflow"]["run_url"],
        "screening_audit_sha256": _sha256_bytes(audit_bytes),
        "reviewer_a_packet_sha256": _sha256_bytes(reviewer_a_bytes),
        "reviewer_b_packet_sha256": _sha256_bytes(reviewer_b_bytes),
        "private_key_sha256": _sha256_bytes(private_key_bytes),
        "reviewer_packets_omit": [
            "case_id",
            "public pull-request URL/body/title",
            "provisional root-cause/suitability/contamination labels",
            "screening artifacts/logs",
        ],
    }
    destinations["manifest_output"].parent.mkdir(parents=True, exist_ok=True)
    destinations["manifest_output"].write_bytes(_json_bytes(packet_manifest))

    instructions_path = destinations["manifest_output"].parent / "REVIEWER_INSTRUCTIONS.md"
    instructions_path.write_text(
        "# Kör kaynak incelemesi — takip deneyi\n\n"
        "Bu paket ön eleme içindir; hiçbir vaka otomatik olarak doğrulayıcı örnekleme kabul edilmez. "
        "Diğer incelemecinin yanıtını veya özel eşleştirme anahtarını görmeden, yalnızca paket içindeki sabitlenmiş iki kod sürümünü ve ilgili regresyon testlerini inceleyin. "
        "İlk değerlendirmeyi kilitlemeden herkese açık PR açıklamasını, tartışmasını veya önceki CI günlüklerini açmayın.\n\n"
        "Her review_id için ayrı bir JSONL yanıt satırı hazırlayın ve şu alanları doldurun: "
        "review_id, reviewer_id, decision (keep, revise, exclude), root_cause_rationale, "
        "components, dependency_edges (her kenar için source/relation/target/evidence URLs), "
        "is_single_coherent_defect, ccdg_suitability (strong, moderate, weak, ineligible), "
        "license_reviewed, contamination_risk (low, medium, high, unknown), limitations, evidence_urls.\n\n"
        "Her bağımlılık kenarını kaynak kod satırları, dosya yolları ve sürüme bağlı URL'lerle destekleyin. "
        "Public issue anlatımını tek başına kanıt saymayın. Birden fazla ayrı mekanizmayı birleştiren, yalnızca tek bileşen sınır hatası olan veya güçlü kaynak kanıtı olmayan vakaları gerekçeyle revise ya da exclude edin. "
        "Kör ilk değerlendirmeler tamamlanıp kilitlenmeden yanıt dosyalarını birbirinizle paylaşmayın.\n",
        encoding="utf-8",
    )
    return {
        **packet_manifest,
        "reviewer_a_output": str(destinations["reviewer_a_output"]),
        "reviewer_b_output": str(destinations["reviewer_b_output"]),
        "private_key_output": str(destinations["key_output"]),
        "manifest_output": str(destinations["manifest_output"]),
        "instructions_output": str(instructions_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build separately randomized, source-only review packets for prospective follow-up candidates."
    )
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = args.output_dir
    try:
        report = build_packets(
            audit_path=args.audit,
            reviewer_a_output=out / "reviewer_a_packet.jsonl",
            reviewer_b_output=out / "reviewer_b_packet.jsonl",
            key_output=out / "private_key_do_not_share.json",
            manifest_output=out / "packet_manifest.json",
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
