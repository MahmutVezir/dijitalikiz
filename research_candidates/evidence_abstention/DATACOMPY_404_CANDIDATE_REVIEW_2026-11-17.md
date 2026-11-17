# DataComPy #404 — candidate scope and target-test suitability review

**Review date:** 17 November 2026  
**Frozen cohort rank:** 27  
**Dataset instance:** capitalone__datacompy-404  
**Dataset row SHA-256:** 960a975dc433d1357dbeb575fba8ae15ef68ed9609866293ff4493b6804325fd  
**Dataset revision:** fb9aa226b2ce37c708ea7732e7b980abacdadb67  
**Issue:** [capitalone/datacompy #58](https://github.com/capitalone/datacompy/issues/58)  
**Fix PR:** [capitalone/datacompy #404](https://github.com/capitalone/datacompy/pull/404)

## 1. Decision

**Disposition: hold — mixed scope and issue-specific target-test mismatch.**

The upstream issue #58 is narrow: comparing two equal empty NumPy arrays should not report inequality. The frozen SWE-rebench row for PR #404 contains three selectors:
1. NumPy array compatibility,
2. Python list compatibility,
3. Polars list compatibility.

The NumPy selector itself is a broad feature/regression method. Its first assertion compares non-empty one-element arrays and occurs before the empty-array assertions at the end of the method. In the exact base implementation, pandas.api.types.infer_dtype() classifies the non-empty ndarray object series as mixed; the base columns_equal() branch then returns an all-False Series. Thus the method can fail on generic array support **before it reaches the empty-array case reported in issue #58**. The other two frozen selectors explicitly test list/Polars-list support, not issue #58's empty-NumPy-array condition.

The row's selectors will not be silently filtered, replaced, or re-labelled. No Stage 2 test run was performed for this candidate because the immutable selector set fails the issue-specific scope/oracle gate before execution. This is a methodological hold, not a claim that the upstream fix is technically wrong.

- **Stage 2:** held before execution; no base/fixed selector result is claimed.
- **Stage 3:** not started.
- **Final case acceptance:** not granted; accepted-case count remains 0.
- **Model boundary:** no model loading, inference, fine-tuning, or training.

## 2. Frozen dataset row identity

Immutable dataset:
- Dataset: PrimeIntellect/SWE-rebench-V2-Filtered-Verified
- Revision: fb9aa226b2ce37c708ea7732e7b980abacdadb67
- Parquet SHA-256: 7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9

Authenticated row:
- instance_id: capitalone__datacompy-404
- repo: capitalone/datacompy
- base_commit: 5ab81a14c59728c7ed338a855d1a94c7c1425259
- created_at: 2025-04-17 23:56:12
- language: Python
- license: Apache-2.0
- Frozen selector count: 3
- Canonical row SHA-256: 960a975dc433d1357dbeb575fba8ae15ef68ed9609866293ff4493b6804325fd

### Exact frozen selectors

~~~text
tests/test_core.py::test_columns_equal_numpy_arrays
tests/test_core.py::test_columns_equal_lists
tests/test_polars.py::test_columns_equal_lists
~~~

The row problem statement contains NumPy/array/empty-array language, but it does not contain the literal issue number #58. The issue/PR link is separately established by PR #404's body: “This should fix #58.” Issue #58's own description specifically demonstrates two equal np.array([]) values being treated as unequal.

## 3. Issue and PR scope

Issue #58:
- Title: Inequality when comparing two empty numpy arrays.
- Body describes two equal empty NumPy arrays being reported unequal and gives a DataFrame-level reproduction.
- State: closed.
- Labels include bug/help wanted/question.

PR #404:
- Title: feat: Compatibility for Array and Lists.
- Body: “This should fix #58”.
- Changed paths include datacompy/core.py, datacompy/polars.py, Pandas and Polars tests, Spark tests, and .gitignore.
- It adds general list/NumPy-array support to the pandas comparator and list/array type compatibility to the Polars comparator.

The PR includes an empty-NumPy-array assertion, but it is embedded at the end of a broader test method that first checks non-empty ndarray equality/mismatch behavior. The two list selectors also belong to the wider feature, not the narrowly stated issue.

## 4. Why the frozen NumPy selector is not issue-specific

Exact base source:
- datacompy/core.py blob: 9e88d057ce3bdc07194d7b63f477ada548af09ec
- tests/test_core.py blob: 1534cc43dbf5abfb4f1c0af6dc831d60e575e603

Exact fixed source:
- datacompy/core.py blob: 09ea1813315f413bc12f8c26309c6edfe2c2b58b
- tests/test_core.py blob: 4040c478b52e640574d9ca64263f52b54a84958e

On the buggy base, columns_equal() has this mixed-type short-circuit:

~~~python
if pd.api.types.infer_dtype(col_1).startswith("mixed") or pd.api.types.infer_dtype(
    col_2
).startswith("mixed"):
    compare = pd.Series(False, index=col_1.index)
~~~

For the exact test's first inputs:

~~~python
df1 = pd.DataFrame({"array_col": [np.array([j]) for j in range(10)]})
df2 = pd.DataFrame({"array_col": [np.array([j]) for j in range(10)]})
actual = datacompy.columns_equal(df1.array_col, df2.array_col)
assert actual.all()
~~~

With Pandas 2.2.3, the object Series created from non-empty ndarray cells is classified as mixed by infer_dtype. The base short-circuit therefore returns all False and the first assert actual.all() fails before the function reaches the later empty-array block in the same test method.

The PR's fix changes that branch to explicitly process rows where every cell is a list or ndarray, using np.array_equal(..., equal_nan=True). That change supports both generic arrays/lists and the empty-array case. This demonstrates why the test method's base failure alone cannot be attributed to issue #58's empty-array defect.

The other two frozen selectors are:
- test_columns_equal_lists for Pandas Python lists;
- test_columns_equal_lists for Polars List arrays.

Neither isolates the issue's equal-empty-NumPy-array behavior.

## 5. Frozen row selector discovery evidence

**GitHub Actions run:** [44138363070](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44138363070)  
**Job ID:** 134234019328  
**Artifact ID:** 14351794927  
**Artifact SHA-256:** 6dac19d093acdbc22b0ed009aa2cee5987bf57360bf0f2af9399b91b4797eca1  
**Artifact size:** 1,308 bytes

The artifact was downloaded and independently checked:
- 3/3 inner SHA-256 entries passed.
- It contains only row summary, selector list, row hash and the hash manifest.
- It does not contain the Parquet, full row, full problem statement, or test source.

## 6. Required next action / exit criterion

The exact immutable row must remain unchanged. The candidate cannot be counted as a Stage 2 issue-specific pass by:
- dropping the two list selectors,
- replacing the broad NumPy selector with a hand-written empty-only selector,
- moving the empty-array assertion earlier in the PR test method, or
- counting a supplemental reproducer as the frozen dataset selector.

A separate minimal empty-array reproducer could confirm that the upstream base mishandles the precise issue #58 input and that the PR fix corrects it. Such a reproducer would be diagnostic support only; it would not repair the frozen row's mixed-scope selector set or become a replacement case. Unless the immutable row/oracle is independently adjudicated as acceptable under the preregistered protocol, this candidate remains held.

**Final disposition:** frozen row authenticated; issue linked to PR; target-test scope unsuitable for issue-specific Stage 2; no Stage 2 pass claimed; Stage 3 not started; final acceptance not granted.
