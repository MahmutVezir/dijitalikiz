# Stage 3 AI advisory — EODAG #1530

Date: 20 November 2026  
Role: technical advisory and evidence audit only; not a project-lead decision.

## Defect and scope

Issue #1530 reports that the public Geodes provider and Geodes S3 provider use the same top-level `geodes` key in `user_conf_template.yml`. The exact pinned base file confirms two consecutive `geodes` mappings. The first contains `apikey`; the second contains AWS access-key, secret-key and session-token fields.

The independent reproducer loads the exact source file with `yaml.safe_load`. On the buggy base the parsed mapping has no `geodes_s3`; the surviving `geodes` mapping contains the AWS credential keys. The fixed revision renames the second key to `geodes_s3`, and the same test passes.

The upstream test helper in the pinned base, `write_eodag_conf_with_fake_credentials`, reads the packaged template with `yaml.safe_load`, loops over the resulting provider mapping, and writes a mock credential file. This provides a direct link between the duplicate key and the test fixture. The frozen selectors then fail on the base and pass on the fixed revision.

## Gold scope

The proposed gold is the duplicate top-level YAML key in the user configuration template and the resulting loss of the separate `geodes_s3` provider mapping. PR #1536 also modifies `eodag/config.py` to add `StacListAssets`; that is a separate change and is excluded from the #1530 gold.

Issue #1517 is related in provider area but has a distinct product-type discovery defect (missing `result_type`); it must not be merged into #1530. Later issues #1939, #1941, #1978 and #2376 describe other configuration, product mapping, retrieval and archive extraction behaviors; they are not additional instances of this defect. One EODAG repository contributes at most one case.

## Evidence-tier advisory

The issue narrative contains the duplicate YAML excerpt. It is more informative than a symptom-only issue, so E3 sufficiency is a genuine project-lead judgment rather than an automatic abstention. The proposal recommends E3=ABSTAIN only for a narrow question about the actual parser/fixture mechanism; E2=ANSWER once the pinned reproducer demonstrates the parse result; and E1=ANSWER once the project fixture path is evidenced. The project lead must decide the operational answer boundary.

## License and exposure limits

The exact upstream root license is Apache-2.0; the selected dataset row uses that as a source-repository license field, while the dataset itself is recorded as CC-BY-4.0. The Stage 2 artifact's 52-package metadata inventory is not legal clearance and does not inspect every native/bundled library. No full environment wheel/binary redistribution is proposed.

The project lead has reviewed issue, PR, source and reproduction evidence; full source exposure is disclosed. Prior candidate-specific pipeline/debug exposure has not yet been declared and must not be assumed to be none. No blind-review or inter-rater reliability claim is made.

## Status

Stage 2 technical reproduction: passed and artifact integrity verified.  
Gold/tier project-lead decision: pending.  
Prior pipeline/debug exposure declaration: pending.  
Bounded license-scope acknowledgement: pending.  
Final case acceptance: not accepted.  
Model loading, inference, fine-tuning and training: not authorized.
