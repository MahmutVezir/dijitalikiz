# simpeg/simpeg#1633 timestamp exception — independent recheck (15 November 2026)

**Decision: exception remains OPEN. No cohort eligibility decision is made by this note.**

## Source record

A fresh GitHub issue/PR fetch was performed for the upstream pull request:

- Repository: `simpeg/simpeg`
- Pull request: [#1633](https://github.com/simpeg/simpeg/pull/1633)
- Title: `Deprecate components in potential field surveys`
- GitHub state: `closed`
- GitHub `created_at`: **2025-03-20T23:46:01Z**
- GitHub `updated_at`: `2025-04-22T22:47:16Z`
- GitHub `closed_at`: `2025-04-22T22:47:10Z`

The connector returned the above normalized issue fields. This note does **not** claim possession of the unmodified raw GitHub REST response body or its response headers; therefore it is not a cryptographically authenticated raw-payload archive.

## Comparison with the pinned dataset register

The committed V2 timestamp reconciliation part records:

- Dataset `created_at`: `2025-03-20T23:46:00Z`
- Previously recorded GitHub API `created_at`: `2025-03-20T23:46:01Z`
- Difference: **+1 second** (GitHub value later than dataset value)

The fresh fetch independently corroborates the GitHub-side value of `23:46:01Z`. It does not explain why the pinned dataset stores `23:46:00Z`.

## Disposition

1. Retain the row as `one_second_difference`; do not rewrite either timestamp.
2. Do not infer that the dataset rounded, truncated, or normalized timestamps: that behavior has not been established from the dataset's source-generation specification.
3. Do not automatically accept or reject the candidate on this timestamp alone.
4. Resolve only after documenting the dataset field's timestamp-generation/precision semantics from an authoritative source, or after a predeclared cohort rule explicitly specifies how such differences are handled.
5. Preserve this as a source-level recheck, not as a full raw-response provenance capture.

**Effect on readiness:** none. The timestamp exception remains unresolved, the 104-row register remains partial (96 primary plus 8 of 17 declared reserves), and the V2 dataset-validation gate remains OPEN. No case is accepted and no model inference is authorized.
