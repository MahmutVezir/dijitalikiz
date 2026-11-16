# Reagento/Dishka #435 — proposed technical gold and evidence-tier adjudication

**Status:** AI-assisted proposal for the student project lead's human decision. Not an accepted case.  
**Case candidate:** `reagento__dishka-436` (primary cohort rank 2).  
**Technical reproduction:** passed exact base-fail/fix-pass gate in run `43875984845`.

## 1. Proposed technical gold

**Gold mechanism ID:** `G1_STALE_PER_SCOPE_FACTORY_REGISTRATION`

The buggy `RegistryBuilder._process_factory` writes each provider factory into the registry for that factory's declared scope immediately. It also overwrites the global `processed_factories[provides]` entry as later providers are processed. When two providers register the same dependency in different scopes, the earlier factory remains in its original scope registry even after the global map points to the later provider.

In issue #435:
- `RealProvider` registers `int=1` in `Scope.REQUEST`;
- `FakeProvider` is later and registers `int=42` in `Scope.APP`;
- `Interactor` is request-scoped and depends on `int`;
- the request container checks its own REQUEST registry before falling back to the parent APP container;
- the stale REQUEST registration therefore returns 1 and shadows the later APP override.

The fixed revision stops inserting factories into scope registries during each provider's processing. It builds the registries after provider processing and inserts the final `processed_factories` mapping into the winning factory's scope. The same issue reproducer then returns 42.

This mechanism is directly supported by the exact fail-to-pass test and the base/fixed implementation diff. It is the proposed gold, pending the student's human sign-off.

## 2. Predeclared candidate mechanisms

| ID | Mechanism | Testable prediction |
|---|---|---|
| `G1_STALE_PER_SCOPE_FACTORY_REGISTRATION` | Earlier provider factory remains in its original scope registry after a later cross-scope override wins the global processed-factory map. | At the buggy base, the REQUEST registry still contains the earlier `int=1` factory; fixed construction inserts only the final winner, so request lookup falls back to APP and returns 42. |
| `A1_SCOPE_CHAIN_PRECEDENCE` | The observed result is caused by the container's normal local-scope-before-parent lookup rule, rather than a stale registration. | A request-local `int` should win whenever present; if no stale request-local entry exists, the APP value should be returned. The issue's expected provider-order override and PR's cross-scope parameterized tests are needed to distinguish intended precedence from a stale entry. |
| `A2_CONSUMER_BINDING_OR_CACHE` | The `Interactor` factory or container cache captured an earlier value, independently of registry population. | A fresh container's first dependency resolution should still produce the wrong value even if the current-scope registry does not contain the earlier factory; the behavior may differ between direct `get(int)` and `get(Interactor)`. |

These are candidate mechanisms for adjudication, not three equally likely explanations. The proposed G1 is the only mechanism that currently explains both the observed failure and the specific base-to-fix source change.

## 3. Proposed nested evidence packets

### E3 — insufficient evidence; all three mechanisms remain possible

Evidence included:
- `ISSUE_435_REPORT`: pinned issue snapshot, SHA-256 `62ee31658aca98a51d2ff1505b44f857294f431f169fba1fff2e2a849b96c49f`.
- `ISSUE_435_REPRODUCER`: exact issue reproducer, SHA-256 `4d06c3ab006c43b134daa7c2b6df5b13ec4e087cecde4170570d6a6f213229f8`.
- `BASE_FAILURE_LOG`: SHA-256 `42ad6d870c4513551c367b58c1b4391a58cf0c40d68eae0105d72df8df5df4ae`.
- `FIXED_PASS_LOG`: SHA-256 `79b43685bdf6dd4ce2c3c6c0e877c473a299caa6557b6682f44b50d3d91e9ae0`.

Rationale: the issue and reproduction establish a cross-scope override failure and the expected value, but do not expose the internal resolution path. G1, A1, and A2 remain plausible at this tier. No mechanism is eliminated.

### E2 — partial evidence; A2 is eliminated, G1 and A1 remain

E3 evidence is retained unchanged, with:
- `BASE_CONTAINER_LOOKUP`: exact base `src/dishka/container.py`, SHA-256 `23bc4ba168e03a2f053c58f98bdf388a9bc21c920c99332fbc4bc53fb5f641c6`.
- `BASE_REGISTRY_LOOKUP`: exact base `src/dishka/registry.py`, SHA-256 `24a9967f47a11d63a0d12bd1f3a9ec590f12aa85d55361aba032acaf94674fe3`.

Rationale: the issue constructs a fresh container and makes the failing request as its first dependency resolution. The base container's `_get_unlocked` checks its local cache, then the current container's registry, and only then the parent container. The registry lookup is direct against that registry's factory map. There is no prior `int` retrieval in the issue reproducer to populate a stale value cache. This makes a pre-captured consumer value or prior-resolution cache an inadequate explanation (A2 eliminated). The packet still does not show why the REQUEST registry contains the wrong factory, so G1 and A1 remain.

### E1 — sufficient evidence; G1 remains as the proposed gold

E2 evidence is retained unchanged, with:
- `BASE_REGISTRY_BUILDER`: exact base `src/dishka/registry_builder.py`, SHA-256 `58cdb82ab89e44549fbf8789390c085040e1f862d0d9887859310959d42dd84f`.
- `FIXED_REGISTRY_BUILDER`: exact fixed `src/dishka/registry_builder.py`, SHA-256 `eb245123fd20eb629b7c80ccf0a57246c1bd48db337e019d87db7447ee081a60`.
- `REGISTRY_BUILDER_DIFF`: exact base-to-fix diff, SHA-256 `360e7f262662646280fc3b5cf5cfd519b28b9f4d0be7b5c2ea2c3f535a4d0e7e`.
- `UPSTREAM_CROSS_SCOPE_TEST`: fixed PR test file `tests/unit/container/override/test_provide.py`, SHA-256 `58b027fab7170fff552d1019b3051f2611ef068a2360e98bf3bd55681e60b462`.

Rationale: the base code explicitly writes every factory into its own scope registry during provider processing. The fixed code removes that immediate insertion and builds fresh registries from the final `processed_factories` map after provider processing. The PR's cross-scope test asserts that the later provider wins for APP→REQUEST and REQUEST→APP combinations. This distinguishes the stale per-scope entry from an inherent scope-chain precedence rule. G1 is the sole surviving mechanism.

## 4. Reproduction record

- Workflow run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/43876245379
- Workflow artifact: `dishka-issue-435-reproduction-43876245379-1`
- Artifact ID: `14229259503`
- Artifact ZIP SHA-256: `d5b611e6264462d4bbb0ae5e4083d95c0f125dc92cf690a8e64d9a51980fc359`
- Artifact includes base/fixed source snapshots, registry builder diff, four fixed upstream test files, runtime record, raw test logs, and SHA256SUMS.
- Test source SHA-256: `4d06c3ab006c43b134daa7c2b6df5b13ec4e087cecde4170570d6a6f213229f8`.\n- Nested E3/E2/E1 packet draft SHA-256: `244e31b986ae883988fb007ab709684da390174f1f01b43758eccb340d8749dc`.\n- Gold/tier adjudication draft SHA-256: `6bd6c6f88cba9d21a1654553821fe3c5e7903994a3c0ed3559c2c72611bce4f9`.
- Python 3.11.9, Ubuntu 22.04.5 LTS; no pip dependencies installed; stdlib `unittest` only.

## 5. Remaining limitations and human decision

1. The exact issue/patch and base-fail/fix-pass reproduction are established.
2. The documentary license screen covers the minimal no-install Python 3.11.9 reproducer only; it is not legal advice or a general license clearance.
3. The model was not loaded and no inference was performed.
4. The temporal exposure screen is supportive, not proof of complete model training-data provenance.
5. The proposed E1/E2/E3 labels and G1 gold mechanism require the student's human decision. ChatGPT's critique is advisory and is not a second human rating.

**Current status: not accepted.** The candidate should be accepted only after the student project lead confirms the gold mechanism, alternatives, tier boundaries, independence/exposure decision, and license-screen scope.
