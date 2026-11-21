# Meltano SDK #3090 — E3/E2/E1 evidence-elimination matrix

**Date:** 21 November 2026  
**Candidate:** meltano/sdk issue #3090 / fix PR #3091  
**Dataset row:** `meltano__sdk-3091`  
**Status:** **SOURCE-AUDITED MATRIX; E2 DIAGNOSTIC ADDED BUT CI RESULT PENDING; PRIOR PROJECT-LEAD GOLD/TIER DECISION RETAINED WITHOUT SILENT AMENDMENT; CASE NOT ACCEPTED**

## 1. Purpose

Apply the strengthened tier-construction criterion used in the PyThaiNLP review:

> E2 must eliminate at least one predeclared plausible alternative, while leaving at least two plausible mechanisms for the defect unresolved.

The existing 21 November project-lead decision approved G1 and E3 ABSTAIN / E2 ABSTAIN / E1 ANSWER under the earlier evidence-tier description. This matrix is a subsequent audit under the stricter criterion. It does not silently amend or overwrite that decision.

**Current finding:** the historical E2 evidence alone does not eliminate any of A1–A3. A new E2 diagnostic test has therefore been added to the pinned independent reproducer to test whether the underlying resolver itself returns incomplete data on a repeated direct lookup. Its exact-environment execution result is pending CI. E2 can be considered methodologically supported only if the diagnostic passes on the exact pinned base environment and returns the same complete target twice.

## 2. Frozen provenance

- Issue: https://github.com/meltano/sdk/issues/3090
- Fix PR: https://github.com/meltano/sdk/pull/3091
- Exact buggy base: `ae326fe394ec15d528ec2f1e396b8bb3dd5e99a2`
- Exact fixed PR head: `9505ff1989b9be4d53b5bc9664b3fe3885879cb1`
- Exact buggy-base `singer_sdk/singerlib/schema.py` blob: `035851fe4c3cb574b8015cf7f44da278cb4f1767`
- Exact fixed-source blob: `7754f835e4b11d13a4778669fb94a68c461b9f40`
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset row: `meltano__sdk-3091`
- Dataset row SHA-256: `318893b8546a4a6b2d8bc75d986a079c818951658fc1293ac59ba05d84682266`
- Frozen selector: `tests/singerlib/test_schema.py::test_resolve_schema_references[resolve_schema_multiple_properties_with_same_reference]`
- Independent reproducer: `research_candidates/evidence_abstention/reproduction/meltano_issue_3090/test_issue_3090.py`

Stage 2 artifact previously re-downloaded and rechecked:
- Run/job/artifact: `44331092872 / 134895968235 / 14440520435`
- ZIP size: 18,363 bytes; outer SHA-256: `b1336169d7b6d8e4e47edbcd920d842ad525c7a4e2df841b998182099bed1bd3`
- Recomputed outer SHA-256 matches the recorded GitHub digest.
- ZIP CRC test: PASS.
- Internal SHA256SUMS: 14/14 entries PASS.
- Base independent public-API reproducer: fails because the second sibling remains `{}`.
- Fixed independent public-API reproducer: passes (1 test).
- Exact frozen selector: fails on buggy base and passes on fixed revision (1 test each).

## 3. Predeclared alternatives

| ID | Alternative mechanism | Distinguishing prediction |
|---|---|---|
| G1 | One mutable `visited_refs` set is shared across sibling JSON Schema branches; after the first sibling resolves a reference, the second sibling is incorrectly stopped by the visited-reference guard. | Direct resolver lookup itself succeeds repeatedly; the failure appears only when sibling traversal reuses the shared visited-state. |
| A1 | Resolver lookup/cache behavior returns incomplete contents on a second lookup of the same reference, independently of sibling traversal. | Two direct lookups of the same reference through one exact-environment `Resolver` object produce a complete first result but an empty/incomplete second result. |
| A2 | Shared referenced-object mutation or aliasing causes a first sibling's resolution to change the target or reference data seen by the second sibling. | Direct repeated lookups may both succeed; the issue may still depend on how returned objects are merged or mutated during sibling expansion. |
| A3 | Schema merge order, pre-existing fields, or mutation of sibling schema dictionaries causes the second property to lose the resolved target. | Direct repeated lookups may both succeed; the sibling traversal may still fail because of merge/mutation behavior unrelated to the visited-reference set. |

These alternatives are not claims of equal probability. They are predeclared diagnostic hypotheses to make the tier's evidential limits explicit.

## 4. E3 → E2 → E1 matrix

| Evidence | E3 | E2 (after diagnostic) | E1 |
|---|---|---|---|
| Issue symptom | First sibling resolves; second identical sibling reference becomes `{}`. | Same issue symptom plus exact pinned base/fixed reproductions. | Same symptom and reproductions. |
| Reporter clue | The reporter says the second ref is “presumably” already visited. Preserve this tentative wording exactly; it is a hypothesis, not source proof. | Same clue remains visible. | Same clue remains visible. |
| A1: resolver's repeated direct lookup fails | Live; issue output alone cannot distinguish. | **To be eliminated only if the new exact-base direct lookup diagnostic returns the full target on both consecutive lookups.** Pending CI result at matrix creation. | The source-level early guard shows the second sibling exits before a second resolver lookup is attempted. |
| A2: shared target mutation/aliasing | Live. | Remains live if the direct lookup diagnostic passes; no sibling target object has been mutated in that diagnostic. | The exact-base control flow identifies the early visited-reference return as the point that produces the empty second sibling, distinguishing it from target-object aliasing as the cause of this issue output. |
| A3: schema merge/pre-existing-field interaction | Live. | Remains live if the direct lookup diagnostic passes; it does not execute schema sibling merging. | The exact-base control flow shows the second sibling returns at the visited-reference guard before resolver lookup or a target merge can occur. |
| G1 | A plausible hypothesis, suggested by the reporter but not established. | Remains one of at least three live explanations if A1 is eliminated. | Directly supported by the exact-base state ownership and early-return path; fixed revision changes state to an immutable tuple scoped to the current recursion path. |

### E2 diagnostic added

The reproducer now contains a second, separate test:

`test_repeated_direct_resolver_lookup_returns_target_each_time`

It loads the exact pinned upstream `schema.py` file in the same workflow environment and constructs the same `referencing` registry/resolver path used by the public API. Without entering the recursive sibling traversal, it calls:

- `resolver.lookup("components#/schemas/ComputeUnit")`
- the same lookup again on the same resolver object.

Both returned `contents` values are asserted to equal `{"type": "number"}`.

The diagnostic is deliberately limited to an observable output; it does not place the resolver's internal implementation or the Meltano `visited_refs` source excerpt in the model-visible E2 packet.

**Expected interpretation:**
- If both direct lookups return the complete target on the exact buggy base, A1 is eliminated for this reference and exact pinned resolver environment.
- A2 and A3 remain possible because this direct lookup test does not execute sibling mutation or schema merge behavior.
- G1 also remains possible. Thus E2 would eliminate one alternative and leave at least two live mechanisms.
- If the diagnostic fails, or if the exact pinned environment cannot be confirmed, do not claim E2 meets the criterion. Reconsider the tier or leave this candidate unclassified under the strengthened protocol.

The new test was committed in the research reproducer, but its workflow result is **pending** at the time this matrix was prepared. Do not describe the diagnostic as passed until CI logs show the exact buggy-base run passed this diagnostic while the separate sibling reproducer failed.

## 5. E1 source-level discrimination

Pinned buggy source:  
https://github.com/meltano/sdk/blob/ae326fe394ec15d528ec2f1e396b8bb3dd5e99a2/singer_sdk/singerlib/schema.py

The exact buggy base shows:

1. Lines 254–271: `_resolve_schema_references` receives and initializes `visited_refs` as a mutable set.
2. Lines 273–278: it removes `$ref` from the child schema, checks whether the reference path is already in `visited_refs`, and immediately returns the now-reference-free schema if present.
3. Lines 280–283: on first encounter, it mutates the same set with `.add(reference_path)`, performs `resolver.lookup`, merges the resolved contents, and recurses with the same set.
4. Lines 285–291: the properties loop passes that same mutable set to each sibling child.

Therefore the first sibling leaves its path in shared mutable state. The second sibling with the identical path is stopped at the visited-reference guard, after its `$ref` has been popped and before another `resolver.lookup` or target-content merge. This predicts exactly why the second property is empty.

Pinned fixed source:  
https://github.com/meltano/sdk/blob/9505ff1989b9be4d53b5bc9664b3fe3885879cb1/singer_sdk/singerlib/schema.py

The fixed revision initializes an empty tuple, creates a new tuple when descending into the current reference, and passes the unchanged ancestor tuple to sibling properties. This preserves recursion-path cycle detection while avoiding sibling-state leakage.

This source-level chain discriminates G1 from A1–A3. Do not expose the fixed implementation or patch in model-visible evidence packets; retain it as hidden technical validation only.

## 6. E3 disclosure and sample-suitability risk

The reporter's issue body says the second reference was “presumably” already visited. This clue is mechanistically close to G1 and must remain visible in the E3 packet. It cannot be removed to manufacture uncertainty.

E3 ABSTAIN is defensible only if the scoring rubric distinguishes a tentative reporter hypothesis from an evidence-supported diagnosis. If the task accepts a plausible root-cause guess based on that wording, E3 may be answerable and the sample's suitability for a primary abstention tier should be reconsidered. The prior project-lead approval is preserved as a historical decision; any changed tier or sample disposition requires a new explicit project-lead decision.

## 7. Methodological and independence boundaries

- The public-API reproducer and frozen dataset selector are two forms of evidence for one issue, not two independent cases.
- Related PR #3009 introduced the earlier circular-reference tracking in the same Meltano repository; it is repository lineage, not a second candidate.
- The project lead's prior pipeline/debug exposure declaration is `none` by direct self-report; it is not independently audited.
- Researcher source exposure is `full`. No blinded adjudication, independent second-rater, or inter-rater reliability claim is made.
- Root repository Apache-2.0, dataset-row Apache-2.0 metadata, dataset card CC-BY-4.0, dependency package metadata and third-party notices remain separate review layers. The exact immutable dataset-card README SHA/bytes and canonical dependency license/notices are still open.
- Bounded research-scope acknowledgement is in principle only, with open verification gates; not legal clearance or redistribution permission.

## 8. Decision and acceptance boundaries

- Historical project-lead technical decision: G1; E3 ABSTAIN, E2 ABSTAIN, E1 ANSWER — approved 2026-11-21.
- This matrix: a stricter post-decision methodological audit; new E2 direct-lookup diagnostic result pending.
- Final case acceptance: **not accepted**.
- Registry inclusion: **false**.
- Model loading, inference, fine-tuning and training: **not performed and not authorized**.
