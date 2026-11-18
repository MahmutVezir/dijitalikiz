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
- Latest reproduction workflow: https://github.com/MahmutVezir/dijitalikiz/actions/runs/44337982370
- NumPyro job: `134919948613`; artifact ID: `14443210820`
- Artifact ZIP SHA-256: `f39d21e0d3d2c4719b16d8639ca84d8349ebba42c99a7c5276ed81e916a720d5`

The run authenticated the pinned SWE-rebench row and ran both frozen FAIL_TO_PASS selectors in the same pinned CPU environment. Both selectors executed and failed on the buggy base with JAX's batched-key error; both passed on the fixed merge revision. This is technical Stage 2 evidence, not semantic tier adjudication.

Exact upstream source anchors fetched at the pinned revisions:
- Buggy-base `numpyro/infer/mcmc.py`: Git blob SHA-1 `dd3ec0c3a782c1e1530b138153d821392ee5bebd`.
- Buggy-base `numpyro/infer/ensemble.py`: Git blob SHA-1 `64a2870ade0565cb6547cc92d97c11502e769bfd`.
- Fixed `numpyro/infer/mcmc.py`: Git blob SHA-1 `7dd596bca382c4f6517e93458c5806c690cddb59`.
- Fixed regression test file: Git blob SHA-1 `bda377b993ef198960eddc0b27b9e217978d20a3`.

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
| `NP1916-BASE-MCMC-RUN-HANDOFF` | Verbatim buggy-base `numpyro/infer/mcmc.py` lines 654–660 showing chain-key batching and the warmup-state key handoff; parent file blob SHA-1 `dd3ec0c3a782c1e1530b138153d821392ee5bebd` | `f2b649fd9a8c9771ef857c01c04c36dc98f75bea82a2da908be6fe4147401e4f` |
| `NP1916-BASE-ENSEMBLE-SPLIT` | Verbatim buggy-base `numpyro/infer/ensemble.py` lines 190–193 showing the sampler's direct `random.split(rng_key)`; parent file blob SHA-1 `64a2870ade0565cb6547cc92d97c11502e769bfd` | `de79ca7039c71eb3999ca8daf9f190d6a70c1659221514e945a554d6218be190` |

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
- `NP1916-BASE-MCMC-RUN-HANDOFF`;
- `NP1916-BASE-ENSEMBLE-SPLIT`.

Rationale: the buggy-base `MCMC.run` excerpt shows that vectorized execution creates a per-chain key array and then assigns that array unchanged into the warmup state. The buggy-base ensemble sampler excerpt shows the next sampling step calling `random.split(rng_key)` directly. Together, these source excerpts expose the incompatible key-shape handoff without showing the maintainer's correction. The project lead must still confirm that this evidence leaves exactly one defensible mechanism.

## 5. Hidden adjudication-only evidence (not model-visible)

The following records support the project lead's technical-gold adjudication but must **not** be included in E1, E2 or E3 model-input packets:

- Full upstream PR #1918 patch SHA-256: `d05cbdbc3b934c55ace104d7d031c9987d61db5e1abba815104eab8004af5512`.
- Fixed-revision test log SHA-256: `e268b6d982d0d335970c28310727c3e822e7e1684a076db2f2b854b9b186901b`.
- Machine-readable base results SHA-256: `cf097c64ed25a67cbc40fedeca542a4c74e18f1e059f494669d1192c65b7d35b`.
- Machine-readable fixed results SHA-256: `5f3389f5183c4683d8bf9d24e3b1b7c41a4fcab57d9007d41102088d5861a736`.

These hidden records establish the upstream maintainer's chosen correction and the paired Stage 2 result. Keeping the correction out of model-visible packets avoids direct answer/fix leakage. The raw records remain hash-bound and available for project-lead adjudication.

## 6. Integrity and packet-construction controls

Before operationalizing these tiers:

1. Preserve the complete canonical row and the original source material. The issue narrative and traceback above are separately declared source excerpts, not replacements for the complete row.
2. Generate exact packet JSON files from the listed byte-identical evidence items. Do not paraphrase the included issue text or traceback.
3. Record every evidence item's source URL, source revision, byte boundaries (where excerpted), content SHA-256, and packet-manifest SHA-256.
4. Enforce identical content and source hashes for shared item IDs across tiers; E3 ⊂ E2 ⊂ E1 must be strict at each step.
5. Have the project lead review the semantic tier definitions against the complete source record and explicitly record if any level is not defensible. Do not force a three-tier classification to preserve a candidate.
6. Keep technical gold, alternative hypotheses, exposure/independence, and license scope in separate adjudication records. A successful Stage 2 test does not close these gates.

## 7. Exposure and role boundary

The student project lead has already reviewed the public issue, PR, patch and reproduction output during technical screening. This is disclosed exposure, not blinded review. Rater B has not been confirmed as consented or case-specific exposure-cleared and is not a technical-gold or evidence-tier adjudicator. ChatGPT critique is advisory only.

## 8. Current disposition

- Stage 2 technical reproduction: **passed**, latest run `44337982370`.
- Proposed technical gold: **not adjudicated**.
- Alternatives: **proposed; project-lead review pending**.
- E1/E2/E3 packet set: **not operationalized, not validated and not frozen**.
- Independence/exposure and license-scope gates: **open**.
- Final case acceptance: **not accepted**.
- Model loading, inference or fine-tuning: **not authorized**.
