# cta-observatory/ctapipe issue #2730 — conditional candidate review

**Cohort rank:** 31 of 96 primary candidates  
**Dataset instance:** cta-observatory__ctapipe-2732 (exact row identity to be authenticated)  
**Issue:** https://github.com/cta-observatory/ctapipe/issues/2730  
**Fix PR:** https://github.com/cta-observatory/ctapipe/pull/2732  
**Review status:** source/patch alignment is plausible, but the return-type contract is internally inconsistent. Conditional hold; not an accepted case.

## 1. Defect contract and unresolved semantic point

Issue #2730 reports a DataWriter failure involving muon-parameter skewness and excess kurtosis. PR #2732 changes the radial-light-distribution routine so that skewness and excess kurtosis are returned as plain numeric values rather than dimensionless Astropy quantities. It also changes the zero-image branch to return plain NaN values. The regression test asserts that both outputs are float or numpy.floating.

However, the exact-base and fixed source retain docstring return annotations describing skewness and excess_kurtosis as astropy.units.Quantity, while the fixed implementation and new tests require plain numeric values. This documentation/contract mismatch must be resolved before the gold mechanism can be locked. The issue's short description alone does not fully explain why DataWriter's conversion path fails.

## 2. Pinned source identity

- Repository: cta-observatory/ctapipe
- Buggy base: 287e7685e0e963f3fb44d92832ca97ac8c265c40
- Fixed PR head: 5007b6ab61887d7555155edb4d1d296603a9735e
- Merge commit: ba4546f2027e2f820982c4e40730097b7e16434c
- Issue #2730 created: 2025-04-02T15:59:14Z
- PR #2732 created: 2025-04-02T17:48:48Z
- Exact-base root LICENSE Git blob: 7d85dda24fa481e24c4b33dd98dbc13245ee1fd2
- Exact-base pyproject.toml Git blob: 9f4bbee5eb6619a36bf327d7f34157a2c2ee0bd5
- Exact-base features.py Git blob: 8d547bf52c52dee18a3fa82dd47395a03bded282
- Fixed features.py Git blob: f18f1c3f16b41a5e7b1076512296ca8a4efa1c2f
- Exact-base project license declaration: BSD-3-Clause.

## 3. Scientific/technical gate

The issue-specific function is radial_light_distribution. The PR changes the output types for skewness and excess kurtosis, and the test verifies those types plus numerical values for a uniform synthetic image. A narrow AST-extracted test could execute this exact function with only NumPy and Astropy, avoiding unrelated ctapipe runtime imports.

Before advancing, we must:
1. reconcile the public return contract (docstring vs implementation/test);
2. verify the DataWriter failure path and show that the type change addresses it;
3. authenticate and run the dataset FAIL_TO_PASS selectors on the exact base and fixed revisions;
4. confirm that no external test data or provenance-sensitive fixtures are involved.

No inference or training is authorized.

## 4. Current decision

Issue/patch alignment: plausible.  
Technical semantic contract: unresolved.  
License: exact-base BSD-3-Clause screen passed.  
Final case acceptance: not accepted; conditional hold.
