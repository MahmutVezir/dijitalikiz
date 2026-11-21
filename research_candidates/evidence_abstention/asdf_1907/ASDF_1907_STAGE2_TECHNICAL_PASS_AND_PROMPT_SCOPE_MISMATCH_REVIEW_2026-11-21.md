# ASDF #1907 / issue #1821 — Stage 2 technical result and prompt/PR scope mismatch

**Date:** 21 November 2026  
**Candidate:** asdf-format/asdf issue #1821 / fix PR #1907  
**Cohort rank:** 43 of 96  
**Disposition:** **TECHNICAL PR-REGRESSION REPRODUCTION PASSED; FROZEN E3 ISSUE BODY DOES NOT DESCRIBE THE FAILING PR-1907 SCENARIO; HELD OUT OF PRIMARY ABSTENTION SAMPLE; NOT ACCEPTED**

## 1. Frozen upstream identities

- Issue: https://github.com/asdf-format/asdf/issues/1821
- PR #1907: https://github.com/asdf-format/asdf/pull/1907
- Issue created: `2024-08-12T17:13:29Z`.
- PR created: `2025-03-12T17:51:23Z`.
- Exact PR #1907 buggy base: `74fdcd96540049e4824b4da2bbe3ffdf42d23cfc`.
- Exact PR #1907 fixed head: `fc001f65e46d149ea179322e02f39065f4ee861c`.
- Merge commit: `291528b031b38f2f83d00f7618bb823b026bed75`.
- Related earlier PR #1825: merged `2024-08-20T20:04:08Z`, commit `c5cb4daae91fd3e0d76b1a0a04cf36f205de6cdd`. This is part of the same upstream defect/repair history and is not an independent candidate.

## 2. Frozen dataset row and model-visible issue statement

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`.
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`.
- Whole Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`.
- Row instance: `asdf-format__asdf-1907`.
- Canonical row SHA-256: `6781cd9d8d818672f881769b7eea67b482fa95536ef0d17bbc65b89261186bde`.
- Row `created_at`: `2025-03-12 17:51:23`.
- Frozen FAIL_TO_PASS selector: `asdf/_tests/test_util.py::test_load_yaml_recursion_with_tags[False]`.

The authenticated row's `problem_statement` is the original issue body from 12 August 2024. It describes a plain recursive dictionary serialized through `AsdfFile`, then read with `asdf.util.load_yaml` using its default `tagged=False` argument. It reports `ConstructorError: found unconstructable recursive node` and notes that `tagged=True` is a workaround.

The frozen `problem_statement` does **not** contain the later custom-tagged recursive mapping/sequence example added in an issue comment on 12 March 2025. That later comment is the specific behavior addressed by PR #1907's new regression test. Researcher exposure to the later comment is full; it is not silently added to the model-visible E3 packet.

## 3. Stage 2 technical PR-regression reproduction

Workflow run/job/artifact:
- Run: `44914702403`.
- Job: `136877789859` (`asdf-issue-1821-reproduction`).
- Artifact: `14711301958` (`asdf-issue-1821-reproduction`).
- Artifact size: 30,173 bytes.
- Artifact SHA-256: `88351a762594c92e5673ab06fd18c711962ecd81d25cdff112fd19aa9aac5584`.

Independent archive verification:
- Artifact downloaded from GitHub and outer SHA-256 recomputed; digest exactly matches the GitHub artifact digest.
- ZIP CRC: PASS (`ZipFile.testzip()` returned `None`).
- Archive members: 18.
- Internal SHA256SUMS: 17/17 entries PASS.
- The archive includes the exact tested reproducer source and its own source hash `49dda2e459b7ff83d75caf139b2542300c8e7e0edaaf006ab8684f1238562e46`.

Exact row/selector reproduction:
- The immutable Parquet row was authenticated and extracted; canonical row SHA-256 is recorded above.
- Exact frozen selector on the exact buggy base fails with `ConstructorError: found unconstructable recursive node`.
- The same selector on the exact fixed revision passes (1 test).

Independent reproducer at the exact PR #1907 base and fixed head:
- Recursive custom-tagged mapping with `tagged=False`: fails on base with the expected `ConstructorError`.
- Recursive custom-tagged sequence with `tagged=False`: fails on base with the expected `ConstructorError`.
- The same custom-tagged mapping and sequence passed through `tagged=True`: positive control passes on base.
- Original issue `AsdfFile` self-reference example, loaded with default `tagged=False`: passes on the PR #1907 base.
- The same original issue example loaded with `tagged=True`: positive control also passes on the PR #1907 base.
- All five independent reproducer tests pass on the PR #1907 fixed revision.

Thus the Stage 2 job establishes that PR #1907 fixes the later custom-tagged recursive mapping/sequence defect and that the exact PR-added selector is base-fail/fixed-pass. It also establishes that the original issue-body example is already passing at the PR #1907 buggy base.

## 4. Critical issue-to-PR scope mismatch

The Stage 2 reproducer deliberately contains both the original issue example and the later custom-tagged examples. The base run output is `2 failed, 3 passed`:

- The two failures are the custom-tagged recursive mapping and sequence under `tagged=False`.
- The three passes are the `tagged=True` positive control for those examples, the original untagged `AsdfFile` self-reference scenario, and its `tagged=True` control.

The exact original issue example therefore does not reproduce the alleged failure on PR #1907's exact buggy base. This is not an assertion from source inspection alone; it is confirmed by the independently run base/fixed reproducer.

Why this happens:
- PR #1825, merged on 20 August 2024, introduced `_IgnoreCustomTagsLoader` for `load_yaml(tagged=False)` and addressed the earlier ordinary/untagged recursion case.
- PR #1907's description explicitly says the earlier fix was partial and only handled non-tagged nodes.
- PR #1907 changes how the unrecognized-tag constructor handles recursive MappingNode and SequenceNode values, and adds the custom-tagged recursive mapping/sequence regression test.
- The frozen dataset prompt still contains only the earlier generic self-referential dictionary symptom and `tagged=True` workaround. It does not contain the later custom-tagged example that the #1907 selector exercises.

**Conclusion:** PR #1907's technical fix is valid and reproducible, but the frozen E3 issue text is stale with respect to the defect scenario exercised by the PR #1907 test. The original issue-body behavior had already been repaired before PR #1907's base. The E3-to-patch contract is therefore not sufficiently aligned for a primary root-cause/abstention case.

## 5. Exact source mechanism for PR #1907 — technical explanation only

At exact base `asdf/yamlutil.py` blob `5615f4b8ba1defdf05cd09cd3892cd07208291b6`, `_IgnoreCustomTagsLoader.construct_undefined` dispatches unknown-tag nodes by node type:

- MappingNode -> `self.construct_mapping(node)`.
- SequenceNode -> `self.construct_sequence(node)`.

These ordinary PyYAML constructor methods build a mapping/list by recursively descending before a placeholder object for the tagged node is registered in the loader's constructed-object cache. If a child node contains an alias back to the current node, PyYAML detects the node in `recursive_objects` and raises `ConstructorError` rather than resolving a cycle.

At exact fixed head, `asdf/yamlutil.py` blob `c1143814cd89c3bedba7746f470bc1a0046ab7e5`, those calls are changed to generator-based `construct_yaml_map` and `construct_yaml_seq`. These constructors yield a placeholder mapping/list before populating its children, allowing recursive aliases to refer to the already-registered container.

This explains the tagged mapping/sequence behavior covered by PR #1907. It must not be presented as the cause of the original untagged self-reference example at the PR #1907 base, because that example already passes there.

## 6. Temporal and researcher-exposure limits

- Issue #1821 was opened on 12 August 2024, before Qwen2.5's public announcement on 19 September 2024 and before the pinned Qwen2.5-3B-Instruct weights were uploaded in September 2024. Exposure to the issue text or pre-existing ASDF source is therefore plausible; the exact training corpus/cutoff is not verified.
- PR #1907 and the later tagged-recursion comment are dated March 2025, after the checkpoint's public release. This reduces the likelihood of PR/comment-specific training exposure, but does not prove the pre-existing source or initial issue was absent.
- Researcher exposure is full: issue body, later issue comment, PR description/diff, previous PR #1825, exact base/fixed sources, tests, workflow logs and artifact have all been reviewed.
- No blinded adjudication or independent second-rater/inter-rater claim is made.
- Project-lead prior pipeline/debug exposure declaration and temporal-exposure acknowledgement are pending.

## 7. Sample disposition

- Technical Stage 2 for the PR #1907 regression: **passed**.
- Frozen E3 problem statement vs PR #1907 failing scenario: **mismatched**.
- Primary abstention sample eligibility: **false pending project-lead review; recommended exclusion**.
- The candidate may remain in provenance/engineering records. It must not count as a primary independent abstention case. Any separately labelled engineering-control use requires separate study-design permission.
- Final case acceptance: **not accepted**.
- Registry inclusion: **false**.
- Model loading, inference, fine-tuning and training: **not performed and not authorized**.

## 8. Next decision gate

Project lead should confirm exclusion from the primary abstention sample because the issue body no longer reproduces on the exact PR #1907 base and the failing custom-tagged scenario appears only in later issue-thread material that is absent from the frozen model-visible problem statement. No gold/tier approval or final case-acceptance request should be made before this scope discrepancy is resolved.