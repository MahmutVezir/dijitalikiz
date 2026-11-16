# Kozea/WeasyPrint issue #2270 — conditional candidate review

**Cohort rank:** 34 of 96 primary candidates  
**Dataset instance:** Kozea__WeasyPrint-2416 (exact row identity to be authenticated)  
**Issue:** https://github.com/Kozea/WeasyPrint/issues/2270  
**Fix PR:** https://github.com/Kozea/WeasyPrint/pull/2416  
**Review status:** source/patch alignment plausible, but dataset-test scope and Pyphen dictionary provenance are unresolved. Conditional hold; not an accepted case.

## 1. Defect contract

Issue #2270 reports that automatic hyphenation fails for a word when a non-breaking space appears earlier in the same text run. PR #2416 changes the line-breaking routine to search all words before the next break opportunity, rather than considering only the first word. It also tracks the offset of the selected word so dictionary hyphenation positions are applied to the correct substring.

The PR's added regression test is named test_hyphen_nbsp, but its comment says "Regression test for issue #1817", not #2270. That issue-reference mismatch does not prove the test is unrelated, but it must be reconciled. The exact dataset FAIL_TO_PASS selectors must demonstrate that issue #2270 is actually isolated.

## 2. Pinned source identity

- Repository: Kozea/WeasyPrint
- Buggy base: 1b24ad91323c8444e398b75ed40ad54cf678ea0d
- Fixed PR head: ad338b66333d6a79fb513e2d7668e282962ba470
- Merge commit: 4087af4d3048b4f9b968c2795ca497442dc72513
- Issue #2270 created: 2024-10-07T12:07:54Z
- PR #2416 created: 2025-03-24T16:54:52Z
- Exact-base root LICENSE Git blob: 5b460bb52be9552ca2aa999642c6d66da9589fb3
- Exact-base pyproject.toml Git blob: a6b9f362ce81d9fe26d2f0fae50365cb0491d536
- Exact-base line_break.py Git blob: ea9c6ca736cff3f29eb1ef9e91d1f40ef7cd908c
- Exact-base project license: BSD-3-Clause.

## 3. Test data and license/provenance hold

The new test sets lang="en" and hyphens="auto", which invokes Pyphen's installed English hyphenation dictionary. The exact dictionary file is therefore an input to the regression test, not merely a package implementation detail. Before execution, the study must identify:
- the exact Pyphen version used by the upstream test environment;
- the exact English dictionary file selected at runtime and its SHA-256;
- the dictionary's source repository, copyright, and license;
- whether the dictionary is included in the Pyphen wheel or resolved from a system path.

The full WeasyPrint test also depends on Pango/Cairo and other native components. These must be pinned or documented. The current evidence is not enough to clear the external dictionary and native runtime provenance.

## 4. Current decision

Issue/patch alignment: plausible.  
Test-to-issue mapping: unresolved (#2270 vs #1817 comment).  
Pyphen dictionary provenance/license: unresolved.  
Native runtime environment: not yet frozen.  
Final case acceptance: not accepted; conditional hold.
