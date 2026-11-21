# Modin #7554 — candidate technical review and Stage 2 result

**Review date:** 17 November 2026  
**Frozen cohort rank:** 22  
**Dataset instance:** `modin-project__modin-7554`  
**Dataset row SHA-256:** `02d8f6266c2b60eb29cb417fb1c157bd56ebe2152e39b53bcadd423e4490631a`  
**Dataset revision:** `fb9aa226b2ce37c708ea7732e7b980abacdadb67`  
**Issue:** [modin-project/modin #7553](https://github.com/modin-project/modin/issues/7553)  
**Fix PR:** [modin-project/modin #7554](https://github.com/modin-project/modin/pull/7554)

## 1. Decision

- **Technical Stage 2 result:** passed for the exact two frozen selectors. Both selectors were executed on the exact buggy base and each produced a real `NotImplementedError` test failure; the identical selectors both passed on the exact fixed commit in the pinned environment.
- **Dataset case count:** one frozen dataset row / one project case. The two parameterized selectors are not two independent cases.
- **Scope classification:** conditional hold. Issue #7553's title says `AutoSwitchBackend is on`; PR #7554's description says the bug occurred while it was off; both frozen selector IDs explicitly select `auto_switch_backend_False`. The issue body is empty in the retrieved GitHub issue record and has no comments. The release note and PR description corroborate the disabled/False interpretation, but the title/contract discrepancy is not silently rewritten. A separate human scope decision is still required.
- **Stage 3:** not started. Full dependency/license scope, project independence/related-defect clustering, exposure assessment and human gold/alternative/E1/E2/E3 adjudication remain pending.
- **Final case acceptance:** not granted. Accepted independent case count remains **0**.
- **Model boundary:** no model was loaded; no inference, fine-tuning, or training was performed.

This review distinguishes the technical test result from the issue-scope decision. A pinned base-fail/fixed-pass does not independently settle the issue-title/PR-contract discrepancy.

## 2. Frozen row identity and selectors

Immutable Parquet:
- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`

Authenticated dataset row:
- `instance_id`: `modin-project__modin-7554`
- `repo`: `modin-project/modin`
- `base_commit`: `1817ae423ba86c467f5a737817a8c00653be75cb`
- `created_at`: `2025-05-02 19:12:19`
- `language`: Python
- `license`: Apache-2.0
- `FAIL_TO_PASS` selector count: 2

Exact selectors, with the original parameter IDs preserved:
```
modin/tests/pandas/native_df_interoperability/test_compiler_caster.py::TestSwitchBackendPostOpDependingOnDataSize::test_auto_switch_config_can_disable_groupby_agg_auto_switch[auto_switch_backend_False-DataFrameGroupBy]
modin/tests/pandas/native_df_interoperability/test_compiler_caster.py::TestSwitchBackendPostOpDependingOnDataSize::test_auto_switch_config_can_disable_groupby_agg_auto_switch[auto_switch_backend_False-SeriesGroupBy]
```

The canonical selected-row JSON hash matched the expected row SHA-256. The evidence artifact retains only the row hash and limited metadata summary; it does not contain the Parquet, canonical row or full problem statement.

## 3. Issue/PR scope discrepancy — explicit hold

Issue #7553:
- Title: `Using groupby while AutoSwitchBackend is on tries to pin the backend of DataFrameGroupy, raising NotImplementedError`.
- Retrieved issue body: `null` (empty).
- Retrieved issue comment count: 0.
- State: closed on 2 May 2025.

PR #7554:
- Title: `FIX-#7553: Fix groupby when AutoSwitchBackend is disabled.`
- PR description says that groupby while `AutoSwitchBackend` was off raised `NotImplementedError`.
- Exact frozen selectors both set `auto_switch_backend_False`.
- The Modin release note for PR #7554 describes the fix as making groupby work when `AutoSwitchBackend` is disabled.

Therefore:
- The exact data selectors, PR description, and release-note wording consistently test the `False`/disabled configuration.
- The issue title says `on`, and the issue body provides no clarification.
- The exact test path is a technical reproduction of the PR's disabled/False contract. It does not establish that the title's enabled/True contract was also fixed.

**Disposition:** technical reproduction is confirmed, but the candidate remains conditional until a human reviewer resolves whether the issue title is a wording error or the PR/test scope only covers one configuration of a broader issue. No automatic correction of the issue title or reinterpretation of the frozen row is made.

## 4. Source change and defect-specific failure

Exact upstream base:
`1817ae423ba86c467f5a737817a8c00653be75cb`

Exact fixed commit:
`48ef1adda0b09791081909ffc267730e265b2f88`

Source blobs:
- Base `modin/core/storage_formats/pandas/query_compiler_caster.py`: `a7bf3a19644100682166debcb15bc76f50c7a6ea`
- Fixed `modin/core/storage_formats/pandas/query_compiler_caster.py`: `3027d238563a6102c5e48c8761d5d8e1bfb94b90`
- Base test file `modin/tests/pandas/native_df_interoperability/test_compiler_caster.py`: `1f6ada74433d930179144bf25d7bf3ffd548ad69`
- Fixed test file: `688a568551989e62eb71e70c024f669a7bc3bf03`

In the base `register_query_compilers` wrapper, the branch for `not AutoSwitchBackend.get()` also unconditionally calls `_set_backend_pinned(True)` on a `QueryCompilerCaster` result. GroupBy aggregation results may be `QueryCompilerCaster` objects that do not implement that pinning operation, producing `NotImplementedError`.

The fix computes whether the inputs themselves were pinned (`inputs_pinned`) and:
1. executes the extension directly when AutoSwitchBackend is disabled or when the single input is already pinned; and
2. sets the output's pin state only when `inputs_pinned` is true.

The regression test covers both:
- `DataFrameGroupBy.sum()`, and
- `SeriesGroupBy["col1"].sum()`,

under `AutoSwitchBackend=False`. It checks that the result remains on the configured `Big_Data_Cloud` backend and matches pandas' result.

## 5. Test-only base preparation

The full production PR diff was **not** applied to the buggy base.

Only the exact regression method from the fixed test file was inserted into the base test file, so the two frozen parameter selectors could execute. The base production source blob remained unchanged:
`a7bf3a19644100682166debcb15bc76f50c7a6ea`.

Test-only preparation summary:
- Changed path: `modin/tests/pandas/native_df_interoperability/test_compiler_caster.py` only.
- Inserted method: 99 lines.
- Inserted method SHA-256: `881e1b8bb3274f2eef58e225688e562efd8efa7c78eae41de3bd830d09d2ede8`.
- No production code change on buggy base.
- No unrelated pre-existing xfail cases removed from buggy base.

## 6. Pinned Stage 2 run

**Canonical GitHub Actions run:** [44137294820](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44137294820)  
**Job ID:** `134230204005`  
**Research branch head:** `89af774a7572874e61f531a3a5166a4487785e9b`  
**Workflow:** `.github/workflows/modin-7554-stage2-pinned.yml`

Pinned runtime:
- Ubuntu 22.04 runner
- CPython 3.11.9
- pip 24.3.1
- pytest 8.3.5
- Modin `0.32.0+55.g1817ae42` from exact editable source checkout
- pandas 2.2.3
- NumPy 1.26.4
- 16 external/runtime lock entries; 17 installed distribution metadata records including editable Modin.
- Installed `pip freeze` matched `requirements.lock` exactly.
- `pip check`: `No broken requirements found.`
- All 17 distribution records contained license metadata. Metadata completeness is not legal license approval.

Observed exact selector results:

| Frozen selector | Buggy base | Fixed commit |
|---|---|---|
| DataFrameGroupBy / AutoSwitchBackend=False | `NotImplementedError: This functionality is not yet available in Modin.` | Pass |
| SeriesGroupBy / AutoSwitchBackend=False | `NotImplementedError: This functionality is not yet available in Modin.` | Pass |

The runner reported both as executed test failures on the buggy base (pytest return code 1), not collection/setup errors, and both passed on the exact fixed commit (return code 0).

## 7. Sanitized evidence integrity

**Canonical artifact:** [modin-7554-pinned-exact-selector-evidence](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44137294820/artifacts/14352871592)  
**Artifact ID:** `14352871592`  
**Size:** 38,077 bytes  
**ZIP SHA-256:** `1eb504d1eafedd1caf395d3731ac4b736302c87b00effdea4234fc9896fffded`

Artifact downloaded and independently inspected:
- 12/12 internal SHA-256 entries verified.
- External ZIP SHA-256 matched the GitHub Actions artifact digest.
- Contains the exact requirements lock, installed freeze, dependency metadata inventory, runtime summary, source provenance, dataset row hash/summary, test-only patch scope, and sanitized base/fixed selector result summaries.
- Does not contain the Parquet, canonical row, issue problem statement, full PR diff, inserted test source contents, raw stdout, or full pytest logs.
- The base failure summary stores the actual traceback exception line: `E       NotImplementedError: This functionality is not yet available in Modin.`

## 8. Remaining gates

1. **Issue contract reconciliation:** obtain an independent human decision on the issue-title `on` versus PR/frozen-selector `off/False` discrepancy. Until then this candidate remains conditional and must not be treated as an unqualified issue-level confirmation.
2. Review the complete dependency/license scope for all direct/transitive distributions and bundled/native components. The root Apache-2.0 LICENSE and NOTICE, and package metadata presence, do not substitute for a complete obligation review.
3. Complete upstream project independence and related-defect clustering.
4. Complete researcher source-exposure and model training-data/exposure assessment.
5. Stage 3 gold mechanism, plausible alternatives, E1/E2/E3 and independent human adjudication.
6. Complete case-acceptance record schema and fail-closed registry audit before final acceptance.

**Final disposition:** pinned exact-selector technical reproduction = passed; scope classification = conditional hold; Stage 3 = not started; final accepted case = no. The accepted independent case count remains 0. No model inference or training was performed.
