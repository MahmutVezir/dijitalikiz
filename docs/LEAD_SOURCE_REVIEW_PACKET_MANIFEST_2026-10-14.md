# Blind source-review packet manifest — 2026-10-14

## Provenance

These reviewer packets were assembled from the strict technical screening audit in
`data/followup_v2/discovery_screening_audit_run_38057613670.json`.

- GitHub blob SHA of source audit: `b39c063bd428b45e5f3db86ea0a046c8a06a5785`
- Audit status: `technical_screening_pass_human_review_pending`
- Technical screening workflow: [run 38057613670](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38057613670)
- Repository no-inference validation: [run 38057613640](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38057613640)
- Candidate count: 12
- Case-source review / separate adjudication: **pending**
- Model inference authorization: **false**

The source audit confirms pinned pre-fix/fixed regression checks passed for technical screening. It does not certify root-cause ground truth, independent suitability, or confirmatory eligibility.

## Separate reviewer packages

The ZIP files are kept outside the repository so that reviewer packets, answers, and coordinator key do not leak into version control.

| File | SHA-256 | Contents |
|---|---|---|
| `reviewer_A_source_review_package.zip` | `c088cf249e5d8122dee0e4fa7e2146a7ea196627ffe18880b9a2ddc1b9d1b632` | Reviewer A's 12-row packet, answer template, instructions |
| `reviewer_B_source_review_package.zip` | `49f0571a25d9f2d27ae8acc36d664c0568680b1edcede5f04f68a403a646f47f` | Reviewer B's same opaque ID set in a different order, answer template, instructions |
| `packet_manifest.json` (local coordinator copy) | `c038f973e3806c5e380f5cef514c634169c5c3d867faef02fe5908d2dd6a0f0c` | Packet and key digest inventory |

Local output folder created on 2026-10-14: `/mnt/data/tubitak_dijitalikiz_source_review_2026-10-14/`.

## Blinding and validation checks

- Both packets contain 12 unique opaque review IDs; both cover the same ID set.
- Reviewer order differs between packets.
- Reviewer packets omit case IDs, public PR URLs, screening-run URLs, provisional suitability/contamination labels, and screening logs.
- The coordinator mapping key is in a separate coordinator-only ZIP and is not included in either reviewer package.
- ZIP structure, ID coverage, and absence of designated case/PR/coordinator fields were checked after creation.
- The initial screen still requires two independent reviewers plus a separate adjudicator. No annotations have been invented and no case has been promoted automatically.

**Distribution rule:** send Reviewer A's ZIP only to Reviewer A and Reviewer B's ZIP only to Reviewer B. Do not share the coordinator key until both reviews are received and locked. These are source-review materials for prospective case selection, not scoring-calibration examples and not proof that any candidate will be included in the confirmatory study.

## Remaining gate sequence

1. Complete and lock two independent source reviews.
2. Adjudicate disagreements with revision-pinned code/test evidence.
3. Exclude cases that do not represent one coherent, defensible cross-component defect.
4. Keep any case used for scoring calibration, prompt development, or adjudication training out of the final held-out sample.
5. Only after a defensible case pool is approved should tokenizer/prompt audits, sample-size rationale, protocol freeze, and any new inference proceed.
