# Meltano SDK #3090 — source-aware gold and evidence-tier proposal

**Status:** ADVISORY PROPOSAL ONLY — not project-lead approved, not a case acceptance decision  
**Prepared:** 2026-11-21  
**Candidate:** meltano/sdk issue #3090 / fix PR #3091  
**Proposed case ID:** SRV2E-MELTANO_3090  
**Dataset row:** meltano__sdk-3091  
**Cohort position:** primary cohort rank 26/96; project-lead selection on 2026-11-20 permits Stage 3 evaluation only

## 1. Proposed technical gold

**G1 — shared mutable visited-reference set leaks across sibling schema branches.**

On the exact buggy base, _resolve_schema_references receives visited_refs: set[str] | None. It initializes one mutable set, adds the current reference path, and then passes the same set into recursive calls. When it iterates sibling entries under properties, it passes the same set to each child. The first property resolves components#/schemas/ComputeUnit and leaves that path in the shared set. The second sibling uses the identical reference path, reaches the already-visited guard, has its $ref removed by schema.pop, and returns the now-empty schema without looking up or merging the target. This produces the reported max_compute_units: {}.

PR #3091 changes the state to an immutable tuple representing only the current recursion path. A child recursion extends the tuple for its descendants, while sibling branches receive the unchanged ancestor tuple. The same reference is therefore resolvable in a sibling, while a true recursive reference on the current call path is still stopped.

The defect is limited to this repeated-sibling-reference behavior in the schema resolver. It is not a claim that all JSON Schema circular-reference handling is defective.

### Pinned source basis

- Buggy source: singer_sdk/singerlib/schema.py, base ae326fe394ec15d528ec2f1e396b8bb3dd5e99a2, SHA-256 2c741e465d44fee12519b708b5d31a09ec0cd0d631149251afb43179f379f61a.
  - visited_refs is a mutable set: lines 254–271.
  - the reference path is popped and checked before lookup: lines 273–283.
  - the same set is passed through sibling properties: lines 285–291.
- Fixed source: singer_sdk/singerlib/schema.py, PR head 9505ff1989b9be4d53b5bc9664b3fe3885879cb1, SHA-256 0f9bab22193cefda9c845c4ca5a612a40869372e29bb66ced39d78f5b319aad1.
  - tuple state is scoped to the current recursion path: lines 254–284.
  - sibling properties receive the ancestor tuple: lines 286–292.
- PR #3091 changes only singer_sdk/singerlib/schema.py and tests/singerlib/test_schema.py.

## 2. Alternative mechanisms retained for adjudication

These are hypotheses for the human adjudicator to consider, not claims that they are equally likely.

- **A1 — repeated resolver lookup/cache behavior:** the resolver returns incomplete contents on a second lookup of the same reference. Prediction: two direct lookups of the same reference would return different or empty contents even when invoked independently of sibling traversal.
- **A2 — shared referenced-object mutation/aliasing:** the first sibling's expansion mutates a shared target object or reference structure that the second sibling then observes. Prediction: a deep-copied target or non-mutating expansion would change the outcome even with the same traversal-state policy.
- **A3 — schema merge / pre-existing-field interaction:** mutation or merge order in the sibling schema dictionaries, rather than recursion-path tracking, causes the second property to lose its expanded target. Prediction: changing merge semantics while holding the recursion state constant would change the second property's result.

The pinned base source makes G1 the supported mechanism: the second sibling is returned at the visited-reference guard before a second resolver.lookup occurs. The three alternatives are included to make the evidential discrimination explicit; they are not independent dataset cases.

## 3. Proposed evidence-tier decisions

| Tier | Proposed supplied evidence | Proposed outcome | Rationale |
|---|---|---|---|
| **E3** | Frozen issue narrative only, including the reported first-property/second-property output and the reporter's explicitly tentative “presumably already visited” comment | **ABSTAIN** | The report supplies a symptom and a conjecture, not source-level evidence that identifies which state or subsystem caused it. A plausible hint is not proof of the mechanism. |
| **E2** | E3 plus the frozen dataset selector and independent public-API reproducer, both run on the exact buggy base and exact fixed PR revision; base fails and fixed passes | **ABSTAIN** | The two reproductions establish that the symptom is real, repeatable, and fixed by the PR. They still do not expose whether the cause is traversal state, resolver behavior, aliasing, or schema merge semantics. Correctly guessing G1 would not make the answer evidence-supported. |
| **E1** | E2 plus the exact buggy and fixed schema.py source snapshots and the relevant sibling-recursion call sites | **ANSWER** | The base source shows the shared mutable set being updated in the first branch and passed into the second sibling; the already-visited guard returns after removing $ref and before another lookup. The fixed source changes this to a tuple scoped to the current recursion path. This directly discriminates G1 from A1–A3. |

Proposed surviving mechanism sets:

- E3: {G1, A1, A2, A3}
- E2: {G1, A1, A2, A3}
- E1: {G1}

E3 and E2 deliberately retain the same causal hypothesis set: reproduction strengthens confidence in the observed failure but does not, by itself, distinguish among the proposed internal mechanisms. The E2 packet must not include source implementation excerpts; otherwise it would leak E1's causal evidence.

## 4. Reproduction and integrity evidence

The Stage 2 artifact was downloaded and checked locally on 2026-11-21:

- GitHub artifact: run 44331092872, artifact 14440520435.
- ZIP SHA-256: b1336169d7b6d8e4e47edbcd920d842ad525c7a4e2df841b998182099bed1bd3, matching GitHub's reported digest.
- ZIP CRC test: passed (ZipFile.testzip() == None).
- Internal SHA256SUMS.txt: 14/14 files matched after normalizing the manifest's leading ./ path prefix.
- Canonical row SHA-256: 318893b8546a4a6b2d8bc75d986a079c818951658fc1293ac59ba05d84682266.
- Base independent reproducer: failed as expected; the second sibling remained an empty object.
- Fixed independent reproducer: passed (1 test).
- Base frozen dataset selector: failed on the same repeated-reference assertion.
- Fixed frozen dataset selector: passed (1 test).

This establishes Stage 2 technical reproducibility, not independent human adjudication or legal clearance.

## 5. Adjudication and exposure limits

The 20 November project-lead decision selected this candidate for Stage 3 evaluation only. It did not approve this gold or the proposed E1/E2/E3 decisions.

The candidate review states that the researcher had already reviewed the issue and PR during screening. Accordingly, perfect blinding must not be claimed. The exact degree of prior source-code exposure should be recorded conservatively. A candidate-specific declaration of prior pipeline/debug exposure is still required; no “none” value is inferred from the existing review.

This proposal uses a source-aware single-project-lead adjudication route if approved. It is not independent blinded adjudication, an inter-rater reliability result, or a second-rater review.

## 6. Explicitly not decided

This proposal does not:
- approve the technical gold or tier membership on behalf of the project lead;
- approve any license scope or state that legal review is complete;
- accept Meltano into the exploratory registry;
- add a second Meltano case from related PR #3009;
- authorize model loading, inference, fine-tuning, or training.

The next gates are the project lead's separate gold/tier decision, candidate-specific exposure declaration, bounded license-scope acknowledgement, final proposed-record validation, and a separate final YES/NO case-acceptance decision.
