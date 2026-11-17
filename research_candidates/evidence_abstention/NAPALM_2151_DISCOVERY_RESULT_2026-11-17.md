# NAPALM #2151 / PR #2152 — technical discovery record

**Assessment date:** 17 November 2026  
**Dataset instance:** `napalm-automation__napalm-2152`  
**Frozen row SHA-256:** `badc723c07fe415e42d9e329529f9669932f43f18d2d0a61907f17d983c3f555`  
**Upstream base:** `d0d2a3e70d21d0556de71ab0462bd71a1450f820`  
**Upstream fix:** `a3781b83e02cb7ea87da948d82e0c9ee4d91a39a`

## Decision

The candidate has a **confirmed technical base-fail/fixed-pass reproduction**. It remains **conditional / not accepted** because the original upstream PR fixture has an unresolved file-level provenance question and the first discovery artifact was broader than the intended evidence packet. The pinned synthetic reproduction workflow added alongside this record is the next gate. Stage 3 and model inference remain unauthorized.

## Exact upstream test result

GitHub Actions run [44123756600](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44123756600), job `134181787051`, authenticated the frozen row and exact source revisions, installed the exploratory environment, and ran the row's only `FAIL_TO_PASS` selector:

```
test/nxos_ssh/test_getters.py::TestGetter::test_get_facts[issue2151]
```

Observed results:

| Revision | Result | Relevant value |
|---|---|---|
| Buggy base | 1 failed | actual `os_version="version"`; expected `"10.3(5)"` |
| Fixed revision | 1 passed | `os_version="10.3(5)"` |

The base assertion was:

```
Expected result varies on some keys
{"os_version": {"result": "version", "expected": "10.3(5)"}}
```

This is a defect-specific assertion, not merely a schema/type smoke test. At the exact base revision, `napalm/base/test/getters.py`'s `wrap_test_cases` wrapper loads `attr.expected_result`, compares the returned object with `dict_diff`, and raises an assertion when values differ.

The source-level cause is consistent with the observed result. The base parser accepts every line containing `"NXOS: "`; both `NXOS: version ...` and `Host NXOS: version ...` match. The latter line's third token is `version`, overwriting the valid version. The fix restricts the condition to a stripped line starting with `NXOS: version`, so the secondary `Host NXOS` line is ignored.

## Discovery environment

The exploratory run used CPython 3.11.9, pip 24.3.1, pytest 8.3.5 and mock 5.2.0. `pip check` passed. The environment had 51 distributions including the editable NAPALM source, and all 51 exposed license metadata. This is metadata-availability screening, not a full legal approval of every dependency.

A 50-distribution platform lock has been extracted from the discovery freeze. The new pinned workflow reinstalls that lock with dependency resolution disabled, checks the resulting freeze byte-for-byte, and reruns an independently authored minimal synthetic regression on the exact base and fix commits.

## Fixture and artifact limitations

The issue's raw example and the PR's added `show_version.txt` are not identical device captures. The issue describes a Nexus 9000 C93180YC-FX3 and includes a 2002–2024 Cisco copyright line; the PR fixture identifies a Nexus 3048, a different serial/uptime, and a 2002–2017 copyright line. Both contain the two parser-relevant lines:

- `NXOS: version 10.3(5) [Maintenance Release]`
- `Host NXOS: version 10.3(5)`

The exact-base repository license is Apache-2.0 and a root `NOTICE` exists, but that does not independently establish the redistribution provenance of the PR's Cisco device-output fixture or its embedded third-party notices. The original fixture therefore remains on hold and is not copied into the new pinned evidence packet.

The discovery run's artifact is [14345838155](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44123756600/artifacts/14345838155), SHA-256 `81a690d51ad80c2828af6fcdd43f13a38fc7824cb85d3336a5a76c6e8a96925d`. It contains the full Parquet file (226,272,977 bytes uncompressed), the full upstream PR patch, the test-only fixture patch, the upstream test harness source, and captured fixture-derived values. **Do not treat this raw discovery artifact as the canonical case packet or redistribute it.** The new workflow downloads the Parquet file only to a temporary runner path, extracts a row hash/summary, uses a minimal synthetic parser input, and uploads only sanitized evidence.

## Next gate

The pinned workflow must demonstrate all of the following before a Stage 2 technical disposition is recorded:

1. Python 3.11.9 and all 50 locked distributions install without dependency resolution.
2. The installed freeze exactly matches `requirements.lock` (excluding the separately pinned editable NAPALM source).
3. `pip check` succeeds and dependency license metadata remains complete.
4. The minimal synthetic test fails on the exact buggy base and passes on the exact fixed revision.
5. The uploaded artifact contains no Parquet payload, copied upstream fixture, raw PR patch, or full upstream test harness.

The synthetic test is an independent reproducer; it is **not** relabelled as the dataset's original selector. The original exact selector's base-fail/fixed-pass result remains documented above as discovery evidence.

No model was loaded. No inference, fine-tuning, or training was performed. Final accepted-case count remains unchanged.
