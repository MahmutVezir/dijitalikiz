# Black-9 evidence packet review plan — 24 October 2026

Status: draft only; no model-facing evidence packet is frozen and no model inference is authorized.

## Goal

Construct three packets from the pinned buggy source and observed failure only. Do not expose the fixed patch, fixed commit, issue/PR identity, upstream fix title, or gold root-cause statement in model-facing text.

## Planned evidence-level contrasts

- E1 (candidate sufficient): retain the source input, observed parser failure, target mode, generic parser flow and the relevant grammar-selection implementation from the buggy snapshot.
- E2 (candidate partial): retain the same common context, input, error, target mode and generic parser flow, but omit the grammar-selection implementation so at least two mechanisms remain plausible.
- E3 (candidate insufficient): retain only the reported parser error and coarse task context, removing source/control-flow evidence. This should leave multiple materially different causes unresolved.

These are initial construction hypotheses, not accepted evidence labels. The evidence-sufficiency panel must confirm or reject each level before model outputs are generated. Packet edits following review require a new version and new hashes.

## Review controls

1. The root-cause panel may see buggy and fixed source, test and patch information.
2. The evidence-sufficiency panel must not see the fixed patch or sealed gold root-cause notes; it sees only the proposed packets and the scoring rubric.
3. Panel memberships must be disjoint. Preserve each reviewer's initial E1/E2/E3 judgment before adjudication.
4. Each packet is assigned an opaque case alias and stable evidence-item IDs. Packet-level labels are kept outside the model-facing text.
5. This case is publicly available upstream code, so prior model-training exposure cannot be ruled out. Do not claim zero contamination. Even a validated packet and reproduced test pair do not by themselves qualify the case for confirmatory analysis.

## Current state

- Paired buggy-fail/fixed-pass reproduced: yes.
- Report/log/source hash audit passed: yes.
- Independent root-cause review: pending.
- MIT attribution/reuse review: pending.
- Leakage and prior-exposure review: pending.
- E1/E2/E3 panel adjudication: pending.
- Confirmatory registry acceptance: no.
- Model inference: not performed.
