# Dymos #1166 — latest independent reproducer repeat and artifact-integrity verification

Date: 21 November 2026

## Reproduction

- Workflow run: `44903822528`
- Job: `136845091011`
- Conclusion: **success**
- Exact buggy base: `3efd1035c3bf62890034eb9e07de543f3d117867`
- Exact fixed PR head: `0ffc82225d6125dcb5c5b5acfb9be9fd712ef949`

The independent public-API reproducer created a fresh polynomial-control phase using `add_control(val=[5.0, 15.0])`. On the exact buggy base, the promoted control input was `[[1.0], [1.0]]` instead of the requested `[[5.0], [15.0]]`; the defect-specific assertion executed and failed as required. The identical reproducer passed on the exact fixed PR head (`1 passed`).

## Artifact integrity

- Artifact ID: `14707022685`
- GitHub SHA-256: `698e2f6b9d37522fd276f58ce57d85934bb0e8df16cd978284c3e79ef3a346dc`
- Independently downloaded ZIP SHA-256: exact match
- ZIP CRC: **PASS**
- Internal SHA256SUMS: **15/15 files matched**

## Decision boundary

This is a technical reproduction repeat and integrity record only. It does not change the approved G1 or E1/E2/E3 adjudication, the bounded documentary scope acknowledgement, or the candidate's acceptance state.

The proposed case record remains `acceptance_decision=proposed` with `final_acceptance.status=pending`. Dymos #1166 remains outside the accepted registry pending a separate explicit project-lead YES/NO decision. No model loading, inference, fine-tuning, or training is authorized.


## Additional exact-base/fixed-revision repeat — 21 November 2026

A further run on the corrected PR head repeated the same independent issue-level public-API reproducer:
- Workflow run: `44904476319`; job `136847003822` — **success**.
- Buggy-base reproduction executed and failed as expected; the identical reproducer passed on the exact fixed PR head.
- Artifact ID: `14707880070`.
- GitHub SHA-256: `3ab3855505e9fee81a0d04eb59c3b10c65fe9a4397806ea8c8d18f2d10942979`.
- Independently downloaded ZIP SHA-256: exact match; ZIP CRC: **PASS**; internal SHA256SUMS: **15/15 files matched** (16 archive members including the manifest).
- Base output again showed `[[1.0], [1.0]]` instead of requested `[[5.0], [15.0]]`; fixed test result: `1 passed`.

This is an additional technical repeat, not a second case. The case record remains strictly schema-conformant and pending final project-lead acceptance; no registry inclusion or model-execution authorization is inferred.
