# ccdproc #901 / issue #814 — static scope and E3 sample-suitability review

**Date:** 21 November 2026  
**Candidate:** astropy/ccdproc issue #814 / fix PR #901  
**Cohort rank:** 41 of 96  
**Disposition:** **TECHNICAL BUG ALIGNMENT STRONG; PRIMARY ABSTENTION SAMPLE SUITABILITY FLAGGED; NO STAGE 2 EXECUTION**

## 1. Scope and exact upstream identity

- Issue: https://github.com/astropy/ccdproc/issues/814
- PR: https://github.com/astropy/ccdproc/pull/901
- Issue created: `2023-12-13T04:47:16Z`.
- PR created: `2025-07-13T21:05:06Z`.
- Exact PR base: `e793d77023ddfb62c4a1e7ca822e5a03a10b1776`.
- Exact PR head: `6599299aa19f21b14be44eda011adaacaf0e765e`.
- Merge commit: `bd0057f6437a5d27c149c7556dac55852dd18cfc`.
- Changed files: `AUTHORS.rst`, `ccdproc/image_collection.py`, `ccdproc/tests/test_image_collection.py`.

## 2. Static source and patch alignment

At the exact buggy base, `ccdproc/image_collection.py` blob `35a8acda3a83906c3583fa0a555ada88fe886ed7`, `ImageFileCollection.filter` does:

`files = self.files_filtered(include_path=True, **kwd)`

`return ImageFileCollection(filenames=files, keywords=self.keywords)`

The method does not forward the current collection's extension selection.

At the exact PR head, `ccdproc/image_collection.py` blob `7163dfa72d528538c6e2f0926454fbdae290c62a`, the return path includes:

`ImageFileCollection(filenames=files, keywords=self.keywords, ext=self._ext)`

The PR adds `test_filter_on_check_ext` in `ccdproc/tests/test_image_collection.py` blob `bb480f66ba26e716de139785ac7e7e81f9991ad9`. It creates a multi-extension FITS file, constructs `ImageFileCollection(tmp_path, ext=1)`, calls `filter()`, then checks that the resulting collection remains valid and `ifc2.ext == 1`.

Static code/patch alignment is strong: the missing extension argument described in the issue is the precise state forwarded by the patch, and the regression test asserts its preservation.

## 3. E3 answerability risk

The issue body states:

> “The call of `ImageFileCollection` here should be with arg `ext`, otherwise the keywords not in the first extension will become `--` in the returned collection.”

This is not merely a symptom description. The report identifies the missing constructor argument (`ext`) and explains the resulting metadata failure. The PR adds precisely `ext=self._ext`.

Therefore, an E3 packet containing the frozen issue text already exposes the likely root cause and repair direction. Under a rubric that accepts a source-level diagnosis such as “forward the parent collection's `ext` into the filtered collection”, this candidate is answerable at E3. An E3 ABSTAIN label would be difficult to defend without an unusually strict rubric requiring evidence about the exact internal state propagation or additional downstream proof.

**Advisory recommendation:** do not use ccdproc #814 as a primary abstention case. It may be retained as a separately labelled easy-answer / evidence-sufficient control only if the preregistered study design explicitly permits such controls and the project lead approves that use. Do not count it toward the minimum number of independent primary abstention cases.

## 4. Temporal exposure note

The issue was opened on 13 December 2023, before the Qwen2.5 family public announcement on 19 September 2024. A November 2026 AACL paper reports an October 2023 knowledge cutoff for Qwen2.5-3B-Instruct (Table 5); that is a secondary-source report, not a vendor guarantee. The issue text postdates that reported cutoff by roughly two months, but the underlying `ImageFileCollection.filter` implementation and missing-`ext` behavior existed in upstream source before the issue was filed. No claim is made that the underlying source was absent from pretraining.

Researcher exposure is full for the issue, PR, exact source and test changes. No blind adjudication or inter-rater claim is made. Project-lead prior pipeline/debug exposure declaration is pending.

References:
- Official Qwen2.5 announcement (19 September 2024): https://qwenlm.github.io/blog/qwen2.5/
- Qwen2.5-3B-Instruct model page: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct
- Hassan et al. (2026), AACL-IJCNLP, Table 5 reported cutoff: https://aclanthology.org/2026.aacl-long.168/

## 5. Stage 2 and acceptance boundary

- No independent reproducer has been created or executed in this review.
- No exact SWE-rebench row has been extracted or authenticated.
- No frozen selector has been run on the exact buggy base and fixed revision.
- No Stage 2 artifact, archive hash, CRC result or selector outcome is claimed.
- No model has been loaded and no inference, fine-tuning or training has been performed.
- Final case acceptance: **not accepted**; registry inclusion: **false**; inference authorization: **false**.

## 6. Next decision gate

Keep the candidate on a temporary sample-suitability hold until the project lead decides whether an explicitly labelled easy-answer/engineering control is permitted. If not, exclude it from the primary abstention sample and continue the frozen cohort order. Stage 2 should not be run solely to increase the number of technically reproducible candidates.