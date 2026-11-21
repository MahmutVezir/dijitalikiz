# ASDF #1907 / issue #1821 — Stage 2 evidence and prompt-to-test scope review

**Date:** 21 November 2026  
**Candidate:** asdf-format/asdf issue #1821 / fix PR #1907  
**Dataset instance:** `asdf-format__asdf-1907`  
**Disposition:** TECHNICAL PATCH REPRODUCED; DATASET TEST PASSES BASE-FAIL/FIXED-PASS; ORIGINAL ISSUE PROMPT DOES NOT REPRODUCE THAT FAILURE; NOT ACCEPTED FOR PRIMARY ABSTENTION SAMPLE

## 1. Exact Stage 2 provenance

- Buggy base: `74fdcd96540049e4824b4da2bbe3ffdf42d23cfc`.
- Fixed PR head: `fc001f65e46d149ea179322e02f39065f4ee861c`.
- PR merge: `c5cb4daae91fd3e0d76b1a0a04cf36f205de6cdd`.
- Upstream source blobs at the exact buggy base: `asdf/yamlutil.py` `5615f4b8ba1defdf05cd09cd3892cd07208291b6`; `asdf/util.py` `c03b458b1ddc6618d6791844f6a6e7993f6da6ab`; `asdf/_tests/test_util.py` `97923e7939ea1f18fba736a9bd5eb37f1bec27bc`.
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`.
- Exact row: `asdf-format__asdf-1907`; repo `asdf-format/asdf`; base commit matches; created_at `2025-03-12 17:51:23`; dataset row SHA-256 `6781cd9d8d818672f881769b7eea67b482fa95536ef0d17bbc65b89261186bde`.
- Frozen FAIL_TO_PASS selector: `asdf/_tests/test_util.py::test_load_yaml_recursion_with_tags[False]`.
- Python `3.11.9`; lockfile `research_candidates/evidence_abstention/reproduction/asdf_issue_1821/requirements.lock`.

Workflow run `44914416693`; ASDF job `136876908414`; artifact `14710853774` (`asdf-issue-1821-reproduction`).

## 2. Artifact integrity

- GitHub artifact SHA-256: `86bf7581e161b86cb189bb7b57c8783ed83236023fe53ec3786b24c64e9d5f31`.
- Independent downloaded ZIP SHA-256: same value.
- ZIP CRC check: PASS (`ZipFile.testzip()` returned no corrupt member).
- Archive files: 16 including `SHA256SUMS.txt`.
- Internal SHA-256 manifest: 15 entries, 15/15 passed after normalizing the manifest's `./` path prefix.
- The Parquet file itself is not retained in the uploaded artifact; it was authenticated in the job against the pinned dataset-file SHA-256 before extracting the single row.

## 3. Exact observed results

### Independent reproducer

The five-test reproducer includes:
1. Tagged recursive mapping through `load_yaml(tagged=False)`.
2. Tagged recursive sequence through `load_yaml(tagged=False)`.
3. `tagged=True` positive control for the two tagged recursive structures.
4. The original issue's untagged `AsdfFile` self-reference example (`d = {}; d['a'] = d; AsdfFile(d).write_to(...); load_yaml(...)`).
5. The same original issue self-reference example with `tagged=True`.

On exact buggy base, the two tagged recursive mapping/sequence cases fail with `yaml.constructor.ConstructorError: found unconstructable recursive node`; three tests pass. Crucially, the original issue self-reference case passes on the buggy base under both untagged and tagged loading. On exact fixed PR head, all five tests pass.

### Frozen dataset selector

- Exact buggy base: selector fails with `ConstructorError: found unconstructable recursive node`.
- Exact fixed PR head: same selector passes.

This is a reproducible base-fail/fixed-pass result for the frozen selector and for the later tagged-recursion regression tests. It does **not** establish base-fail/fixed-pass for the simple recursive-object example in the frozen issue body.

## 4. Why this is a material prompt-to-test mismatch

The frozen dataset `problem_statement` says `asdf.util.load_yaml` fails on a recursive object, and its example is a simple self-reference:

`d = {}; d['a'] = d; asdf.AsdfFile(d).write_to('recursive.asdf'); asdf.util.load_yaml('recursive.asdf')`.

It states `tagged=True` is a workaround. The exact buggy-base run of that original example does not raise the reported error; it passes. The hidden FAIL_TO_PASS selector instead tests a different scenario: custom-tagged recursive mapping/sequence nodes processed by the `_IgnoreCustomTagsLoader` used for `tagged=False`.

The public issue comment later adds a more complex tagged recursive ASDF transform/WCS structure. The PR #1907 regression test closely matches this later comment, not the original problem statement field frozen into the benchmark row. Earlier PR #1825 added `_IgnoreCustomTagsLoader` and addressed the first recursion issue; PR #1907 then moved unknown-tag mapping/sequence construction to PyYAML's generator-based constructors for the tagged recursion edge case.

Therefore, the visible E3 prompt and hidden E2 selector/reproducer do not describe the same failure instance. An E3 model cannot be expected to infer the later comment's custom-tag scenario from a frozen prompt that only gives the simpler self-reference example. This is not a minor phrasing difference; it changes the relevant failure mechanism and expected evidence packet.

## 5. Source mechanism of PR #1907, for technical provenance only

At the buggy base, `_IgnoreCustomTagsLoader.construct_undefined` dispatches MappingNode to `self.construct_mapping(node)` and SequenceNode to `self.construct_sequence(node)`. Those non-generator helper paths do not register the incomplete object before recursively constructing children, so self-references through unknown/custom tags raise `ConstructorError`.

PR #1907 changes those branches to `self.construct_yaml_map(node)` and `self.construct_yaml_seq(node)`, which are generator-based PyYAML constructors and register the container before filling it. This preserves recursive identity for tagged mapping and sequence nodes.

This technical mechanism is supported by exact-base/fixed source and the passing frozen selector, but it is not the failure demonstrated by the frozen issue-body example.

## 6. Researcher exposure and issue-family linkage

- One upstream repository and one candidate only. Do not count PR #1825 as a separate independent case; it is an earlier partial fix in the same issue family.
- Researcher exposure is full for issue comments, PR discussion, PR diff, exact source, hidden selector, Stage 2 logs and artifact.
- The later issue comment's tagged transform/WCS example informed the independent reproducer. That content is not present in the frozen dataset `problem_statement`, and must not be silently inserted into an E3 packet.
- No blind adjudication or inter-rater reliability claim is made.
- Project-lead prior pipeline/debug exposure declaration remains a separate pending gate.

## 7. Disposition

- Stage 2 technical result for the hidden tagged-recursion defect: **passed**.
- Prompt-to-selector/reproducer equivalence: **failed** for the frozen issue-body example.
- E3/E2/E1 tier adjudication for the primary study: **not performed**, because the sample does not align the visible prompt with the tested failure.
- Primary abstention sample: **exclude / not eligible under the current fixed prompt contract**.
- A separately labelled dataset-construction or benchmark-alignment audit may retain this case as an example of prompt/test semantic drift; it must not count toward the primary independent-case denominator.
- Final case acceptance: **not accepted**; registry inclusion: **false**; inference authorization: **false**.

## 8. Sources

- Frozen issue #1821: https://github.com/asdf-format/asdf/issues/1821
- Fix PR #1907: https://github.com/asdf-format/asdf/pull/1907
- Earlier partial fix PR #1825: https://github.com/asdf-format/asdf/pull/1825
- Stage 2 Actions run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/44914416693
- Artifact: https://github.com/MahmutVezir/dijitalikiz/actions/runs/44914416693/artifacts/14710853774