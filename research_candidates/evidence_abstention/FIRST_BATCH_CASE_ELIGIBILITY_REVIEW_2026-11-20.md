# First-batch case eligibility review — 20 November 2026

**Protocol:** SWE-rebench V2 exploratory v0.2, using the accepted Dishka #435 case as the controlling precedent.  
**Decision source:** project lead's 20 November instruction to accept first-batch candidates when they genuinely satisfy the existing criteria.  
**Scope:** NumPyro #1916, Dymos #1166, EODAG #1530, Robocop #1371, Meltano SDK #3090, PyFar #721.  
**Boundary:** this is a technical and eligibility assessment, not a final accepted-case registry update. Model loading, inference, fine-tuning and training remain unauthorized.

## Executive result

Five candidates remain eligible to continue through candidate-specific Stage 3 case construction: **NumPyro, Dymos, EODAG, Meltano SDK and PyFar**. Their recorded Stage 2 results meet the technical base-fail/fixed-pass requirement. They are not yet accepted cases because candidate-specific source-aware gold/tier decisions, truthful prior pipeline/debug exposure declarations, bounded license-scope acknowledgements and complete acceptance records are still outstanding.

**Robocop #1371 is excluded from the v0.2 model-evaluation sample**, despite a successful technical reproduction. The 15 November master audit and project roadmap explicitly record it as previously used for technical debugging and excluded under the predeclared source-exposure/debugging rule. Its successful reproduction is engineering/feasibility evidence only. This exclusion is not reversible by a later passing test and must not be silently waived.

## Candidate-by-candidate disposition

| Order | Candidate | Technical evidence | Case assessment | Remaining case-specific work |
|---:|---|---|---|---|
| 1 | NumPyro #1916 | Two frozen selectors (AIES/ESS) and separate 100-chain public-API warmup→run reproducer pass base-fail/fixed-pass. Latest repeat run 44745926817, artifact 14632847111; local outer digest, ZIP CRC and 10/10 inner hashes verified. | **Strong; proceed toward acceptance.** Proposed E3/E2/E1 packets exist; E1 now includes the buggy-base sampler initialization excerpt that addresses the batched-key alternative. | Project-lead gold/tier decision; prior pipeline/debug exposure declaration; bounded license scope including NumPy/SciPy bundled notices and authentication of the pinned dataset-card license; final case record and validation. |
| 2 | Dymos #1166 | Exact frozen dataset selector and independent fresh Brachistochrone public-API reproducer both fail on the exact base and pass on the exact fix. Latest repeat run 44745926619, artifact 14632443444; local digest, ZIP CRC and 15/15 inner hashes verified. | **Strong; proceed toward acceptance.** Proposed E3/E2/E1 packets and structural tests exist. Issue #531 is related history, not a second case. | Project-lead gold/tier decision; prior pipeline/debug exposure declaration; bounded license scope including bundled NumPy/SciPy notices and exact pinned dataset-card license; final record and validation. Preserve the PR-before-issue timestamp relationship (145 seconds) transparently. |
| 3 | EODAG #1530 | Two exact dataset selectors plus independent YAML configuration reproducer pass base-fail/fixed-pass. Latest branch repeat run 44331092872, job 134895967977, artifact 14440370494 (GitHub digest recorded in run metadata). | **Strong; proceed to Stage 3.** The duplicate top-level geodes key overwrites the public-provider mapping; the corrected geodes_s3 key preserves both. | Keep mixed PR scope visible: PR #1536 also contains a separate StacListAssets change, while the frozen selectors and minimal YAML reproducer isolate the duplicate-key issue. Complete related-issue/lineage review, source-aware gold/tier, exposure declaration and bounded dependency/license scope. |
| 4 | Meltano SDK #3090 | Exact dataset selector and separate direct-source JSON Schema reproducer both pass base-fail/fixed-pass. Latest branch repeat run 44331092872, job 134895968235, artifact 14440520435 (GitHub digest recorded in run metadata). Exact row/timestamp authenticated. | **Strong; proceed to Stage 3.** Shared mutable visited_refs state causes a repeated sibling $ref to be mistaken for a recursion cycle. PR #3091 identifies #3009 as the introduction history; this remains one Meltano case. | Complete related issue/lineage and dependency-license scope review, source-aware gold/tier, prior pipeline/debug exposure declaration, and final record. |
| 5 | PyFar #721 | Corrected pinned environment and latest branch repeat run 44331092872/job 134895967816 pass all 23 frozen selectors base-fail/fixed-pass; artifact 14440390942 (GitHub digest recorded in run metadata). | **Strong numerical candidate; proceed to Stage 3.** Issue #721 covers both energy and power normalization. The fix applies the square-root relationship required because these measures are quadratic in amplitude. The 23 selectors remain one project case. | Supersede older pre-rerun candidate notes; complete related-issue/lineage, prior pipeline/debug exposure and bounded runtime/native-notice license scope. Build the source-aware gold/E1/E2/E3 packet. A separately authored minimal public-API reproducer is a recommended parity enhancement before final acceptance, not a reason to erase the 23/23 Stage 2 pass. |
| — | Robocop #1371 | Exact row and sole frozen selector passed base-fail/fixed-pass in controlled runs. | **Exclude from model-evaluation sample; retain engineering/feasibility only.** This is a prior-exposure exclusion, not a technical failure. | No further sample work. Preserve the original audit and successful raw reproduction evidence. |

## Dishka-equivalent adjudication route

For technical gold and E1/E2/E3 construction, use the same v0.2 route as accepted Dishka #435:

- The project lead is the single source-aware human technical adjudicator.
- ChatGPT provides advisory critique only.
- Hasan may be recorded as project-lead-reported supplementary source-aware technical input; no separate signed independent adjudication or blind-review claim is made.
- Full researcher source exposure is disclosed.
- Two independent human scorers remain required for the separate later task of blind scoring raw model-output evidence support. This is not a gold/tier acceptance gate.

## Acceptance rule

The project lead's portfolio-level instruction is conditional acceptance authorization, not an automatic case acceptance. For each of the five remaining candidates, acceptance requires:

1. Coherent exact issue/PR/dataset-row identity, source provenance and defect-specific base-fail/fixed-pass evidence.
2. One accepted case maximum per upstream project and a documented issue-family/lineage screen.
3. Project-lead source-aware gold mechanism, plausible alternatives and E1/E2/E3 membership/sufficiency decision.
4. Candidate-specific prior pipeline/debug exposure truthfully recorded as none. The full researcher source exposure is recorded separately.
5. Project-lead bounded documentary license-scope acknowledgement, covering actual sources, runtime dependencies, bundled/native notices and any dataset/fixture use. This is not legal clearance or redistribution permission.
6. Complete proposed v0.2 case record, Draft 2020-12 schema validation and fail-closed registry validation.
7. A separate case-specific project-lead final YES before the case enters the accepted registry.

The existing accepted registry remains unchanged: **Dishka #435 is the only accepted case**. No Stage 2 pass, structural CI pass, or portfolio authorization by itself changes that count.

## Recommended next action

Continue exactly in order: finish NumPyro's gold/tier and case-specific declarations; then Dymos; then EODAG, Meltano SDK and PyFar. Do not spend further sample-validation effort on Robocop. If a candidate fails a gate, preserve its evidence and move to the next candidate without weakening the protocol.
