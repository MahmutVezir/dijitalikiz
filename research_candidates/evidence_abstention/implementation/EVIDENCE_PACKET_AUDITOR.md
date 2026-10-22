# Evidence packet integrity auditor

This module adds a deterministic, no-model integrity check to the evidence-abstention prototype.

## Packet contract

Each packet contains only `schema_version`, `items`, and `packet_sha256`. Each item contains an ID, kind, visible content, source URI, and SHA-256 of the exact visible content. IDs must be unique. The packet hash is SHA-256 over canonical UTF-8 JSON with sorted keys and compact separators, excluding only the `packet_sha256` field.

The auditor rejects unknown fields and known gold-label/answerability fields such as `gold_root_cause`, `evidence_level`, `fixed_patch`, and `solution`. This is a structural guard, not a complete semantic leakage detector: content still requires human review.

## Commands

Validate a packet:

```bash
python research_candidates/evidence_abstention/implementation/evidence_packet_audit.py path/to/packet.json
```

Validate a packet and response citations together:

```bash
python research_candidates/evidence_abstention/implementation/evidence_packet_audit.py path/to/packet.json --response path/to/response.json --expected-sha256 <frozen-packet-sha256>
```

A diagnosis must cite at least one evidence item, and every cited ID must exist in the validated packet. Hash mismatch, duplicate IDs, missing content/source references, malformed references, or forbidden packet keys fail closed.

## Explicit limitation

The result field `semantic_support_status` is always `not_assessed`. This auditor cannot decide whether a cited log or source excerpt semantically entails a root-cause claim. It must never populate `supported_claim_coverage`, `self_check_conflict`, or `explicit_contradiction` and must never use hidden E1/E2/E3 labels or gold root causes to do so. Those semantic signals remain a separate, not-yet-validated research requirement. The decision layer should abstain when they are unavailable.

The tests use synthetic fixtures only. Passing them does not validate real-world source licensing, evidence sufficiency, model behavior, calibration, or the confirmatory experiment.
