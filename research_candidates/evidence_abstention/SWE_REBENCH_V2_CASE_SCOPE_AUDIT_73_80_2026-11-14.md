# SWE-rebench V2 — cohort rows 73–80: PR scope and exact-base license audit

**Audit date:** 14 November 2026  
**Cohort:** 12 November 2026 tarihli sabit 96-proje primary cohort'un 73–80. satırları.  
**Audit scope:** Cohort metadata, GitHub PR/issue açıklamaları, exact PR base SHA, changed-file listeleri ve exact-base root LICENSE/NOTICE kayıtları. Upstream source checkout, package installation, target test execution, human adjudication, model loading, inference veya training yapılmadı.

## 1. Reproducibility inputs

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Immutable Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Primary cohort CSV: `SWE_REBENCH_V2_COHORT_96_PRIMARY_2026-11-12.csv`
- Primary CSV SHA-256: `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`
- Cohort manifest SHA-256: `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`
- GitHub Actions cohort artifact: run [43257277504](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43257277504), artifact ID `13960884569`.
- Retrieved ZIP SHA-256: `d9d1fc04cb84233c021006f13205623ea9aa390caa6eb54ca4bc9d974e9a4c6c`; ZIP CRC check passed.
- The local CSV byte count was 17,409 and matched the cohort manifest. Its SHA-256 matched the manifest.

All eight upstream PR base SHAs match their corresponding pinned cohort `base_commit` (**8/8**). This is a provenance/lineage check only, not proof of a defect or case acceptance.

## 2. Candidate-by-candidate findings

| Rank / cohort ID | PR / linked issue | PR base SHA | Exact-base root license | Scope decision |
|---:|---|---|---|---|
| 73 — `crewaiinc__crewai-2408` | [CrewAI #2408](https://github.com/crewAIInc/crewAI/pull/2408) / [#2402](https://github.com/crewAIInc/crewAI/issues/2402) | Match — `4f6054d439c602f93283eda351fe6b67133b9a84` | `LICENSE`, MIT-style permission text; blob `a6ee25527ec07201e4373fcbf89f128f304a6f2e` | Defect candidate |
| 74 — `microsoft__azuretre-4352` | [AzureTRE #4352](https://github.com/microsoft/AzureTRE/pull/4352) / [#2510](https://github.com/microsoft/AzureTRE/issues/2510) | Match — `78f4a1351625ce9f1f6bd4fcc532e396bf989338` | `LICENSE`, MIT; blob `9e841e7a26e4eb057b24511e7b92d42b257a80e5` | Exclude — feature request / new endpoint and UI |
| 75 — `aiogram__aiogram-1657` | [aiogram #1657](https://github.com/aiogram/aiogram/pull/1657) / [#1656](https://github.com/aiogram/aiogram/issues/1656) | Match — `78748d36fd1fe9a71c3d42a7a88e0b63edd1c3d7` | `LICENSE`, MIT-style permission text; blob `caa060cc11617395df2f01be9287264ab25f9c5f` | Exclude — enhancement / convenience API |
| 76 — `apiflask__apiflask-642` | [APIFlask #642](https://github.com/apiflask/apiflask/pull/642) / [#602](https://github.com/apiflask/apiflask/issues/602) | Match — `47e51cbbd2e067e793941ca9731a22088e145a94` | `LICENSE`, MIT; blob `e20c979e01b409151c1a6b2e6eac0a4315633d47`; root `NOTICE` blob `c336807cc098a26ab0e3b049d40c8860748055ee` | Exclude — interoperability option/enhancement; keep NOTICE obligations |
| 77 — `xknx__xknx-1663` | [XKNX #1663](https://github.com/XKNX/xknx/pull/1663) / [#1650](https://github.com/XKNX/xknx/issues/1650) | Match — `12ad7c9c7e081d68a91005c8ea2e7f5aac6a7bde` | `LICENSE`, MIT-style permission text; blob `89de354795ec7a7cdab07c091029653d3618540d` | Exclude — explicit feature request |
| 78 — `narwhals-dev__narwhals-1869` | [Narwhals #1869](https://github.com/narwhals-dev/narwhals/pull/1869) / [#1313](https://github.com/narwhals-dev/narwhals/issues/1313) | Match — `364a6256c0c57abae825a0c070fa4c19d6430d82` | `LICENSE.md`, MIT; blob `b9e2a9336ac1efccddbe91a123d45d8c490ebe74` | Defect candidate |
| 79 — `callowayproject__bump-my-version-325` | [bump-my-version #325](https://github.com/callowayproject/bump-my-version/pull/325) / [#317](https://github.com/callowayproject/bump-my-version/issues/317) | Match — `f60d60b07227729bc3d5b413be0906ca9fb86b8c` | `LICENSE`, MIT; blob `b3b84048fcde8217e54dd5acfd7541c98f9f01b3` | Conditional defect candidate — broad Mercurial refactor; issue-specific commit proof should be strengthened |
| 80 — `dynaconf__dynaconf-1293` | [Dynaconf #1293](https://github.com/dynaconf/dynaconf/pull/1293) / [#1235](https://github.com/dynaconf/dynaconf/issues/1235) | Match — `934a8f833bd2a9648d7bbb0174a00c83f8577675` | `LICENSE`, MIT; blob `cbc6bbf2903b0a3a7b4c1999b36cd32e6b301a66` | Defect candidate, with expected exit-code semantics to be frozen before acceptance |

### Rank 73 — CrewAI: optional prompt template causes AttributeError

Issue #2402 gives a concrete failure: configuring only `system_template` while leaving `prompt_template=None` raises `AttributeError: 'NoneType' object has no attribute 'replace'`. The report also notes the analogous missing-`response_template` path. PR #2408 changes `_build_prompt()` to fall back to the default format when either required template is absent and only process a response template when it exists. Its changed files are `docs/concepts/agents.mdx`, `src/crewai/utilities/prompts.py`, and `tests/agent_test.py`; it adds separate tests for system-only, prompt-only, and missing-response-template configurations.

**Decision:** retain as a defect candidate. Technical reproduction must use the issue's minimal setup, pin the CrewAI/Pydantic runtime, and show fail-on-base/pass-on-fixed. The model/LLM backend must not be needed merely to exercise initialization.

### Rank 74 — AzureTRE: view requests across workspaces

Issue #2510 is labelled `feature` and asks for a TRE-level view of airlock requests, a new API endpoint, and a UI menu. PR #4352 adds that endpoint and corresponding UI/repository behaviour across 13 files (+728/−48).

**Decision:** exclude. This is a feature request, not evidence of an existing software defect. Do not include it in a root-cause bug sample.

### Rank 75 — aiogram: shortcut methods for formatting kwargs

Issue #1656 is labelled `enhancement` and asks for a convenience method to avoid repeating `as_kwargs(text_key="caption", entities_key="caption_entities")`. PR #1657 adds shortcut methods for caption, poll question/explanation, and gift text kwargs, with tests and changelog. This adds convenience API surface rather than fixing incorrect existing behaviour.

**Decision:** exclude from the defect sample.

### Rank 76 — APIFlask: absolute OAuth redirect URI option

Issue #602 describes Swagger UI's relative redirect URI being rejected by Okta and explicitly questions whether the behaviour is an incompatibility rather than a bug. PR #642 adds the optional `docs_oauth2_redirect_path_external` parameter to support external/absolute redirect URLs; it changes `src/apiflask/app.py`, `tests/test_openapi_blueprint.py`, and `CHANGES.md`.

**Decision:** exclude from the root-cause defect sample. It is an interoperability enhancement/opt-in configuration, not a demonstrated failure of a documented existing contract.

**License notice:** the exact-base root `NOTICE` file exists. It identifies bundled third-party code and records attributions/conditions for APIFairy, Flask, and Flask-Marshmallow. Any later source reuse or redistribution must preserve and review the applicable notices; the MIT root LICENSE alone is not a complete representation of the repository's third-party obligations.

### Rank 77 — XKNX: configurable timezone for Datetime device

Issue #1650 is explicitly labelled a feature request: allow a Datetime device to use a configured timezone when the host is set to UTC. PR #1663 introduces `datetime.tzinfo` support for `localtime` and adds datetime/time tests, documentation and changelog updates.

**Decision:** exclude. This extends supported behaviour; the issue does not establish a defect in the previously documented behaviour.

### Rank 78 — Narwhals: timezone-aware Datetime columns omitted by Polars selector

Issue #1313 is labelled `bug: incorrect result` and provides a minimal example where `nw.selectors.by_dtype(nw.Datetime)` selects a naive Datetime column but omits a timezone-aware Datetime column in Polars, despite both being Datetime columns. PR #1869 changes Polars dtype normalization in `narwhals/_polars/namespace.py` and adds a timezone-aware selector regression test in `tests/selectors_test.py`.

**Decision:** retain as a strong defect candidate. Reproduction must pin Narwhals/Polars versions and check the exact expected selected-column set on the cohort base and fixed PR revision.

### Rank 79 — bump-my-version: Mercurial bump fails to create a commit

Issue #317 says that since version 0.30.0, running bump-my-version with `commit = true` in a Mercurial repository updates files but does not create a commit. PR #325 refactors `bumpversion/scm/hg.py`, changes shared error handling and project coverage configuration, and substantially expands `tests/test_scm/test_hg.py`. It adds an integration test that runs a bump and verifies the `v1.1.0` tag is present.

The issue and patch are aligned, and the new integration test uses a real temporary Mercurial repository. However, the PR is broad (+348/−33 across five files), and the shown integration assertion checks the tag rather than directly asserting that the bump-generated file changes appear in the Mercurial commit log.

**Decision:** keep conditionally. Before promotion, reproduce the issue exactly with `commit = true` and verify the post-bump file content is present in a new `hg log` commit, not merely that a tag exists. Check both configured commit and no-commit behaviour.

### Rank 80 — Dynaconf: missing key returns success exit status

Issue #1235 shows `dynaconf list -k D --json` printing “Key not found” but returning exit code 0; expected status is 1. It also contains an unresolved discussion of whether an empty JSON object could be preferable, so that policy must be frozen before confirmatory acceptance. PR #1293 changes the missing-key path to call `sys.exit(1)` and adds parametrized tests for `list`, `inspect`, and `get` missing-key commands.

**Decision:** retain as a defect candidate for technical reproduction. The experiment protocol must explicitly freeze the tested contract as “missing requested key produces non-zero exit status”; do not treat the PR's closure alone as evidence that this is the only acceptable CLI contract.

## 3. Aggregate outcome and remaining gates

| Check | Outcome |
|---|---:|
| Cohort rows audited | 8 |
| PR base SHA matches pinned cohort base | **8/8** |
| Exact-base root LICENSE file located | **8/8** |
| Root NOTICE file present | **1/8** (APIFlask; third-party notices recorded) |
| Strong defect candidates for technical reproduction | 2 (73, 78) |
| Additional defect candidates requiring protocol/reproducer freeze | 1 (80) |
| Conditional candidate requiring stronger commit-level reproduction | 1 (79) |
| Feature/enhancement/interoperability items excluded | 4 (74–77) |
| Accepted confirmatory cases added | **0** |
| Upstream target tests executed | **0** |
| Human evidence adjudications | **0** |
| Model inference / training | **0 / 0** |

Root LICENSE discovery does not complete legal clearance. The APIFlask `NOTICE` includes third-party attribution; other repositories may contain nested licenses, per-file notices, test fixtures, generated content, or dependencies whose obligations are not visible in a root-level lookup. The dataset's own CC BY 4.0 label does not override upstream source licensing. Do not redistribute source snapshots until relevant project and file-level permissions are reviewed.

## 4. Next bounded work

1. Continue static scope and exact-base PR checks with cohort rows 81–88.
2. Close the outstanding exact-base LICENSE/NOTICE and changed-file provenance checks for rows 17–56, and the repository redirect/base/license gap for row 64.
3. Create isolated reproducibility dossiers for rows 73 and 78 first; include row 80 only after freezing the missing-key exit-status contract; include row 79 only after its commit-level assertion is strengthened.
4. Do not execute upstream tests or use source artifacts until changed-file provenance and relevant license/NOTICE conditions are reviewed.
5. Keep all these candidates outside `CASE_REGISTRY.json` until exact base-fail/fixed-pass evidence, two independent blinded human panels, evidence-tier adjudication, and the global preregistration/sample gates are complete.

**Conclusion:** This audit advances candidate triage only. The confirmatory registry remains empty and model inference remains prohibited.
