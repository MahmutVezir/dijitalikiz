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

## Public schema documentation checked

The upstream Nebius SWE-rebench V2 dataset card describes `created_at` as an `int64` Unix timestamp in milliseconds ([upstream dataset card](https://huggingface.co/datasets/nebius/SWE-rebench-V2/blob/main/README.md)). The filtered PrimeIntellect dataset card instead declares `created_at` as a string/date field ([filtered dataset card](https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified/blob/main/README.md)). The public documentation inspected does not specify the exact transformation from the upstream millisecond integer to the filtered string representation, nor whether seconds are rounded, truncated, or derived from another source field. The upstream builder repository README identifies the project as a task-building/evaluation repository but does not document this timestamp conversion ([builder repository](https://github.com/SWE-rebench/SWE-rebench-V2)).

This schema difference is a plausible place to investigate, **not proof** that the one-second discrepancy was caused by conversion or precision loss. The exception must remain open until the actual transformation code or a maintainer's authoritative explanation is obtained.

## Disposition

1. Retain the row as `one_second_difference`; do not rewrite either timestamp.
2. Do not infer that the dataset rounded, truncated, or normalized timestamps: that behavior has not been established from the dataset's source-generation specification.
3. Do not automatically accept or reject the candidate on this timestamp alone.
4. Resolve only after documenting the dataset field's timestamp-generation/precision semantics from an authoritative source, or after a predeclared cohort rule explicitly specifies how such differences are handled.
5. Preserve this as a source-level recheck, not as a full raw-response provenance capture.

**Effect on readiness:** none. The timestamp exception remains unresolved, the expanded 113-row register now covers all 96 primary candidates and all 17 declared reserves; 112/113 match the dataset timestamp exactly, and the V2 dataset-validation gate remains OPEN. No case is accepted and no model inference is authorized.
