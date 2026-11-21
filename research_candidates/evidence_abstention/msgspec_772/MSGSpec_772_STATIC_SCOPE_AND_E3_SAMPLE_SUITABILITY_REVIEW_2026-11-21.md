# msgspec #772 / issue #769 — static scope and E3 sample-suitability review

**Date:** 21 November 2026  
**Candidate:** msgspec/msgspec issue #769 / fix PR #772  
**Cohort rank:** 44 of 96  
**Disposition:** **STRONG TECHNICAL BUG ALIGNMENT; E3 ANSWERABILITY / CLUE-LEAKAGE RISK; NO STAGE 2 EXECUTION**

## 1. Scope and exact upstream identity

- Issue: https://github.com/msgspec/msgspec/issues/769
- PR: https://github.com/msgspec/msgspec/pull/772
- Issue created: `2024-11-12T00:09:42Z`.
- PR created: `2024-11-15T17:19:04Z`.
- Exact PR base: `148f9a17e04915dcb50be96efc6a3e6732340a5a`.
- Exact PR head: `8d330971506111b0fe525bc157dbf54d2ce6330e`.
- Merge commit: `595c33c4a71c6d0c539b82233982a65819e240cf`.
- Changed files: `msgspec/_utils.py`, `tests/test_utils.py`.

## 2. Static source and patch alignment

At the exact buggy base, `msgspec/_utils.py` blob `2a8a5715b87426ba159d8626910e7dffa215463c`, `_apply_params` obtains `params` via `getattr(obj, '__parameters__', None)` and then immediately iterates it to create `tuple(mapping.get(p, p) for p in params)`. It assumes that every truthy `__parameters__` value is iterable.

The issue body explicitly states that `types.UnionType` returns a descriptor for `__parameters__`, rather than a tuple of type parameters. Attempting to iterate this descriptor raises `TypeError: 'getset_descriptor' object is not iterable`.

At the exact fixed PR head, `msgspec/_utils.py` blob `7761b07f967638b341436564e9d9394f79a8eb5d`, `_apply_params` handles TypeVar first, then attempts `tuple(obj.__parameters__)` inside `try/except Exception`. If accessing or materializing parameters fails, it returns the original object unchanged. Empty parameters also return the original object; only valid non-empty parameter tuples are substituted.

The PR adds `test_generic_invalid_parameters` in `tests/test_utils.py` blob `a991b42f7c4c1ea2379fd11a978f526e192b3124`. It constructs a class with an invalid `__parameters__` property, uses it as a generic base parameter, and expects `get_class_annotations(Sub) == {'x': Invalid}`.

Technical alignment is strong: the issue's descriptor-not-iterable symptom maps directly to the unguarded iteration, and the patch changes that path by safely materializing the attribute before iterating.

## 3. E3 answerability and leakage risk

The issue body itself includes all of the following:
- the exact failing function `_utils._apply_params`;
- the failing assumption that `__parameters__` is iterable;
- the actual problematic type, `types.UnionType`;
- an explicit observation that `UnionType.__parameters__` returns a descriptor;
- the exact `TypeError` message;
- a workaround that avoids applying parameters to `types.UnionType`.

This is unusually diagnostic E3 evidence. A model does not need E1 source access to identify the key failure: a descriptor is being treated as an iterable collection of type parameters. The reporter's workaround directly names the special case.

**Advisory recommendation:** do not use msgspec #769 as a primary abstention case under a rubric that credits a correct evidence-supported diagnosis at E3. At E3, a reasonably competent model can already explain the descriptor/iteration mismatch and propose a safe guard. The candidate is more suitable as a separately-labelled easy-answer / evidence-sufficient control, but only if the preregistered design allows such controls and the project lead explicitly authorizes it. Do not count it toward the primary abstention sample.

## 4. Issue/PR scope notes

The issue body has no minimal reproduction at opening and includes a full traceback plus a workaround. A later issue comment (id `2477766484`) supplies a concrete Python 3.13 reproducer using `types.UnionType` as a generic base in a `msgspec.Struct`, then round-trips through MessagePack. This comment is not part of the frozen issue `problem_statement` and must not be silently added to E3. Researcher exposure includes it.

PR #772 adds a generic invalid-`__parameters__` regression test rather than the exact `UnionType` example. The patch is broader than a special-case check for `UnionType`: it guards both access to and tuple conversion of `__parameters__`, returning the original object when the attribute is absent or invalid. This scope appears consistent with the issue symptom, but Stage 2 would be needed to verify exact row selectors and base/fixed behavior. No such execution has been done.

## 5. Temporal exposure note

The issue was filed on 12 November 2024, after the public Qwen2.5 announcement on 19 September 2024 and after the checkpoint weights were initially uploaded to Hugging Face in September 2024. This reduces the likelihood that the exact issue/PR text was in the pinned released Qwen2.5-3B-Instruct checkpoint's pre-release training corpus. It does not prove the model's exact training cutoff and does not rule out exposure to pre-existing msgspec source code.

Researcher exposure is full for the issue, comments, PR, source and tests. No blind adjudication or inter-rater claim is made. Project-lead prior pipeline/debug exposure declaration is pending.

## 6. Stage 2 and acceptance boundary

- No independent reproducer has been created or executed in this review.
- No exact SWE-rebench row has been extracted or authenticated.
- No frozen selector has been run on the exact buggy base and fixed revision.
- No Stage 2 artifact or digest is claimed.
- No model has been loaded and no inference, fine-tuning or training has been performed.
- Final case acceptance: **not accepted**; registry inclusion: **false**; inference authorization: **false**.

## 7. Next decision gate

Keep msgspec #769 on a primary-sample suitability hold. The project lead should decide whether it is excluded from the primary abstention sample or retained only as a separately-labelled easy-answer control. Stage 2 should not be run for primary-sample eligibility unless that scope decision is approved; technical reproducibility alone would not solve the E3 clue-leakage problem.