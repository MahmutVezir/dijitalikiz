# SWE-rebench V2 — cohort rows 57–64: PR scope and exact-base license audit

**Audit date:** 14 November 2026  
**Cohort:** 12 November 2026 tarihinde üretilen deterministic 96-project primary pre-review cohort'un 57–64. satırları.  
**Boundary:** GitHub PR/issue metadata, changed-file patches, exact PR base SHA and exact-base root license files. No upstream checkout, package installation, target-test execution, model loading, inference, training or human adjudication was performed.

## 1. Reproducibility inputs

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Immutable Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Primary candidate CSV: `SWE_REBENCH_V2_COHORT_96_PRIMARY_2026-11-12.csv`
- Primary CSV SHA-256: `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`
- Cohort manifest SHA-256: `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`
- GitHub Actions run/artifact: [run 43257277504](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43257277504), artifact ID `13960884569`.
- Retrieved artifact ZIP: 42,194 bytes; SHA-256 `d9d1fc04cb84233c021006f13205623ea9aa390caa6eb54ca4bc9d974e9a4c6c`; ZIP CRC test passed. The embedded primary CSV and cohort manifest matched the SHA-256 values above.

A matching PR base SHA confirms lineage alignment only; it does not prove that the issue is a defect, reproduce the failure, or accept a case.

## 2. Candidate-by-candidate findings

| Rank / candidate ID | Upstream PR | PR base SHA vs cohort base | Exact-base root license | Scope decision |
|---:|---|---|---|---|
| 57 — `ethereum__web3.py-3690` | [ApeWorX/web3.py #3690](https://github.com/ApeWorX/web3.py/pull/3690) | Match — `a08787d08a8f30a099ea1daf1a5e6575dff07681` | `LICENSE`, MIT text; blob `e81cd192f3b785df084e5439e3aeb45bda5c7c5b` | Defect candidate |
| 58 — `pypsa__linopy-438` | [PyPSA/linopy #438](https://github.com/PyPSA/linopy/pull/438) | Match — `a57d24be104dfcdbf316ee68f9b89d06ca30795f` | `LICENSE.txt`, MIT; blob `e1cb51959a60b472cd390b04d302ad12b040017a` | Defect candidate; verify reproducer |
| 59 — `jazzband__tablib-613` | [jazzband/tablib #613](https://github.com/jazzband/tablib/pull/613) | Match — `70775bc922602ae535e0b2e525f6926030334ab8` | `LICENSE`, MIT terms; blob `9bfca256684905e950decdeaf85de465c2977b63` | Defect candidate |
| 60 — `silx-kit__silx-4282` | [silx-kit/silx #4282](https://github.com/silx-kit/silx/pull/4282) | Match — `ca54e9e34df37ca791d6db9703fd274a8beada9a` | `LICENSE`, MIT terms; blob `c010dc33e73757638e9201fad73d3c31847547ba`; root `copyright` also present | Exclude — feature/usability enhancement |
| 61 — `twisted__towncrier-696` | [twisted/towncrier #696](https://github.com/twisted/towncrier/pull/696) | Match — `f080db690e77bf2a39692422d60df277632cb398` | `LICENSE`, MIT-style terms; blob `72912bfa6163452b16cb349e5e364b9f808a24bd` | Defect candidate |
| 62 — `sissbruecker__linkding-984` | [sissbruecker/linkding #984](https://github.com/sissbruecker/linkding/pull/984) | Match — `c5a300a4357d40d202f92dd08894ea520f2ade3f` | `LICENSE.txt`, MIT; blob `357447c54f16445a0e4e6cc9b3b89265b4b9fb42` | Exclude — explicitly requested new feature |
| 63 — `simpeg__simpeg-1633` | [simpeg/simpeg #1633](https://github.com/simpeg/simpeg/pull/1633) | Match — `f2440e63c6ab92191ae4f452808a9e4169af84e3` | `LICENSE`, MIT; blob `cd67a7669e3e768bb03686567ec0c3088d79560d` | Defect candidate |
| 64 — `oceanparcels__parcels-1723` | [OceanParcels/Parcels #1723](https://github.com/OceanParcels/Parcels/pull/1723) | **Not independently verified** — cohort base `a1f76d2f7ca4b50de874e61b752ec8ccaf50283e` | **Pending** — exact-base root license not inspected | Provisional bugfix candidate; hold |

### Rank 57 — web3.py: subscription termination

The PR is now served under `ApeWorX/web3.py`; the former `ethereum/web3.py` location redirects to the same repository identity, not a separate fork. The PR is titled “bugfix: subscription manager break on `PersistentConnectionClosedOK`”. Its description says the subscription manager must break when the persistent connection closes normally. The patch adds a regression test for `handle_subscriptions(run_forever=True)`, adjusts the empty-stream exception construction, and adds the missing loop break. The cohort base SHA matches the PR's exact base. Root `LICENSE` at that base is MIT.

**Decision:** retain as a defect candidate. Reproduce the named regression test on the exact base and fixed commits before acceptance.

### Rank 58 — linopy: model serialization recursion

Issue [#340](https://github.com/PyPSA/linopy/issues/340) reports a recursion error when serializing/deserializing an already serialized model, preventing model handoff through `ProcessPoolExecutor`. PR #438 adds `__getstate__`/`__setstate__` to the constraints and variables objects and adds a pickle round-trip test. Although the release-note section labels this a feature, the linked issue documents a concrete malfunction with an observable failure mode.

**Decision:** retain as a defect candidate, but do not classify it from the PR title alone. The exact reproduction must demonstrate that the reported second-serialization path fails at base and passes after the patch.

### Rank 59 — tablib: ODS empty-string import

Issue [#612](https://github.com/jazzband/tablib/issues/612) describes an ODS round-trip failure when an empty string is stored: loading the exported file raises `ValueError` because an empty `text:p` cell does not have the expected `value` attribute. PR #613 handles this path and extends the ODS round-trip test with an empty-string column. The exact base SHA matches and the root MIT license file was verified.

**Decision:** retain as a defect candidate. Reproduce the specific empty-string ODS failure/pass pair.

### Rank 60 — silx: dataset names with units

Issues [#2927](https://github.com/silx-kit/silx/issues/2927) and [#4199](https://github.com/silx-kit/silx/issues/4199) request displaying unit attributes alongside axis/signal labels. PR #4282 adds units to displayed dataset names and adds tests. The issue language describes a desired additional display capability, not an existing incorrect behavior that violates a documented contract.

**Decision:** exclude from the root-cause defect sample as a feature/usability enhancement. Keep the metadata record for transparent exclusions.

### Rank 61 — towncrier: Markdown heading hierarchy

Issue [#695](https://github.com/twisted/towncrier/issues/695) documents a Markdown rendering defect: custom `title_format` headings cause section and category headings to use incorrect levels. PR #696 infers the Markdown heading level from the configured title format, adjusts template output and updates rendering tests. The exact base SHA matches; root `LICENSE` was checked.

**Decision:** retain as a defect candidate. Reproduce the reported custom-title-format rendering failure.

### Rank 62 — linkding: public RSS discovery link

Issue [#879](https://github.com/sissbruecker/linkding/issues/879) is explicitly titled “[New feature] Add a link to public RSS from public bookmarks page”. PR #984 adds an RSS `<link rel="alternate">` element and tests public/shared page behavior. This is a newly requested discovery affordance, not a bug fix.

**Decision:** exclude from the root-cause defect sample.

### Rank 63 — SimPEG: misleading `Survey.components` behavior

Issue [#1609](https://github.com/simpeg/simpeg/issues/1609) is explicitly a bug report. It says the documented `components` property should return the number of components at each receiver, while the actual output returns the component-name array from the first receiver; different receivers can also have different component sets. PR #1633 deprecates the misleading property, changes simulation code to obtain components through a receiver-aware helper, and adds tests for the deprecation and component handling. The exact base SHA matches; root `LICENSE` was verified as MIT.

**Decision:** retain as a defect candidate, with an explicit review question: does the repaired downstream behavior fully resolve the reported contract defect, or only route new code around the deprecated property? The Panel A root-cause review must decide before acceptance.

### Rank 64 — Parcels: backward-in-time writing

The official Parcels changelog lists PR #1723 as “Fixing bug in backward-in-time-writing” in the v3.1.0 release notes ([changelog source](https://data.safetycli.com/packages/pypi/parcels/changelog)). However, the GitHub API endpoint for the historical repository path currently returns a permanent-move response to a numeric repository endpoint that the connected GitHub reader cannot inspect. Consequently, the PR's exact base SHA and the root `LICENSE` at the cohort base were not independently verified in this audit.

**Decision:** keep only as a provisional bugfix candidate. Do not accept, run or expose it until the repository redirect is resolved and base/license/patch lineage is verified.

## 3. Aggregate outcome

| Check | Outcome |
|---|---:|
| Candidate rows audited | 8 |
| PR base SHA matches | 7/8 |
| Exact-base root license files inspected | 7/8 |
| Defect-shaped candidates retained for next technical review | 5 |
| Provisional bugfix candidate, pending repository/base/license verification | 1 |
| Feature/usability requests excluded | 2 |
| Accepted confirmatory cases | **0** |
| Upstream target tests executed | **0** |
| Human root-cause/evidence adjudications | **0** |
| Model inference/training | **0 / 0** |

A verified root license at a commit is not a complete legal clearance. Changed-file lineage, bundled third-party components, attribution/NOTICE requirements, dataset permissions, issue-text rights and any needed consent must still be checked. Metadata license fields and PR descriptions do not replace those checks.

## 4. Next bounded work

1. Resolve rank 64's repository redirect; verify exact PR base SHA, root license and changed-file patch.
2. Complete exact-base root LICENSE/NOTICE and changed-file provenance checks for rows 17–56. Rows 57–63 root license checks are recorded above.
3. Continue metadata/scope inspection with cohort rows 65–72.
4. Only after licensing and scope checks, define a frozen isolated reproduction environment and run the same named target test at buggy and fixed revisions.
5. Keep all candidates outside `CASE_REGISTRY.json` until independent Panel A/Panel B review, evidence-level approval and the global preregistration/sample gates are complete.

**Conclusion:** This audit advances the candidate triage, not the confirmatory dataset. No candidate in rows 57–64 is accepted. The empty registry and closed inference gate remain correct.
