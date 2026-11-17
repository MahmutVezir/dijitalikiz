# PyThaiNLP #1046 — candidate technical review and Stage 2 decision

**Review date:** 17 November 2026  
**Frozen cohort rank:** 21  
**Dataset instance:** `pythainlp__pythainlp-1046`  
**Dataset row SHA-256:** `80b244dd8b406d095f7ec727f968dacbb6b2f620dc8b10c21d44e726ba3e5803`  
**Dataset revision:** `fb9aa226b2ce37c708ea7732e7b980abacdadb67`  
**Issue:** [PyThaiNLP/pythainlp #1004](https://github.com/PyThaiNLP/pythainlp/issues/1004)  
**Fix PR:** [PyThaiNLP/pythainlp #1046](https://github.com/PyThaiNLP/pythainlp/pull/1046)

## 1. Decision

- **Stage 2 technical result:** passed. The exact frozen SWE-rebench selector ran on a pinned environment; it produced a real pytest assertion failure on the exact buggy base and passed on the exact fixed commit.
- **Independent issue-level corroboration:** both reported Thai word examples were additionally tested separately. Each failed as an executed assertion on the buggy base and passed on the fixed commit.
- **Stage 3:** not started. Dependency/license scope sign-off, related-defect/project independence, researcher/model exposure and training-data contamination assessment, and human gold/alternative/E1-E2-E3 adjudication remain open.
- **Final case acceptance:** not granted. The accepted-case count remains **0**.
- **Model boundary:** no model was loaded; no inference, fine-tuning, or training was performed.

The two independent one-word tests are supporting reproductions of the same upstream issue. They are not additional dataset cases and do not increase the independent-project or accepted-case count.

## 2. Frozen row and issue/PR alignment

Immutable Parquet:
- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`

Authenticated row:
- `instance_id`: `pythainlp__pythainlp-1046`
- `repo`: `PyThaiNLP/pythainlp`
- `base_commit`: `188904f22c4c80fd7406706850c798f611690a4a`
- `created_at`: `2024-12-25 06:25:09`
- `language`: Python
- `license`: Apache-2.0
- Exact `FAIL_TO_PASS` selector count: 1

Exact selector, including class and method names:
```
tests/core/test_util.py::UtilTestCase::test_tone_detector
```

The canonical row SHA-256 was computed over the selected row's canonical JSON representation and matched the frozen expected value. The artifact stores only the row hash and limited metadata; it does not store the Parquet, canonical row, or full problem statement.

The dataset problem statement does not literally include the string `#1004`; this was not treated as a contradiction. Issue/PR linkage is separately authenticated through PR #1046's `Fixes #1004` reference, the upstream issue/PR metadata, exact repository/base commit, and reconciled PR timestamp. The problem statement itself contains `tone_detector` and both issue examples (`ครับ`, `ค่ะ`), so its substantive defect scope matches the issue.

## 3. Upstream change and defect-specific oracle

Exact upstream base:
`188904f22c4c80fd7406706850c798f611690a4a`

Exact fixed commit:
`6f1dc929f853ecd9910d1d25a56716b864b2ee98`

Source blobs:
- Base `pythainlp/util/syllable.py`: `9d480d815ee23edc74a39f34edea253dd4fd88fc`
- Fixed `pythainlp/util/syllable.py`: `bf3d4be4c50d59005f3e752ec426861c53428ba6`
- Base `tests/core/test_util.py`: `de7a7a9d1614d695be2455913197c586a47509a9`
- Fixed `tests/core/test_util.py`: `aef11e09487009f63c6e6a2317caa4a5cb6a8f80`

PR #1046 makes two production-level changes in `pythainlp/util/syllable.py`:
1. It changes the `syllable_length()` consonant-count boundary from fewer than three consonants to at most three.
2. It moves tone-mark-specific branches in `tone_detector()` ahead of broader consonant-class/syllable-state branches, preventing a general rule from taking precedence over the more specific tone-mark rule in the reported cases.

The PR also adds two expected cases to `UtilTestCase.test_tone_detector`:
- `tone_detector("ครับ")` must return `"h"` (high tone).
- `tone_detector("ค่ะ")` must return `"f"` (falling tone).

The issue reports the opposite outputs on the base implementation:
- `ครับ`: actual `"f"`, expected `"h"`.
- `ค่ะ`: actual `"h"`, expected `"f"`.

The frozen upstream selector is defect-sensitive because it executes the method containing these exact expected outputs. One methodological limitation is that the upstream method iterates through both words and stops at the first failed assertion on the base. Therefore, to establish each issue example independently, two separate one-word support tests were also executed. Those tests are reported as supporting reproducers, not as additional dataset selectors or independent cases.

## 4. Pinned Stage 2 reproduction

**Canonical GitHub Actions run:** [44133576730](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44133576730)  
**Job ID:** `134216923258`  
**Research branch head:** `182412611857ae881e991b52109320320d739381`  
**Workflow:** `.github/workflows/pythainlp-1046-stage2-pinned.yml`

### Exact dataset selector

| Revision | Executed result | Assertion contract |
|---|---|---|
| Buggy base | 1 failed | actual `"f"` vs expected `"h"` for `ครับ` |
| Fixed commit | 1 passed | same frozen selector passed |

### Independent one-word corroboration

| Example | Buggy base | Fixed commit |
|---|---|---|
| `ครับ` → high (`h`) | actual `f`; assertion failure | pass |
| `ค่ะ` → falling (`f`) | actual `h`; assertion failure | pass |

These two additional tests isolate each issue example. They support the exact dataset result but do not count as additional SWE-rebench cases.

### Pinned environment

- OS: Ubuntu 22.04.5 LTS
- Python: CPython 3.10.15
- pip: 24.3.1
- pytest: 8.3.5
- PyThaiNLP: 5.0.6.dev0 (editable install from exact upstream source commit)
- PyICU: 2.17
- Native ICU: `libicu-dev=70.1-2`, `libicu70=70.1-2`, ICU i18n 70.1
- C++ compiler: 11.4.0
- Python runtime lock: 19 exact distribution pins; installed runtime contains 20 distributions including the separately installed editable PyThaiNLP source tree.
- Installed freeze matched `requirements.lock` exactly.
- `pip check`: `No broken requirements found.`
- All 20 installed distribution records contained license metadata; missing metadata count = 0.

The exploratory attempt before pinning `wheel==0.45.1` stopped during package metadata generation with `invalid command 'bdist_wheel'`. That was a packaging-tool setup failure, not a source-code/test failure. The environment was corrected by pinning wheel; the later pinned run completed successfully. The exploratory run is retained as history and is not used as the canonical Stage 2 result.

License metadata completeness is not legal license approval. In particular, NumPy's package metadata describes bundled components including OpenBLAS, LAPACK, GCC runtime libraries and other separately licensed components. Their exact scope and obligations require a separate license review; no legal sign-off is claimed here.

## 5. Test-only patch scope

The pinned run applied only the test-file portion of the upstream PR to the buggy base:
- Changed path: `tests/core/test_util.py`
- Added lines: 2
- Deleted lines: 0
- The two added assertions were exactly the reported `ครับ` and `ค่ะ` cases.
- No production source change was applied to the buggy base.
- The base production `syllable.py` blob remained `9d480d815ee23edc74a39f34edea253dd4fd88fc`.

The full PR patch and test-only patch contents were not uploaded; only their SHA-256 fingerprints were retained.

## 6. Canonical sanitized evidence

**Artifact:** [pythainlp-1046-pinned-exact-selector-evidence](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44133576730/artifacts/14351751109)  
**Artifact ID:** `14351751109`  
**Size:** 23,069 bytes  
**ZIP SHA-256:** `ce2ab3bbefd3148510992a7503d8c07b17fb87fe2c2a76173c1971d21e12dcb8`

The artifact was downloaded and independently inspected:
- 17/17 internal SHA-256 entries verified.
- The outer ZIP SHA-256 matched the GitHub Actions artifact digest.
- It contains the exact requirements lock, installed freeze, native toolchain summary, dependency license metadata inventory, dataset row hash/summary, sanitized base/fixed assertion summaries, source provenance, test-only patch scope and hash manifest.
- It does not contain the Parquet, full dataset row, problem statement, raw stdout/logs, copied issue test fixture, the temporary one-word reproducer file, or patch contents.

## 7. Remaining Stage 3 / acceptance gates

PyThaiNLP now passes the technical Stage 2 gate. It is not yet an accepted research case. Before Stage 3/final acceptance:
1. Complete direct/transitive and native dependency license review, including NumPy's bundled components, PyICU and ICU runtime/build scope. Metadata presence alone is insufficient.
2. Complete independent upstream-project and related-defect clustering; verify the case represents a distinct project-level case, not a duplicate/related defect already in the accepted set.
3. Complete researcher source-exposure and model training-data/exposure assessment. The dataset timestamp is 2024-12-25; exact model training-data cutoff and any potential exposure to the issue/PR material must be assessed before model evaluation.
4. Prepare the gold mechanism, plausible alternatives and E1/E2/E3 evidence packages, with human adjudication separately recorded.
5. Pass the complete case-acceptance record schema and fail-closed registry checks before any final acceptance.

**Final disposition:** Stage 2 technical pass = yes; Stage 3 = not started; final accepted case = no. The overall accepted independent case count remains 0. No model inference or training was authorized or performed.
