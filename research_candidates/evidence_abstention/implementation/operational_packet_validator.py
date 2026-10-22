import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping


HEX64 = re.compile(r"^[0-9a-f]{64}$")
PACKET_ID = re.compile(r"^PACKET_[A-Z0-9_-]{1,64}$")
EVIDENCE_ID = re.compile(r"^[A-Z][A-Z0-9_-]{0,63}$")
EVIDENCE_KINDS = {
    "test_output",
    "stack_trace",
    "source_excerpt",
    "configuration",
    "runtime_log",
    "documentation",
    "other",
}
TOP_LEVEL_KEYS = {"schema_version", "packet_id", "evidence_items", "packet_sha256"}
ITEM_KEYS = {"id", "kind", "content", "content_sha256", "source_snapshot_sha256"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def packet_digest(packet: Mapping[str, Any]) -> str:
    payload = {key: value for key, value in packet.items() if key != "packet_sha256"}
    return sha256_bytes(canonical_json(payload))


def validate_packet(packet: Any) -> dict:
    blockers = []
    available_ids = set()
    if not isinstance(packet, dict):
        return {"status": "invalid", "blockers": ["Packet must be a JSON object."], "available_evidence_ids": []}

    if set(packet) != TOP_LEVEL_KEYS:
        extras = sorted(set(packet) - TOP_LEVEL_KEYS)
        missing = sorted(TOP_LEVEL_KEYS - set(packet))
        if extras:
            blockers.append("Unexpected top-level fields; remove case/gold/condition or unreviewed metadata: " + ", ".join(extras))
        if missing:
            blockers.append("Required top-level fields missing: " + ", ".join(missing))

    if packet.get("schema_version") != "1.0":
        blockers.append("schema_version must equal '1.0'.")
    if not isinstance(packet.get("packet_id"), str) or not PACKET_ID.fullmatch(packet.get("packet_id", "")):
        blockers.append("packet_id must be a pseudonymous PACKET_ identifier.")

    items = packet.get("evidence_items")
    if not isinstance(items, list) or not items:
        blockers.append("evidence_items must be a non-empty list.")
        items = []
    seen = set()
    for index, item in enumerate(items):
        prefix = f"evidence_items[{index}]"
        if not isinstance(item, dict):
            blockers.append(prefix + " must be an object.")
            continue
        if set(item) != ITEM_KEYS:
            blockers.append(prefix + " has missing or unexpected fields.")
            continue
        evidence_id = item.get("id")
        if not isinstance(evidence_id, str) or not EVIDENCE_ID.fullmatch(evidence_id):
            blockers.append(prefix + " has an invalid evidence item ID.")
            continue
        if evidence_id in seen:
            blockers.append("Evidence item IDs must be unique.")
        seen.add(evidence_id)
        kind = item.get("kind")
        if kind not in EVIDENCE_KINDS:
            blockers.append(prefix + " has an unsupported evidence kind.")
        content = item.get("content")
        if not isinstance(content, str) or not content.strip():
            blockers.append(prefix + " content must be a non-empty string.")
        elif item.get("content_sha256") != sha256_bytes(content.encode("utf-8")):
            blockers.append(prefix + " content SHA-256 mismatch.")
        if not isinstance(item.get("source_snapshot_sha256"), str) or not HEX64.fullmatch(item["source_snapshot_sha256"]):
            blockers.append(prefix + " source_snapshot_sha256 is missing or invalid.")
    if seen:
        available_ids = sorted(seen)

    recorded_packet_sha = packet.get("packet_sha256")
    if not isinstance(recorded_packet_sha, str) or not HEX64.fullmatch(recorded_packet_sha):
        blockers.append("packet_sha256 is missing or invalid.")
    elif recorded_packet_sha != packet_digest(packet):
        blockers.append("packet SHA-256 mismatch.")

    return {
        "status": "valid" if not blockers else "invalid",
        "blockers": blockers,
        "packet_id": packet.get("packet_id"),
        "packet_sha256": recorded_packet_sha if isinstance(recorded_packet_sha, str) else None,
        "evidence_item_count": len(items),
        "available_evidence_ids": available_ids if not blockers else [],
        "semantic_support_audit_performed": False,
        "contradiction_audit_performed": False,
        "gold_evidence_label_read": False,
        "model_inference_performed": False,
        "note": "Structural and hash validation only. This validator does not judge causal sufficiency, claim support, contradiction, or root-cause correctness.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate integrity and blinding-safe structure of an evidence packet.")
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        result = validate_packet(packet)
    except (OSError, json.JSONDecodeError) as exc:
        result = {
            "status": "invalid",
            "blockers": [f"{type(exc).__name__}: {exc}"],
            "available_evidence_ids": [],
            "semantic_support_audit_performed": False,
            "contradiction_audit_performed": False,
            "gold_evidence_label_read": False,
            "model_inference_performed": False,
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "valid" else 2


if __name__ == "__main__":
    sys.exit(main())

