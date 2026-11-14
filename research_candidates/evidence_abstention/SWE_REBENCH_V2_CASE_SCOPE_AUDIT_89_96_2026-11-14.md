# SWE-rebench V2 — Cohort rows 89–96 case-scope audit
**Audit date:** 14 November 2026  
**Status:** Static source/PR/metadata review only. No target tests were run. No case was accepted. No model inference or training was performed.

## 1. Frozen source and audit method

Primary source: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`  
Immutable Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`  
Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`  
Frozen cohort: `SWE_REBENCH_V2_COHORT_96_PRIMARY_2026-11-12.csv`  
CSV SHA-256: `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`  
Manifest SHA-256: `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`  
Cohort ZIP SHA-256: `d9d1fc04cb84233c021006f13205623ea9aa390caa6eb54ca4bc9d974e9a4c6c`  
ZIP CRC check: passed; frozen CSV contains 96 rows.

For each row, the audit checked the upstream PR, PR base commit against the cohort's pinned `base_commit`, linked issue(s), changed-file scope, root-level license at the pinned base commit, and root-level NOTICE presence. Repository redirects were resolved to the current repository name while retaining the original pinned commit. Root-level license presence is not a complete legal clearance: nested notices, vendored code, generated files, changed-file attribution, and per-file provenance remain separate checks.

**Result:** PR/base-SHA match **8/8**; exact-base root license file **8/8**; root NOTICE **1/8**. All eight PRs are merged upstream. These metadata checks do not make an experimental case accepted.

## 2. Row-by-row findings

| Cohort row | Instance / repository | PR and exact base SHA match | Exact-base root license | Scope decision |
|---:|---|---|---|---|
| 89 | `igorbenav__fastcrud-190` — current repo `benavlabs/fastcrud` | [#190](https://github.com/benavlabs/fastcrud/pull/190), yes — `7b9a4d113c75068558b63476128eb16036cdfdcf` | `LICENSE`, MIT; blob `e7eb605193d5af8de0f73290e1b080abc668f1ad`; no root NOTICE | Exclude: composite multi-issue PR |
| 90 | `pyfar__pyfar-722` — `pyfar/pyfar` | [#722](https://github.com/pyfar/pyfar/pull/722), yes — `648dda4c60c5a6f74acf335f7808c590c9d23929` | `LICENSE`, MIT; blob `430184952c6fcb292ee01cb114bb9c39f32f78ff`; no root NOTICE | Strong defect candidate |
| 91 | `gtalarico__pyairtable-422` — `gtalarico/pyairtable` | [#422](https://github.com/gtalarico/pyairtable/pull/422), yes — `eb1c815ea4b45999664d54fd84d16090539b8d42` | `LICENSE`, MIT; blob `eed8caa716e5203db18796cf2973324dc4f2f575`; no root NOTICE | Conditional defect candidate |
| 92 | `stanfordnlp__dspy-1853` — `stanfordnlp/dspy` | [#1853](https://github.com/stanfordnlp/dspy/pull/1853), yes — `2aa6f0172eff8d488b4d88e58168c97e641b6da0` | `LICENSE`, MIT; blob `be3f5c0e3fc7e6b0e7c9dddd9db313ab15bfa62b`; no root NOTICE | Conditional defect candidate |
| 93 | `joke2k__faker-2203` — `joke2k/faker` | [#2203](https://github.com/joke2k/faker/pull/2203), yes — `827585b134d730550820f307fb31a555d758c58c` | `LICENSE.txt`, MIT; blob `1e1ef066f06ea28525260b67c20d527381fafe74`; no root NOTICE | Conditional defect candidate |
| 94 | `owkin__pydeseq2-349` — current repo `scverse/PyDESeq2` | [#349](https://github.com/scverse/PyDESeq2/pull/349), yes — `9355b55e6c7c10c759db674d9a26d067be50b827` | `LICENSE`, MIT; blob `57721cc72e071560f61388d6784dfc5a73f21e25`; no root NOTICE | Strong defect candidate; issue-state discrepancy noted |
| 95 | `mitmproxy__pdoc-813` — `mitmproxy/pdoc` | [#813](https://github.com/mitmproxy/pdoc/pull/813), yes — `57ee1d628027feffbd734180287e74294ddab7df` | `LICENSE`, MIT; blob `9d75d3de543742e219b1c7301901a95f65ad353a`; no root NOTICE | Strong defect candidate |
| 96 | `aws-cloudformation__cfn-lint-3991` — `aws-cloudformation/cfn-lint` | [#3991](https://github.com/aws-cloudformation/cfn-lint/pull/3991), yes — `7fee6bdab9355e1c927dd4eab09c8b94c5a36402` | `LICENSE`, MIT No Attribution / MIT-0; blob `fc06cc4fe49b44e11bec7337390c85c509bfb4d7`; root NOTICE present, blob `7511ba9c6df2785abaa9ad656e8e01a7c178ef3e` | Conditional, partial issue fix |

### Row 89 — FastCRUD #190: exclude

The old repository path `igorbenav/fastcrud` redirects to `benavlabs/fastcrud`; the pinned base commit and PR #190 still match the cohort exactly. The PR is titled “Some fixes” and closes both #126 and #123. Its patch also changes behavior for `update()` when no row matches.

The changes cover at least three distinct concerns:
1. Dynamic-filter conversion of URL strings to typed UUID/int/string values (#126).
2. `get_multi()` type annotations and response-shape discussion (#123).
3. Raising `NoResultFound` instead of emitting a deprecation warning for a missing update target.

These are not one root cause or one isolated failure mode. The row should not enter a single-bug root-cause experiment as a combined case. Do not split one PR into multiple independent cohort cases without a separately frozen and justified design.

### Row 90 — pyfar #722: strong defect candidate

Issue [#721](https://github.com/pyfar/pyfar/issues/721) reports that `normalize(..., reference_method="energy")` and `"power"` do not achieve the requested target. The reported outputs scale inversely with energy (for example, input energy 20 yielded output energy 0.05 rather than target 1). PR #722 applies square-root scaling to the energetic reference and target, and adds parameterized tests across energy/power/RMS, multiple targets, and channel-handling modes.

This is a specific numerical defect with a concrete counterexample and a narrow causal change. The PR also restructures the normalization tests: several earlier expected-value rows are removed and replaced with the newer parameterized target assertions. A reviewer must compare that oracle change against the API semantics before acceptance. No test was executed in this audit.

### Row 91 — pyairtable #422: conditional defect candidate

Issue [#421](https://github.com/gtalarico/pyairtable/issues/421) describes a linked ORM field not respecting `Meta.use_field_ids=True` when populated. The PR changes `Model.from_ids()` to reuse `cls.all(...)`, thereby passing the model's normal request settings through the same path used elsewhere. It adds a test asserting that the Airtable request includes `returnFieldsByFieldId=1`.

The implementation-level behavior is testable and the PR is small. The issue is phrased as a usage question rather than a precise bug report, so acceptance requires an independent reviewer to confirm that the expected contract is unambiguous and that the test's fixture captures a genuine base-commit failure rather than only a preferred usage pattern.

### Row 92 — DSPy #1853: conditional defect candidate

Issue [#1826](https://github.com/stanfordnlp/dspy/issues/1826) reports a `TypeError` when a Pydantic input object contains a `datetime` that is not natively JSON serializable. PR #1853 centralizes serialization/formatting utilities and updates both ChatAdapter and JSONAdapter. It adds tests for datetime-bearing Pydantic inputs/outputs and enum inputs/outputs, plus generated reliability fixture changes.

The underlying serializer failure is concrete, but the PR is broader than the single datetime report: enum conversion and common utility extraction are also changed. Keep it conditional until the exact datetime failure can be isolated into a minimal failing/passing test pair and the additional enum/format changes are shown not to confound the target task.

### Row 93 — Faker #2203: conditional defect candidate

Issue [#1817](https://github.com/joke2k/faker/issues/1817) reports `fake.unique.profile()` raising `TypeError: unhashable type: 'dict'`. PR #2203 converts dictionaries, lists, and sets to hashable representations for membership in the unique-value set while returning the original generated value. The patch adds a test that calls `unique.pydict()`, `unique.pylist()`, and `unique.pyset()`.

The mechanism matches the reported TypeError. However, the new test does not explicitly assert that repeated calls remain distinct; it primarily checks that complex return types do not crash. Before acceptance, add/verify assertions for returned-value uniqueness and representative nested structures. The patch also changes a development dependency lower bound and includes unrelated text/style changes; isolate those from the defect under study.

### Row 94 — PyDESeq2 #349: strong defect candidate, with issue-state caveat

The original repository path `owkin/PyDESeq2` now resolves to `scverse/PyDESeq2`; the cohort's pinned base commit matches PR #349 exactly. PR #349 addresses issue [#347](https://github.com/scverse/PyDESeq2/issues/347), where the negative-binomial GLM used by `lfc_shrink()` can stop before convergence, producing unstable or aberrant shrunken log-fold changes for very large counts (including sign changes). The patch tightens SciPy optimizer `ftol`/`gtol` and adds a large-count reference test against R output.

This is a consequential numerical defect with a focused parameter change and a new reproducible test fixture. **Caveat:** issue #347 still reports as open in the repository even though PR #349 is merged and says it fixes #347. Treat closure/resolution as unconfirmed until the exact base/fixed test pair and issue state are reconciled by a human reviewer.

### Row 95 — pdoc #813: strong defect candidate

Issue [#812](https://github.com/mitmproxy/pdoc/issues/812) reports that `python -m pdoc .` fails with `ValueError: No modules found matching spec: .`. PR #813 resolves the local path with `Path.resolve()` and adds a test that changes into a nested package directory before checking both `parse_spec(".")` and `parse_spec("..")`.

The reported command, affected path handling, fix, and regression test align closely. This is a narrow candidate. Acceptance still requires running the exact base failing test and fixed passing test in the frozen environment.

### Row 96 — cfn-lint #3991: conditional, partial issue fix

Issue [#3614](https://github.com/aws-cloudformation/cfn-lint/issues/3614) reports two distinct CodeBuild validation gaps: (a) S3 source should require `Location`; and (b) an S3 artifact `Location` should not contain forward slashes. PR #3991 adds rule E3636 and a JSON schema requiring `Location` when the relevant `Type` is `S3`. Its tests cover the missing-`Location` condition.

The patch does **not** implement the reported forward-slash restriction for artifact `Location`. Therefore it is not a complete fix for the whole issue. It may be considered only as a narrowly scoped case for the missing-`Location` subproblem, after confirming the frozen fail-to-pass tests target that subproblem and do not expect the unimplemented second behavior.

Root NOTICE content: `cfn-flip — Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.` This attribution must be retained and checked against any source files actually used in a case.

## 3. Cohort-level decision

- Strong defect candidates: **3** — rows 90, 94, 95.
- Conditional candidates: **4** — rows 91, 92, 93, 96.
- Excluded: **1** — row 89.
- Exact PR/base SHA match: **8/8**.
- Exact-base root license: **8/8**.
- Root NOTICE: **1/8**.
- Newly accepted confirmatory cases: **0**.

“Strong” and “conditional” are static screening categories only. Neither category is a case acceptance, and neither substitutes for a demonstrated failing test at the exact base commit followed by a passing test at the exact fix commit.

## 4. Required next gates

For each potential case, before changing `CASE_REGISTRY.json`:
1. Pin the issue, PR, base SHA, merge/fix SHA, changed-file list, license/NOTICE blobs, and source dataset row in a versioned evidence packet.
2. Obtain the exact upstream fail-to-pass test identifiers and verify they test the stated issue rather than adjacent behavior.
3. Reproduce failure at the pinned base and pass at the pinned fix in an isolated, recorded environment; save full logs and hashes.
4. Have two independent reviewers adjudicate the evidence-supported root cause without seeing model outputs; reconcile disagreements.
5. Review nested notices, vendored/third-party code, per-file copyright, and the right to store/redistribute any source snippets.
6. Freeze case evidence and hashes, then separately re-run the fail-closed readiness gate.

**No inference, fine-tuning, or result claims are authorized by this audit.** The prior preflight remains `ready=false`; the latest known status is 21 blockers and zero accepted cases/projects. Cohort rows 89–96 do not remove those blockers.
