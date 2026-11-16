# skypilot-org/skypilot issue #5981 — candidate review

**Cohort rank:** 17 of 96 primary candidates  
**Dataset instance:** skypilot-org__skypilot-5985 (exact row identity to be authenticated)  
**Issue:** https://github.com/skypilot-org/skypilot/issues/5981  
**Fix PR:** https://github.com/skypilot-org/skypilot/pull/5985  
**Review status:** source/patch semantics and root license screen passed; exact dataset selector execution and focused integration reproduction pending. Not an accepted case.

## 1. Defect contract

Issue #5981 reports misuse of Python str.lstrip("ssh-"). lstrip treats its argument as a set of characters, not an exact prefix. For example, "ssh-staging".lstrip("ssh-") produces "taging", not "staging". This corrupts SSH Kubernetes context names and node-pool filtering/display.

PR #5985 adds common_utils.removeprefix and replaces the affected lstrip("ssh-") calls across SSH context parsing, filtering, display, and resource formatting. The PR adjusts an existing mixed-filtering regression scenario so the expected node pool is "staging", not the incorrect "taging".

The defect mechanism is unambiguous at the Python semantics level. However, the PR touches multiple integration call sites, and the dataset selectors must be checked to confirm they test the intended SSH prefix behavior.

## 2. Pinned source identity

- Repository: skypilot-org/skypilot
- Buggy base: 60a6c930feeb8c48511f74c25bc2d7e12b290dd6
- Fixed PR head: c8154ff3a4875cbb1bac8f29bb45254f264d72ba
- Issue #5981 created: 2025-06-12T17:18:04Z
- PR #5985 created: 2025-06-12T21:52:38Z
- Exact-base root LICENSE Git blob: aad27dddb0055248d9ceb93ac287898fc1d25b29
- Exact-base pyproject.toml Git blob: a8fd2403a4c34d645369af07753b1608602f3d86
- Exact-base common_utils.py Git blob: a0ca0e97a4360019af0c5ec17381a2a3c753a094
- Fixed common_utils.py Git blob: 5745c98b0ddd233625a3f49da20a032833cd95ff
- Exact-base root license: Apache-2.0.

## 3. Technical and runtime scope

The core defect is a standard-library string-prefix semantic error. The new helper itself is small and deterministic. However, the dataset regression test imports SkyPilot's SSH and Kubernetes integration modules, which may require a broader optional dependency set. A source-only demonstration of lstrip semantics is not sufficient for acceptance; the actual call-site regression test must run.

No real Kubernetes cluster, SSH endpoint, cloud credentials, or external service should be used. The test must use the upstream mocks and local fixtures only. The dependency license inventory must cover the exact packages required to collect and run the selected tests.

## 4. Dataset selector requirement

The workflow must authenticate the exact Parquet row skypilot-org__skypilot-5985, record its canonical row hash and FAIL_TO_PASS selectors, and run every selector against the patched buggy base and fixed revision. Each base failure must show the wrong "taging" result or an equivalent assertion on the SSH prefix; each fixed selector must pass. Import/setup failures are not reproduction evidence.

## 5. Independence and exposure

- The frozen primary cohort contains one skypilot-org/skypilot candidate; this repository can contribute at most one accepted case.
- Issue and PR were created in June 2025, after the September 2024 public release of the pinned Qwen2.5-3B-Instruct family. This lowers the likelihood that the exact public issue/patch was present in the released weights, but does not prove the model's full training-data cutoff.
- The student researcher has reviewed the issue and PR during candidate screening; perfect blinding must not be claimed.
- Related issue-family and repository-lineage review remains required.

## 6. Current decision

Issue/patch semantics: strong.  
Independent issue-specific integration reproducer: pending.  
Dataset FAIL_TO_PASS selectors: pending exact-row authentication and execution.  
Dependency/license inventory: pending.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading/inference authorization: false.
