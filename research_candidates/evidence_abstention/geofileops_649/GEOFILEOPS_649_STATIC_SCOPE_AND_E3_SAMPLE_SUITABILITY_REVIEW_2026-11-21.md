# GeofileOps #649 / issue #648 — static scope and E3 sample-suitability review

**Date:** 21 November 2026  
**Candidate:** geofileops/geofileops issue #648 / fix PR #649  
**Cohort rank:** 49 of 96  
**Disposition:** **ISSUE/PR TECHNICAL ALIGNMENT STRONG FOR DEFAULT DESTINATION-LAYER BEHAVIOR; E3 ALREADY STATES THE MISMATCH; PR HAS BROADER ADJACENT CHANGES; HOLD OUT OF PRIMARY ABSTENTION SAMPLE; NO STAGE 2 EXECUTION**

## 1. Frozen upstream identity

- Issue: https://github.com/geofileops/geofileops/issues/648
- Fix PR: https://github.com/geofileops/geofileops/pull/649
- Issue created: `2025-03-06T14:07:54Z`.
- PR created: `2025-03-06T15:39:28Z`.
- Exact PR base: `f7f8a4cf49b1278f3e9e5f4157718de441a21b57`.
- Exact PR head: `ec1438fbf8527269cd1193647d05c8d7fdb83802`.
- Merge commit: `d475d6d2ec5719c7f00d1e441e1cdbe0765087b7`.
- Changed files: `CHANGELOG.md`, `geofileops/fileops.py`, `geofileops/util/_geoops_gpd.py`, `geofileops/util/_geoops_sql.py`, `tests/test_geofile.py` (9 files reported across the PR; file list retrieved above).

## 2. Static issue/PR alignment

The issue title itself states: `BUG: in copy_layer and append_to the default dst_layer is not the stem of the filename`.

The issue body is short and says the documentation specifies the expected behavior, notes that this is inconsistent with the rest of `geofileops`, and acknowledges that changing it may be backward-incompatible. It does not include a minimal code example, a concrete observed output, or a stack trace.

The PR title repeats the same contract: `the default dst_layer in copy_layer and append_to is not the stem of the filename`.

At the exact buggy base, `geofileops/fileops.py` leaves `dst_layer` as `None` in the public `append_to` and `copy_layer` paths and eventually uses it in layer creation/appending without deriving a default from the destination path.

At the exact fixed PR head, the relevant changes add:

- in `append_to`: `if dst_layer is None: dst_layer = get_default_layer(dst)`;
- in the internal `_append_to_nolock` path: the same default derivation when `dst_layer` is None;
- in `copy_layer`: `if dst_layer is None: dst_layer = get_default_layer(dst)`.

The PR adds `test_copy_layer_layer`, parameterized over `dst_layer=None` and an explicit layer name, asserting that a missing layer argument selects `dst.stem` and an explicit name remains respected.

The primary issue-to-patch contract is clear: missing default layer naming is corrected by deriving the default from the destination file stem.

## 3. E3 answerability / sample-suitability risk

The issue title directly states both the affected API methods and the expected-vs-actual mismatch: the default `dst_layer` is not the destination filename stem. The PR title repeats that diagnosis. The body says the documentation already specifies the expected behavior.

A model does not need exact source code to infer the required behavior: when `dst_layer` is omitted, derive it from the destination filename stem for `copy_layer` and `append_to`. The likely implementation is explicitly visible in the PR title and can be inferred from the issue title and documented contract.

**Advisory recommendation:** do not include GeofileOps #648 as a primary abstention case under a rubric that accepts a correct diagnosis of the default-value mismatch. It may be retained as a separately labelled easy-answer / specification-conformance control only if the preregistered study design explicitly allows such controls and the project lead authorizes it. Do not count it toward the primary abstention sample.

## 4. PR breadth and scope risk

PR #649 changes more than the default layer behavior:
- updates the `append_to` and `copy_layer` default layer logic and documentation;
- modifies internal geo-operation callers to pass explicit `src_layer` and `dst_layer` values;
- changes `get_layerinfo` and `add_column` calls to pass `layer` explicitly;
- changes an exception wrapper from `Exception` to `RuntimeError` in a geo-operation path;
- adjusts tests, fixture sizes, test helper behavior and formatting configuration;
- adds `print(np.mean(is_impure))`? No such line is present in this PR; do not confuse it with the separate scikit-activeml #504 debug-print observation.

The PR is therefore broader than a single isolated default-parameter correction. The added layer-name regression test does directly cover the target defaulting contract, but the remaining geo-operation changes would need separate scope mapping if Stage 2 were ever authorized. Do not count each adjacent change/test as another case.

## 5. Temporal and researcher-exposure note

- Issue #648 and PR #649 were created on 6 March 2025, after the public September 2024 Qwen2.5 release and the initial public checkpoint upload. This reduces the likelihood of issue/PR-specific exposure in the pinned checkpoint's pre-release training data, but does not prove the exact cutoff or rule out exposure to pre-existing GeofileOps source code.
- Researcher source exposure is full for the issue, PR diff, exact base/fixed source and tests reviewed here. No blind adjudication or inter-rater claim is made.
- Project-lead prior pipeline/debug exposure declaration remains pending.

## 6. Stage 2 and acceptance boundary

- No independent reproducer has been created or executed in this review.
- No exact SWE-rebench row has been extracted or authenticated.
- No frozen selector has been run on exact buggy base and fixed revisions.
- No Stage 2 build, artifact, digest, CRC result or selector outcome is claimed.
- Project-lead decision on exclusion versus a separately labelled easy-answer/specification-conformance control: pending.
- Final case acceptance: **not accepted**; registry inclusion: **false**; inference authorization: **false**.
- Model loading, inference, fine-tuning and training: **not performed and not authorized**.