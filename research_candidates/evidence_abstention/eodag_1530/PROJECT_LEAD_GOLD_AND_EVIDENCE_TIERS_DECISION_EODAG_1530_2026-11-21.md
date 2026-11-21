# Project-lead gold and evidence-tier decision — EODAG #1530

Date: 2026-11-21
Decision maker: student project lead
Decision route: source-aware, single project-lead technical adjudication for the v0.2 exploratory/feasibility study.

## Decision

The project lead approves the technical gold mechanism and approves EODAG #1530 to proceed as a case through the remaining v0.2 eligibility and registry gates.

This decision records the following tier dispositions:

- E3: **ABSTAIN**
- E2: **ABSTAIN**
- E1: **ANSWER**

The E2 disposition follows the operational distinction in the current study design: the pinned YAML reproducer directly demonstrates duplicate-key collapse in the exact source template, but the E2 packet does not yet show the in-repository fixture/loading path. At least two competing explanations remain possible at that tier, so a definitive answer is not warranted under P1. E1 adds the active test-fixture source path that loads the packaged template with `yaml.safe_load` and iterates the resulting provider mapping; the project lead judges that only the duplicate-key mechanism remains viable at E1.

## Approved technical gold

The exact buggy `eodag/resources/user_conf_template.yml` contains two top-level provider mappings named `geodes`. The first mapping contains the public Geodes API-key configuration; the second contains the Geodes S3 AWS-credential configuration. The packaged template is loaded with `yaml.safe_load`. Under the parser's ordinary mapping behavior, the later duplicate key replaces the earlier mapping, leaving one `geodes` mapping with AWS credential fields and no distinct `geodes_s3` mapping. PR #1536 renames the second key to `geodes_s3`, preserving both provider mappings.

The gold is limited to this duplicate-key/configuration defect. The separate `StacListAssets` change in PR #1536 is excluded. Issue #1517 (missing `result_type` during product-type discovery) remains related context but is a distinct mechanism and is not included in this case's gold.

## Predeclared alternatives and tier interpretation

The case's source-aware review considers these competing explanations:

- G1 — duplicate YAML mapping key: the second `geodes` mapping overwrites the first during parsing and no separate `geodes_s3` mapping is produced.
- A1 — wrong template or installed-source revision is loaded.
- A2 — a separate provider-registration or plugin-discovery failure causes the missing provider.
- A3 — a generated or user-specific configuration override independently changes the provider credentials.

The approved surviving-mechanism sets are:

- E3: G1, A1, A2, A3 — the issue narrative alone does not establish the exact parser result or the application's loading path.
- E2: G1, A2, A3 — exact pinned-template parsing removes A1, but does not yet connect the template to the in-repository fixture path.
- E1: G1 — the additional fixture-source evidence links the packaged template to `yaml.safe_load` and provider-configuration generation.

The EODAG #1530 packet set remains strictly nested (E3 subset E2 subset E1), with identical provenance/content for repeated evidence IDs. The approved labels are a source-aware project-lead judgment, not an independent blinded Panel A/Panel B result.

## Disclosed limitations and remaining gates

- Project-lead/researcher source exposure is **full** and disclosed. No researcher blinding is claimed; ChatGPT is an AI technical advisor only.
- The candidate-specific prior pipeline/debug exposure declaration remains **pending**. It must not be inferred as `none`; the frozen acceptance validator excludes a candidate if this value is not `none`.
- The bounded documentary license-scope acknowledgement for the exact retained EODAG source/data/reproduction artifacts remains **pending**. The inventory is not legal advice, legal clearance, or blanket redistribution permission.
- The complete schema-conformant case record, fail-closed registry validation and formal accepted-registry update remain pending until all mandatory gates pass.
- This decision does not authorize model loading, inference, fine-tuning or training. Inference remains disabled.

