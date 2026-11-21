# Dishka #435 — post-run resource timestamp correction

**Prepared:** 2026-11-16  
**Candidate:** `reagento__dishka-436`  
**Supersedes the inaccurate sentence in:** `REAGENTO_DISHKA_436_RESOURCE_TYPE_RECONCILIATION_2026-11-16.md`  
**Does not modify:** immutable GitHub Actions run `43881610067` or artifact `14231689140`.

## Authoritative resource timestamps

These are separate GitHub resources:

| Resource | Created at (UTC) | Role |
|---|---|---|
| Issue #435 | `2025-04-14T17:22:16Z` | defect narrative and reported behavior |
| PR #436 | `2025-04-15T22:52:26Z` | dataset-linked code-fix task |
| Dataset instance `reagento__dishka-436` | `2025-04-15T22:52:26Z` | PR-derived row; exact timestamp match to PR #436 |

The prior resource-reconciliation note contains the incorrect sentence: “The separate bug report is issue #435, created at the same timestamp and explicitly closed by PR #436.” The phrase “created at the same timestamp” is false. Issue #435 was created on 14 April; PR #436 was created on 15 April. PR #436 later merged on 24 April and closed issue #435.

## Corrected source-snapshot hashes

- Corrected issue #435 snapshot:
  - Research repository path: `research_candidates/evidence_abstention/reproduction/dishka_issue_435/issue_435_source_snapshot.json`
  - Content SHA-256: `086ee0aba856f76397da74a704d98cc8a82e40e165739d9cc352b202d103e8f3`
  - Its `created_at` now reads `2025-04-14T17:22:16Z`.
- PR #436 snapshot:
  - Research repository path: `research_candidates/evidence_abstention/reproduction/dishka_issue_435/pull_436_source_snapshot.json`
  - Content SHA-256: `f87785a9189d468e4211ec60aeddf7fdaa1677915fce5dc2c7b3e7a658103d58`
  - Its `created_at` remains `2025-04-15T22:52:26Z`.
- Dataset canonical row:
  - SHA-256: `c548969ec886af21b56c93daae34db1a86b3a10c8dd1473d3d5c886549a9e86d`
  - Dataset `created_at`: `2025-04-15 22:52:26`.
- Dataset Parquet file SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`.

## Immutable historical run note

The original run artifact recorded the old incorrect issue-snapshot hash `62ee31658aca98a51d2ff1505b44f857294f431f169fba1fff2e2a849b96c49f`. The artifact remains unchanged and its ZIP digest remains:

`99c47e28c1707436d7dfa75dcb776f5a0865b2288f1ac16d1baee8d6684c7827`

The incorrect snapshot timestamp and hash are retained as historical audit evidence. The corrected issue snapshot is a later source-provenance amendment only. No source code, environment lock, test selector, dataset row, test log, or Stage 2 outcome was altered.

## Acceptance interpretation

The candidate's dataset row is PR-derived. For dataset provenance, compare its `created_at` to PR #436, not issue #435. Issue #435 remains the separate defect-report source. The resource-type reconciliation CSV's `is_pull_request=false` value for the `/pull/436` URL is also a known metadata classification error; preserve that historical CSV and use the separate correction note.

This addendum corrects the prior timestamp wording and must be cited alongside the older reconciliation document. It does not waive any other acceptance gate or authorize model inference.
