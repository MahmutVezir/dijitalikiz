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

---

## 2. Advisory gold and evidence-tier proposals — 20 November 2026

The following are **ChatGPT advisory proposals** for the project lead's source-aware decision under the Dishka-equivalent exploratory route. They are not represented as already approved human gold or accepted E1/E2/E3 tiers. Proposed model-visible packets must continue to exclude the fix patch, fixed-revision outputs, hidden gold label and tier labels.

### 2.1 NumPyro #1916 — proposed gold and tiers

**Proposed gold mechanism**

During the documented `MCMC.warmup()` → `MCMC.run()` lifecycle with vectorized AIES/ESS chains, `MCMC.run()` creates a per-chain PRNG-key batch for the 100 chains and places that batch into the saved warmup sampler state. The normal `EnsembleSampler.init()` path stores a scalar sampler key, and `EnsembleSampler.sample()` later calls `random.split()` as though the state field were still scalar. The warmup-resume handoff therefore violates the sampler state's key-shape invariant, producing the observed `(100, 2)` key-array error.

**Competing explanations to retain and assess:** unsupported caller lifecycle/misuse; an intended batched-key contract for the ensemble sampler; a JAX version/API incompatibility; or a more general vectorized-chain state-handling defect. The pinned initializer excerpt and the same-environment fixed-pass result weaken, but do not automatically eliminate, these alternatives.

**Proposed evidence tiers**
- **E3:** issue narrative and reproduction example only.
- **E2:** E3 plus the issue's exact traceback showing `random.split` receives a key array of shape `(100, 2)`.
- **E1:** E2 plus the three pinned buggy-base source excerpts already present in the proposed packet set: the `MCMC.run` warmup-state handoff, the scalar `random.split` call in `EnsembleSampler.sample`, and `EnsembleSampler.init` selecting `rng_key[0]` and storing a scalar key.

The proposed v0.2 packet set already exists (E3=1, E2=2, E1=5; SHA-256 `e1730956eb9cfc9015bb43c5725f49d3ebff9dfc3c564594060209bab5e5485d`). Its structural validation passed; this does not itself prove E1 semantic sufficiency.

### 2.2 Dymos #1166 — proposed gold and tiers

**Proposed gold mechanism**

On the buggy base, `ControlInterpComp._configure_controls` initializes the promoted polynomial-control input with `np.ones(input_shape)` rather than the requested `options['val']`. The earlier `reshape_val(options['val'], ...)` / `set_input_defaults(...)` route is commented out. Consequently, `add_control(val=[...])` does not determine the initial value observed on the phase's promoted `controls:* ` input. PR #1165 routes the requested value through `reshape_val` and uses it as the input's initial value.

**Competing explanations to retain and assess:** shape/broadcast normalization; stale test-fixture `set_val` state; ODE target/units or downstream model setup; and a transcription-specific issue rather than a shared polynomial-control input initialization defect. The independent fresh Brachistochrone problem reduces the fixture/previous-value alternatives, but the claim should remain bounded to the tested polynomial-control paths.

**Proposed evidence tiers**
- **E3:** frozen issue narrative describing ignored `add_control` / `set_control_options` values.
- **E2:** E3 plus the independent fresh-model Brachistochrone public-API reproducer and its buggy-base observation `[[1.0], [1.0]]` instead of `[[5.0], [15.0]]`.
- **E1:** E2 plus the pinned buggy-base excerpts showing the unconditional ones input, the commented-out value normalization and the commented-out input-default path.

The proposed nested packet set already exists (E3=1, E2=3, E1=6; SHA-256 `07b9547ba6bc30dd525acff0b9916542b81e47f9ed8451f2b0fba5ca8a22b17d`). The independent reproducer and packet contract have passed; the source-aware gold/tier decision remains the project lead's.

### 2.3 EODAG #1530 — proposed gold and tiers

**Proposed gold mechanism**

The pinned default `user_conf_template.yml` contains two top-level YAML mappings named `geodes`. Under ordinary YAML mapping semantics, the later mapping replaces the earlier one. The public Geodes `apikey` mapping is therefore lost and the S3 credential mapping occupies the `geodes` key. The fix renames the second mapping to `geodes_s3`, preserving both providers under distinct keys.

**Competing explanations to retain and assess:** YAML parser-specific duplicate-key handling; provider registration/metadata problems separate from YAML key replacement; the related #1517 / StacListAssets changes in the same PR; and a malformed user configuration rather than the shipped default template. The exact-base YAML reproducer directly exercises the template, and the two frozen selectors concern the `geodes_s3` registration/sortables path. Keep the separate StacListAssets change out of this case's gold statement.

**Proposed evidence tiers**
- **E3:** issue narrative and the reported duplicate-key YAML example.
- **E2:** E3 plus the independent base-only YAML parsing observation showing the later `geodes` mapping survives while the public `apikey` mapping is absent and `geodes_s3` is absent.
- **E1:** E2 plus exact pinned buggy-base source excerpts showing both top-level `geodes` mappings in the shipped template and, if needed, the narrow code path that loads that template. Do not include the renamed fixed key or fixed output in the model-visible packet.

The two frozen selectors and independent YAML reproducer pass base-fail/fixed-pass. The 52-distribution runtime inventory is recorded; project-lead acknowledgement of the actual dependency/bundled-notice scope remains pending. The root Apache-2.0 and PyYAML MIT screen for the minimal reproducer is narrower than the full test runtime.

### 2.4 Meltano SDK #3090 — proposed gold and tiers

**Proposed gold mechanism**

The base implementation carries one mutable `visited_refs` set through recursive traversal of sibling JSON Schema branches. After the first property resolves a component reference, the same reference encountered in a sibling property is treated as though it were a recursion cycle, so the second property is returned as an empty object. The defect is that the set records references visited anywhere in the traversal instead of references on the current recursion path.

**Competing explanations to retain and assess:** the reference resolver itself returns empty contents; an invalid reference URI; genuine circular schema recursion; mutation of the input schema; or a shared-state bug in the sibling traversal. The exact public example, exact-base source and direct-source reproducer support the shared mutable-state explanation. PR #3091's link to #3009 should be retained as introduction history, not counted as another case.

**Proposed evidence tiers**
- **E3:** issue narrative with the two sibling properties, expected result and actual empty second property.
- **E2:** E3 plus the independent exact-source reproducer's buggy-base result showing the first property resolved and the second remained empty.
- **E1:** E2 plus pinned buggy-base excerpts showing the mutable `visited_refs` set is initialized, mutated on a reference, and passed unchanged into each sibling property recursion.

The one exact frozen selector and independent reproducer both pass base-fail/fixed-pass. Root source license is Apache-2.0; the pinned subset dependency/license inventory is recorded but still needs project-lead scope acknowledgement and a related-issue/lineage screen.

### 2.5 PyFar #721 — proposed gold and tiers

**Proposed gold mechanism**

For energy and power normalization, the measured quantity is quadratic in signal amplitude. The buggy implementation computes an energy or power reference but scales amplitude linearly by `target / reference`. That does not yield the requested energy/power target. The amplitude factor must instead follow the square-root relationship, equivalent to `sqrt(target / reference)` for positive target/reference values. Keep RMS analytically distinct: RMS is already amplitude-linear and must not be described as requiring the same square-root correction.

**Competing explanations to retain and assess:** an incorrect energy/power measurement implementation; an unexpected target convention; channel-handling or signal-shape behavior; a test fixture error; or confusion between RMS and energy/power semantics. The issue's numerical examples and the 23 exact frozen selectors provide a quantitative oracle. The issue and PR explicitly concern energy and power; the 23 parameterized test selectors are one PyFar case, not 23 independent cases.

**Proposed evidence tiers**
- **E3:** issue narrative and numerical examples, including energy 20 producing energy 0.05 instead of target 1.
- **E2:** E3 plus base-only numeric output from exact frozen selector runs demonstrating that requested energy/power targets are missed, with the same 23 selectors' base-fail outcomes summarized without showing fixed results.
- **E1:** E2 plus exact pinned buggy-base source excerpts showing `energy(signal)` / `power(signal)` used as the reference and the linear `signal * target / reference_norm` scaling. Do not show the fixed square-root implementation in the packet.

All 23 frozen selectors now pass base-fail/fixed-pass in the corrected pinned environment. A separate standalone public-API issue reproducer has **not** been run; it is a useful parity enhancement but should not be falsely described as existing evidence. The corrected dependency inventory is recorded, but its exact package/native notice scope still requires project-lead acknowledgement and the candidate's prior pipeline/debug exposure declaration.

## 3. Cross-candidate acceptance review — shared boundaries

The five candidates have technical Stage 2 evidence, but the following status is candidate-specific and still must be completed before any final acceptance:

| Candidate | Recorded source exposure | Prior pipeline/debug declaration | Bounded dependency/license scope | Human gold/E1-E2-E3 decision |
|---|---|---|---|---|
| NumPyro | Project lead and Hasan exposed to source/design; disclose full exposure | Must be explicitly confirmed for this candidate | Pending; exact pinned dataset-card license and bundled notices need scope review | Advisory proposal only; project-lead decision pending |
| Dymos | Project lead and Hasan exposed to source/reproduction; disclose full exposure | Pending | Pending; NumPy/SciPy bundled notices and exact pinned dataset-card license | Advisory proposal only; project-lead decision pending |
| EODAG | Partial candidate-screening source exposure recorded | Pending | 52-package inventory recorded; scope acknowledgement pending | Advisory proposal only; project-lead decision pending |
| Meltano SDK | Partial candidate-screening source exposure recorded | Pending | Minimal dependency/source inventory recorded; scope acknowledgement pending | Advisory proposal only; project-lead decision pending |
| PyFar | Partial candidate-screening source exposure recorded | Pending | Corrected runtime inventory recorded; native/system notice review and scope acknowledgement pending | Advisory proposal only; project-lead decision pending |

Candidate screening exposure is not automatically prior pipeline/debug exposure. These fields must not be conflated. Do not fill a pending exposure declaration as `none` without the project lead's factual confirmation. Likewise, a metadata inventory is not legal clearance; the acknowledgement is only a bounded documentary scope decision for the specified research use.

## 4. Current portfolio outcome

- **Eligible to continue candidate-specific Stage 3 review:** NumPyro, Dymos, EODAG, Meltano SDK and PyFar.
- **Excluded from model-evaluation sample:** Robocop; engineering/feasibility only due prior technical debugging exposure.
- **Accepted exploratory cases:** Dishka #435 only.
- **Final case acceptances added by this review:** none.
- **No model weights loaded; no inference, fine-tuning or training performed or authorized.**

The project lead's conditional selection is honoured: these five are the first cases to process, and a candidate should be accepted once it truly satisfies the same Dishka-equivalent standard. It is not an instruction to convert a Stage 2 pass into an accepted case without the remaining case-specific records and human decision.

### EODAG scope note — superseding clarification

The related #1517 report is a separate `KeyError: 'result_type'` in the remote `fetch_product_types_list` path. PR #1536's body says “Fixes #1530”; its diff only renames the duplicate key in `user_conf_template.yml`, adds `StacListAssets` to a config list, and updates expected `geodes_s3` provider/product-type/sortable lists. The frozen `test_list_product_types_for_provider_ok` selector uses `fetch_providers=False`, so it does not exercise #1517's remote-fetch path. Keep #1517 as a related distinct issue and keep `StacListAssets` out of the #1530 gold statement. The direct independent YAML reproducer remains the clearest isolated confirmation of the duplicate-key mechanism.

## 5. Superseding project-lead decision — 20 November 2026

The project lead has now explicitly accepted all five strong candidates for continued v0.2 Stage 3 case evaluation:

1. NumPyro #1916
2. Dymos #1166
3. EODAG #1530
4. Meltano SDK #3090
5. PyFar #721

For NumPyro #1916, the project lead separately approved the exact source-aware technical gold mechanism quoted in the NumPyro candidate review. This gold approval is recorded as a human decision, not an AI recommendation.

For Dymos, EODAG, Meltano and PyFar, the project lead has approved candidate selection only. Their proposed gold mechanisms and E1/E2/E3 tier membership remain advisory proposals pending separate project-lead decisions.

The five candidate selections are **not five final accepted cases**. The accepted-case registry remains unchanged until each candidate independently closes its prior pipeline/debug exposure declaration, bounded documentary license-scope acknowledgement, final gold/alternative/E1-E2-E3 decision, complete schema-conformant case record, fail-closed registry validation and separate case-specific final YES. Existing prior-debug exclusion of Robocop remains in force.

The NumPyro and Dymos current-branch exact base/fix reproducer workflows both completed successfully on commit `8ab2c2cb36b8f8bee00d12a990d9cc76cc205aaa`: NumPyro run 44751142001/job 136339034841 and Dymos run 44751142114/job 136339035133. The no-inference preflight run 44751142329 completed successfully, and repository/configuration validation run 44751141885 completed successfully. These are structural/reproduction validations only; no model inference was performed.

## Latest CI confirmation after project-lead decisions — 20 November 2026

- NumPyro current-head independent reproduction: run 44755560775/job 136354249543 — success; artifact 14637651511, GitHub SHA-256 `bd05413602aaf5de6e8b213708dee68cfc863a97dd9f7620ed196afc2b071d3a`. Exact buggy base showed the expected `(100, 2)` PRNG-key error; the exact fixed revision passed.
- No-inference preflight: run 44755547992/job 136354205627 — success. Packet audit, operational/nested packet contracts, NumPyro and Dymos review-contract tests, selector runner contract, v0.2 readiness/acceptance contract and dual-human scoring amendment tests passed.
- The preflight's successful contract tests do not close its 13 global readiness blockers and do not authorize model loading or inference. Dishka remains the only final accepted case.
