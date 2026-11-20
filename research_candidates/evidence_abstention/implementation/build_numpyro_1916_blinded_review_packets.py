from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import sys
import zipfile
from pathlib import Path
from typing import Any

from evidence_level_packet_set import validate_packet_set


LEVELS = ("E1", "E2", "E3")
REVIEWERS = ("A", "B")
REVIEWER_README = """# Independent coded evidence review

This bundle contains three coded evidence packets in a reviewer-specific randomized order.

Instructions:
- Review each packet independently. Do not discuss the contents or scores with another reviewer.
- Do not search the web, GitHub, package repositories, or external sources while rating.
- Do not infer that one packet is stronger, weaker, nested, or paired with another. Rate only the visible evidence in the packet currently being reviewed.
- Preserve the evidence wording exactly. Cite only neutral item IDs shown in the packet.
- A stack frame, symptom, call-site, error message, or API name is not automatically a causal explanation. Explain the causal link.
- List all plausible distinct mechanisms. Explain which alternatives are excluded, unresolved, or merely unsupported.
- If you recognize the project, issue, PR, codebase, or source, stop and disclose this on the form. Do not silently continue as a blinded reviewer.
- Record uncertainty and unscorable items. Do not force a definitive cause.
- Return the completed form separately from the bundle. Do not alter packet JSONL bytes.

Source identity may be inferable from technical identifiers in the verbatim excerpts. Perfect source-identity blinding is not claimed. Report any recognition or external lookup on the form.
"""

REVIEW_FORM = """# Coded evidence packet — independent review form

Reviewer code:
Date/time (UTC):
Conflict-of-interest screen completed: YES / NO
Prior access to issue, PR, source, patch, fixed revision or reproduction: NO / YES
Prior access to proposed gold, tier design or advisory notes: NO / YES
Participation in reproduction or packet construction: NO / YES
External search performed: NO / YES
Did you recognize the source or project? NO / POSSIBLY / YES
If YES or POSSIBLY, explain and stop the blinded review.

For each packet code, complete one copy of sections A–G.

## A. Packet code and readability
Packet code:
Can it be interpreted without hidden context? YES / PARTLY / NO
Material ambiguity or missing context:

## B. Free-form causal mechanisms
List each distinct mechanism still consistent with the visible evidence. Do not guess a hidden answer.

| Neutral mechanism code | Explanation in your own words | Neutral item IDs and exact support | Status |
|---|---|---|---|
| M1 | | | PLAUSIBLE / EXCLUDED / UNRESOLVED |
| M2 | | | PLAUSIBLE / EXCLUDED / UNRESOLVED |
| M3 | | | PLAUSIBLE / EXCLUDED / UNRESOLVED |
| M4 | | | PLAUSIBLE / EXCLUDED / UNRESOLVED |

## C. Causal link and alternatives
For every mechanism above:
- Does the packet establish causality or merely show a compatible symptom/call-site?
- Which exact visible item supports the causal link?
- What alternative remains plausible?
- What visible evidence excludes an alternative, if any?

## D. Overall judgment
Choose exactly one:
- One causal mechanism is uniquely supported.
- Multiple distinct mechanisms remain plausible.
- No causal mechanism can be assessed.
- Unscorable.

Number of distinct mechanisms still plausible: 0 / 1 / 2 / 3 / 4+ / CANNOT DETERMINE
Does the packet eliminate at least one plausible alternative? YES / NO / UNCLEAR
Is a definitive root-cause diagnosis justified by this packet alone? YES / NO / UNCLEAR
Rationale:

## E. Smallest additional evidence needed
What observable evidence would discriminate the remaining explanations?

## F. Confidence and exclusion check
Confidence: LOW / MODERATE / HIGH
Any reason this rating should be excluded from blinded adjudication?
Details:

## G. Lock record
I confirm this is my independent first rating: YES / NO
I have not seen another reviewer's score: YES / NO
Reviewer signature/code:
Timestamp:
"""

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_private_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass


def build_review_bundles(packet_set: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    report = validate_packet_set(packet_set)
    if report["status"] != "valid":
        raise ValueError("Packet set is not structurally valid: " + "; ".join(report["blockers"]))
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError("Output directory must be new or empty.")
    output_dir.mkdir(parents=True, exist_ok=True)

    mapping: dict[str, Any] = {
        "schema_version": "0.1-numpyro-1916-private-custodian-map",
        "packet_set_sha256": packet_set["packet_set_sha256"],
        "warning": "PRIVATE CUSTODIAN FILE. Never place this file in a reviewer ZIP, public repository, or shared reviewer folder.",
        "reviewers": {},
    }
    bundle_summaries = {}

    for reviewer in REVIEWERS:
        rows = []
        reviewer_map = []
        for level in LEVELS:
            packet = packet_set["packets"][level]
            packet_code = "PKT-" + secrets.token_hex(8).upper()
            item_ids = list(packet["evidence_items"])
            # Random item order per packet and reviewer. Evidence content bytes are not changed.
            secrets.SystemRandom().shuffle(item_ids)
            reviewer_items = []
            item_map = {}
            for index, item in enumerate(item_ids, start=1):
                neutral_id = "item-" + str(index).zfill(2)
                reviewer_items.append({
                    "item_id": neutral_id,
                    "kind": item["kind"],
                    "content": item["content"],
                })
                item_map[neutral_id] = item["id"]
            rows.append({
                "packet_code": packet_code,
                "items": reviewer_items,
            })
            reviewer_map.append({
                "packet_code": packet_code,
                "hidden_level": level,
                "source_packet_sha256": packet["packet_sha256"],
                "neutral_to_source_item_id": item_map,
            })

        secrets.SystemRandom().shuffle(rows)
        secrets.SystemRandom().shuffle(reviewer_map)
        mapping["reviewers"][reviewer] = reviewer_map

        jsonl = "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
            for row in rows
        )
        bundle_name = "reviewer-" + reviewer + ".zip"
        bundle_path = output_dir / bundle_name
        with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("README_REVIEWER.md", REVIEWER_README)
            archive.writestr("review_packet.jsonl", jsonl)
            archive.writestr("PANEL_B_REVIEW_FORM.md", REVIEW_FORM)
        try:
            bundle_path.chmod(0o600)
        except OSError:
            pass
        bundle_summaries[reviewer] = {
            "bundle": bundle_name,
            "bundle_sha256": sha256_bytes(bundle_path.read_bytes()),
            "packet_count": len(rows),
            "packet_codes": [row["packet_code"] for row in rows],
        }

    mapping_path = output_dir / "CUSTODIAN_MAPPING_PRIVATE.json"
    write_private_json(mapping_path, mapping)
    return {
        "status": "created",
        "reviewer_bundles": bundle_summaries,
        "private_mapping_file": mapping_path.name,
        "private_mapping_sha256": sha256_bytes(mapping_path.read_bytes()),
        "packet_set_sha256": packet_set["packet_set_sha256"],
        "semantic_sufficiency_assessed": False,
        "model_inference_performed": False,
        "warning": "The bundles are not sent or uploaded anywhere. The custodian must deliver them through a restricted channel and maintain an access log.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create reviewer-specific anonymized NumPyro #1916 Panel B ZIPs.")
    parser.add_argument("--packet-set", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        packet_set = json.loads(args.packet_set.read_text(encoding="utf-8"))
        result = build_review_bundles(packet_set, args.output_dir)
    except (OSError, json.JSONDecodeError, ValueError, FileExistsError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
