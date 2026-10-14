from __future__ import annotations

import argparse
import hashlib
import json
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "calibration" / "case_pool_manifest.json"
DEFAULT_OUTPUT_DIR = Path("/tmp/dijitalikiz-case-ground-truth-review")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read JSON object at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object at {path}")
    return value


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_json(value: Any) -> str:
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    return _sha256_bytes(raw)


def _resolve(root: Path, value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Candidate is missing {label}")
    path = Path(value)
    return path if path.is_absolute() else root / path


def _pack_candidate(candidate: dict[str, Any], record: dict[str, Any], review_id: str) -> dict[str, Any]:
    snapshot = record.get("software_twin_snapshot")
    if not isinstance(snapshot, dict):
        raise ValueError(f"{candidate.get('case_id')}: missing software_twin_snapshot")

    repository_url = str(candidate.get("repository_url", "")).rstrip("/")
    pre_fix_revision = candidate.get("pre_fix_revision")
    fixed_revision = candidate.get("fix_revision")

    # Reduce priming: do not expose the PR body/title, reproduction log, or
    # observed-failure synopsis before initial source annotations are locked.
    # Provisional labels, I_base, CCDG edges, graph suitability, and selection
    # rationale stay in the private key, never in the reviewer packet.
    return {
        "review_id": review_id,
        "repository_url": repository_url,
        "pre_fix_revision": pre_fix_revision,
        "fixed_revision": fixed_revision,
        "source_tree_urls": {
            "pre_fix": f"{repository_url}/tree/{pre_fix_revision}",
            "fixed": f"{repository_url}/tree/{fixed_revision}",
        },
        "regression_test_targets": candidate.get("regression_test_targets"),
        "review_task": {
            "inspect_both_pinned_revisions": True,
            "inspect_source_and_regression_tests_before_issue_discussion": True,
            "do_not_open_public_pr_body_or_reproduction_logs_before_initial_review_locked": True,
            "identify_actual_root_cause_from_source": True,
            "identify_affected_and_interacting_components": True,
            "draw_only_evidence_supported_dependency_edges": True,
            "decide_whether_this_is_one_coherent_defect_case": True,
            "decide_ccdg_suitability": True,
        },
    }


def build_packets(
    *,
    manifest_path: Path = DEFAULT_MANIFEST,
    reviewer_a_output: Path,
    reviewer_b_output: Path,
    key_output: Path,
    manifest_output: Path,
) -> dict[str, Any]:
    manifest_path = manifest_path.resolve()
    root = manifest_path.parents[2] if len(manifest_path.parents) >= 3 else ROOT
    manifest = _read_json(manifest_path)
    candidates = manifest.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("case-pool manifest must contain a non-empty candidates array")

    destinations = {
        "reviewer_a_output": reviewer_a_output.resolve(),
        "reviewer_b_output": reviewer_b_output.resolve(),
        "key_output": key_output.resolve(),
        "manifest_output": manifest_output.resolve(),
    }
    if destinations["reviewer_a_output"] == destinations["reviewer_b_output"]:
        raise ValueError("Reviewer A and B packet paths must be different")
    if destinations["key_output"] in (destinations["reviewer_a_output"], destinations["reviewer_b_output"]):
        raise ValueError("Private key must not overwrite a reviewer packet")

    # Private key and raw annotations must stay outside version control.
    for field in ("key_output", "reviewer_a_output", "reviewer_b_output"):
        try:
            destinations[field].relative_to(ROOT.resolve())
        except ValueError:
            continue
        raise ValueError(f"{field} must be outside the repository; choose a /tmp or private local path")

    rows_by_id: dict[str, dict[str, Any]] = {}
    mapping: dict[str, dict[str, Any]] = {}
    seen_case_ids: set[str] = set()
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ValueError("Each candidate must be a JSON object")
        case_id = candidate.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip() or case_id in seen_case_ids:
            raise ValueError(f"Missing or duplicate candidate case_id: {case_id!r}")
        seen_case_ids.add(case_id)

        record_path = _resolve(root, candidate.get("case_record_path"), f"case_record_path for {case_id}")
        record = _read_json(record_path)
        if record.get("case_id") != case_id:
            raise ValueError(f"{case_id}: case record ID mismatch")
        if record.get("source_url") != candidate.get("source_url"):
            raise ValueError(f"{case_id}: source URL mismatch")
        if record.get("provenance", {}).get("pre_fix_revision") != candidate.get("pre_fix_revision"):
            raise ValueError(f"{case_id}: pre-fix revision mismatch")
        if record.get("provenance", {}).get("fix_commit") != candidate.get("fix_revision"):
            raise ValueError(f"{case_id}: fixed revision mismatch")

        review_id = "REV-" + secrets.token_hex(8).upper()
        while review_id in rows_by_id:
            review_id = "REV-" + secrets.token_hex(8).upper()
        row = _pack_candidate(candidate, record, review_id)
        rows_by_id[review_id] = row
        mapping[review_id] = {
            "case_id": case_id,
            "case_record_sha256": _sha256_bytes(record_path.read_bytes()),
            "ground_truth_sha256": _sha256_json(record.get("ground_truth")),
            "ccdg_sha256": _sha256_json(record.get("ccdg")),
        }

    order_a = list(rows_by_id.values())
    order_b = list(rows_by_id.values())
    secrets.SystemRandom().shuffle(order_a)
    secrets.SystemRandom().shuffle(order_b)
    reviewer_a_bytes = b"".join(
        (json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        for row in order_a
    )
    reviewer_b_bytes = b"".join(
        (json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        for row in order_b
    )

    key = {
        "key_version": "case-ground-truth-review-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_sha256": _sha256_bytes(manifest_path.read_bytes()),
        "mapping": mapping,
        "warning": "PRIVATE. Do not commit or give to reviewers. Use only after both independent review files are locked.",
    }
    packet_manifest = {
        "status": "packets_created_review_pending",
        "case_count": len(rows_by_id),
        "reviewer_a_packet_sha256": _sha256_bytes(reviewer_a_bytes),
        "reviewer_b_packet_sha256": _sha256_bytes(reviewer_b_bytes),
        "manifest_sha256": key["manifest_sha256"],
        "key_sha256": _sha256_bytes((json.dumps(key, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")),
        "reviewer_packets_contain_provisional_ground_truth": False,
        "human_review_completed": False,
    }

    for field in ("reviewer_a_output", "reviewer_b_output", "key_output", "manifest_output"):
        destinations[field].parent.mkdir(parents=True, exist_ok=True)
    destinations["reviewer_a_output"].write_bytes(reviewer_a_bytes)
    destinations["reviewer_b_output"].write_bytes(reviewer_b_bytes)
    destinations["key_output"].write_text(
        json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    destinations["manifest_output"].write_text(
        json.dumps(packet_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    guide = destinations["manifest_output"].parent / "REVIEWER_INSTRUCTIONS.md"
    guide.write_text(
        "# Bağımsız kaynak-kök neden ve CCDG incelemesi\n\n"
        "Bu paketler model promptu değildir. Her değerlendirici kendi paketini bağımsız incelemeli; özel eşleştirme anahtarını ve diğer değerlendiricinin yanıtlarını görmemelidir.\n\n"
        "Her `review_id` için kaynak bağlantısını, tam pre-fix sürümünü, düzeltilmiş sürümü ve listelenen regresyon testlerini inceleyin. Ayrı bir JSONL yanıtında şu alanları doldurun: "
        "`review_id`, `reviewer_id`, `decision` (keep, revise veya exclude), `root_cause_rationale`, `components`, "
        "`dependency_edges` (source, relation, target, evidence_urls), `is_single_coherent_defect` (boolean), "
        "`ccdg_suitability` (strong, moderate, weak veya ineligible), `contamination_risk` (low, medium, high veya unknown), "
        "`evidence_urls` (mümkünse en az iki sürüme bağlı bağlantı) ve `limitations`.\n\n"
        "İlk kararınızı kilitlemeden public PR açıklamasını/tartışmasını veya önceden toplanmış hata günlüğünü açmayın; paket bu bağlantıları kasıtlı olarak içermez. Önce yalnızca sabitlenmiş iki sürümdeki kaynak kodu ve regresyon testlerini inceleyin. PR başlığından veya hata sinyalinden teşhisi kopyalamayın. Her iki sabit sürümdeki davranışı doğrulayın ve kesin kaynak/test konumlarına bağlantı verin. "
        "Kanıt yetersizse ya da kayıt birden fazla paralel mekanizmayı birleştiriyorsa `revise` veya `exclude` seçip gerekçesini yazın. "
        "İki değerlendirici de yanıtlarını bitirip kilitlemeden dosyaları paylaşmayın. Koordinatör özel anahtarı ancak iki yanıt kilitlendikten sonra kullanabilir.\n",
        encoding="utf-8",
    )
    return {
        **packet_manifest,
        "outputs": {key_name: str(value) for key_name, value in destinations.items()},
        "instruction_file": str(guide),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build blinded packets for independent case ground-truth/CCDG review.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--reviewer-a-output", type=Path)
    parser.add_argument("--reviewer-b-output", type=Path)
    parser.add_argument("--key-output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    args = parser.parse_args()

    output_dir = args.output_dir
    report = build_packets(
        manifest_path=args.manifest,
        reviewer_a_output=args.reviewer_a_output or output_dir / "reviewer_a_packet.jsonl",
        reviewer_b_output=args.reviewer_b_output or output_dir / "reviewer_b_packet.jsonl",
        key_output=args.key_output or output_dir / "review_key_private.json",
        manifest_output=args.manifest_output or output_dir / "packet_manifest.json",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
