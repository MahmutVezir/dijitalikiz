# SWE-rebench V2 case-scope audit: primary cohort rows 9–16

**Audit date:** 2026-11-12  
**Scope:** Primary cohort rows 9–16 from the pinned 96-project selection.  
**Method:** GitHub PR/issue metadata, exact base SHA comparison, changed-file path lists, and static patch-shape inspection.  
**Execution boundary:** No upstream checkout, no test execution, no model inference, and no training.

## Executive result

- All 8 instance IDs resolve to the expected upstream PRs.
- All 8 PR base SHAs exactly match the cohort's pinned `base_commit`.
- 4 cases are provisionally retained as defect candidates: Moto, NumPyro, Dymos, and EODAG.
- 4 cases are excluded from the strict software-bug/root-cause pool as feature/API enhancements: D-Wave System, FastMCP, kafka-python, and PennyLane.
- None is an accepted experiment case. This audit does not verify licenses for these eight pinned commits or reproduce tests.

Combined with the first-eight audit, rows 1–16 have 16/16 PR/base-commit mappings confirmed; 8/16 are provisional bug candidates and 8/16 are excluded from the strict bug pool. This observed fraction is descriptive of this small ordered batch only and must not be extrapolated to the whole cohort.

## Row-by-row audit

| # | Cohort instance / repository | PR and linked issue | Exact base SHA? | Patch paths / scale | Issue characterization | Decision |
|---:|---|---|---|---|---|---|
| 9 | `getmoto__moto-8296` — [getmoto/moto](https://github.com/getmoto/moto) | [PR #8296](https://github.com/getmoto/moto/pull/8296), [issue #8269](https://github.com/getmoto/moto/issues/8269) | Yes | `moto/ecr/models.py`, `moto/ecr/responses.py`, `tests/test_ecr/test_ecr_boto3.py`; patch changes response/model behavior and adds multi-tag regression assertions | Issue label `bug`; `list_images()` omitted image tags when a digest had multiple tags | **Retain provisionally** |
| 10 | `dwavesystems__dwave-system-554` — [dwavesystems/dwave-system](https://github.com/dwavesystems/dwave-system) | [PR #554](https://github.com/dwavesystems/dwave-system/pull/554) | Yes | 17 paths; adds `close()` methods to sampler classes, testing support and tests | PR title/body describe a new lifecycle/API capability; no pre-existing bug report established in this record | **Exclude from strict bug pool** — feature/API addition |
| 11 | `jlowin__fastmcp-164` — repository now [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp) | [PR #164](https://github.com/PrefectHQ/fastmcp/pull/164), [issue #162](https://github.com/PrefectHQ/fastmcp/issues/162) | Yes; PR base SHA matches the pinned cohort SHA after repository transfer | 6 paths; resource-manager/template/server implementation, docs and tests | Issue asks for optional resource-template function parameters; existing registration rejected functions whose signature had extra optional parameters | **Exclude from strict bug pool** — new API behavior/enhancement, not a demonstrated regression |
| 12 | `pyro-ppl__numpyro-1918` — [pyro-ppl/numpyro](https://github.com/pyro-ppl/numpyro) | [PR #1918](https://github.com/pyro-ppl/numpyro/pull/1918), [issue #1916](https://github.com/pyro-ppl/numpyro/issues/1916) | Yes | `numpyro/infer/mcmc.py`, `test/infer/test_ensemble_mcmc.py`; implementation fix and warmup regression test | Issue label `bug`; `MCMC.run` raised an RNG key shape error after `MCMC.warmup` with AIES | **Retain provisionally** |
| 13 | `dpkp__kafka-python-2544` — [dpkp/kafka-python](https://github.com/dpkp/kafka-python) | [PR #2544](https://github.com/dpkp/kafka-python/pull/2544), [issue #1346](https://github.com/dpkp/kafka-python/issues/1346) | Yes | 6 paths across consumer/coordinator utilities and tests | Adds optional `timeout_ms` parameters to methods to avoid unexpected blocking; requested API enhancement | **Exclude from strict bug pool** — feature addition |
| 14 | `PennyLaneAI__pennylane-6738` — [PennyLaneAI/pennylane](https://github.com/PennyLaneAI/pennylane) | [PR #6738](https://github.com/PennyLaneAI/pennylane/pull/6738) | Yes | Grover template implementation, tests, and changelog | PR describes a new `work_wires` property; benefits described as “nice to have” | **Exclude from strict bug pool** — API feature addition |
| 15 | `openmdao__dymos-1165` — [OpenMDAO/dymos](https://github.com/OpenMDAO/dymos) | [PR #1165](https://github.com/OpenMDAO/dymos/pull/1165), [issue #1166](https://github.com/OpenMDAO/dymos/issues/1166) | Yes | 6 paths across control interpolation, explicit shooting, utility code, and tests | Issue label `bug`; default values supplied to `add_control` / `set_control_options` were not applied | **Retain provisionally** |
| 16 | `CS-SI__eodag-1536` — [CS-SI/eodag](https://github.com/CS-SI/eodag) | [PR #1536](https://github.com/CS-SI/eodag/pull/1536), [issue #1530](https://github.com/CS-SI/eodag/issues/1530) | Yes | `eodag/config.py`, `eodag/resources/user_conf_template.yml`, `tests/units/test_core.py`; config correction and test | Issue label `bug`; duplicate provider config key caused public Geodes access to request the wrong credentials | **Retain provisionally** |

## Additional lineage and scope notes

### FastMCP repository transfer

The cohort records repository name `jlowin/fastmcp`. GitHub now resolves it to `PrefectHQ/fastmcp`. The repository metadata and PR endpoint show the transferred repository; PR #164's base SHA is exactly `059c0889fdf16b7dfa53e84f08034c3ac914e4a6`, matching the cohort. This is a repository transfer/rename lineage detail, not a base-commit mismatch.

### Static test-adequacy observations

These are patch-shape notes only:
- **Moto:** regression test explicitly asserts that two tags for the same image digest appear separately in `list_images()`. It is closely aligned with the reported behavior.
- **NumPyro:** a new `test_warmup` case is added next to the MCMC implementation fix. The exact environment reproduction remains required.
- **Dymos:** both control-interpolation implementation/tests and explicit-shooting modules change; the breadth of the fix requires later scrutiny to ensure the selected `FAIL_TO_PASS` case tests the reported default-value defect, not an adjacent behavior.
- **EODAG:** a config/template correction and a unit test are changed; confirm that the regression test fails on the exact buggy base revision and passes at the selected fixed revision.
- The four feature additions have changed paths and tests, but tests do not make a feature request a bug case.

## Decision rules preserved

1. A candidate enters the strict pool only when there is evidence of an incorrect or regressed existing behavior, not merely a request for a new capability.
2. An issue's `bug` label supports classification but does not replace reproduction and root-cause validation.
3. A PR/test patch does not establish that the designated benchmark test is sensitive to the claimed defect.
4. The exact pinned base revision must match the cohort metadata; all eight rows in this batch pass that identity check.
5. No case is accepted until case-specific license/notice coverage, test adequacy, exact-environment buggy-fail/fixed-pass reproduction, and independent human review are complete.

## Gate status

- PR-to-cohort base commit mapping: **8/8 exact matches**.
- Provisional bug candidates in this batch: **4**.
- Feature/API additions excluded: **4**.
- License clearance for this batch: **not yet performed**.
- Reproduced cases: **0**.
- Accepted cases/projects: **0/0**.
- Upstream tests and source execution: **not performed**.
- Model inference/training: **not performed**.

**Next task:** Audit root license files and repository lineage for rows 9–16 at their exact pinned base commits. After that, the same unchanged PR/issue/license screen continues with rows 17–24.
