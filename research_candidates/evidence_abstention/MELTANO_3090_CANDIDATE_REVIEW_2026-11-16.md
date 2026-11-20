# meltano/sdk issue #3090 — candidate review

**Cohort rank:** 26 of 96 primary candidates  
**Dataset instance:** meltano__sdk-3091 (exact row identity to be authenticated by the workflow)  
**Issue:** https://github.com/meltano/sdk/issues/3090  
**Fix PR:** https://github.com/meltano/sdk/pull/3091  
**Review status:** issue/patch/source contract and minimal direct reproducer prepared; exact dataset row and selector execution pending. Not an accepted case.

## 1. Defect contract

Issue #3090 demonstrates that two sibling properties in one JSON Schema both reference the same component. The first property resolves correctly, but the second becomes an empty object. The exact base implementation carries a mutable visited_refs set through sibling recursion. Once the first property resolves the component, the second sibling is incorrectly treated as a circular reference even though it is not on the current recursion path.

PR #3091 changes the state from a shared mutable set to an immutable tuple representing the current recursion stack. This prevents repeated sibling references from being mistaken for cycles while preserving protection against genuine recursive references.

The independent reproducer loads the exact upstream schema.py source by file path (without importing the full SDK package), calls resolve_schema_references with two sibling references to the same component, and requires both properties to resolve to {type: number}.

## 2. Pinned source identity

- Repository: meltano/sdk
- Buggy base: ae326fe394ec15d528ec2f1e396b8bb3dd5e99a2
- Fixed PR head: 9505ff1989b9be4d53b5bc9664b3fe3885879cb1
- Merge commit: 948bcec790bafebbb571cf3c0d58116a49d6f6aa
- Issue #3090 created: 2025-06-12T01:45:49Z
- PR #3091 created: 2025-06-12T01:47:30Z
- Exact-base root LICENSE Git blob: 564273905d22b60a0deb1155ece4281c0b855cbc
- Exact-base pyproject.toml Git blob: baae3360646db13ca761362cd99724176016031d
- Exact-base schema.py Git blob: 035851fe4c3cb574b8015cf7f44da278cb4f1767
- Fixed schema.py Git blob: 7754f835e4b11d13a4778669fb94a68c461b9f40
- Exact-base license declaration: Apache-2.0.

## 3. Reproduction and dependency scope

The independent reproducer imports only the exact schema.py file via importlib and requires referencing. The dataset regression selector imports the SDK package through the existing deprecated _singerlib shim, so the workflow uses a pinned subset of the exact base package's declared runtime dependencies plus pytest. All installed distribution license metadata is recorded before upstream source tests.

No external services, remote fixtures, or private data are used. This is a narrow test-environment license screen, not blanket legal clearance for every optional Singer SDK extra or redistribution.

## 4. Dataset selector requirement

The workflow authenticates the exact Parquet row meltano__sdk-3091, records its canonical row hash and FAIL_TO_PASS selectors, and applies the exact PR diff to the buggy base. Every selector must fail on the buggy base for the repeated-reference defect and pass on the fixed PR head. A collection/import/dependency failure is not counted as a reproduction.

## 5. Independence and exposure

- The frozen primary cohort contains one meltano/sdk candidate; this repository can contribute at most one accepted case.
- Issue and PR were created on 2025-06-12, after the September 2024 public release of the pinned Qwen2.5-3B-Instruct family. This temporal ordering lowers the likelihood that the exact public issue/patch was present in the released weights, but does not prove the model's full training-data cutoff.
- The student researcher has reviewed the issue and PR during candidate screening; perfect blinding must not be claimed.
- Related issue-family and repository-lineage review remains required.

## 6. Current decision

Issue/patch alignment: strong.  
Independent source reproducer: prepared; workflow pending.  
Dataset FAIL_TO_PASS selectors: pending exact-row authentication and execution.  
Minimal dependency/license inventory: pending workflow evidence and human review.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading/inference authorization: false.

## Superseding Stage 2 addendum — 20 November 2026

The Meltano #3090 reproduction job completed successfully in two recorded candidate-matrix runs. The latest branch repeat is:
- Workflow run: 44331092872; job: 134895968235 — success.
- Artifact: 14440520435; GitHub-reported SHA-256: b1336169d7b6d8e4e47edbcd920d842ad525c7a4e2df841b998182099bed1bd3.
- The independent source reproducer executed against the exact buggy base and failed on the second sibling reference as expected; the same reproducer passed on the exact fixed revision.
- The exact frozen dataset selector was authenticated and failed on the test-only patched buggy base, then passed on the fixed revision.
- The row timestamp was authenticated against the linked PR resource.

The issue and reproducer agree on one mechanism: a mutable visited_refs set is shared between sibling schema-property branches. After resolving the first property's $ref, the second identical $ref is incorrectly treated as a cycle and left as an empty object. PR #3091 changes this to recursion-path state, preserving cycle protection without treating sibling reuse as recursion.

PR #3091 identifies #3009 as the introduction history. Record that relationship in the issue-family/lineage review; it does not create a second sample case. Meltano contributes at most one upstream-project case.

**Current disposition:** Stage 2 technical reproduction PASS; candidate remains not accepted. Project-lead source-aware gold/E1-E2-E3 decision, candidate-specific prior pipeline/debug exposure declaration, bounded source/dependency/dataset license-scope acknowledgement, related-issue/lineage review, complete proposed case record and fail-closed registry validation remain open. The earlier sections saying the exact row/selectors/reproducer were pending are historical and superseded by this addendum.
