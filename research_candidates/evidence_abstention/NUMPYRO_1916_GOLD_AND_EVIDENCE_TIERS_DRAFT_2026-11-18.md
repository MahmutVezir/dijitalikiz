# NumPyro #1916 — proposed technical gold and E1/E2/E3 design

**Date:** 18 November 2026  
**Candidate:** `pyro-ppl/numpyro`, issue #1916 / PR #1918  
**Status:** Draft proposal only. Not project-lead adjudication, not an accepted case, and not authorization for model inference.

## 1. Evidence basis and immutable identifiers

- Upstream issue: https://github.com/pyro-ppl/numpyro/issues/1916
- Upstream fix: https://github.com/pyro-ppl/numpyro/pull/1918
- Buggy base: `07e4c9bc4524cc0a741ba8f8ad41339d34a0288d`
- Fixed upstream merge commit: `5692d2da335945b756aeae02e3720b9b7f3efef2`
- Dataset row: `pyro-ppl__numpyro-1918`
- Canonical dataset-row SHA-256: `d0dfd87ddd0598ebf368352385419aad6e2d571d2ac83dad04fe57612a7b9646`
- Latest reproduction workflow: https://github.com/MahmutVezir/dijitalikiz/actions/runs/44332892793
- NumPyro job: `134901923864`; artifact ID: `14438938964`
- Artifact ZIP SHA-256: `c122008c972df7e8ecf77b67a9fd050d4b54b883aea9de6dfc4b41e3dd2b67e4`

The run authenticated the pinned SWE-rebench row and ran both frozen FAIL_TO_PASS selectors in the same pinned CPU environment. Both selectors executed and failed on the buggy base with JAX's batched-key error; both passed on the fixed merge revision. This is technical Stage 2 evidence, not semantic tier adjudication.

## 2. Proposed technical gold mechanism

**Proposed mechanism (pending project-lead adjudication):**

During vectorized multi-chain execution with an ensemble kernel, the warmup state carries a batched PRNG key array, with one key per chain. When `MCMC.run` continues from an existing `_warmup_state`, the buggy implementation hands that batched key through to the ensemble state. `EnsembleSampler.sample` then calls `jax.random.split(rng_key)`, an operation that expects a single key at that call site. The received shape is `(num_chains, 2)` rather than a single key's shape, producing the observed `ValueError`.

The upstream PR #1918 changes the `MCMC.run` warmup-state handoff: if `self.sampler.is_ensemble_kernel`, it places `rng_key[0]` into the state; otherwise it retains the prior `rng_key` behavior. The AIES and ESS regression selectors fail on the buggy base and pass on the fixed revision.

This statement identifies the leading causal explanation supported by the source diff and paired reproduction. It is not yet the project's formally adjudicated gold record.

## 3. Plausible, testable alternative mechanisms

These alternatives should be retained in the adjudication record rather than silently discarded:

1. **Ensemble sampler batching contract defect.** The direct failing frame is `EnsembleSampler.sample` calling `random.split`. A plausible competing explanation is that the sampler's internal random-key handling should explicitly support batched keys (for example, by mapping the split) and that the failure is local to the sampler rather than the MCMC warmup-state handoff. The upstream patch's location in `MCMC.run` is evidence against this alternative, but the distinction must be explained explicitly.
2. **Caller/API lifecycle or key-shape misuse.** A competing explanation is that the public `warmup` then `run` sequence, or the caller's PRNG-key use, is unsupported or incorrectly shaped. The reporter supplies an ordinary `jax.random.PRNGKey` to both public calls; the batched `(100, 2)` shape appears inside the library after vectorized chain handling. The pinned selectors also use an ordinary key and reproduce at 10 chains. This evidence weighs against caller misuse, but the API contract should be checked and cited in the final adjudication.
3. **JAX PRNG API/version incompatibility.** A competing explanation is that the failure is due to a JAX key representation or API-version mismatch rather than NumPyro state handoff. The current base and fixed tests use the same pinned JAX/JAXlib versions; the error identifies a batched shape, and the same environment passes on the fixed NumPyro revision. This is evidence against a general runtime incompatibility, not proof that every JAX version is unaffected.

The first two are the primary alternatives to discuss for the causal mechanism. Do not report them as disproven solely because the upstream maintainer chose a particular patch.

## 4. Proposed nested evidence design

The following is a **design proposal**, not the final operational packet set. It is intended to preserve the study rule that E3 is a proper subset of E2, E2 a proper subset of E1, and that source fragments are explicitly bounded and hash-recorded rather than silently truncated.

### Proposed evidence items

| Stable item ID | Source and boundary | SHA-256 |
|---|---|---|
| `NP1916-ISSUE-NARRATIVE-CODE` | Exact first 836 UTF-8 bytes of the pinned dataset row's `problem_statement` field: issue title, narrative and reproducer code, ending before the separately identified traceback | `3a1b4b412dfeb9f33a5fa9a6534a4a7522d79dddd7a8760540c358f21d81bf2c` |
| `NP1916-ISSUE-TRACEBACK` | Exact traceback fragment from the same field, byte range [838, 5775), including the reported key shape and failing `random.split` frame | `4ba5d2d4d78a306adce6b8ce850a3f47fc66b6a1ebce934fcb3b318eed6ada36` |
| `NP1918-FIX-PATCH` | Full upstream PR #1918 patch captured in the latest reproduction artifact | `d05cbdbc3b934c55ace104d7d031c9987d61db5e1abba815104eab8004af5512` |
| `NP1916-BASE-TEST-LOG` | Raw base selector log from the latest reproduction artifact | `0c4e0e335b80877185ab2b54ec527add0bd1e1b9c733511c4f71aa09e4ba20c1` |
| `NP1916-FIXED-TEST-LOG` | Raw fixed-revision selector log from the latest reproduction artifact | `e268b6d982d0d335970c28310727c3e822e7e1684a076db2f2b854b9b186901b` |
| `NP1916-BASE-RESULTS` | Machine-readable base selector results | `cf097c64ed25a67cbc40fedeca542a4c74e18f1e059f494669d1192c65b7d35b` |
| `NP1916-FIXED-RESULTS` | Machine-readable fixed selector results | `5f3389f5183c4683d8bf9d24e3b1b7c41a4fcab57d9007d41102088d5861a736` |

The full canonical row remains available as the source anchor and has SHA-256 `d0dfd87ddd0598ebf368352385419aad6e2d571d2ac83dad04fe57612a7b9646`. The original upstream issue and PR are linked above. The excerpt hashes identify the exact included bytes; the excerpt boundaries must accompany the operational packet manifests.

### E3 — least evidence

Proposed contents:
- `NP1916-ISSUE-NARRATIVE-CODE`

Rationale: the issue description and reproducer establish the reported warmup-then-run symptom and execution configuration, but without the traceback they do not identify where the malformed key arises. Caller/API misuse, sampler batching behavior and runtime interaction remain plausible. This tier must not be labelled E3 unless the project lead confirms that none of the predeclared mechanisms is defensibly eliminated by this packet.

### E2 — intermediate evidence

Proposed contents:
- all E3 items, unchanged;
- `NP1916-ISSUE-TRACEBACK`

Rationale: the traceback adds the batched key shape and the `EnsembleSampler.sample` → `random.split` failure location. It makes a generic model/data failure much less plausible, while still leaving a reasonable distinction between (a) the upstream warmup-state handoff and (b) the sampler's own batched-key handling contract. The project lead must confirm that at least two mechanisms genuinely remain possible after reading this evidence; otherwise the case does not support the intended E2 definition.

### E1 — strongest evidence

Proposed contents:
- all E2 items, unchanged;
- `NP1918-FIX-PATCH`;
- `NP1916-BASE-TEST-LOG`, `NP1916-FIXED-TEST-LOG`;
- `NP1916-BASE-RESULTS`, `NP1916-FIXED-RESULTS`.

Rationale: the patch identifies the exact conditional state handoff in `MCMC.run`; the paired logs/results show both AIES and ESS selectors execute and fail on the pinned buggy base and pass on the pinned fixed merge revision. This should distinguish the proposed gold mechanism from the remaining alternatives. It must be verified by the project lead; a patch author's implementation choice is supporting evidence, not by itself a substitute for causal adjudication.

## 5. Integrity and packet-construction controls

Before operationalizing these tiers:

1. Preserve the complete canonical row and the original source material. The issue narrative and traceback above are separately declared source excerpts, not replacements for the complete row.
2. Generate exact packet JSON files from the listed byte-identical evidence items. Do not paraphrase the included issue text or traceback.
3. Record every evidence item's source URL, source revision, byte boundaries (where excerpted), content SHA-256, and packet-manifest SHA-256.
4. Enforce identical content and source hashes for shared item IDs across tiers; E3 ⊂ E2 ⊂ E1 must be strict at each step.
5. Have the project lead review the semantic tier definitions against the complete source record and explicitly record if any level is not defensible. Do not force a three-tier classification to preserve a candidate.
6. Keep technical gold, alternative hypotheses, exposure/independence, and license scope in separate adjudication records. A successful Stage 2 test does not close these gates.

## 6. Exposure and role boundary

The student project lead has already reviewed the public issue, PR, patch and reproduction output during technical screening. This is disclosed exposure, not blinded review. Rater B has not been confirmed as consented or case-specific exposure-cleared and is not a technical-gold or evidence-tier adjudicator. ChatGPT critique is advisory only.

## 7. Current disposition

- Stage 2 technical reproduction: **passed**, latest run `44332892793`.
- Proposed technical gold: **not adjudicated**.
- Alternatives: **proposed; project-lead review pending**.
- E1/E2/E3 packet set: **not operationalized, not validated and not frozen**.
- Independence/exposure and license-scope gates: **open**.
- Final case acceptance: **not accepted**.
- Model loading, inference or fine-tuning: **not authorized**.
