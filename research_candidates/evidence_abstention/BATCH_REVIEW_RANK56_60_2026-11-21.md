# SWE-rebench V2 — batch candidate review, cohort ranks 56–60

**Date:** 21 November 2026  
**Scope:** Five consecutive frozen-cohort entries, ranks 56–60.  
**Review mode:** Static issue/PR, exact-base source, test-patch and license review plus metadata-only frozen-row authentication.  
**Human governance:** One human participant — the student project lead. ChatGPT is an advisory AI research assistant only.  
**Execution boundary:** No upstream checkout, package installation, upstream test/build, model loading, inference, fine-tuning or training was performed for these five cases.  
**Stage 2 boundary:** No Stage 2 authorization is issued here. Rank 52 GeoPandas remains on a separate final-acceptance HOLD; the existing sequential intake rule remains in force.

## 1. Batch result

| Rank | Candidate | Static decision | Frozen row | F2P / P2P | Recommendation |
|---:|---|---|---|---:|---|
| 56 | vacanza/holidays #2106 | Exclude — calendar-content/policy correction | Authenticated | 1 / 85 | Keep as transparent exclusion |
| 57 | ApeWorX/web3.py #3690 | Valid software defect, but E3 is overly diagnostic | Authenticated | 1 / 21 | Exclude from strict E3-abstention tier set |
| 58 | PyPSA/linopy #438 | Provisional defect; exact reproducer alignment unresolved | Authenticated | 1 / 13 | Hold; require issue-faithful dill/unpickle reproduction and tier review |
| 59 | jazzband/tablib #613 | Strong provisional software defect | Authenticated | 1 / 143 | Prioritise for subsequent project-lead review |
| 60 | silx-kit/silx #4282 | Exclude — explicitly requested feature/usability enhancement | Authenticated | 1 / 20 | Keep as transparent exclusion |

**Batch count:** 3 static exclusions/unsuitable-for-tier candidates (56, 57, 60), 2 remaining defect candidates (58, 59). Only one (rank 59) is recommended as the strongest next candidate for the strict three-tier evidence-abstention study. Nothing in this report is final case acceptance.

## 2. Frozen dataset identity and row-audit evidence

Pinned dataset:
- \`PrimeIntellect/SWE-rebench-V2-Filtered-Verified\`
- revision \`fb9aa226b2ce37c708ea7732e7b980abacdadb67\`
- Parquet SHA-256 \`7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9\`
- size 226,272,977 bytes; 6,272 rows

Metadata-only row-audit workflow:
- [GitHub Actions run 44942458120](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44942458120)
- job ID \`136962437715\`, conclusion success
- artifact ID \`14721714538\`
- artifact ZIP size 5,311 bytes
- artifact ZIP SHA-256 \`bee2402b83844ba6fd46ecff47a03af00b5f13e0e5a6661cef2d8630165ab7bf\`
- ZIP CRC: passed; exactly two members
- \`rows-metadata.json\` SHA-256 \`4db7069de2efa922991b6d3ecdbc5fec3d1ce20b3285643864fb46a47c92c59e\`
- \`SHA256SUMS.txt\` SHA-256 \`cdcbf2f6caffc73fd803ea34e11971368465d1802d78f688c8ee1c3a63e719f6\`
- internal metadata checksum: passed

All five candidate rows were uniquely discovered by immutable base commit + PR-number suffix + canonical repository identity. Every row's full canonical JSON, problem statement, patch and test patch were hashed in memory. The uploaded artifact retains only metadata, hashes and frozen selector lists; it contains no raw problem statement, patch or test patch.

### Per-row identities

| Rank | Exact instance ID | Repository | Base commit | Row SHA-256 |
|---:|---|---|---|---|
| 56 | \`vacanza__holidays-2106\` | \`vacanza/holidays\` | \`60966eaeca137cf2e08826a2b3e08fe6f5af7b36\` | \`e58a91bfcf0e4c3b4018f362d603f9765951794b16a8f084c402a63a1bae7109\` |
| 57 | \`ethereum__web3.py-3690\` | \`ethereum/web3.py\` | \`a08787d08a8f30a099ea1daf1a5e6575dff07681\` | \`515326449b02860fc0d4d1cba18e4e2f91c8a84275a02069242d8826214a5921\` |
| 58 | \`pypsa__linopy-438\` | \`PyPSA/linopy\` | \`a57d24be104dfcdbf316ee68f9b89d06ca30795f\` | \`7fe29ea47bf5d7343c0f9607418386c017615adef79af68829cfeebf0c4f73b2\` |
| 59 | \`jazzband__tablib-613\` | \`jazzband/tablib\` | \`70775bc922602ae535e0b2e525f6926030334ab8\` | \`b464f69af9507c7985cc8968e87f54361b167a3bf765f946b71060430138b2bf\` |
| 60 | \`silx-kit__silx-4282\` | \`silx-kit/silx\` | \`ca54e9e34df37ca791d6db9703fd274a8beada9a\` | \`d76b9d511d9b7054c94bf046eb1bb56a7ad18610720d81a80b0e55352cae538e\` |

All five source-row license fields report MIT. Exact-base root LICENSE files were also inspected for all five, including their Git blob identities. This is a source-license screen, not full dependency/SBOM clearance.

## 3. Candidate 56 — vacanza/holidays #2106

- Issue: [#2103 — Columbus Day is not observed in all states?](https://github.com/vacanza/holidays/issues/2103)
- PR: [#2106](https://github.com/vacanza/holidays/pull/2106)
- PR base: \`60966eaeca137cf2e08826a2b3e08fe6f5af7b36\`
- Root \`LICENSE\` blob: \`9bfa781d404b068ea21a586100de953f366dfacb\`; source license field: MIT
- Changed paths: \`holidays/countries/united_states.py\`, \`tests/countries/test_united_states.py\`, \`snapshots/countries/US_COMMON.json\`
- Frozen selector: \`tests/countries/test_united_states.py::TestUnitedStates::test_columbus_day\`
- F2P 1; P2P 85
- Row SHA-256: \`e58a91bfcf0e4c3b4018f362d603f9765951794b16a8f084c402a63a1bae7109\`
- Problem SHA-256: \`8ab92fe6150b2f8c830476e6fe6e263ba930e8dfb262c8b61dc575655d3c13cb\`
- Patch SHA-256: \`a9e8e75bcc540f947d5ff7cd77b61cc2b6c95bec5277b7a5f707329dff21785e\`
- Test-patch SHA-256: \`b168b679fa1ca049fea9419fb130912cc8b9be2a0c85e9da023dbb31cc8acdc0\`

**Static finding:** the issue questions whether Columbus Day should be emitted as a countrywide holiday when it is not observed in every subdivision. The PR explicitly labels itself “Supported country/market holidays update (calendar discrepancy fix, localization)” and removes Columbus Day from countrywide output while retaining it in selected subdivisions. Its source, tests and snapshots change the represented holiday data/policy; there is no identified software execution failure or violated implementation contract.

**Decision:** **EXCLUDE** from the software root-cause sample as a domain-calendar/content correction. The issue's “Bug Report” heading does not override the actual semantics of the requested change or the PR's own category.

**Recommendation:** preserve the row and rationale in the exclusion ledger. Do not spend Stage 2 runtime on it.

## 4. Candidate 57 — ApeWorX/web3.py #3690

- Issue: [#3689 — SubscriptionManager.handle_subscriptions hangs on PersistentConnectionClosedOK exception](https://github.com/ApeWorX/web3.py/issues/3689)
- PR: [#3690](https://github.com/ApeWorX/web3.py/pull/3690)
- Frozen dataset owner alias: \`ethereum/web3.py\`; current upstream repository identity: \`ApeWorX/web3.py\`
- PR base: \`a08787d08a8f30a099ea1daf1a5e6575dff07681\`
- PR fixed head: \`813371fed7b921760d833cae090305af5df813af\`
- Root \`LICENSE\` blob: \`e81cd192f3b785df084e5439e3aeb45bda5c7c5b\`; MIT
- Changed paths: \`web3/providers/persistent/subscription_manager.py\`, \`web3/providers/persistent/async_ipc.py\`, \`tests/core/providers/test_websocket_provider.py\`, \`newsfragments/3690.bugfix.rst\`
- Frozen selector: \`tests/core/providers/test_websocket_provider.py::test_connection_closed_ok_breaks_handle_subscriptions_iteration\`
- F2P 1; P2P 21
- Row SHA-256: \`515326449b02860fc0d4d1cba18e4e2f91c8a84275a02069242d8826214a5921\`
- Problem SHA-256: \`c1bb2297838c13203487ccd5624b2c5cf222db6eb4743bfa5126c2844ddd862f\`
- Patch SHA-256: \`764d1da60871564ed617ed02867977bb6b1db81270edfc6c89ef2f0750ac739c\`
- Test-patch SHA-256: \`505e5385ee797f25b7a2d1fa1b7cb39b80659f3e69287e95d6f3cd498a1acb44\`

**Gold mechanism proposal:** \`G1_SUBSCRIPTION_MANAGER_CONTINUES_AFTER_TASK_NOT_RUNNING_AND_WAITS_ON_EMPTY_QUEUE\`. When the persistent listener ends after a graceful connection close, \`TaskNotRunning\` is placed on the subscription queue. The handler logs the condition but continues its loop; the next queue read can wait indefinitely despite there being no listener.

**Alternatives:** \`A1_MESSAGE_LISTENER_CLOSE_STATE_NOT_PROPAGATED\`; \`A2_SUBSCRIPTION_QUEUE_LIFECYCLE_NOT_TERMINATED_OR_RESET\`.

**Source/fix alignment:** the issue itself says the \`TaskNotRunning\` branch logs and continues, then \`await queue.get()\` hangs, and explicitly suggests that a \`return\` or \`break\` is missing. The PR adds \`break\` to that exact \`except TaskNotRunning\` branch. A second source change constructs \`PersistentConnectionClosedOK\` using the current \`user_message\` argument.

**Answerability assessment:** the frozen issue is unusually revealing. It states the precise handler, queue behavior and likely missing control-flow statement. For the study's strict E3 semantics (“all predeclared mechanisms remain possible and none is defensibly eliminated”), the issue appears to disclose enough to answer the implementation-mechanism question. This is not a clean E3-abstention case even though it is a valid software defect.

**Decision:** retain as a genuine software defect in the screening record, but **recommend exclusion from the strict E3/E2/E1 abstention comparison** rather than weakening the tier rule or rewriting the issue statement.

**Recommendation:** do not spend Stage 2 time unless the study design explicitly has a separate already-answerable E3 stratum. Do not convert it into an E3=ABSTAIN case simply to fill the sample.

## 5. Candidate 58 — PyPSA/linopy #438

- Issue: [#340 — Serializing and deserializing linopy.Model](https://github.com/PyPSA/linopy/issues/340)
- PR: [#438 — Support pickling a linopy model](https://github.com/PyPSA/linopy/pull/438)
- PR base: \`a57d24be104dfcdbf316ee68f9b89d06ca30795f\`
- Fixed head: \`8dd5e66b505b15fbf24d2fb88ade925b07dcaa40\`
- Root \`LICENSE.txt\` blob: \`e1cb51959a60b472cd390b04d302ad12b040017a\`; MIT
- Changed paths: \`linopy/constraints.py\`, \`linopy/variables.py\`, \`test/test_io.py\`, \`doc/release_notes.rst\`
- Frozen selector: \`test/test_io.py::test_pickle_model\`
- F2P 1; P2P 13
- Row SHA-256: \`7fe29ea47bf5d7343c0f9607418386c017615adef79af68829cfeebf0c4f73b2\`
- Problem SHA-256: \`a25017903c53d4b758010f24f6e0837fd830a17cfcca1aa37cad52b69cdf23f4\`
- Patch SHA-256: \`0d175737c38867d40d0ebf43ea038db86f94042234973d493e4de2cec7aa2ea3\`
- Test-patch SHA-256: \`04f89b7d7fd3a2a1f480ffc2c15c63c26fdfaff98f2eaa71454f359c58cf6fef\`

**Gold mechanism proposal:** \`G1_VARIABLES_OR_CONSTRAINTS_GETATTR_RECURSES_BEFORE_PICKLE_STATE_IS_RESTORED\`. During unpickling, one of the custom \`Variables\`/\`Constraints\` objects can have its dynamic \`__getattr__\` invoked before the \`data\` member is available. The \`__getattr__\` implementation checks \`self.data\`, which recursively invokes \`__getattr__\` and ends in \`RecursionError\`. The PR adds explicit \`__getstate__\` and \`__setstate__\` methods to both classes.

**Alternatives:** \`A1_SERIALIZER_PROTOCOL_OR_DILL_PICKLE_COMPATIBILITY\`; \`A2_CYCLIC_MODEL_GRAPH_OR_REFERENCES_CAUSE_RECURSION\`; \`A3_CONSTRAINTS_STATE_RESTORATION_ORDER\`.

**Important reproducer mismatch:** the issue's example uses \`dill.dump\` / \`dill.load\` and identifies a use case involving \`ProcessPoolExecutor\`; the frozen FAIL_TO_PASS selector added by the PR uses standard-library \`pickle\` on a model fixture. This may exercise the same state-restoration mechanism, but it does not by itself prove the original dill/process-pool path is fixed. The issue traceback is also highly diagnostic: repeated calls point directly to \`Variables.__getattr__\` while it evaluates \`self.data\`, so E3 may already be answerable.

**Tier recommendation (provisional):** E3=ABSTAIN only if the project lead concludes that the traceback still leaves at least two credible mechanisms; otherwise classify E3 as answerable and exclude from the strict abstention tier set. E2=ABSTAIN is plausible with the fixed pickle regression-test source alone; E1=ANSWER with exact source and state-restoration implementation. Do not freeze this tiering from static review alone.

**Decision:** **HOLD / conditional defect candidate**.

**Recommendation:** if advanced, Stage 2 must first reproduce the exact frozen \`test_pickle_model\` selector and add a separately recorded issue-faithful supplementary reproducer using the issue's \`dill\` round-trip (and, if feasible, process-pool transfer). The extra reproducer is supplementary and must not replace or silently modify the frozen selector. Check both \`Variables\` and \`Constraints\` state-restoration behavior and preserve non-pickle regressions.

## 6. Candidate 59 — jazzband/tablib #613

- Issue: [#612 — ODS loading issue: ValueError: 'value' is not in list](https://github.com/jazzband/tablib/issues/612)
- PR: [#613 — Fix bug in ODS import regarding cells with empty strings](https://github.com/jazzband/tablib/pull/613)
- PR base: \`70775bc922602ae535e0b2e525f6926030334ab8\`
- Fixed head: \`2890ec610a5f61c6bee91a4d2328043945a2771d\`
- Root \`LICENSE\` blob: \`9bfca256684905e950decdeaf85de465c2977b63\`; MIT
- Changed paths: \`src/tablib/formats/_ods.py\`, \`tests/test_tablib.py\`
- Frozen selector: \`tests/test_tablib.py::ODSTests::test_ods_export_import_set\`
- F2P 1; P2P 143
- Row SHA-256: \`b464f69af9507c7985cc8968e87f54361b167a3bf765f946b71060430138b2bf\`
- Problem SHA-256: \`12644fb93d120b60f8c00f65722e63dddd447449e1919004cefe49dcdab4cc02\`
- Patch SHA-256: \`8f86f66f688e603f24252e0e800e573a345d3cb9249d7e53a8d88312f2975da5\`
- Test-patch SHA-256: \`d3f44244befabd8f88568374936edb641629efd94a7bf4aca8b48eddd33b8230\`

**Gold mechanism proposal:** \`G1_ODS_EMPTY_STRING_CELL_WITHOUT_VALUE_ATTRIBUTE_RAISES_DURING_READ_CELL\`. An ODS cell representing an empty string can be parsed through a child/text node for which the \`value\` attribute is not available. The existing \`read_cell\` path assumes the attribute can be retrieved; the resulting \`ValueError\` aborts ODS import. The fix catches that missing-attribute condition and preserves the empty value as an empty string.

**Alternatives:** \`A1_ODS_EXPORT_CREATES_INVALID_EMPTY_CELL_STRUCTURE\`; \`A2_READ_CELL_CHILD_NODE_TRAVERSAL_DROPS_EMPTY_VALUES\`; \`A3_CELL_VALUE_TYPE_OR_ATTRIBUTE_NORMALIZATION_MISMATCH\`.

**Why this is a good abstention candidate:** the frozen issue describes a reproducible ODS round-trip failure for an empty-string cell and notes that replacing the empty string with \`None\` avoids the issue. It does not identify the internal parser method or the missing \`value\` attribute handling. The regression test adds an empty-string column and checks round-trip preservation, but it still does not disclose the exact source mechanism. The base/fixed source reveals the \`getAttribute('value')\` exception handling.

**Tier recommendation (advisory):** E3=ABSTAIN; E2=ABSTAIN; E1=ANSWER. This is the clearest three-tier structure in the current batch.

**Secondary risk:** the patch also changes child-node traversal from “return the first truthy subnode result” to “return the first subnode result.” That is broader than the \`getAttribute\` exception catch. It may be intentional, but could affect cells with multiple child nodes where the first child resolves to an empty value. Stage 2 must include a supplementary regression matrix for empty string, \`None\`, non-empty text and multi-child/mixed-content cells; do not assume the frozen single selector covers all of these.

**Decision:** **STRONG PROVISIONAL DEFECT CANDIDATE; recommend first priority after preceding sequence gates**.

## 7. Candidate 60 — silx-kit/silx #4282

- Issues: [#2927 — Display units in addition to the label of axes](https://github.com/silx-kit/silx/issues/2927) and [#4199 — Add units to axes and color bars when present](https://github.com/silx-kit/silx/issues/4199)
- PR: [#4282 — Add units to dataset name (signal/axes)](https://github.com/silx-kit/silx/pull/4282)
- PR base: \`ca54e9e34df37ca791d6db9703fd274a8beada9a\`
- Fixed head: \`12ee1efadea6b88ae6a5b4aabc7250e7aa9233e0\`
- Root \`LICENSE\` blob: \`c010dc33e73757638e9201fad73d3c31847547ba\`; MIT
- Changed paths: \`src/silx/io/nxdata/_utils.py\`, \`src/silx/io/nxdata/parse.py\`, \`src/silx/io/test/test_nxdata.py\`
- Frozen selector: \`src/silx/io/test/test_nxdata.py::test_units\`
- F2P 1; P2P 20
- Row SHA-256: \`d76b9d511d9b7054c94bf046eb1bb56a7ad18610720d81a80b0e55352cae538e\`
- Problem SHA-256: \`b98d283b73031355486d27dff8924f33a6e0b8d7c86a61cdf707ecc479a58d20\`
- Patch SHA-256: \`764385e9295247e85a77b33e1dac2526e8927a7c1afba772720ac3a620125455\`
- Test-patch SHA-256: \`f9ee82a15e0698b5a2094f12f09fb384436b9bb498dc2d348b83848eb4df0826\`

**Static finding:** the issues explicitly request additional display of unit attributes on NXdata axes and signal labels. The PR adds a helper that prefers \`long_name\`, otherwise uses the dataset name plus \`units\`, and otherwise preserves the dataset name. This is an enhancement to displayed metadata, not a correction of an existing incorrect software result or violated documented contract.

**Decision:** **EXCLUDE** as feature/usability enhancement.

**Recommendation:** retain the row and rationale in the exclusion ledger; do not run Stage 2.

## 8. Project-level exposure and sequence gates

- The project lead has explicitly declared candidate-specific prior pipeline/debug exposure for Django-bird #219 as \`none\`. That declaration applies only to rank 55.
- For ranks 57–59, candidate-specific prior pipeline/debug exposure remains **pending explicit project-lead declaration**. Do not infer \`none\` from absence in a historical list.
- Current source-review exposure for ranks 56–60 is full and disclosed.
- No Stage 2 run was performed or authorized for ranks 56–60.
- GeoPandas #3591 (rank 52) has passed its pinned Stage 2 reproduction twice, but remains HOLD / not in accepted registry. Its separate publication derivative is complete; the limited license/provenance audit still does not establish redistribution clearance for verbatim user-generated comments, and the dependency lock lacks package hashes/SPDX/SBOM/native-license audit. A separate project-lead acceptance decision is still required.
- The sequential candidate queue is not relaxed by this batch review. Rank 55 Django-bird, whose prior pipeline/debug exposure is now declared \`none\`, still requires the project lead's gold/tier decision; its Stage 2 sequencing remains behind rank 52's final disposition.

## 9. Recommended action order

1. Close rank 52 GeoPandas with a separate project-lead ACCEPT / REJECT decision after the publication and dependency-scope review; do not confuse technical reproduction pass with final acceptance.
2. Complete rank 55 Django-bird's project-lead gold/tier decision. The project lead has declared prior pipeline/debug exposure \`none\`; full source exposure remains disclosed.
3. Apply unchanged sequential gates to the next eligible case. Rank 57 should be excluded from the strict three-tier sample because E3 nearly states the remedy. Rank 58 remains conditional on E3 answerability and an issue-faithful dill reproducer. Rank 59 is the strongest recommended next case, subject to exposure declaration, project-lead gold/tier approval, and later authorized Stage 2.
4. Preserve all exclusions and holds. Do not lower evidence-tier, test-reproduction, exposure or licensing standards to reach the sample target.

**Final batch disposition:** rank 56 EXCLUDE; rank 57 valid defect but not a suitable strict E3-abstention case; rank 58 HOLD/conditional; rank 59 strong provisional candidate; rank 60 EXCLUDE. No new case is accepted; model inference remains unauthorized.
