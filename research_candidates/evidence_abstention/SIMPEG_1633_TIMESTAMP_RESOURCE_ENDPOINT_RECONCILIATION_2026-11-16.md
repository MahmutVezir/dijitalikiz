# simpeg/simpeg#1633 timestamp resource-endpoint reconciliation — 16 November 2026

**Disposition: the one-second difference is reconciled at the GitHub resource-endpoint level. This does not accept the case or close the broader dataset provenance gate.**

## Exact source identity

- Dataset instance: `simpeg__simpeg-1633`
- Repository: `simpeg/simpeg`
- Pull request: [#1633](https://github.com/simpeg/simpeg/pull/1633)
- Dataset timestamp in the pinned reconciliation register: `2025-03-20T23:46:00Z`

## Direct GitHub REST resource comparison

Two distinct public GitHub REST resources were queried for the same pull request:

| Resource | returned created_at |
|---|---|
| `GET /repos/simpeg/simpeg/pulls/1633` | `2025-03-20T23:46:00Z` |
| `GET /repos/simpeg/simpeg/issues/1633` | `2025-03-20T23:46:01Z` |

Both responses identify the same PR URL and report the same `updated_at` value (`2025-04-22T22:47:16Z`). The dataset value matches the pull-request resource, while the earlier one-second discrepancy came from comparing it with the issue resource representation.

## Interpretation and rule

This is sufficient to reconcile the apparent one-second discrepancy for this PR when the source is compared using the resource type represented by the dataset row. It is not evidence that the dataset rounded, truncated, or converted timestamps.

Apply this uniform rule to the cohort:
1. For a PR-derived task, compare `created_at` with GitHub's `/pulls/{number}` resource.
2. For an issue-derived task, compare with GitHub's `/issues/{number}` resource.
3. Record the resource type and exact endpoint in the case's timestamp evidence.
4. If the resource type cannot be established, keep the timestamp check blocked.

The public filtered-dataset reproduction script shown in the dataset card loads the Nebius dataset, filters rows, and rewrites `image_name`; it contains no explicit `created_at` transformation. That supports not attributing this one-second difference to a conversion step.

## Remaining limitations

The connector exposed the response fields/body but did not provide response headers, request IDs, or a byte-authenticated HTTP capture. Do not claim raw-response cryptographic authentication. The broader dataset-validation gate remains OPEN for provenance and source-code license review.

This endpoint reconciliation does not establish defect correctness, exact-base license eligibility, technical reproduction, independence, evidence-tier validity, or case acceptance. Accepted case count remains unchanged; model inference remains unauthorized.
