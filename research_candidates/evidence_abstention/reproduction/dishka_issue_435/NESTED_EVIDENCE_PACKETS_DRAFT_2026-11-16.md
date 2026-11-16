# Dishka #435 — nested E3/E2/E1 evidence packet drafts

**Status:** proposed packet material; the student project lead approved the technical gold, alternatives, and E3/E2/E1 hierarchy on 2026-11-16. Not accepted case material yet. No gold label is exposed in the packet contents.

## E3 — insufficient evidence

**E3-01: upstream issue report**

Source: https://github.com/reagento/dishka/issues/435  
Snapshot SHA-256: `086ee0aba856f76397da74a704d98cc8a82e40e165739d9cc352b202d103e8f3`

Title: “bug: Provider doesn't override factory with lower scope”

The issue's minimal example registers `int=1` in `Scope.REQUEST`, then registers `int=42` in `Scope.APP`, and resolves a request-scoped `Interactor` that depends on `int`. The expected result is 42; the reporter observes 1. The issue also reports that reversing the two scopes works.

**E3-02: independent exact reproducer**

Source: `research_candidates/evidence_abstention/reproduction/dishka_issue_435/test_issue_435.py`  
SHA-256: `4d06c3ab006c43b134daa7c2b6df5b13ec4e087cecde4170570d6a6f213229f8`

The test recreates the issue's provider order, scopes, dependency, and expected value. At E3, no implementation source is shown.

**E3 surviving mechanisms:** stale per-scope factory registration; scope-chain precedence/fallback; consumer dependency binding or cache behavior. None is eliminated by this packet.

---

## E2 — partial evidence

**Includes E3-01 and E3-02 unchanged**, plus:

**E2-01: base container lookup**

Source: https://github.com/reagento/dishka/blob/8718d5af93f9e48bc2506c64827663fdccc5ad89/src/dishka/container.py  
Commit: `8718d5af93f9e48bc2506c64827663fdccc5ad89`  
SHA-256: `23bc4ba168e03a2f053c58f98bdf388a9bc21c920c99332fbc4bc53fb5f641c6`

Relevant exact excerpt:

```python
def _get_unlocked(self, key: DependencyKey) -> Any:
    if key in self._cache:
        return self._cache[key]
    compiled = self.registry.get_compiled(key)
    if not compiled:
        if not self.parent_container:
            raise NoFactoryError(key)
        return self.parent_container._get(key)
    try:
        return compiled(self._get_unlocked, self._exits, self._cache)
    except NoFactoryError as e:
        e.add_path(cast(Factory, self.registry.get_factory(key)))
        raise
```

**E2-02: base registry lookup**

Source: https://github.com/reagento/dishka/blob/8718d5af93f9e48bc2506c64827663fdccc5ad89/src/dishka/registry.py  
Commit: `8718d5af93f9e48bc2506c64827663fdccc5ad89`  
SHA-256: `24a9967f47a11d63a0d12bd1f3a9ec590f12aa85d55361aba032acaf94674fe3`

Relevant exact excerpt:

```python
def get_factory(self, dependency: DependencyKey) -> Factory | None:
    try:
        return self.factories[dependency]
    except KeyError:
        origin = get_origin(dependency.type_hint)
        if not origin:
            return None
        # generic lookup continues here
```

**E2 rationale:** the issue creates a fresh container and the failing resolution is its first dependency access. The container checks the current scope's cache, then its own registry, and only delegates to the parent if no local factory is found. The registry first checks its own factory dictionary. This makes a prior-resolution cache or consumer-specific captured value an inadequate explanation (A2 eliminated). The evidence still does not show why the current-scope registry contains the wrong factory; stale registration and scope-chain precedence remain possible.

**E2 surviving mechanisms:** stale per-scope factory registration; scope-chain precedence/fallback.

---

## E1 — sufficient evidence

**Includes all E3 and E2 evidence unchanged**, plus:

**E1-01: buggy base registry construction**

Source: https://github.com/reagento/dishka/blob/8718d5af93f9e48bc2506c64827663fdccc5ad89/src/dishka/registry_builder.py  
Commit: `8718d5af93f9e48bc2506c64827663fdccc5ad89`  
SHA-256: `58cdb82ab89e44549fbf8789390c085040e1f862d0d9887859310959d42dd84f`

```python
self.processed_factories[provides] = factory
registry = self.registries[cast(Scope, factory.scope)]
registry.add_factory(factory)
```

**E1-02: fixed registry construction**

Source: https://github.com/reagento/dishka/blob/b1eae11734e64551d7b101195f27cb6870e1c364/src/dishka/registry_builder.py  
Commit: `b1eae11734e64551d7b101195f27cb6870e1c364`  
SHA-256: `eb245123fd20eb629b7c80ccf0a57246c1bd48db337e019d87db7447ee081a60`

```python
for key, factory in self.processed_factories.items():
    scope = cast(BaseScope, factory.scope)
    registries[scope].add_factory(factory, key)
return tuple(registries.values())
```

The fixed `_process_factory` stores the processed factory but no longer inserts it immediately into a scope registry. Registry population occurs after provider processing.

**E1-03: base-to-fix source diff**

Path: `src/dishka/registry_builder.py`  
SHA-256: `360e7f262662646280fc3b5cf5cfd519b28b9f4d0be7b5c2ea2c3f535a4d0e7e`

**E1-04: upstream cross-scope regression test**

Source: https://github.com/reagento/dishka/blob/b1eae11734e64551d7b101195f27cb6870e1c364/tests/unit/container/override/test_provide.py  
Commit: `b1eae11734e64551d7b101195f27cb6870e1c364`  
SHA-256: `58b027fab7170fff552d1019b3051f2611ef068a2360e98bf3bd55681e60b462`

The added `test_override_different_scope` parameterizes APP→REQUEST, REQUEST→APP, and APP→APP provider scope pairs and asserts that the later provider's value is returned.

**E1 rationale:** the base source writes every provider factory to its own scope registry immediately. The fixed source delays registry population and inserts only the final processed-factory mapping. The upstream regression test establishes later-provider precedence across the tested scope combinations. This distinguishes a stale per-scope entry from an inherent scope-chain precedence rule.

**E1 proposed surviving mechanism:** one source-level registry-construction defect. The student project lead approved this technical-gold and tier rationale on 2026-11-16; the approval is recorded in `HUMAN_ADJUDICATION_DECISION_DISHKA_435_V0_1_DRAFT_2026-11-16.md`.

---

## Provenance and acceptance limitations

The issue report and dataset-linked pull request are separate GitHub resources with separate creation timestamps. The issue snapshot's timestamp was corrected against the upstream issue endpoint; the dataset row's `created_at` matches PR #436's creation timestamp, not issue #435's timestamp. The row is therefore reconciled as a pull-request instance, while the issue remains the defect narrative source.

The researcher has reviewed the issue and patch during candidate screening; perfect blinding must not be claimed. The working design has one human adjudicator. ChatGPT's critique is advisory AI input, not a second human rating. No human-human inter-rater reliability or Cohen's kappa claim is permitted. The documentary license screen applies only to the pinned minimal reproduction environment and is not legal advice or blanket clearance.

The evidence packet remains a draft until each source snapshot, source URI/commit/path, content hash, and proper nested-set relation is independently revalidated against the actual evidence files.

## Remaining case-acceptance gates

Even after technical gold and evidence-tier adjudication, separately verify:

1. exact dataset-row identity and timestamp/resource-type provenance;
2. one-case-per-upstream-project independence and related-defect/fork lineage;
3. exposure classification and the model-training contamination limitation;
4. exact-base license and changed-file/dependency scope, with documentary evidence;
5. immutable evidence packet files, packet hashes, and provenance;
6. the case-acceptance schema and validator against the actual record.

Until all gates pass and the case record is accepted, the registry count remains zero and model inference remains unauthorized.
