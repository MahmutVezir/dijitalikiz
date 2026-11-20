# CS-SI/eodag #1530 — proposed technical gold and E1/E2/E3 adjudication

Date: 20 November 2026  
Status: advisory proposal only; project-lead approval is pending.

## Candidate identity

- Upstream issue: https://github.com/CS-SI/eodag/issues/1530
- Fix PR: https://github.com/CS-SI/eodag/pull/1536
- Exact buggy base: `b7cc06e19025e5bbf14e28a0975f1749e21e9be3`
- Exact fixed PR head: `312966a46513a082333d46cd7212bdce36aaf769`
- Frozen dataset row: `cs-si__eodag-1536`
- Canonical row SHA-256: `35f612f1b6524f37cca6766f25a0637bc5d5740da9695427dba556354ce61a47`

## Proposed gold mechanism

The exact buggy `eodag/resources/user_conf_template.yml` contains two top-level provider mappings named `geodes`: the first holds the public Geodes API-key credential configuration; the second holds the AWS credentials intended for Geodes S3. The test helper `write_eodag_conf_with_fake_credentials` reads that exact template using `yaml.safe_load`, then iterates the resulting mapping to create the mock credential configuration. The duplicate key is collapsed during YAML loading, so the parsed mapping contains only one `geodes` entry, with the latter AWS-credential mapping, and no distinct `geodes_s3` key. That removes the public Geodes API-key schema and leaves the expected S3 provider configuration absent. PR #1536 renames the second key to `geodes_s3`, allowing both mappings to coexist.

This gold is deliberately limited to the duplicate-key/configuration defect. PR #1536 also adds `StacListAssets` to a separate plugin-type list in `eodag/config.py`; that change is out of scope for this case and must not appear in the gold mechanism.

## Competing mechanisms to retain before adjudication

1. **G1 — duplicate YAML mapping key:** the second `geodes` mapping replaces the first during `yaml.safe_load`, and the S3 mapping is not available under `geodes_s3`.
2. **A1 — wrong template or installed-source revision:** the runtime or test helper loads a different template than the exact pinned source under review.
3. **A2 — separate provider-registration/plugin discovery failure:** `geodes_s3` is absent because of provider registry configuration rather than the duplicate mapping.
4. **A3 — user-config/environment override:** a generated or user-specific configuration overwrites the provider credentials independently of the template.
5. **A4 — issue #1517 product-type discovery defect:** missing `result_type` in discovery configuration. This is a related but distinct issue, not part of #1530's gold.

The pinned issue reproducer uses the exact `EODAG_SOURCE_ROOT`; the base fails because `geodes_s3` is absent from the YAML-parsed mapping and the fixed revision passes. The frozen unit-test selectors are run in a fixture that generates its configuration from the same packaged template. These observations strongly favor G1; source-aware project-lead adjudication remains pending.

## Proposed evidence-tier outcomes

| Tier | Contents | AI advisory recommendation | Reason |
|---|---|---|---|
| E3 | Frozen issue narrative, including the duplicate-key YAML excerpt and the reported public-Geodes credential failure | **ABSTAIN (provisional)** | The issue exposes two same-named mappings, but does not show the exact parser output or the in-repository fixture path. The specific last-mapping-wins effect is strongly suggested, not yet observed in the pinned project runtime. |
| E2 | E3 plus independent pinned YAML reproducer and base output showing `geodes_s3` missing after parsing; the same reproducer passes on fixed source | **ANSWER (provisional)** | The exact pinned source template is parsed and the observable mapping matches the predicted loss of `geodes_s3`; the duplicate-key mechanism is directly supported by a reproducible base/fixed contrast. |
| E1 | E2 plus active pinned source excerpts from `tests/utils.py` showing `yaml.safe_load` of the packaged template and the subsequent provider iteration/config generation, with the base test fixture and selectors | **ANSWER (provisional)** | The implementation/test-fixture path links the exact duplicate-key template to the generated test configuration and observed missing provider. |

The key design distinction is whether E3 should already support an evidence-based answer because the issue includes the duplicate YAML snippet. The project lead should decide this explicitly; do not promote an answer merely because the defect is easy to guess.

## Reproduction already recorded

- Independent YAML reproducer: the pinned buggy base failed because `geodes_s3` was absent from the parsed mapping; the same reproducer passed on the pinned fixed revision.
- Frozen selectors:
  - `tests/units/test_core.py::TestCore::test_available_sortables`
  - `tests/units/test_core.py::TestCore::test_list_product_types_for_provider_ok`
- Buggy base: 2/2 selectors executed and failed on the expected missing-provider/sortables behavior.
- Fixed PR head: same selectors passed 2/2.
- Test-only patch changed `tests/units/test_core.py` only; no production source was patched into the buggy base.
- Artifact 14440370494; SHA-256 `6a732364873d12d78d407f41aa671cc56851f67b58492c4762ff33e36a59a437`; ZIP CRC PASS; 22/22 internal hashes PASS.

This is one issue-specific case, not three cases (two selectors plus one reproducer are corroborating routes only).

## Open decisions

- Project-lead source-aware gold mechanism approval.
- Project-lead E1/E2/E3 outcome approval, including the E3 boundary.
- Truthful prior pipeline/debug exposure declaration.
- Bounded license-scope acknowledgement.
- Complete schema-conformant case record, fail-closed registry validation, and separate final YES/NO decision.

No model loading, inference, fine-tuning or training is authorized by this proposal.
