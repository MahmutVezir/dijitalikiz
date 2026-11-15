"""Validate that E1/E2/E3 packets form an immutable, strictly nested evidence set.

This module performs structural and hash checks only. It does not assign or
verify semantic evidence sufficiency, identify a gold cause, or run a model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

from operational_packet_validator import validate_packet

SCHEMA_VERSION = "1.0"
LEVELS = ("E1", "E2", "E3")
PACKET_SET_FIELDS = {
    "schema_version",
    "packet_set_id",
    "packets",
    "packet_set_sha256",
}
PACKET_SET_ID_PATTERN = re.compile(r"^PACKETSET_[A-Z0-9_-]{1,64}$")
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def packet_set_digest(packet_set: Mapping[str, Any]) -> str:
    payload = {
        key: value
        for key, value in packet_set.items()
        if key != "packet_set_sha256"
    }
    return sha256_bytes(canonical_json(payload))


def create_packet_set(
    packet_e1: Mapping[str, Any],
    packet_e2: Mapping[str, Any],
    packet_e3: Mapping[str, Any],
    packet_set_id: str,
) -> dict[str, Any]:
    """Build a hash-bound wrapper; level labels remain outside each inner packet."""
    packet_set: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "packet_set_id": packet_set_id,
        "packets": {
            "E1": dict(packet_e1),
            "E2": dict(packet_e2),
            "E3": dict(packet_e3),
        },
    }
    packet_set["packet_set_sha256"] = packet_set_digest(packet_set)
    report = validate_packet_set(packet_set)
    if report["status"] != "valid":
        raise ValueError(
            "cannot create invalid packet set: " + "; ".join(report["blockers"])
        )
    return packet_set


def _item_map(packet: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item["id"]: item
        for item in packet["evidence_items"]
    }


def validate_packet_set(
    packet_set: Any,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    blockers: list[str] = []
    if not isinstance(packet_set, Mapping):
        return {
            "status": "invalid",
            "blockers": ["Packet set must be a JSON object."],
            "available_evidence_ids_by_level": {},
            "semantic_sufficiency_assessed": False,
            "model_inference_performed": False,
        }

    fields = set(packet_set)
    missing = sorted(PACKET_SET_FIELDS - fields)
    unexpected = sorted(fields - PACKET_SET_FIELDS)
    if missing:
        blockers.append("Required packet-set fields missing: " + ", ".join(missing))
    if unexpected:
        blockers.append("Unexpected packet-set fields: " + ", ".join(unexpected))

    if packet_set.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version must equal '" + SCHEMA_VERSION + "'.")

    packet_set_id = packet_set.get("packet_set_id")
    if (
        not isinstance(packet_set_id, str)
        or PACKET_SET_ID_PATTERN.fullmatch(packet_set_id) is None
    ):
        blockers.append("packet_set_id must be a pseudonymous PACKETSET_ identifier.")

    packets = packet_set.get("packets")
    if not isinstance(packets, Mapping):
        blockers.append("packets must be an object keyed by E1, E2, and E3.")
        packets = {}
    else:
        actual_levels = set(packets)
        if actual_levels != set(LEVELS):
            missing_levels = sorted(set(LEVELS) - actual_levels)
            unexpected_levels = sorted(actual_levels - set(LEVELS))
            if missing_levels:
                blockers.append("Missing evidence levels: " + ", ".join(missing_levels))
            if unexpected_levels:
                blockers.append("Unexpected evidence levels: " + ", ".join(unexpected_levels))

    packet_reports: dict[str, dict[str, Any]] = {}
    packet_values: dict[str, Mapping[str, Any]] = {}
    packet_ids: list[str] = []

    for level in LEVELS:
        packet = packets.get(level)
        if packet is None:
            continue
        report = validate_packet(packet)
        packet_reports[level] = report
        if report.get("status") != "valid":
            blockers.extend(
                level + ": " + blocker
                for blocker in report.get("blockers", ["inner packet is invalid"])
            )
            continue
        packet_values[level] = packet
        packet_id = report.get("packet_id")
        if isinstance(packet_id, str):
            packet_ids.append(packet_id)

    if len(packet_ids) != len(set(packet_ids)):
        blockers.append("Each evidence level must have a distinct packet_id.")

    additions: dict[str, list[str]] = {}
    if all(level in packet_values for level in LEVELS):
        maps = {level: _item_map(packet_values[level]) for level in LEVELS}

        # An item ID must always identify the same immutable evidence item.
        all_ids = set().union(*(set(item_map) for item_map in maps.values()))
        for evidence_id in sorted(all_ids):
            versions = [
                maps[level][evidence_id]
                for level in LEVELS
                if evidence_id in maps[level]
            ]
            if any(item != versions[0] for item in versions[1:]):
                blockers.append(
                    "Evidence item " + evidence_id
                    + " changes across levels; IDs must retain identical content and provenance."
                )

        ids_e1 = set(maps["E1"])
        ids_e2 = set(maps["E2"])
        ids_e3 = set(maps["E3"])

        if not ids_e3.issubset(ids_e2):
            blockers.append("E3 evidence items must be a subset of E2.")
        if not ids_e2.issubset(ids_e1):
            blockers.append("E2 evidence items must be a subset of E1.")
        if ids_e3 == ids_e2:
            blockers.append("E2 must add at least one evidence item beyond E3.")
        if ids_e2 == ids_e1:
            blockers.append("E1 must add at least one evidence item beyond E2.")

        additions = {
            "E2_over_E3": sorted(ids_e2 - ids_e3),
            "E1_over_E2": sorted(ids_e1 - ids_e2),
        }

    computed_hash = None
    try:
        computed_hash = packet_set_digest(packet_set)
    except (TypeError, ValueError):
        blockers.append("Packet set contains values that cannot be canonically serialized.")

    declared_hash = packet_set.get("packet_set_sha256")
    if not isinstance(declared_hash, str) or HASH_PATTERN.fullmatch(declared_hash) is None:
        blockers.append("packet_set_sha256 must be 64 lowercase hexadecimal characters.")
    elif computed_hash is not None and declared_hash != computed_hash:
        blockers.append("packet_set_sha256 does not match canonical packet-set content.")

    if expected_sha256 is not None:
        if not isinstance(expected_sha256, str) or HASH_PATTERN.fullmatch(expected_sha256) is None:
            blockers.append("expected_sha256 must be 64 lowercase hexadecimal characters.")
        elif computed_hash != expected_sha256:
            blockers.append("packet set hash does not match external expected_sha256.")

    ids_by_level = {
        level: packet_reports[level].get("available_evidence_ids", [])
        for level in LEVELS
        if level in packet_reports and packet_reports[level].get("status") == "valid"
    }
    status = "valid" if not blockers else "invalid"
    return {
        "status": status,
        "blockers": blockers,
        "packet_set_id": packet_set_id if isinstance(packet_set_id, str) else None,
        "packet_set_sha256": computed_hash,
        "packet_sha256_by_level": {
            level: packet_reports[level].get("packet_sha256")
            for level in LEVELS
            if level in packet_reports
        },
        "available_evidence_ids_by_level": ids_by_level if status == "valid" else {},
        "additional_evidence_ids": additions if status == "valid" else {},
        "strictly_nested": status == "valid",
        "semantic_sufficiency_assessed": False,
        "gold_root_cause_read": False,
        "model_inference_performed": False,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-set", type=Path, required=True)
    parser.add_argument("--expected-sha256")
    args = parser.parse_args(argv)

    try:
        value = json.loads(args.packet_set.read_text(encoding="utf-8"))
        report = validate_packet_set(value, expected_sha256=args.expected_sha256)
    except (OSError, json.JSONDecodeError) as exc:
        report = {
            "status": "invalid",
            "blockers": [type(exc).__name__ + ": " + str(exc)],
            "available_evidence_ids_by_level": {},
            "semantic_sufficiency_assessed": False,
            "gold_root_cause_read": False,
            "model_inference_performed": False,
        }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "valid" else 2


if __name__ == "__main__":
    sys.exit(main())
