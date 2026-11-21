# jsonpickle #565 / issue #564 — static scope and E3 sample-suitability review

**Date:** 21 November 2026  
**Candidate:** jsonpickle/jsonpickle issue #564 / fix PR #565  
**Cohort rank:** 47 of 96  
**Disposition:** **TECHNICAL ISSUE/PR ALIGNMENT STRONG; E3 ALREADY EXPOSES THE FAILURE PATH; HOLD OUT OF PRIMARY ABSTENTION SAMPLE; NO STAGE 2 EXECUTION**

## 1. Frozen upstream identity

- Issue: https://github.com/jsonpickle/jsonpickle/issues/564
- Fix PR: https://github.com/jsonpickle/jsonpickle/pull/565
- Issue created: `2025-06-05T23:52:17Z`.
- PR created: `2025-06-08T19:40:12Z`.
- Exact PR base: `9a6822734ea5d06967c0c514db3c5d577d6c1dc2`.
- Exact PR head: `78f102d1e2cc7fc23c5ef8c7c696f692026f38ea`.
- Merge commit: `10b1b4236823d4723e941f8e2cb89c44f58ecf6d`.
- Changed files: `CHANGES.rst`, `jsonpickle/unpickler.py`, `tests/jsonpickle_test.py`.

## 2. Static source and patch alignment

At the exact buggy base, `jsonpickle/unpickler.py` blob `0821579f6ae36185b49a05407f154e757fe4156b`, `_restore_reduce` parses the reduction tuple into `f`, `args`, and `state`, and then invokes `stage1 = f(*args)` for ordinary callable constructors. The decoded example has only the positional tuple item `"a"`; the required keyword-only field `b` is not passed through that call. The traceback in issue #564 points directly to this line and reports `Foo.__init__() missing 1 required keyword-only argument: 'b'`.

The serialized issue example is:

`{"py/reduce": [{"py/type": "__main__.Foo"}, {"py/tuple": ["a"]}, {"a": "a", "b": "b"}]}`

The state dictionary contains both `a` and `b`, but the default reconstruction path invokes the class constructor with the positional arguments only. Thus a required keyword-only parameter is missing at constructor call time, even though the relevant value will be available in the later state restoration phase.

At the exact fixed PR head, `jsonpickle/unpickler.py` blob `b36533eec0a3b0c6a928b49ff985e746124b0716`, the constructor call is wrapped in `try/except TypeError`. If the call fails, jsonpickle constructs an uninitialized instance with `f.__new__(f, *args)`, then continues into the existing state-restoration logic.

The PR adds a regression class `KwargsSubclassTest(Exception)` with `__init__(self, a, *, b)` and a test that encodes and decodes an instance, asserting the restored object has the same type and computed state. This directly aligns with the issue.

## 3. E3 answerability / sample-suitability risk

The frozen issue body itself provides:
- a minimal class with `__init__(self, a, *, b)`;
- a direct `jsonpickle.encode` / `jsonpickle.decode` example;
- the serialized `py/reduce` payload showing positional `args` contains only `"a"` while the state dictionary contains `a` and `b`;
- the full traceback pointing to `stage1 = f(*args)` in `_restore_reduce`;
- the exact TypeError stating that the required keyword-only argument `b` is missing.

That is strong causal evidence at E3. A model can infer that the restoration path invokes the constructor without keyword arguments and that the state dictionary is applied only after construction. The likely repair direction—avoid calling `__init__` when the pickled positional arguments cannot satisfy the signature, allocate with `__new__`, then restore state—is also strongly suggested by the supplied payload and traceback.

**Advisory recommendation:** do not use jsonpickle #564 as a primary abstention case under a rubric that accepts evidence-supported diagnosis from an exact minimal reproduction and traceback. It may be retained as a separately labelled easy-answer / evidence-sufficient control only if the preregistered study design explicitly permits such controls and the project lead authorizes it. Do not count it toward the primary abstention sample.

## 4. Patch-risk caveat (not a reason to force primary inclusion)

The PR catches `TypeError` around the constructor call and falls back to `f.__new__(f, *args)`. At source level, this catch is broader than a narrowly identified missing-keyword binding error: a `TypeError` raised inside a constructor body could also enter the fallback path. This is a legitimate technical review question about the generality of the patch, but it does not make the original E3 diagnosis uncertain. The issue's traceback points specifically to a missing required keyword-only argument at call binding time.

No claim is made here that the patch is universally safe for every constructor with internal TypeError behavior. That would require separate tests and a broader compatibility review.

## 5. Temporal and researcher-exposure note

- Issue #564 was created on 5 June 2025 and PR #565 on 8 June 2025, both after the public September 2024 Qwen2.5 release and the initial upload of the pinned checkpoint weights. This lowers the likelihood of issue/PR-specific training exposure, but does not prove the exact model training-data cutoff or rule out exposure to pre-existing jsonpickle source code.
- Researcher exposure is full for the issue, comments, PR diff, exact base/fixed source, and regression tests reviewed here. No blinded adjudication or inter-rater reliability claim is made.
- Project-lead prior pipeline/debug exposure declaration is pending and must be answered separately.

## 6. Stage 2 and acceptance boundary

- No independent reproducer has been created or executed in this review.
- No exact SWE-rebench row has been extracted or authenticated.
- No frozen selector has been run on the exact buggy base and fixed revision.
- No Stage 2 build, artifact, digest, CRC result or selector outcome is claimed.
- Project-lead decision on exclusion versus a separately labelled easy-answer/evidence-sufficient control: pending.
- Final case acceptance: **not accepted**; registry inclusion: **false**; inference authorization: **false**.
- Model loading, inference, fine-tuning and training: **not performed and not authorized**.