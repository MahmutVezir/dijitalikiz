# Confirmatory Scoring Protocol Amendment (2026-10-09)

## Status
This protocol is a pre-confirmatory amendment. The frozen 40-run pilot has completed, but no confirmatory inference has been run. The main manifest must remain `draft` until the rubric, tests, case records, and hashes pass validation.

## Why this amendment exists
The pilot's legacy complete-diagnostic score required exact normalized matches for component, entity, and machine-form root-cause labels, plus literal operation and relation tokens. This is reproducible, but it can count a substantively explanatory paraphrase as a failure. We do not rewrite the pilot's original records or legacy evaluation. We record the limitation and change the *pre-confirmatory primary endpoint* to match the stated research question more directly: root-cause correctness.

Pilot outputs were consulted only to diagnose this scoring-protocol problem. Confirmatory outputs have not been consulted, and root-cause aliases are derived from the frozen confirmatory case records and source facts, not model outputs. This amendment and its reason must be reported in the final TÜBİTAK report.

## Primary endpoint
For each confirmatory seed-level record, concatenate `root_cause_class` and `explanation`, normalize to lowercase alphanumeric tokens (punctuation, spaces, and underscores are separators), and search for a predeclared case-specific root-cause alias as a contiguous phrase. A match passes the primary seed-level root-cause score; otherwise it fails. Schema/parse failures are failures, not excluded observations.

The exact alias list lives in `data/benchmark/evaluation_rubric.json` and is integrity-bound to the confirmatory manifest by SHA-256. Changing that rubric after confirmatory inference begins invalidates the frozen experiment and must not be done.

## Case-level endpoint and inference
Each case-condition passes if at least 3 of its 5 fixed seeds pass the primary root-cause score. Each independent software defect is the unit of analysis. Compare paired case-level outcomes under Standard Context and CCDG Context with the predeclared exact two-sided McNemar test at alpha = 0.05. The effect is reported as the difference in case-level root-cause correctness, CCDG minus Standard.

## Secondary endpoints
Report the original strict complete-diagnostic score unchanged as a secondary endpoint, including exact component, entity, operation phrase, canonical root cause and required-relation checks. Also report each component metric and parse failure rate. These results are not substitutes for the frozen primary endpoint.

## Limitations
This is a deterministic string-alias rubric, not an automated semantic judge. It will reject paraphrases that do not match a predeclared alias and can therefore still produce false negatives. The aliases must be audited against ground truth and source evidence before manifest freeze. No post-hoc alias additions are permitted after confirmatory outputs are observed.

## Preservation
Keep the 40 pilot JSONL records, raw outputs, original pilot evaluation, and existing artifact manifest unchanged. The pilot remains feasibility / scoring-protocol evidence, not confirmatory evidence of CCDG effectiveness. The prior complete-diagnostic evaluation must not be overwritten or relabeled as root-cause scoring.
