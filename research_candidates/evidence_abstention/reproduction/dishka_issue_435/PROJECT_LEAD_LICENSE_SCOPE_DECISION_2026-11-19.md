# Dishka #435 — bounded documentary license-scope decision

**Decision timestamp (UTC):** 2026-11-19T15:55:16Z  
**Decision-maker role:** student project lead  
**Candidate:** `reagento__dishka-436`  
**Decision:** `no_obvious_prohibition_identified_for_documented_scope`  
**Status:** project-lead scope decision recorded; **not legal advice or legal clearance**

## 1. Explicit project-lead decision

The project lead accepts the existing documentary license/provenance screen as sufficient **only for the exact exploratory research and reproduction scope listed below**.

This approval does not grant, imply, or represent formal legal advice, legal clearance, a blanket redistribution right, or approval for optional integrations, development extras, other environments, or later experiments.

## 2. Exact approved scope

The approval is limited to:

1. **Dishka upstream source at the exact pinned revisions**
   - Buggy base: `8718d5af93f9e48bc2506c64827663fdccc5ad89`
   - Fixed revision: `b1eae11734e64551d7b101195f27cb6870e1c364`
   - Root `LICENSE` at the exact buggy base: Apache-2.0.
   - Git blob SHA-1: `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`.
   - Exact LICENSE content SHA-256: `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`.

2. **The five changed files in PR #436 only**
   - `src/dishka/registry_builder.py`
   - `tests/unit/container/override/test_alias.py`
   - `tests/unit/container/override/test_context_var.py`
   - `tests/unit/container/override/test_provide.py`
   - `tests/unit/container/test_context_vars.py`
   - The documentary changed-file manifest is SHA-256 `34e09fdcf5d33849659490e2e50cdf80c8c5c8e6f01108dd542c60de203cf360`.
   - The manifest records only the root LICENSE, with no additional nested license/NOTICE/COPYING files found within the screened changed-file scope.

3. **Independent issue reproducer environment**
   - Ubuntu 22.04.5 LTS, CPython 3.11.9.
   - Exact Dishka source imported through `PYTHONPATH=src`.
   - Python standard-library `unittest`.
   - No pip-installed third-party upstream runtime dependencies.
   - No wheel build or package installation.

4. **Frozen dataset FAIL_TO_PASS selector environment**
   - Separate isolated environment, CPython 3.11.9.
   - `pytest==8.3.5`, `iniconfig==2.0.0`, `packaging==24.2`, `pluggy==1.5.0`.
   - Installed with `pip --no-deps` from the frozen lock.
   - Lock SHA-256: `86df530333234a4da0407f344d39b7851aac892fd9ad485a5c1ed7b9d8870d5d`.

5. **Dataset extraction environment**
   - Separate isolated environment, CPython 3.11.9 and PyArrow 19.0.1 (Apache-2.0).
   - Used only to read the pinned public Parquet dataset and authenticate the exact row; it does not execute Dishka source.

## 3. Evidence references

- Changed-file license manifest: `REAGENTO_DISHKA_436_CHANGED_FILE_LICENSE_MANIFEST_V0_1.json`.
- Reproduction environment lock: `reproduction/dishka_issue_435/reproduction_environment_lock.json`.
- Dataset test lock: `reproduction/dishka_issue_435/dataset_test_requirements.lock`.
- Exact base LICENSE URL: https://github.com/reagento/dishka/blob/8718d5af93f9e48bc2506c64827663fdccc5ad89/LICENSE
- Current technical reproduction bundle: workflow run `44537219541`, artifact `14536192821`, ZIP SHA-256 `b8dfe9e89e44f246fbf8d093ba31dc01c74c6dc167434555405693d6a0f1df52`.

## 4. Scope exclusions and safeguards

This decision does **not** cover:
- optional Dishka integrations, adapters, or extras;
- the complete upstream development/build/test environment;
- unpinned dependencies or other OS/Python/runtime combinations;
- redistribution of upstream source, wheels, binaries, or third-party packages;
- redistribution of the SWE-rebench dataset or any rights beyond its separate dataset license and attribution obligations;
- model weights, adapters, or training data;
- any future experiment whose dependency or distribution scope differs from the list above.

The dataset must continue to be attributed to PrimeIntellect and identified by its frozen dataset revision. The project-wide raw dataset provenance gate remains separate and open.

## 5. Final decision boundary

**Project-lead decision:** YES — the bounded documentary screen is adequate for this exact exploratory case file and the environments listed in section 2.

**Not decided:** formal legal clearance, blanket permission to redistribute upstream materials/dependencies, final case acceptance, and model-inference authorization.

The case must still pass the complete proposed-record schema checks, fail-closed registry checks, and a separate final project-lead case-acceptance decision. This decision does not place Dishka in the accepted registry.
