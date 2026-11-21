# django-bird #219 — static scope, frozen-row and source-license candidate review

**Date:** 21 November 2026  
**Frozen cohort rank:** 55  
**Candidate:** joshuadavidthomas/django-bird issue #218 / PR #219  
**Disposition:** **STRONG PROVISIONAL SOFTWARE-BUG CANDIDATE; EXACT ROW AUTHENTICATED; HOLD BEFORE STAGE 2**  
**Research mode:** single-human exploratory/feasibility study. The student project lead is the only human participant and decision-maker; ChatGPT is advisory only.

## 1. Executive finding

The issue/PR pair has strong defect-to-fix alignment. The issue reports that rendered asset URLs omit the \`django_bird\` prefix even though collected files live beneath that prefix. The fix changes the custom storage's URL generation to prepend the configured prefix once, and the modified tests assert the corrected URL across direct, template-inheritance, manifest, debug and fallback paths.

The frozen dataset row is authenticated against the pinned SWE-rebench Parquet snapshot. It contains **9 FAIL_TO_PASS selectors and 42 PASS_TO_PASS selectors**. The exact source-project license is MIT at the buggy base and fixed PR head.

This is still a provisional candidate. No upstream tests, package install, source checkout, build, model loading, inference, fine-tuning or training were run by the row-audit workflow. Stage 2 has not been run for this candidate. The project's frozen sequential queue does not permit starting rank 55 Stage 2 while rank 52 GeoPandas remains unresolved. Candidate-specific prior pipeline/debug exposure also requires an explicit project-lead declaration before acceptance.

## 2. Frozen dataset identity and integrity

- Dataset: \`PrimeIntellect/SWE-rebench-V2-Filtered-Verified\`
- Pinned revision: \`fb9aa226b2ce37c708ea7732e7b980abacdadb67\`
- Whole Parquet SHA-256: \`7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9\`
- Size: 226,272,977 bytes
- Rows: 6,272
- Cohort rank: 55
- Exact instance ID: \`joshuadavidthomas__django-bird-219\`
- Repository: \`joshuadavidthomas/django-bird\`
- Base commit: \`6641de58a71e94689fb96c09a3aca25aab8efc25\`
- Dataset \`created_at\`: \`2025-03-06 20:48:48\`
- Language: Python
- Row source-license field: **MIT**
- Canonical row SHA-256: \`c1517308f6845a31dc32ba4302a63e1558f3d4782134663d1d3b9dff654197d7\`
- Problem-statement SHA-256: \`930ce28cd067c4e99ec11f1a4471d406bf592a7f85c04dc3fc1d4914a9ebf829\`
- Patch SHA-256: \`c7ec362ec55a0081d9125f9a455fc8a204fb039aa3edcab950922361093d1d83\`
- Test-patch SHA-256: \`e688f7613958cf9714c4e81cc6ebf05c9af6ca7c688d4ed22910c25ae552343d\`

Metadata-only extraction:
- Workflow run: [44941417507](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44941417507)
- Job: \`136959235620\`
- Artifact ID: \`14721782351\`
- Artifact SHA-256: \`c5f69851b84d7e54d02b7aeb3b2e37888331d716c06d229e628acff966ecf529\`
- Downloaded ZIP bytes: 1,808
- Members: \`row-audit-metadata.json\`, \`SHA256SUMS.txt\`
- ZIP CRC: passed
- Internal metadata file SHA-256: \`55f6ff23c7f430b730cd3be4b7c3956d1b9c458928a7eec4a705bfab8d14a7ae\`
- Internal checksum file matches the metadata file.

The workflow discovered the exact row from immutable base SHA + PR-number suffix + repository slug. It checked the full canonical row in memory to compute hashes, but did not retain the raw problem statement, patch or test patch in the uploaded audit artifact. It performed metadata extraction only.

### Frozen selectors

**FAIL_TO_PASS (9):**
1. \`tests/test_staticfiles.py::TestAssetClass::test_url\`
2. \`tests/templatetags/test_asset.py::TestManifest::test_asset_tag_with_manifest_in_production\`
3. \`tests/templatetags/test_asset.py::TestManifest::test_asset_tag_fallback_when_template_not_in_manifest\`
4. \`tests/templatetags/test_asset.py::TestManifest::test_asset_tag_in_debug_mode\`
5. \`tests/templatetags/test_asset.py::TestTemplateTag::test_unused_component_asset_not_rendered\`
6. \`tests/templatetags/test_asset.py::TestTemplateTag::test_template_inheritence_no_bird_usage\`
7. \`tests/templatetags/test_asset.py::TestTemplateTag::test_component_render_order\`
8. \`tests/templatetags/test_asset.py::TestTemplateTag::test_template_inheritence\`
9. \`tests/templatetags/test_asset.py::TestTemplateTag::test_asset_duplication\`

**PASS_TO_PASS:** 42 selectors. Their exact identities are recorded in the metadata-only artifact.

The nine failing selectors cover the direct asset URL and multiple rendering paths (manifest production, manifest fallback, debug mode, inheritance, unused assets, ordering and deduplication). This is better than relying on a single isolated assertion, but selector adequacy and base-fail/fixed-pass behavior remain unverified until authorized Stage 2 execution.

## 3. Upstream issue and PR scope

- Issue: [#218 — Static file urls not correct](https://github.com/joshuadavidthomas/django-bird/issues/218)
- PR: [#219 — Fix static URLs to include django_bird prefix](https://github.com/joshuadavidthomas/django-bird/pull/219)
- Issue created: \`2025-03-06T20:40:27Z\`
- PR created: \`2025-03-06T20:48:48Z\`
- PR merged: \`2025-03-06T20:50:06Z\`
- Exact PR base: \`6641de58a71e94689fb96c09a3aca25aab8efc25\`
- PR commits:
  - implementation/tests: \`365691a865a80378d6002b9a8ea8fada08c660f2\`
  - changelog-only follow-up: \`ead809ef6f8c4a65610bd3f0e13d46f1a2c9c5e9\`
- PR merge commit: \`f15bd054cc393bc0d00b5ab4f7fe1ca253c80302\`

The exact PR changed four paths:
- \`src/django_bird/staticfiles.py\` — implementation change;
- \`tests/test_staticfiles.py\` — direct asset URL regression assertion;
- \`tests/templatetags/test_asset.py\` — rendered asset URL assertions across template contexts;
- \`CHANGELOG.md\` — release note only.

The issue has zero follow-up comments; the PR has zero review comments. The PR description and implementation commit message both identify \`BirdAssetStorage\` as not applying the \`django_bird\` prefix to generated URLs. That explicit implementation attribution is kept out of the E3 issue-body packet and reserved for E1 source-aware evidence.

## 4. Implementation-level gold and alternatives

**Recommended gold mechanism:**

\`G1_BIRD_ASSET_STORAGE_URL_OMITS_CONFIGURED_STORAGE_PREFIX\`

The \`Asset.url\` path resolves a static asset, calculates a path relative to its template directory and passes that relative name to \`self.storage.url(...)\`. \`BirdAssetStorage.__init__\` stores the configured \`prefix\`, but at the buggy base it does not override \`url()\` to apply that prefix. The inherited storage URL method therefore emits a path that omits \`django_bird\`. The fix adds an idempotent prefix step before delegating to the parent URL implementation.

This is an implementation-mechanism statement, not simply “the URL should contain the prefix.”

**Predeclared alternative mechanisms:**

- \`A1_ASSET_RELATIVE_PATH_OR_FINDER_DROPS_PREFIX\`: the URL mismatch is introduced while \`Asset.relative_path\` or the finder-derived \`static_relative_path\` is constructed, rather than in storage URL generation.
- \`A2_STATIC_STORAGE_BASE_URL_OR_LOCATION_CONFIGURATION\`: the configured Django static base URL or storage location composition is inconsistent with the collected path, rather than the custom storage's missing URL-prefix application.

These alternatives are testable against the pinned source control flow. They must remain predeclared before any model output is inspected.

## 5. Recommended evidence tiers — advisory only, not yet project-lead approved

| Tier | Advisory decision | Rationale |
|---|---|---|
| E3 | **ABSTAIN** | The frozen issue states the missing \`django_bird\` path component and identifies a storage-prefix/Asset-URL disconnect, but does not identify which internal path transformation loses the prefix. G1, A1 and A2 remain plausible under the implementation-mechanism target. |
| E2 | **ABSTAIN** | Add the fixed-revision regression-test source showing the expected prefixed URL across test contexts, but do not expose the PR description or implementation body. This confirms the required behavior, not whether the fault is in path derivation, storage URL generation or configuration. G1 and at least one alternative remain plausible. |
| E1 | **ANSWER** | Add the exact buggy/fixed \`Asset.url\` and \`BirdAssetStorage\` source, the PR description and the patch-level source change. The base passes the unprefixed relative name to inherited URL handling without using the stored prefix; the fix applies the prefix at \`BirdAssetStorage.url\`. G1 is the surviving mechanism. |

**Answerability warning:** the E3 issue statement is unusually diagnostic: it explicitly points to the difference between the storage prefix and the generated URL. This creates a moderate-to-high easy-answer risk. The recommended E3 ABSTAIN is defensible only because the diagnostic target is the precise implementation location/mechanism, not merely identifying “a missing prefix.” The project lead should challenge this boundary before freezing packets. If the project lead concludes that E3 already uniquely establishes G1, exclude the case from the strict three-tier abstention sample rather than forcing an E3 abstention.

There are no issue comments or PR review comments to create a natural E2 discussion layer. The fixed regression-test source provides the E2 addition, but the E2 packet must be reviewed carefully for a meaningful and defensible distinction from E3. If it does not support a genuine nested tier, record the case as unclassifiable and exclude it from the three-tier comparison.

## 6. Source license and provenance

At the exact buggy base and fixed PR head:
- Root \`LICENSE\` path: \`LICENSE\`
- LICENSE Git blob SHA-1: \`c159dcad5e8808651d43e7faf1c0e79dac7b322e\` (identical at base and fixed head)
- \`pyproject.toml\` Git blob SHA-1: \`b3d9888d87871ca3d6622eb757c84e85d5e7c063\` (identical at base and fixed head)
- \`pyproject.toml\` declares \`license = {file = "LICENSE"}\`
- License: **MIT**

The four PR-changed paths do not alter the root license or the project license declaration. The dataset publisher declares CC BY 4.0 for the curated dataset; the row-level source-license field identifies MIT for the upstream repository. These are separate layers. Preserve appropriate MIT attribution if source code/diffs are redistributed and attribute the dataset if dataset-derived material is published. This is a documentary screen, not legal clearance. No dependency binary/environment/license screen has been completed for this candidate.

Pinned license/source links:
- [MIT license at exact buggy base](https://github.com/joshuadavidthomas/django-bird/blob/6641de58a71e94689fb96c09a3aca25aab8efc25/LICENSE)
- [Project metadata at exact buggy base](https://github.com/joshuadavidthomas/django-bird/blob/6641de58a71e94689fb96c09a3aca25aab8efc25/pyproject.toml)
- [Buggy-base storage code](https://github.com/joshuadavidthomas/django-bird/blob/6641de58a71e94689fb96c09a3aca25aab8efc25/src/django_bird/staticfiles.py)
- [Fixed storage code](https://github.com/joshuadavidthomas/django-bird/blob/ead809ef6f8c4a65610bd3f0e13d46f1a2c9c5e9/src/django_bird/staticfiles.py)

## 7. Exposure and execution boundary

- Project structure: one human participant, the student project lead. ChatGPT is advisory only.
- Researcher exposure to the issue, PR, changed files, source and tests reviewed in this static audit: **full and disclosed**.
- Candidate-specific prior pipeline/debug exposure: **not yet declared by the project lead**. Do not assume \`none\` from the absence of a matching entry in older exposure records.
- No upstream repository checkout, package installation, upstream test or build, model loading, inference, fine-tuning or training was performed during frozen-row authentication.
- Stage 2: **not started**.
- Final acceptance: **not accepted**.
- Registry inclusion: **false**.
- Model inference: **not authorized**.

## 8. Current gate and next step

The frozen queue remains sequential. GeoPandas #3591 at rank 52 is still **HOLD** pending its separate final project-lead decision. Therefore rank 55 django-bird may be statically screened and documented, but its Stage 2 reproduction must not start until rank 52 is formally accepted or excluded according to the unchanged protocol.

Before any later Stage 2 authorization:
1. the project lead must disclose candidate-specific prior pipeline/debug exposure;
2. the project lead must approve or revise the gold mechanism and the proposed E3/E2/E1 boundaries;
3. the fixed selector set and exact base/fixed source revisions must be independently authenticated in the pinned Stage 2 workflow;
4. the environment and dependency license/notice scope must be reviewed;
5. the project lead must separately authorize Stage 2.

**Current disposition: HOLD — strong provisional candidate; no case acceptance and no model inference.**
