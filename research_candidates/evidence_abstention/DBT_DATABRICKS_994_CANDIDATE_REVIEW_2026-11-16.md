# databricks/dbt-databricks #994/#995 — candidate review

**Cohort rank:** 8 of 96 primary candidates  
**Dataset instance:** `databricks__dbt-databricks-995`  
**Issue:** https://github.com/databricks/dbt-databricks/issues/994  
**Fix PR:** https://github.com/databricks/dbt-databricks/pull/995  
**Buggy base:** `9e89d6ba3c6f894131df86fdd42ec93e9e71a3ad`  
**PR head:** `7579cb92ea0f39fdb8f297ea8fe444d2b8a78afe`  
**Merge commit:** `500b635afd75fc0072f5f784406b5cc7eae9d098`  
**Decision:** exclude from strict reproduction shortlist due to defect-insensitive regression tests. Stage 2 was not executed. Not an accepted case.

## 1. Issue contract

Issue #994 is labelled `bug` and reports that incremental materialization with `unique_tmp_table_suffix=True` produces temporary table names containing a UUID. The generated name includes hyphens, which are illegal in an unquoted Databricks SQL identifier. Session-close cleanup attempts to drop the table and receives an `INVALID_IDENTIFIER` error, leaving the temporary table behind.

The issue states that the temporary table is created during an incremental run and remains after session close, with warnings. Expected behavior is that the temporary table is dropped without warnings.

Issue #994 was created at `2025-04-15T21:06:28Z`. PR #995 was created at `2025-04-15T21:29:47Z` and merged at `2025-04-15T22:56:29Z`. These are distinct GitHub resources and timestamps. The dataset row's exact timestamp/resource identity must be checked against its Parquet bytes before any case can be accepted.

## 2. Source-level fix

The exact-base method is:

```python
@available
def generate_unique_temporary_table_suffix(
    self, suffix_initial: str = "__dbt_tmp"
) -> str:
    return f"{suffix_initial}_{str(uuid4())}"
```

The PR changes it to:

```python
@available
@staticmethod
def generate_unique_temporary_table_suffix(
    suffix_initial: str = "__dbt_tmp"
) -> str:
    return f"{suffix_initial}_{re.sub(r'[^A-Za-z0-9]+', '_', str(uuid4()))}"
```

This source change is mechanically consistent with the issue: hyphens and other non-alphanumeric UUID characters are replaced by underscores before the generated name reaches the cleanup path.

The PR changes exactly three files:
- `dbt/adapters/databricks/impl.py`
- `tests/unit/test_adapter.py`
- `CHANGELOG.md`

The implementation fix is plausible, but test adequacy must be assessed independently of the code change.

## 3. Regression-test defect

The PR adds two tests.

### Test 1: uniqueness

`test_generate_unique_temporary_table_suffix_adds_unique_identifier` checks that the output differs from the initial suffix, starts with the suffix, and differs from a second generated value. The buggy base already appends a fresh UUID, so this test also passes on the buggy base.

### Test 2: illegal-character check

`test_generate_unique_temporary_table_suffix_generates_no_new_illegal_characters` asserts:

```python
assert not re.match(
    r"[^A-Za-z0-9_]+",
    result.replace(suffix_initial, ""),
)
```

This assertion is not a valid whole-string character check. `re.match` only checks from the beginning of the string. For both old and new implementations, after removing `suffix_initial`, the tested suffix starts with an underscore. The first character is permitted by the negated character class, so `re.match` returns `None` immediately and the assertion passes without examining later characters. A buggy UUID such as `_a232cf9a-252c-40b4-8d10-f45e23011df4` therefore passes the assertion even though it contains hyphens.

A `re.search` check for any disallowed character, or a full-string `re.fullmatch(r"[A-Za-z0-9_]*", ...)`, would test the intended property. The PR test as written does neither.

Neither added test creates an incremental temporary table, triggers session close, or asserts that the cleanup/drop operation succeeds. The tests therefore do not directly verify the failure described in issue #994.

## 4. Stage 2 decision

| Gate | Evidence | Status |
|---|---|---|
| Issue is a defect report | Issue #994 labelled `bug`; concrete invalid identifier and cleanup failure | Pass |
| Issue/fix semantic alignment | UUID sanitization plausibly removes the reported illegal characters | Plausible |
| Exact base/fixed source pins | Base and PR head recorded above | Pass for source identity |
| Regression test sensitivity | New uniqueness test passes on old behavior; character test is defeated by `re.match` anchoring | **Fail** |
| End-to-end cleanup oracle | Added tests do not create/drop temporary tables or assert session-close cleanup | **Fail** |
| Dataset row and exact FAIL_TO_PASS selectors | Parquet row/selectors not yet authenticated in this review | Open |
| Exact environment and dependency license screen | Not assembled or run | Not run |
| Base-fail/fixed-pass logs and artifact | No run performed | Not run |

**Stage 2 result: REJECT FROM STRICT REPRODUCTION SHORTLIST.** The observed tests do not establish the predeclared fail-on-buggy-base/pass-on-fixed requirement for this defect. Do not run the upstream candidate tests expecting them to provide a valid defect-specific reproduction, and do not repair their assertions inside the study as though that were the frozen dataset oracle.

A separately written diagnostic test could demonstrate that the changed helper returns a sanitized UUID, but it would be a new test, not the dataset's original defect-specific FAIL_TO_PASS oracle. Under the fixed protocol, that does not rescue this candidate.

## 5. License and provenance notes

- Exact-base `pyproject.toml` blob: `15735f00aa4c0c79b1b4705523cd92f9cdc373e1`; declares Apache-2.0.
- Exact-base root `License.md` blob: `8dada3edaf50dbc082c9a125058f25def75e625a`; contains Apache License 2.0.
- Changed implementation/test/changelog files are inside the upstream repository and are covered by the declared repository license.
- The dependency set in the project metadata is substantially larger than a minimal helper-only reproducer; it was not installed or executed for this candidate.

This is a narrow source-level license screen, not blanket clearance for the full dependency tree, optional extras, external services, or redistribution.

## 6. Independence, exposure, and acceptance

- Maximum contribution from `databricks/dbt-databricks`: one accepted case.
- Researcher screening of issue and patch is exposure and must be recorded; perfect blinding must not be claimed.
- The exact Parquet row, fork/lineage and related-defect checks, model exposure, and nested evidence packet were not completed because the test-sensitivity gate failed.
- Technical gold and E1/E2/E3 adjudication were not started.
- Case acceptance: `not_accepted`.
- Model inference authorization: `false`.

This exclusion is a second-pass technical test-oracle decision. The original frozen 96-row metadata ledger remains unchanged; the candidate-yield review records this post-screen adjustment separately.
