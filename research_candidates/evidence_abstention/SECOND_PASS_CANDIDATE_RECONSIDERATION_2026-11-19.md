# Second-pass candidate reconsideration register — 19 November 2026

**Study:** SWE-rebench V2 evidence-abstention exploratory study  
**Primary frozen cohort:** 96 distinct upstream projects  
**Decision owner:** student project lead  
**Status:** two prior internal second-pass exclusions reopened for a controlled reconsideration review; neither is restored to the strict primary intake yet.

## 1. Who made the earlier exclusions?

The two records were marked `excluded_strict_bug_shortlist` during the project's own second-pass technical/oracle screen. They were not excluded by TÜBİTAK, an external jury, Hasan, Batuhan, or a formal independent review panel. The original ledger recorded the reasons, but the decision had not yet been put before the proposed human reviewers.

The frozen dataset, original selector IDs and original second-pass notes remain unchanged. This document does not overwrite history or silently repair a frozen benchmark row.

## 2. Candidate A — databricks/dbt-databricks #994 / PR #995 (primary rank 8)

**Earlier disposition:** excluded from the strict primary shortlist because the PR's newly added tests do not detect the reported bug.

**What the source issue reports:** UUID hyphens in temporary table identifiers cause an invalid Databricks SQL identifier and a session-close cleanup/drop failure, leaving temporary tables behind.

**Why the original PR oracle was rejected:**
- The uniqueness test also passes on the buggy implementation because the buggy code already appends a fresh UUID.
- The character test uses `re.match` against a string beginning with an underscore after removing the initial suffix. The first character is allowed, so the regex can return no match without inspecting later UUID hyphens.
- The added tests do not execute incremental materialization and session-close cleanup.

**Reconsideration route:** create a separate, clearly labelled research-authored defect-specific reproducer, not a replacement or rewrite of the frozen dataset selectors. A defensible test should use a deterministic hyphenated UUID and prove that the buggy identifier reaches the SQL/cleanup path with illegal characters while the exact fixed revision emits a valid identifier and cleanup succeeds (or, where a full adapter integration is infeasible, explicitly limit the claim to the identifier-generation contract and do not claim end-to-end cleanup).

**Required before any promotion:**
1. Exact Parquet row and original selectors authenticated and preserved.
2. The new test is authored from the issue's observable contract, separately stored, and never represented as the original SWE-rebench selector.
3. Exact pinned buggy base produces a real defect-specific assertion failure; exact fixed revision passes the same new test.
4. The test does not simply restate the PR implementation or inspect whether a hyphen was replaced by an underscore without establishing the user-visible invalid-identifier contract.
5. A protocol amendment explicitly states whether this becomes a supplemental exploratory case or is excluded from the primary frozen-selector analysis.
6. Reviewers record yes/no and rationale.

**Current disposition:** `RECONSIDERATION_PENDING_INDEPENDENT_TEST_AND_PANEL_DECISION`. Not counted among the 65 strict primary candidates; not permanently erased from research provenance.

## 3. Candidate B — simpeg/simpeg #1609 / PR #1633 (primary rank 63)

**Earlier disposition:** excluded because the PR deprecates the ambiguous `Survey.components` property rather than changing it to an integer, and the previous second-pass screen considered this inconsistent with the expected integer-return interpretation.

**New source-level verification:**
- The actual defect report is issue [#1609](https://github.com/simpeg/simpeg/issues/1609), titled “Inconsistency between docstring and result of ... Survey.components()”.
- The issue gives a single-receiver example where the property returns a component-name list although its docstring says `int`.
- Crucially, the issue itself says that for heterogeneous receivers the expected value is unclear (1 or 2, or perhaps not defined); it explicitly asks what the correct result should be.
- PR [#1633](https://github.com/simpeg/simpeg/pull/1633) says the property is misleading because receivers in one survey can have different components. It deprecates the survey-level property and directs callers to iterate over sources/receivers.
- The PR adds deprecation-warning tests in `tests/pf/test_components.py`. The fixed gravity survey property carries a `FutureWarning` deprecation decorator and explains why a single survey-level component property is ambiguous.

**Why the previous rejection may be too strong:** interpreting the issue solely as “return an integer count” ignores the issue author's own acknowledgement that the heterogeneous-receiver expected value is undefined. Deprecating a misleading abstraction may be a legitimate resolution of the broader reported defect. It is not automatically a valid candidate, but it merits a human scope review rather than an unqualified exclusion.

**Reconsideration route:** reframe the candidate only if the review panel agrees that the research target is the misleading/underspecified survey-level API contract, not an integer conversion. The gold mechanism would need to describe why selecting the first receiver's components cannot represent a heterogeneous survey, and why deprecation plus receiver-level iteration is the chosen resolution. The E1/E2/E3 packets must distinguish this from a mere docstring typo or an alternative policy of returning a union/count.

**Required before any promotion:**
1. Re-authenticate the exact frozen Parquet row and every original FAIL_TO_PASS selector.
2. Demonstrate each relevant selector on the exact buggy base and fixed revision; collection/setup errors are not failures.
3. Verify selector semantics against issue #1609 and PR #1633; preserve the PR #1633 and issue #1609 resource identities separately.
4. Predeclare the reframed problem, competing API-contract hypotheses, and E1/E2/E3 evidence before any model outputs.
5. Obtain independent human yes/no approval of the new framing and whether it belongs in the primary or supplemental exploratory set.
6. Keep the older second-pass rationale visible as a superseded screening judgement, not deleted.

**Current disposition:** `RECONSIDERATION_PENDING_ROW_SELECTOR_AND_HUMAN_SCOPE_REVIEW`. Not counted among the 65 strict primary candidates yet; not permanently erased from research provenance.

## 4. Count policy

Until the two reviews complete:
- Strict primary shortlist stays **65**.
- The two reconsideration candidates are tracked separately as **2 conditional re-review records**.
- Separate distinct-project reserve pool stays **17**.
- The broad pipeline view may therefore be described as **65 strict-queue + 2 re-review + 17 reserve = 84 tracked candidate pathways**, not 84 eligible or accepted defects.
- Within-project alternatives remain replacements within their project and do not create independent projects.
- Final accepted cases remain **0**.

If a candidate is promoted, update the study protocol, denominator and progress ledger transparently in a versioned amendment. Do not retroactively rewrite the frozen 96-row cohort or the original second-pass decision.

## 5. Reviewer decision requested

For each candidate, reviewers should answer independently:
- **YES** — approve the described reconsideration route.
- **NO** — retain exclusion from the primary study.
- **REVISE** — provide the specific evidence or protocol amendment required.
- **OUT OF SCOPE** — not within the reviewer's competence.

No candidate is promoted by this document. The student's project-lead decision is recorded only after reviewer responses and evidence are available.
