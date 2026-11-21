# scikit-activeml #504 / issue #503 — static scope and E3 sample-suitability review

**Date:** 21 November 2026  
**Candidate:** scikit-activeml/scikit-activeml issue #503 / fix PR #504  
**Cohort rank:** 48 of 96  
**Disposition:** **TECHNICAL ISSUE/PR ALIGNMENT STRONG; E3 DIRECTLY DISCLOSES ROOT CAUSE; HOLD OUT OF PRIMARY ABSTENTION SAMPLE; NO STAGE 2 EXECUTION**

## 1. Frozen upstream identity

- Issue: https://github.com/scikit-activeml/scikit-activeml/issues/503
- Fix PR: https://github.com/scikit-activeml/scikit-activeml/pull/504
- Issue created: `2025-05-14T11:41:05Z`.
- PR created: `2025-05-14T12:46:53Z`.
- Exact PR base: `8bc5882a47ad9a9600c5806ea56987c2892167cb`.
- Exact PR head: `59d3a890c16983d96e2a0dc34ade9d9036cc385f`.
- Merge commit: `2c6a86aaf707b37270c8a925eb3b32083b98b272`.
- Changed files: workflow/docs/config files plus ProbCover and TypiClust source and tests (9 files total).

## 2. Static source and patch alignment

The issue title is `BUG: Propagate random_state to cluster_algo in TypiClust and ProbCover`. The issue body says:

> “Currently, the `random_state` set as `__init__` parameter of the query strategies `TypiClust` and `ProbCover` is not explicitly propagated to the `cluster_algo` but the user must set its `random_state` via `cluster_algo_dict`.”

It gives the explicit contrast:
- `TypiClust(random_state=0)` is not deterministic, while `TypiClust(random_state=0, cluster_algo_dict={"random_state": 0})` is.
- The same contrast is provided for `ProbCover`.

At the exact buggy base, the TypiClust query path injects `n_clusters` into `cluster_algo_dict` and then constructs `self.cluster_algo(**cluster_algo_dict)` without forwarding the query strategy's own `self.random_state`. The ProbCover path similarly creates/uses a copy of `cluster_algo_dict` and calls the clustering algorithm without adding the strategy-level random state.

At the exact fixed PR head, both paths inspect `signature(self.cluster_algo.__init__).parameters`, check whether the algorithm supports `random_state`, check whether `cluster_algo_dict` already provides it, and—when the strategy's own `random_state` is not None and the algorithm supports that parameter—copy the strategy random state into the clustering algorithm kwargs.

The fix deliberately preserves an explicit `cluster_algo_dict["random_state"]` value rather than overriding it. This follows the issue's requested propagation semantics while allowing a caller-specified cluster algorithm seed to take precedence.

## 3. E3 answerability / sample-suitability risk

The E3 issue statement already identifies:
- the two affected algorithms (`TypiClust` and `ProbCover`);
- the exact missing data flow (strategy `random_state` is not propagated to `cluster_algo`);
- the workaround (manually pass `random_state` through `cluster_algo_dict`);
- the observable consequence (the default construction is not reproducible).

That is almost a full causal diagnosis. A model does not need source code or test execution to infer that `self.random_state` should be forwarded into `cluster_algo` unless the caller has explicitly supplied `random_state` in `cluster_algo_dict`.

**Advisory recommendation:** do not use scikit-activeml #503 as a primary abstention case under a rubric that credits a correct diagnosis of the missing random-state propagation. It may be retained as a separately labelled easy-answer / evidence-sufficient control only if the preregistered study design explicitly permits such controls and the project lead authorizes it. Do not count it toward the primary abstention sample.

## 4. Additional patch-quality observation

The PR diff adds `print(np.mean(is_impure))` inside the ProbCover query path. This appears unrelated to random-state propagation and is potentially an unintended debug print in a library method. It is present at the exact PR head in `skactiveml/pool/_prob_cover.py`; it was not present at the base. A separate code-quality review should determine whether it is intended, whether it leaks unwanted stdout, and whether it should be removed.

The PR also changes the tests to use larger deterministic synthetic data, adds reproducibility checks comparing repeated runs on the same strategy instance and two separately initialized strategy instances, and updates formatting configuration. Those are ancillary changes and should not be mistaken for independent defect cases.

## 5. Temporal and researcher-exposure note

- Issue #503 was created on 14 May 2025 and PR #504 on 14 May 2025, after the public September 2024 release of Qwen2.5-3B-Instruct. This reduces the likelihood of exact issue/PR text being present in the released checkpoint's pre-release training data, but does not prove the exact model training-data cutoff or rule out exposure to pre-existing scikit-activeml source code.
- Researcher exposure is full for issue, PR diff, exact base/fixed source and tests reviewed here. No blind adjudication or inter-rater reliability claim is made.
- Project-lead prior pipeline/debug exposure declaration remains pending.

## 6. Stage 2 and acceptance boundary

- No independent reproducer has been created or executed in this review.
- No exact SWE-rebench row has been extracted or authenticated.
- No frozen selector has been run on exact buggy base and fixed revisions.
- No Stage 2 artifact, archive hash, CRC result or selector outcome is claimed.
- Project-lead decision on exclusion versus a separately labelled easy-answer/evidence-sufficient control: pending.
- Final case acceptance: **not accepted**; registry inclusion: **false**; inference authorization: **false**.
- Model loading, inference, fine-tuning and training: **not performed and not authorized**.