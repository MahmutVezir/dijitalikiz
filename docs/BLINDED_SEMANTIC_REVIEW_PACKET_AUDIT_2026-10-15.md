# Blind semantic review packet audit — 15 October 2026

**Status:** v1.2 packets prepared, **not reviewed**. No human labels or adjudications have been collected. These packets are for post-hoc exploratory re-rating only; they do not change the frozen historical endpoint.

## Source artifact integrity

- Source archive SHA-256: `e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd`.
- Internal artifact manifest: 212/212 files verified by size and SHA-256; no missing, unlisted, size-mismatched, or hash-mismatched files (excluding the self-describing manifest from its own file list).
- Expected and observed source run records: 160/160 unique case-condition-seed identities across 16 independent cases; no pilot case overlap.
- Historical records, prompt hashes, manifests, and primary results were not modified.

## Important correction to v1.1

The original reviewer packets exposed a `reference.root_cause` answer-key object and direct public source URLs / project identifiers. These fields could prime the reviewer and reveal exact case identity. **Do not distribute or use the v1.1 packets.**

| Superseded file | SHA-256 |
|---|---|
| Reviewer A v1.1 | `8db44313000cda343fe552c9900ea5c0e1c88646cbdfbe535ad0417193bdef12` |
| Reviewer B v1.1 | `d99a0fefc36cebc1217ff72974ddc1b96676577ed73b4c2cccd03fb210f34490` |

The first local v1.2 ZIP pair was also regenerated to align the exact deterministic seed strings and private-key schema with the repository builder. Use **only** the current hashes in the replacement table below; do not mix a packet from one generation with a key from another.

| Superseded first v1.2 ZIP | SHA-256 |
|---|---|
| Reviewer A first v1.2 | `4aff16afb54a8ab0d2f00b5ec3963308ba5146bf2930950c375e0058f05b5f4d` |
| Reviewer B first v1.2 | `b345925b94115558dddd6aaa263b8273e59765a9fe9d9f11a2e3b823dea42d50` |

## Replacement v1.2 packets

| Packet | Records | Distinct case references | Unique review IDs | SHA-256 |
|---|---:|---:|---:|---|
| Reviewer A | 160 | 16 | 160 | `0604919587fe8063b294c9ca5848d6a5843b683df68de8b66cbb9894ff61fdb0` |
| Reviewer B | 160 | 16 | 160 | `c247950cdf55be67da4adce934397fc558e168c9f74781b550cc56bb1ced81fb` |

Both ZIPs contain only `README_REVIEWER.md` and `review_packet.jsonl`; no private key is packaged. Reviewer-facing rows omit explicit expected-root-cause/ground-truth fields, source URLs, project identifiers, case IDs, condition/seed metadata, source commits, and prompt/context hashes. Review fields are blank in all 320 rows. The exact archived model-response fields are preserved.

The private coordinator mappings were checked against all 160 source records per reviewer: case-condition-seed identity and raw-output SHA-256 matched 160/160, with zero mismatches. The two packets contain the same underlying response multiset and have stable shared case references, but row order differs in 159/160 positions.

## Limitations and distribution

The packets withhold the canonical answer and source URLs, so reviewers assess against a sanitized reported-problem summary and numbered base facts (`B1`, `B2`, …). **This is evidence-summary-based exploratory scoring, not an independent source-code ground-truth audit.** A separate source-grounded adjudication should occur only after both initial review files are locked. Technical content and response wording may still allow case or treatment inference; perfect blinding is not guaranteed.

Send Reviewer A ZIP only to Reviewer A and Reviewer B ZIP only to Reviewer B. The coordinator key files must remain private, must not be committed or put into either ZIP, and must not be shared until both reviews are locked. Key contents and key hashes are deliberately not published in this document.

## Current state

- Human review decisions collected: **No**.
- Inter-rater agreement / Cohen's kappa: **Not calculable until genuine independent ratings are returned**.
- New v2 inference: prohibited; the existing v2 manifest remains draft and `model_inference_permitted=false`.
- Repository unit tests: not yet validated by GitHub Actions because the latest run failed with `runner_id=0` and no executed steps; do not treat this artifact audit as a passing repository test suite.
