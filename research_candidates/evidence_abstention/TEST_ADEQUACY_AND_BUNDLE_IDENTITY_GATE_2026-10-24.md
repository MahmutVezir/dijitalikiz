# Candidate test adequacy and test-bundle identity gate — 24 October 2026

**Status:** Prospective technical-screening rule. It adds a case-eligibility check before any buggy/fixed test runs; it does not change the experiment conditions, primary endpoint, minimum sample size, model selection, or analysis plan.

## Required checks before running a candidate

1. Confirm the pinned BugsInPy metadata, exact buggy/fixed commit IDs, runtime Python version, and all permanent exposure exclusions.
2. Parse every path in the `test_file` metadata field; semicolon-separated paths form a single test bundle. Add any data/fixture files explicitly named by the upstream regression test when required to run it.
3. Record SHA-256 for every test-bundle file at both commits. If files differ, use the fixed-commit version as the canonical bundle only if the test/fixture overlay is prospective, explicit, byte-identical on both sides, and leaves all production files unchanged.
4. Inspect the regression test, fixture, changed production lines and their data/control-flow dependencies to establish that the test reaches the changed logic and its assertion can distinguish the buggy behavior from the fixed behavior. A changed test file or a green overlay preflight alone is not enough.
5. If static control-flow review shows the target test cannot exercise the changed behavior, do not install project dependencies or run the candidate test under the default protocol. Record a pre-execution static rejection and move to the next metadata candidate. Do not report this as a reproduced test failure.
6. Only after all preceding checks pass, proceed to environment/dependency bootstrap and capture raw buggy/fixed test logs. Environment/setup failures do not count as target failures.

## Required artifacts

Preserve metadata, source/test bundle hashes, exact source revisions, license pointers and hashes, environment fingerprint, setup/test commands and raw stdout/stderr. Keep the acceptance registry closed until buggy-fail/fixed-pass is reproduced, the root cause is independently reviewed, E1/E2/E3 evidence is constructed, two disjoint reviewer panels complete, license/leakage/exposure gates pass, and the protocol's global acceptance thresholds are met.

## First application

- `BugsInPy-ansible-7`: its test overlay hash check passed, but static review found the target test mocks the current VLAN configuration as empty. In that scenario `_state_replaced` produces no removal keys, whereas the production change alters ordering/overlap handling for removal keys. The target test therefore does not exercise the changed behavior. Record as `screened_out_before_test_execution_target_not_defect_sensitive`; no test was executed.
- `BugsInPy-black-9`: the metadata names Python 3.8.3 and two test-bundle paths, `tests/data/python2_print_function.py;tests/test_black.py`. The fixed commit adds both the regression test method and its data fixture. Any overlay must copy both paths from the fixed commit to the buggy worktree, verify both hashes equal across the two worktrees, and leave `black.py` unchanged. This candidate still requires its source-overlay preflight and local Python 3.8.3 runtime verification; no test has been run.
