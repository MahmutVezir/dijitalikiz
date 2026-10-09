# New Public Bug Candidate Screening — 10 October 2026

**Purpose:** Expand the research candidate pool with recent real-world fixes while keeping them separate from the completed/frozen confirmatory set. This is a source-screening note, not a claim that the candidates are already eligible for experiment inclusion.

## Summary

Three candidates were independently inspected at the public GitHub PR and patch level. Two show a strong cross-component boundary; one is a weaker secondary candidate. All three candidate records and assessment records are stored in data/candidates/ and data/assessments/.

| Candidate | Public fix | Preliminary CCDG relevance | Current eligibility |
|---|---|---|---|
| Commons Compress #803 — recursion over empty framed LZ4/Snappy units | Merged 17 Aug 2026; merge commit 7e688ebdba45ab16aa5b7f870474dac285a494af | Strong: two distinct framed decoders and corresponding regression tests have the same unbounded-recursion pattern | Not eligible yet: IC6/IC7 and independent reproduction pending |
| Commons Compress #770 — oversized TAR PAX header memory use | Merged 18 Jul 2026; merge commit bab5629f6b3cea44cf0622cdd92c8cefcfbf360a | Strong: shared TAR parsing path wired through both TarArchiveInputStream and TarFile, builder configuration and memory-limit enforcement | Fix independently reproduced; IC6/IC7 and final case adjudication pending |
| Commons Lang #1807 — wildcard upper bounds / equality / hash consistency | Merged 4 Oct 2026; merge commit 43154e016ae213a0da5b727cd1aa18e6e0c56adb | Moderate at best: TypeUtils behavior is constrained by the JDK WildcardType contract and uses ArrayUtils normalization, but the production change is concentrated in one implementation | Not eligible yet: CCDG boundary and controlled-context suitability require further review |

## Candidate details

### A. Commons Compress PR #803

Source: https://github.com/apache/commons-compress/pull/803  
Fix revision: https://github.com/apache/commons-compress/commit/7e688ebdba45ab16aa5b7f870474dac285a494af

The PR description and patch indicate that legal zero-output units in framed LZ4 and Snappy streams could lead to unbounded recursion and a StackOverflowError rather than normal EOF. The patch changes two source files and two corresponding test classes. Regression tests construct 200,000 empty concatenated LZ4 frames and 200,000 Snappy padding chunks, respectively.

Candidate record: data/candidates/commons-compress-github-pr-803-empty-framed-stream-recursion.json  
Assessment record: data/assessments/commons-compress-github-pr-803-empty-framed-stream-recursion.json

### B. Commons Compress PR #770

Source: https://github.com/apache/commons-compress/pull/770  
Fix revision: https://github.com/apache/commons-compress/commit/bab5629f6b3cea44cf0622cdd92c8cefcfbf360a

The fix introduces a configurable PAX-header size bound through the shared TAR builder and propagates it to both streaming and file-based TAR readers and the shared parser. The PR modifies AbstractTarBuilder, TarArchiveInputStream, TarFile, TarConstants, and TarUtils, and adds a PaxHeaderOomTest regression test. This appears to offer an observable dependency path spanning configuration, parser, reading APIs, and memory-limit enforcement.\n\nThe same independent reproduction test was run on pre-fix commit 829b5dd6ffe976c0a03231e65790a65af9f3a6ee and fixed commit bab5629f6b3cea44cf0622cdd92c8cefcfbf360a in [GitHub Actions run 37993954772](https://github.com/MahmutVezir/dijitalikiz/actions/runs/37993954772). On the pre-fix commit it failed as expected because the oversized header did not throw MemoryLimitException; on the fixed commit the same test passed. This verifies the reported regression/fix behavior for the tested scenario, not the candidate's final inclusion eligibility.

Candidate record: data/candidates/commons-compress-github-pr-770-tar-pax-header-memory-bound.json  
Assessment record: data/assessments/commons-compress-github-pr-770-tar-pax-header-memory-bound.json

### C. Commons Lang PR #1807

Source: https://github.com/apache/commons-lang/pull/1807  
Fix revision: https://github.com/apache/commons-lang/commit/43154e016ae213a0da5b727cd1aa18e6e0c56adb

The fix makes unbounded wildcard representation, equality and hash behavior align with Java reflection semantics and adds regression tests. The current code change is more concentrated in TypeUtils.WildcardTypeImpl, so the graph's meaningful component boundary is less clear than in the Commons Compress candidates. The PR description discloses AI assistance (Claude) in locating the issue and drafting the patch/test; this disclosure is retained as provenance information and is not evidence that the frozen Qwen model encountered the case.

Candidate record: data/candidates/commons-lang-github-pr-1807-typeutils-wildcard-bounds.json  
Assessment record: data/assessments/commons-lang-github-pr-1807-typeutils-wildcard-bounds.json

## Quality and contamination policy

- These fixes are publicly visible and postdate the release of the Qwen2.5 model family used in the historical experiment, which may reduce direct memorization risk but does not establish the exact training-data cutoff or absence of exposure.
- The assessments therefore use **medium** contamination risk rather than claiming zero contamination.
- The candidates' public PRs and merge revisions have been verified, and relevant regression test files are visible in the PR patches. Commons Compress #770 now has an independent pre-fix failure/post-fix pass. Equivalent clean-checkout reproductions for #803 and Commons Lang #1807 remain pending.
- The #770 assessment now records fix_quality=pass based on the reproducible run; IC6/IC7 remain unknown and eligibility remains false. The other two candidates still have independent reproduction pending. All three remain outside pilot/main inclusion.
- Before moving any candidate forward, extract the pre-fix and fixed revisions, verify the regression test is red on the pre-fix revision and green on the fixed revision, build a source-grounded ground-truth record, draw and review the CCDG, and render all context-v2 arms while checking for ground-truth leakage.
- Do not change data/benchmark/benchmark_manifest.json or append these candidates to the frozen historical results. They may only enter a separately versioned future study after the measurement rubric and study protocol have been frozen.

## Structured case draft added

The Commons Compress #770 case has also been drafted separately in `data/candidate_case_drafts/commons-compress-github-pr-770-tar-pax-header-memory-bound.json`. The draft contains candidate-safe base facts, a provisional ground-truth record, four dependency edges, and provenance metadata. The three v2 context renderers use the same shared base facts; only the two dependency-enriched arms add edges, in prose or directed-triple form.

The draft is deliberately stored outside both `data/candidates/` and `data/benchmark/cases/`: it does not pollute the candidate-intake schema or the frozen confirmatory manifest. A regression test checks its ResearchCase schema, ensures it remains outside the frozen manifest, checks information parity and verifies that the fix commit and canonical ground-truth root-cause label are not included in the rendered model contexts.

This is a structured draft, not a qualified experiment case yet. Independent reproduction of the PAX-header regression has passed on exact upstream pre-fix and fixed commits (run 37993954772). Final source-grounded ground-truth adjudication and IC6/IC7 eligibility review remain open.

## Status

This screening raises the candidate pool by three entries and creates one structured case draft with regression tests. It does not raise the number of eligible confirmatory cases yet, does not change the frozen 16-case / 160-output results, and does not support any claim that CCDG has been effective or ineffective.
