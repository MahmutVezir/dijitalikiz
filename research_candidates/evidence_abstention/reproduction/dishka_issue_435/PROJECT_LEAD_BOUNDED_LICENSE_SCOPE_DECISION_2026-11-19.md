# Dishka #435 — project-lead bounded documentary license-scope decision

**Decision timestamp:** 2026-11-19T15:56:05Z (18:56:05 Europe/Istanbul)  
**Decision maker:** Student project lead  
**Candidate:** `reagento__dishka-436` — issue #435 / PR #436  
**Disposition:** `no_obvious_prohibition_identified` for the exact, bounded exploratory reproduction and dataset-test scope below  
**Legal clearance:** NOT PROVIDED OR CLAIMED

## 1. Explicit project-lead decision

The project lead stated:

> Dishka için sınırlı belgesel lisans incelemesini yalnızca belirtilen araştırma ve deney ortamı kapsamında yeterli kabul ediyorum. Bunu hukuki izin olarak değil, proje liderinin kapsam kararı olarak kaydet.

This is recorded as a **project-lead scope decision** only. It is not a legal opinion, formal legal clearance, permission to redistribute source/dependencies, or a blanket license approval for other project activities.

## 2. Exact scope reviewed

The decision covers only:

1. The exact Dishka buggy-base source at commit `8718d5af93f9e48bc2506c64827663fdccc5ad89`, including the five changed files listed below.
2. The independent issue reproducer executed from the exact source using Python 3.11.9, direct `PYTHONPATH=src` import, and Python standard-library `unittest`; no upstream wheel build or package installation and no third-party runtime dependencies.
3. The isolated dataset-selector test environment using Python 3.11.9 and the explicit lock:
   - pytest 8.3.5 — MIT
   - iniconfig 2.0.0 — MIT
   - packaging 24.2 — Apache-2.0 OR BSD-2-Clause
   - pluggy 1.5.0 — MIT
   installed with `pip install --no-deps`.
4. The separate dataset-extraction environment using PyArrow 19.0.1 (Apache-2.0), used only to read the pinned public Parquet row and selector metadata; it does not execute Dishka source.

The upstream project's conditional `exceptiongroup` runtime dependency is not selected on Python 3.11.9. Build/test extras and optional integrations are outside this decision.

## 3. Source and notice evidence

- Exact buggy-base root `LICENSE`: Apache-2.0; pinned base commit `8718d5af93f9e48bc2506c64827663fdccc5ad89`.
- Root LICENSE Git blob SHA-1: `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`.
- Root LICENSE content SHA-256: `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`.
- Project metadata at the exact base also declares Apache-2.0.
- Changed-file inventory records these five paths as repository-license files:
  - `src/dishka/registry_builder.py`
  - `tests/unit/container/override/test_alias.py`
  - `tests/unit/container/override/test_context_var.py`
  - `tests/unit/container/override/test_provide.py`
  - `tests/unit/container/test_context_vars.py`
- The exact changed-file manifest SHA-256 is `34e09fdcf5d33849659490e2e50cdf80c8c5c8e6f01108dd542c60de203cf360`.
- The manifest reports no additional nested `LICENSE`, `NOTICE`, `COPYING` or copyright files beyond the root LICENSE for these changed paths.

## 4. Documentary conclusion and limits

Within the exact source files and minimal reproduction/test/extraction environments above, the project lead finds **no obvious prohibition identified** for the stated exploratory research use.

This decision does **not** cover:
- optional Dishka integrations or extras;
- the full upstream development/build/test toolchain;
- packages or native components not listed in the pinned environments;
- distribution, publication or redistribution of upstream source, binaries, dependencies, wheels, model weights or adapters;
- future experiments that change the source, package set, environment, or intended use.

Any expansion requires a new scope review. Where a legal determination is required, obtain qualified legal advice; this record must not be described as legal clearance.

## 5. Evidence references

- Changed-file license manifest: `REAGENTO_DISHKA_436_CHANGED_FILE_LICENSE_MANIFEST_V0_1.json`, SHA-256 `34e09fdcf5d33849659490e2e50cdf80c8c5c8e6f01108dd542c60de203cf360`.
- Reproduction environment lock: `reproduction_environment_lock.json`, SHA-256 `2900c96dc32539abdb34b89a3a8444277cb03ec6f5455c3c7d861b12c49807e7`.
- Dataset selector lock: `dataset_test_requirements.lock`, SHA-256 `86df530333234a4da0407f344d39b7851aac892fd9ad485a5c1ed7b9d8870d5d`.
- Candidate-specific source and Stage 2 evidence: `DISHKA_435_V02_CANDIDATE_GATE_ASSESSMENT_2026-11-19.md` and the independently checked run 44537219541 artifact 14536192821.

## 6. Effect on case acceptance

This decision closes only the **bounded project-lead documentary license-scope acknowledgement** for the exact scope stated above. It does not:
- mark Dishka accepted;
- close the project-wide source/license or raw-dataset provenance gates;
- replace schema or fail-closed registry validation;
- authorize model loading, inference, fine-tuning or training.

The case remains a proposed candidate until the complete v0.2 record passes structural validation and the project lead separately records a final acceptance decision.
