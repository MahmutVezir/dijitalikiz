# GeoFileOps #649 — independence and exposure review

## Independence

- Canonical upstream: `geofileops/geofileops`; GitHub repository metadata reports `fork=false`.
- Current v0.2 accepted registry contains only `reagento/dishka` (`SRV2E-DISHKA_435`) and `CS-SI/eodag` (`SRV2E-EODAG_1530`). Neither is the same upstream project or defect cluster.
- Candidate defect cluster: `geofileops-geofileops-default-destination-layer-fallback-issue-648`.
- One issue, one PR, one frozen dataset row and one upstream repository. The 10 selectors are multiple observations of this one case, not 10 independent cases.
- No related accepted case IDs; one-case-per-upstream-project invariant is preserved.

## Exposure

- Project-lead prior pipeline/debug exposure declaration: `none`.
- Researcher source exposure: `full` — issue #648, PR #649, source diff, exact base/fixed source and Stage 2 artifacts were reviewed. No blinded researcher adjudication or inter-rater reliability is claimed.
- Temporal-exposure acknowledgement: issue/PR created 2025-03-06, approximately 162 days after active pinned model revision 2024-09-25. Issue/PR-specific exposure is chronologically unlikely, but exact training-data cutoff and pre-existing repository-source exposure remain unresolved. Candidate is not described as contamination-free.
- The superseded GPTQ checkpoint is not the active pilot revision; it was replaced before any inference record existed.

## Decision and limitations

The independence and exposure statements are based on the frozen accepted registry, GitHub repository/PR metadata and the project lead's explicit declaration. The temporal qualification is preserved; this review is not a contamination-free certification.