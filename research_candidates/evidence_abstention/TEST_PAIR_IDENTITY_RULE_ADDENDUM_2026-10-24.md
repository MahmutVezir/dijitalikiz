# Test-pair identity rule addendum — 24 October 2026

**Status:** Prospective case-validation rule. Recorded before any candidate test-pair execution for the current intake and before any confirmatory model inference. This does not change the P0/P1 conditions, endpoints, minimum sample size, model lock, or statistical analysis plan.

## Rule

A candidate's buggy and fixed runs must use byte-identical target regression-test content. The target test file's SHA-256 must be recorded for both sides and the values must match.

If the repository's target test file differs between the pinned buggy and fixed commits, the candidate is **not run** under the default checkout-only procedure. A prospective test overlay is permitted only when all of the following are true:

1. The exact target test file from the pinned fixed commit is selected as the canonical regression test before either target run.
2. That exact byte sequence is placed at the same path in disposable buggy and fixed source worktrees; the overlay's SHA-256 is computed once and verified identical in both worktrees.
3. The production source trees remain pinned to their respective buggy and fixed commits; only the target test file is overlaid. No production code is patched or manually edited.
4. The same documented test command is run in both worktrees, with the same frozen dependency specification and Python version required by the benchmark metadata.
5. The overlay is rejected and no test pair is run if it does not import and apply without changing its content or if the two test executions cannot be made equivalent.

The raw test content and its hash, source commit, overlay path, commands, environment fingerprints and unedited logs must be preserved. Environment/setup failures never count as the target bug's failure.

## Why this rule exists

A test file that changes between buggy and fixed commits can confound the paired comparison: different outcomes might be caused by a test change rather than by the program fix. Byte-identical test content is therefore a prerequisite for interpreting buggy-fail/fixed-pass as evidence that the target regression test detects the intended bug.

## Current application: BugsInPy-ansible-7

At the pinned BugsInPy revision `11c5f1eea954a42132cfd06bf257766a7963e0fd`, `BugsInPy-ansible-7` metadata identifies Python 3.6.9, buggy commit `cd146b836e032df785ecd9eb711c6ef23c2228b8`, fixed commit `4ec1437212b2fb3c313e44ed5a76b105f2151622`, and target `test/units/modules/network/eos/test_eos_vlans.py::TestEosVlansModule::test_eos_vlan_replaced`.

The fixed commit is a direct child of the buggy commit and changes both `lib/ansible/module_utils/network/eos/config/vlans/vlans.py` and the target unit-test method. Therefore the checkout-native test contents differ; the candidate remains **blocked pending a fixed-test overlay and hash verification**. Neither buggy nor fixed candidate test has been run. The case is not accepted.

