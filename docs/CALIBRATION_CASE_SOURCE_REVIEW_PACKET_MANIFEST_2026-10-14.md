# Calibration-case blind source-review packet manifest — 2026-10-14

## Purpose and source of truth

This packet set is for **source-ground-truth review of the seven cases reserved for scoring calibration**. It is distinct from the 12 prospective held-out-discovery leads reviewed in `LEAD_SOURCE_REVIEW_PACKET_MANIFEST_2026-10-14.md`.

- Authoritative case-pool file: [`data/calibration/case_pool_manifest.json`](../data/calibration/case_pool_manifest.json)
- GitHub blob SHA: `a72c10b2c931a6c31bbc6bd6460ce081f10e2e07`
- Current case-pool status: `screening_pending`
- `model_inference_permitted`: `false`
- Candidates: 7
- Independent source review: pending
- Separate adjudication: pending

Each case has pinned pre-fix and fixed revisions and named regression test targets. The reviewer packets intentionally do not supply the proposed root cause, relation edges, public PR URL, case ID, or preliminary suitability assessment.

## Packet archive hashes

| Local artifact | SHA-256 | Description |
|---|---|---|
| `calibration_source_review_reviewer_A.zip` | `67416cc2496390b9cb77b06b49e6c91a0cfe7b8fa386d209f6284c7a126d92de` | Reviewer A packet, answer template, instructions |
| `calibration_source_review_reviewer_B.zip` | `3d6ef06d6859092ecac252798efa6ec3a2db59797caad072809a5c481cf08ca0` | Same seven opaque review IDs in a different order |
| `packet_manifest.json` (local coordinator copy) | `5f158effe71c390ff781efca90ce0aa54575b1e4020fe925b9365d3a1610779f` | Packet hashes and review status inventory |

Local output folder: `/mnt/data/tubitak_dijitalikiz_calibration_source_review_2026-10-14/`. Reviewer packets, annotations and private mapping key are intentionally **not committed** to the repository.

## Blinding / privacy checks performed

- Seven unique opaque review IDs in each archive.
- Same ID set across reviewers, with different row order.
- Reviewer archives omit case IDs, public PR URLs, proposed root-cause text, proposed graph edges, suitability/contamination labels and screening logs.
- Coordinator mapping key is a separate package, not included in either reviewer ZIP.
- Archive structure and designated blinding constraints were checked after creation.
- No reviewer labels, source adjudications, calibration responses, or model outputs have been fabricated.

## Distribution and gate policy

Send Reviewer A's ZIP only to Reviewer A, and Reviewer B's ZIP only to Reviewer B. Do not share the coordinator key until both independent answer files are locked. A separate adjudicator must resolve disagreements using evidence at the pinned revisions.

These seven cases are reserved for scoring calibration only. They must remain excluded from the new held-out confirmatory sample. A successful red/green reproduction is necessary evidence but is not by itself proof of a correct root cause or a suitable CCDG case. **No calibration inference or new confirmatory inference is authorized by packet creation.**
