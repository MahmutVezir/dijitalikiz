# CS-SI/eodag #1530 — Stage 2 technical review

**Disposition:** Stage 2 technical reproduction passed. Stage 3 scientific adjudication has not started. The case is not accepted into the final registry.

## 1. Exact source and issue identity

- Repository: https://github.com/CS-SI/eodag
- Issue: https://github.com/CS-SI/eodag/issues/1530
- Fix PR: https://github.com/CS-SI/eodag/pull/1536
- Dataset instance: `cs-si__eodag-1536`
- Buggy base: `b7cc06e19025e5bbf14e28a0975f1749e21e9be3`
- Fixed revision: `312966a46513a082333d46cd7212bdce36aaf769`
- Dataset timestamp: `2025-02-21 10:04:30 UTC`
- Dataset row SHA-256: `35f612f1b6524f37cca6766f25a0637bc5d5740da9695427dba556354ce61a47`
- Root license: Apache-2.0; exact base LICENSE and NOTICE blobs were authenticated in the workflow.

## 2. Independent issue reproducer

The minimal YAML regression reads the exact upstream `eodag/resources/user_conf_template.yml` and asserts that the `geodes` and `geodes_s3` provider configuration keys both exist and retain distinct credential schemas.

- Buggy base: failed as expected because `geodes_s3` was absent after the duplicate-key YAML behavior.
- Fixed revision: the same reproducer passed.
- This is a source-level YAML regression check; it does not make claims about live EODAG provider access.

## 3. Exact SWE-rebench selectors

The exact frozen row contains two selectors; neither was removed or rewritten:

1. `tests/units/test_core.py::TestCore::test_available_sortables`
2. `tests/units/test_core.py::TestCore::test_list_product_types_for_provider_ok`

The focused test environment was installed from the repository's pinned `requirements.test.in`, plus the exact editable upstream source. The workflow ran `pip check`, captured the resolved environment, and recorded dependency license metadata before running the upstream selectors.

**Buggy base:**
- Selector 1 executed and failed on the expected available-sortables mismatch.
- Selector 2 executed and failed because provider `geodes_s3` was unsupported.
- Result: `selector_contracts=2/2 expectation=base-fail`.

**Fixed revision:**
- The same two selectors passed.
- Result: `selector_contracts=2/2 expectation=fixed-pass`.

The exact test-only PR patch was applied to the buggy base and the workflow verified that only `tests/units/test_core.py` changed. Production code was not patched into the buggy base.

## 4. Reproduction provenance

- Workflow run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/44117944004
- Job ID: `134161227052`
- Artifact ID: `14344421574`
- Artifact name: `eodag-issue-1530-reproduction`
- Artifact ZIP SHA-256: `0d9b4cf38b22cf094d080d6f8a87b1ff6373c9ab3a7d8ece68cc003b35964b33`
- Artifact contains raw base/fixed logs, selector JSON, exact row, dependency lock, dependency license inventory, source provenance, test-only patch, and SHA256SUMS.

## 5. Remaining scientific and acceptance gates

1. Human review of the complete dependency-license inventory and scope. Metadata presence is not legal clearance.
2. Independence and related-issue-family review; one EODAG repository may contribute at most one accepted case.
3. Human adjudication of the gold mechanism and alternative hypotheses.
4. Construct nested E1/E2/E3 evidence packets, verify source and artifact hashes, and obtain project-lead approval.
5. Construct a complete schema-conformant final case record and pass fail-closed registry validation.
6. Record a separate final acceptance decision.

**Current disposition:** Stage 2 pass; Stage 3 not started; final case acceptance remains `not_accepted`; no model loading, inference, or training was performed or authorized by this run.
