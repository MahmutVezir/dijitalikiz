# SWE-rebench V2 — Rank 49–52 Stage 2 closure review

**Date:** 21 November 2026  
**Scope:** frozen cohort ranks 49–52  
**Disposition:** **PARTIALLY COMPLETE — NOT CLOSED.** Rank 49 has a verified Stage 2 pass; rank 50 fails the immutable selector-integrity contract; ranks 51–52 remain held before Stage 2 pending exact frozen-row authentication and project-lead suitability decisions.

## Executive summary

| Rank | Candidate | Stage 2 technical gate | Stage 3 / primary-sample status | Current disposition |
|---:|---|---|---|---|
| 49 | geofileops/geofileops #649 / issue #648 | **PASS** — exact base/fixed, independent reproducer, 10/10 selectors, artifact integrity | Strict implementation-mechanism E3/E2/E1 proposal is E3 ABSTAIN / E2 ABSTAIN / E1 ANSWER; project-lead granularity, exposure and remaining gates open | Conditional candidate; not accepted |
| 50 | lektor/lektor #1214 / issue #1213 | **BLOCKED / CONTRACT FAIL** — frozen 149-selector set is not a valid fail-to-pass oracle | No Stage 3; do not trim or rewrite selectors | Not eligible from this frozen row |
| 51 | cuthbertLab/music21 #1736 / issue #1735 | Not run; held before Stage 2 | Upstream issue directly describes the _SplitTuple → plain tuple transition and AttributeError; strong E3 answerability risk; exact frozen row not authenticated | Hold pending exact row and project-lead decision; likely primary-sample exclusion if packet matches issue |
| 52 | geopandas/geopandas #3591 / issue #3590 | Not run; held before Stage 2 | Issue gives exact input, error and workaround but not the internal geometry/dtype recognition branch; exact frozen row and prior-exposure decision remain open | Retain as a potentially useful candidate; no acceptance |

No stage was marked complete merely because a static review or a technical reproducer exists. Technical Stage 2 pass is not equivalent to Stage 3 suitability or final case acceptance.

## Rank 49 — GeoFileOps #649

The later Stage 2 record supersedes the pre-execution statements in the initial static review. The corrected static review and the dedicated reproduction audit are the authoritative records:

- geofileops_649/GEOFILEOPS_649_STAGE2_REPRODUCTION_AND_ARTIFACT_AUDIT_2026-11-21.md
- geofileops_649/GEOFILEOPS_649_E3_E2_E1_EVIDENCE_ELIMINATION_MATRIX_V0_1_2026-11-21.md
- geofileops_649/GEOFILEOPS_649_STATIC_SCOPE_AND_E3_SAMPLE_SUITABILITY_REVIEW_2026-11-21.md (includes the subsequent-execution amendment)

Verified technical results:
- Dataset instance: geofileops__geofileops-649; canonical row SHA-256: 2a85246a15d97ca6e73eb9a02f36022a05f80b8322c24a6522fbfee31fc7d1eb.
- Exact buggy base: f7f8a4cf49b1278f3e9e5f4157718de441a21b57.
- Exact fixed PR head: ec1438fbf8527269cd1193647d05c8d7fdb83802.
- All 10 unchanged frozen selectors failed on base and passed on fixed.
- Independent default-layer reproducer failed on base; explicit-layer positive control passed on base; both reproducer tests passed on fixed.
- Artifact outer SHA-256 matched the GitHub digest; ZIP CRC passed; 18/18 internal hashes passed.

The target gold mechanism is that the existing get_default_layer(dst) helper is not applied when dst_layer=None reaches the public/helper call paths. The frozen E3 statement names the API contract mismatch, but does not show the internal call chain or say that the fallback helper is skipped.

Advisory recommendation: freeze the stricter **implementation-mechanism root-cause** granularity because the study asks whether a model can distinguish a supported causal explanation from a plausible guess. On that granularity, the proposed tiers are E3 ABSTAIN / E2 ABSTAIN / E1 ANSWER. If the gold is instead defined only as API-contract diagnosis, E3 is answerable and the candidate is unsuitable for the primary abstention sample. The project lead must approve the granularity before sample inclusion.

Still open for GeoFileOps: project-lead prior pipeline/debug exposure declaration; temporal-exposure acknowledgement; bounded review of source, dependency and native notices plus dataset-card attribution/scope; project-lead gold/tier approval; complete case record and fail-closed validation; separate final YES/NO acceptance. No registry inclusion or inference.

## Rank 50 — Lektor #1214

The full immutable 149-selector matrix is complete and is recorded in lektor_1213/LEKTOR_1213_STAGE2_SELECTOR_INTEGRITY_HOLD_2026-11-21.md.

- Base matrix: 149 selectors in frozen order; 23 unexpected passes; 125 import/collection failures; one issue-specific permission assertion failure.
- Fixed matrix: 145 passes and four malformed/unresolved node IDs.
- The issue-specific reproducer and direct permission selector fail on base and pass on fixed, but the full frozen dataset selector contract does not pass.
- Do not trim or rewrite the frozen selectors to manufacture a clean Stage 2 result. Do not rerun as a substitute for correcting the underlying dataset row through a separately versioned, justified, prospectively governed dataset correction.

Disposition: keep the Stage 2 contract failure; do not advance to Stage 3 or add this row to the primary sample. This is a dataset-oracle integrity decision, not a claim that the upstream patch is technically ineffective.

## Rank 51 — music21 #1736

The upstream issue #1735 says:
- splitByQuarterLengths([4, 4]) raises AttributeError: 'tuple' object has no attribute 'spannerList';
- the value inside splitAtQuarterLength is _SplitTuple;
- after return to splitByQuarterLengths, it becomes a regular tuple.

That description exposes the key type-preservation mechanism, not merely the symptom. Under the project's evidence-supported root-cause rule, this is a strong E3-answerability concern. PR #1736 also touches music21/figuredBass/resolution.py with separate truthiness changes, in addition to the stream tuple changes and lint/test updates; this mixed scope must not be conflated with the issue-specific gold.

Advisory recommendation: do not run Stage 2 or include this case in the primary abstention sample if the exact frozen problem statement confirms the same type-transition explanation. Before any formal exclusion, authenticate the exact frozen row and selectors and obtain the project lead's decision. The current record remains held; no primary-sample exclusion has been entered.

## Rank 52 — GeoPandas #3591

The upstream issue #3590 provides:
- the exact all-np.nan geometry-column input;
- the ValueError encountered in GeoPandas 1.1.0;
- the successful geometry="geometry" workaround;
- a contrast case in which NaN plus a valid Point does not fail.

PR #3591 adds an all-null geometry-column condition to the constructor's geometry-recognition branch and adds scalar/array regression tests. The issue does not name the internal dtype-recognition condition or the relevant constructor branch. Compared with music21, the issue is less explicit about the implementation mechanism.

Advisory recommendation: keep this candidate on hold as potentially informative under a strict mechanism-level gold; do not classify E3 as answerable solely because the visible behavior is well specified. The exact frozen problem statement, selector list and canonical row digest must be authenticated first. Prior pipeline/debug exposure also requires a separate project-lead declaration. No Stage 2 run, acceptance or inference is recorded.

## Exact row-authentication limitation for ranks 51–52

The pinned source snapshot is known: dataset revision fb9aa226b2ce37c708ea7732e7b980abacdadb67, Parquet SHA-256 7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9. The candidate IDs and base commits are known from the frozen cohort metadata, but the canonical rows for cuthbertLab__music21-1736 and geopandas__geopandas-3591 have **not** been independently extracted and hashed in this review.

A no-inference extraction workflow was drafted in the branch but could not be executed through the available GitHub Actions controls. The unexecuted workflow experiment was removed, and the existing repository-validation workflow was restored to its pre-experiment content. No result was fabricated from a derivative dataset or from the upstream issue text. This blocker must be resolved by a genuine extraction from the pinned Parquet snapshot before ranks 51–52 progress.

## Phase 2 invariants

- Frozen 96-row cohort: unchanged.
- Accepted v0.2 registry: unchanged; Dishka and EODAG remain the only accepted cases.
- No case was added, no easy-answer/control group was created, and the six previously approved exclusions remain as recorded.
- No model weights were loaded; no inference, fine-tuning or training was performed or authorized.
- Candidate-specific researcher exposure and project-lead prior pipeline/debug declarations were not inferred from other candidates.

## Work still required to close this phase

1. Project lead freezes GeoFileOps #649 diagnostic granularity: implementation-mechanism (recommended) or API-contract.
2. Project lead supplies a candidate-specific prior pipeline/debug exposure declaration for GeoFileOps #649 and, if GeoPandas is retained, GeoPandas #3591.
3. Authenticate the exact frozen Parquet rows for music21 #1736 and GeoPandas #3591, then make the corresponding E3 and scope decisions.
4. Record any primary-sample exclusion only after the evidence and project-lead decision are both present; otherwise keep the candidate explicitly held.
5. Recalculate the eligible distinct-project count only after these gates close. Do not lower any eligibility rule to reach the target count.

**Phase 2 status: NOT CLOSED.** The verified work above is preserved; the remaining gates require either exact row evidence or explicit project-lead decisions.


## Project-lead decisions recorded after the initial closure review — 21 November 2026

The project lead subsequently approved the four-item disposition set and supplied candidate-specific prior pipeline/debug exposure declarations of `none` for GeoFileOps #649 and GeoPandas #3591.

- **Rank 49 GeoFileOps #649:** strict implementation-mechanism gold and E3 ABSTAIN / E2 ABSTAIN / E1 ANSWER approved; prior pipeline/debug exposure none. Temporal and license/provenance/scope and final acceptance gates remain open.
- **Rank 50 Lektor #1214:** exclusion from the current primary abstention sample approved due to immutable Stage 2 selector-integrity failure; no selector edits and no control-group assignment.
- **Rank 51 music21 #1736:** conditional primary-sample exclusion approved only if the exact frozen row confirms the same type-transition disclosure in E3. Row authentication is still required; do not run Stage 2 before that check.
- **Rank 52 GeoPandas #3591:** prior pipeline/debug exposure none; retain on hold pending exact row authentication and E3 suitability decision.

The underlying project-lead decision record is `PROJECT_LEAD_RANK49_52_STAGE2_STAGE3_DECISIONS_2026-11-21.md`.

**Phase 2 remains partially complete, not closed.** music21 and GeoPandas frozen rows remain unauthenticated. GeoFileOps' remaining temporal, license/provenance, scope and final acceptance gates are still open. No new case is accepted; the immutable cohort and accepted registry remain unchanged; inference remains unauthorized.


## Row-audit execution correction — 21 November 2026

A first GitHub Actions execution of the no-inference row audit (`44924342085`, job `136907155888`) successfully downloaded the pinned Parquet file and passed its expected byte-length and whole-file SHA-256 checks. It then failed at the first music21 lookup because the initially assumed instance ID `cuthbertLab__music21-1736` was not present (`expected exactly one row, found 0`). This was an incorrect identifier assumption in the audit script; it is not evidence that the candidate row is absent or invalid. No row hash or audit artifact was produced by that failed attempt.

The script was corrected to discover the actual instance ID using the frozen base commit, PR-number suffix and repository slug in metadata columns, and then extract the full row only after exactly one match is found. The corrected execution is GitHub Actions run `44924570231`, job `136907718949`; it was still in progress at the time of this amendment. Exact row authentication remains **pending**, and no Stage 2 work for ranks 51–52 is authorized until the audit artifact and manifest are verified.


## Final exact-row audit result and disposition update — 21 November 2026

The corrected no-inference frozen-row audit completed successfully:

- Workflow run 44924570231; row-audit job 136907864713; artifact 14715535728.
- Exact pinned Parquet: 226,272,977 bytes; 6,272 rows; SHA-256 7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9.
- Artifact ZIP SHA-256: 1abca7d09dfcbf4c4ba773ab87fb21225ec8f4208f44f2f7fbb19b613352459b; independently downloaded digest matched; ZIP CRC passed; internal SHA256SUMS checks passed 6/6.

**Rank 51 — music21 #1736:** exact row cuthbertlab__music21-1736; canonical SHA-256 7bdd5e62281c92e750afb6e34066a28ff429b2bc45e9cc31a0ada13307522db3; E3 SHA-256 06eac6d4bb2e84cb1ecbdb67507954a2e8eb5b531bb19d4a82005ba70f471432; one frozen selector. The frozen E3 repeats the _SplitTuple-to-plain-tuple cause and spannerList AttributeError. The approved condition is satisfied: **formal primary-sample exclusion recorded; no Stage 2**.

**Rank 52 — GeoPandas #3591:** exact row geopandas__geopandas-3591; canonical SHA-256 e543af0bbc5e779661c3b1b79c28849f67dee7c61157c000c6698b15ba1218e2; E3 SHA-256 c4aeb4909495887c065f1f7ae5ec0e321fb350e98ea789cde3f931cad597f12d; one frozen selector. The E3 includes the all-NaN input, error, workaround and valid-geometry contrast, but not the internal constructor dtype/recognition branch. **Hold remains** pending the project lead's semantic E3 tier decision; prior pipeline/debug exposure remains none.

The earlier statement that the row-audit workflow had not executed is superseded by this successful execution. The first attempt's incorrect guessed music21 instance ID and the correction are preserved in the ledger/history; no data was fabricated or inferred from the guessed ID.

**Phase 2 remains partially complete, not closed:** GeoFileOps #649 still has temporal, licensing/provenance/scope and final acceptance gates; GeoPandas #3591 still has its E3 suitability decision. Rank 55 does not start until earlier-ranked open gates are resolved or formally excluded.
