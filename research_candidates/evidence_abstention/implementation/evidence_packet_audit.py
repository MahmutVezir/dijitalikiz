#!/usr/bin/env python3
"""Deterministic evidence-packet and citation integrity checks; no semantic judging."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

PACKET_SCHEMA_VERSION = "1.0"
ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9_-]{0,63}$")
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
PACKET_FIELDS = {"schema_version", "items", "packet_sha256"}
ITEM_FIELDS = {"id", "kind", "content", "source_uri", "content_sha256"}
FORBIDDEN_PACKET_FIELDS = {
    "answerability", "evidence_level", "fixed_commit", "fixed_patch", "gold_label",
    "gold_root_cause", "ground_truth", "hidden_root_cause", "patch", "root_cause",
    "solution", "upstream_fix",
}


@dataclass(frozen=True)
class PacketAudit:
    status: str
    packet_sha256: str | None
    available_evidence_ids: tuple[str, ...]
    errors: tuple[str, ...]
    semantic_support_status: str = "not_assessed"


@dataclass(frozen=True)
class ResponseAudit:
    status: str
    cited_evidence_ids: tuple[str, ...]
    errors: tuple[str, ...]
    semantic_support_status: str = "not_assessed"


def canonical_packet_payload(packet: Mapping[str, Any]) -> bytes:
    payload = {key: value for key, value in packet.items() if key != "packet_sha256"}
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def create_packet(items: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    """Create a canonical packet and its integrity hash from already-curated items."""
    normalized_items = []
    for item in items:
        content = item.get("content")
        if not isinstance(content, str):
            raise ValueError("each item content must be a string")
        normalized_items.append({
            "id": item.get("id"),
            "kind": item.get("kind"),
            "content": content,
            "source_uri": item.get("source_uri"),
            "content_sha256": sha256_bytes(content.encode("utf-8")),
        })
    packet: dict[str, Any] = {
        "schema_version": PACKET_SCHEMA_VERSION,
        "items": normalized_items,
    }
    packet["packet_sha256"] = sha256_bytes(canonical_packet_payload(packet))
    audit = audit_packet(packet)
    if audit.status != "valid":
        raise ValueError("cannot create invalid evidence packet: " + "; ".join(audit.errors))
    return packet


def audit_packet(packet: Any, expected_sha256: str | None = None) -> PacketAudit:
    errors: list[str] = []
    if not isinstance(packet, Mapping):
        return PacketAudit("invalid", None, (), ("packet must be a JSON object",))
    keys = set(packet)
    missing = PACKET_FIELDS - keys
    extra = keys - PACKET_FIELDS
    if missing:
        errors.append("missing packet fields: " + ", ".join(sorted(missing)))
    if extra:
        blocked = extra & FORBIDDEN_PACKET_FIELDS
        if blocked:
            errors.append("forbidden gold/answerability fields: " + ", ".join(sorted(blocked)))
        else:
            errors.append("unexpected packet fields: " + ", ".join(sorted(extra)))
    if packet.get("schema_version") != PACKET_SCHEMA_VERSION:
        errors.append("schema_version must equal " + PACKET_SCHEMA_VERSION)

    items = packet.get("items")
    evidence_ids: list[str] = []
    if not isinstance(items, list) or not items:
        errors.append("items must be a non-empty list")
        items = []
    elif len(items) > 100:
        errors.append("items exceeds the maximum of 100 evidence items")

    seen: set[str] = set()
    for index, item in enumerate(items):
        prefix = "items[" + str(index) + "]"
        if not isinstance(item, Mapping):
            errors.append(prefix + " must be an object")
            continue
        item_keys = set(item)
        if item_keys != ITEM_FIELDS:
            missing_item = ITEM_FIELDS - item_keys
            extra_item = item_keys - ITEM_FIELDS
            if missing_item:
                errors.append(prefix + " missing fields: " + ", ".join(sorted(missing_item)))
            if extra_item:
                blocked = extra_item & FORBIDDEN_PACKET_FIELDS
                if blocked:
                    errors.append(prefix + " contains forbidden fields: " + ", ".join(sorted(blocked)))
                else:
                    errors.append(prefix + " unexpected fields: " + ", ".join(sorted(extra_item)))

        item_id = item.get("id")
        if not isinstance(item_id, str) or not ID_PATTERN.fullmatch(item_id):
            errors.append(prefix + " has an invalid evidence ID")
        elif item_id in seen:
            errors.append(prefix + " duplicates evidence ID " + item_id)
        else:
            seen.add(item_id)
            evidence_ids.append(item_id)

        kind = item.get("kind")
        if not isinstance(kind, str) or not kind.strip() or len(kind) > 64:
            errors.append(prefix + " kind must be a non-empty string of at most 64 characters")
        content = item.get("content")
        if not isinstance(content, str) or not content.strip():
            errors.append(prefix + " content must be a non-empty string")
        elif len(content) > 100_000:
            errors.append(prefix + " content exceeds 100000 characters")
        else:
            content_hash = item.get("content_sha256")
            if not isinstance(content_hash, str) or not HASH_PATTERN.fullmatch(content_hash):
                errors.append(prefix + " content_sha256 must be 64 lowercase hexadecimal characters")
            elif sha256_bytes(content.encode("utf-8")) != content_hash:
                errors.append(prefix + " content_sha256 does not match content")
        source_uri = item.get("source_uri")
        if not isinstance(source_uri, str) or not source_uri.strip():
            errors.append(prefix + " source_uri must be non-empty")

    computed_hash: str | None = None
    try:
        computed_hash = sha256_bytes(canonical_packet_payload(packet))
    except (TypeError, ValueError):
        errors.append("packet contains values that cannot be canonically serialized")

    declared_hash = packet.get("packet_sha256")
    if not isinstance(declared_hash, str) or not HASH_PATTERN.fullmatch(declared_hash):
        errors.append("packet_sha256 must be 64 lowercase hexadecimal characters")
    elif computed_hash is not None and declared_hash != computed_hash:
        errors.append("packet_sha256 does not match canonical packet content")

    if expected_sha256 is not None:
        if not isinstance(expected_sha256, str) or not HASH_PATTERN.fullmatch(expected_sha256):
            errors.append("expected_sha256 must be 64 lowercase hexadecimal characters")
        elif computed_hash != expected_sha256:
            errors.append("packet hash does not match external expected_sha256")

    return PacketAudit(
        status="valid" if not errors else "invalid",
        packet_sha256=computed_hash,
        available_evidence_ids=tuple(evidence_ids),
        errors=tuple(errors),
    )


def audit_response(packet_audit: PacketAudit, response: Any) -> ResponseAudit:
    errors: list[str] = []
    if packet_audit.status != "valid":
        errors.append("evidence packet is not structurally valid")
    if not isinstance(response, Mapping):
        return ResponseAudit("invalid", (), tuple(errors + ["response must be a JSON object"]))
    decision = response.get("decision")
    if not isinstance(decision, str) or decision not in {"diagnose", "abstain"}:
        errors.append("decision must be diagnose or abstain")
    refs = response.get("evidence_refs")
    if not isinstance(refs, list) or any(
        not isinstance(ref, str) or not ID_PATTERN.fullmatch(ref) for ref in refs
    ):
        errors.append("evidence_refs must be a list of valid evidence IDs")
        refs = []
    elif len(refs) != len(set(refs)):
        errors.append("evidence_refs must be unique")
    available = set(packet_audit.available_evidence_ids)
    unknown = sorted(set(refs) - available)
    if unknown:
        errors.append("unknown evidence references: " + ", ".join(unknown))
    if decision == "diagnose" and not refs:
        errors.append("diagnose response must cite at least one evidence item")
    if decision == "abstain" and response.get("root_cause") != "":
        errors.append("abstain response must leave root_cause empty")
    return ResponseAudit(
        status="valid" if not errors else "invalid",
        cited_evidence_ids=tuple(refs),
        errors=tuple(errors),
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path, help="JSON evidence packet")
    parser.add_argument("--response", type=Path, help="optional structured model response JSON")
    parser.add_argument("--expected-sha256", help="expected packet hash from a frozen manifest")
    args = parser.parse_args(argv)

    try:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "invalid", "errors": [str(exc)], "semantic_support_status": "not_assessed"}, indent=2))
        return 2

    packet_result = audit_packet(packet, args.expected_sha256)
    report: dict[str, Any] = {"packet_audit": asdict(packet_result)}
    if args.response is not None:
        try:
            response = json.loads(args.response.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            report["response_audit"] = {"status": "invalid", "errors": [str(exc)], "semantic_support_status": "not_assessed"}
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 2
        report["response_audit"] = asdict(audit_response(packet_result, response))

    print(json.dumps(report, ensure_ascii=False, indent=2))
    response_status = report.get("response_audit", {}).get("status", "valid")
    return 0 if packet_result.status == "valid" and response_status == "valid" else 2


if __name__ == "__main__":
    sys.exit(main())
