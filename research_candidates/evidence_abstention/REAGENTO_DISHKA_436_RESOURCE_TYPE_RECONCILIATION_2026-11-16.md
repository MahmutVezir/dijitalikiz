# Reagento/Dishka #436 — dataset resource-type reconciliation

**Dataset instance:** `reagento__dishka-436`  
**Cohort row:** primary rank 2  
**Decision:** treat the source resource as a pull request; retain a discrepancy note for the timestamp register's boolean flag.

## Observed inconsistency

The primary cohort row identifies `reagento/dishka`, number `436`, and timestamp `2025-04-15T22:52:26Z`.

The timestamp reconciliation CSV row records:
- `issue_url=https://github.com/reagento/dishka/pull/436`
- `is_pull_request=false`
- dataset and GitHub API timestamps both `2025-04-15T22:52:26Z`

The `is_pull_request=false` field conflicts with the URL path `/pull/436`.

## Endpoint verification

GitHub API resource checks:
- `GET /repos/reagento/dishka/pulls/436` identifies PR #436, title “Defer scopes processing to handle overriding properly”, created at `2025-04-15T22:52:26Z`.
- `GET /repos/reagento/dishka/issues/436` returns the issue-style representation of that same pull request, with the same title and `created_at`.
- The separate bug report is issue #435, created at `2025-04-14T17:22:16Z`; PR #436 was created at `2025-04-15T22:52:26Z` and later closed issue #435.

## Corrected interpretation

The dataset row is PR-derived, not a standalone issue-derived row. The correct resource type for source provenance and timestamp endpoint matching is `pull_request`, using `/pulls/436`. The dataset timestamp is an exact match to the PR resource timestamp.

The dataset timestamp value is not discrepant with PR #436. It is one day later than the separate bug report issue #435. The `is_pull_request=false` field in the prior reconciliation CSV is a metadata classification error for this row and must not be used to select the endpoint. This is recorded as a field-level correction; the historical CSV is not silently rewritten.

For case acceptance:
- source resource URL: https://github.com/reagento/dishka/pull/436
- source resource type: `pull_request`
- linked defect issue: https://github.com/reagento/dishka/issues/435
- dataset/upstream PR timestamp: exact match.

This correction resolves the resource-type ambiguity for this candidate but does not accept the case or authorize model inference.
