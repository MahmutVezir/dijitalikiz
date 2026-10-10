# Preparing blinded review packets for v2 candidate screening

**Current status:** The source-only red/green check has passed for 11 candidate leads. Independent human review and adjudication are not complete. This process does not authorize inference.

## Generate the packets

From a clean checkout of the PR branch, run:

```bash
python scripts/build_followup_v2_lead_review_packets.py \
  --output-dir /tmp/dijitalikiz-heldout-source-review
```

The default input audit is `data/followup_v2/discovery_screening_audit_run_38054680670.json`. The builder fails closed unless the source-screening audit succeeded, every candidate has pinned 40-character pre-fix/fixed commits, a named regression target, a completed red/green status, a SHA-256 artifact hash, pending human-review status, and no held-out admission flag.

It produces:
- `reviewer_a_packet.jsonl`
- `reviewer_b_packet.jsonl`
- `REVIEWER_INSTRUCTIONS.md`
- `packet_manifest.json`
- `private_key_do_not_share.json`

Both packets have the same opaque review IDs but independently shuffled order. They contain repository/source-tree links at the exact revisions and named regression tests. They omit case IDs, pull-request URL/body/title, prior screening logs, proposed suitability labels, and contamination labels. The private key maps opaque review IDs back to the case IDs and contains private metadata.

## Distribution safeguards

1. Send Reviewer A only `reviewer_a_packet.jsonl` and `REVIEWER_INSTRUCTIONS.md`; send Reviewer B only `reviewer_b_packet.jsonl` and the same instructions.
2. Do not distribute `private_key_do_not_share.json`, the packet manifest's private-key hash, other reviewers' answers, PR discussion links, or red/green artifacts before both reviews are locked.
3. Each reviewer should independently inspect both pinned revisions and corresponding tests, cite line-specific evidence, draw only source-supported component edges, decide whether each record is one coherent defect, assess licensing/provenance and contamination risk, and choose keep/revise/exclude. Lack of a strong cross-component path should lead to exclusion from the CCDG confirmatory pool, not a forced keep.
4. Ask each reviewer to return one JSON object per line, using the exact opaque review IDs. Keep each original response unchanged and store it outside the repository while review is in progress.
5. Only after both independent files are locked may the coordinator open the key, compare disagreements, and prepare a separate adjudication record. A separate adjudicator must resolve disagreements from pinned source and test evidence.

## Evidence interpretation

The run proves regression reproducibility for these candidate revisions, not that the proposed cause or graph is scientifically correct. Public issue/fix history creates a contamination risk; the model's actual training exposure is unknown. These 11 leads remain excluded from confirmatory inference until independent review and separate adjudication have passed. Calibration cases must also remain disjoint from the eventual held-out set.

The prospective plan still targets 61 distinct, independently reviewed cases. Do not count multiple tests, protocol subcomponents, or repeated model generations as independent defects.
