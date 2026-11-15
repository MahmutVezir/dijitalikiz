# pyfar #721 / PR #722 — prospective case-validation assignment draft

**Status:** DRAFT ONLY — no upstream test/build has been run; no case has been accepted; no model inference is authorized.

## 1. Candidate identity

| Field | Frozen value |
|---|---|
| V2 cohort row | 90 |
| Dataset instance | `pyfar__pyfar-722` |
| Dataset | `PrimeIntellect/SWE-rebench-V2-Filtered-Verified` |
| Parquet revision | `fb9aa226b2ce37c708ea7732e7b980abacdadb67` |
| Parquet SHA-256 | `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9` |
| Repository | `pyfar/pyfar` |
| Issue | [#721](https://github.com/pyfar/pyfar/issues/721) |
| Fix PR | [#722](https://github.com/pyfar/pyfar/pull/722) |
| Exact base | `648dda4c60c5a6f74acf335f7808c590c9d23929` |
| Fix head | `a4d72d380bb8ddb0950d334eb1b0793ee6d86e0e` |
| Merge commit | `ecd0589a3fef83ec17e8d72a4bd5a3c64ef7c445` |
| PR changed paths | `pyfar/dsp/dsp.py`; `tests/test_dsp_normalize.py` |
| Exact-base root license | MIT; exact-base `LICENSE` blob `430184952c6fcb292ee01cb114bb9c39f32f78ff` |
| Exact-base `setup.py` | Declares `License :: OSI Approved :: MIT License` and `license="MIT license"` |
| Root NOTICE | Not present in the inspected exact-base tree |

The candidate's timestamp was re-fetched from GitHub and matches the pinned dataset timestamp: `2024-11-15T08:33:08Z`. The current V2 candidate registry remains empty.

## 2. Research defect statement

Issue #721 reports that `pyfar.dsp.normalize` with `reference_method="energy"` or `"power"` does not produce the requested energy/power target. The issue gives a numerical example: input energy 20 produces output energy 0.05 instead of 1; input energy 5 produces output energy 0.2 instead of 1. A second example compares signals of different lengths and reports output energies 0.05 and 0.025 despite the same requested target.

The static mathematical hypothesis is that energy and power are quadratic in signal amplitude. If a signal with energy `E` is scaled by `T/E`, its resulting energy is `T²/E`, not `T`. The fix square-roots both the channel-handled energetic reference and the target, yielding a scale factor `sqrt(T/E)`. This is a source-grounded hypothesis, not a reproduced result.

## 3. Prospective reproduction design — not yet authorized

The technical validation must be assigned prospectively under the V2 protocol, not used to debug the screening/runner pipeline.

### Required test pair

- Freeze one standalone regression-test module and its SHA-256 before execution.
- Apply the exact same test module to the exact base and fix revisions.
- Include the issue's different-length signal example with deterministic seeds and explicit expected energy/power values.
- Include a separate parameterized invariant test covering `energy`, `power`, and `rms`; targets `0.5`, `1`, and `2`; and channel handling `max`, `individual`, `min`, and `mean` (36 combinations).
- Keep the RMS cases as a control; the patch's square-root transformation applies to energy and power, not RMS.
- Preserve the exact same test bytes, runtime, dependencies, environment variables, commands, and test configuration on both revisions.
- Required technical result: the issue-specific assertion fails at the pinned base and passes at the pinned fix. Any setup failure, unrelated test failure, or non-deterministic outcome is not a valid base-fail/fix-pass result.

### Environment freeze

Before execution, retrieve the exact row's `install_config` and dependency metadata from the pinned Parquet revision. Freeze Python, OS/container image, package versions, test command, environment variables, and all setup inputs. Do not infer an environment from the current upstream branch or install latest dependencies. Save the full environment manifest and SHA-256.

### Evidence preservation

For each revision, retain:
- repository URL and exact commit SHA;
- test-module SHA-256;
- environment/container digest and dependency lock hash;
- exact command and exit code;
- complete raw stdout/stderr and test report;
- timestamps and artifact SHA-256;
- a machine-readable base/fix comparison record.

No retry, log repair, or selective deletion of failing output is permitted. If a run fails for infrastructure reasons, preserve it and document the reason before any separately authorized rerun.

## 4. Source exposure and role separation

The current protocol distinguishes prior pipeline-debug exposure from prospectively assigned case validation:

- Any candidate previously used to debug/calibrate the screening or runner pipeline, or opened for target-test troubleshooting before prospective assignment, is permanently excluded.
- A planned technical reproduction under the frozen protocol is permitted only with designated, logged source-exposed personnel.
- The technical validator and packet preparer may inspect restricted source material but cannot serve on Panel B or as the confirmatory analyst.
- Panel A ground-truth reviewers may inspect issue/source/fix/test material but must be disjoint from Panel B.
- Panel B receives only blinded evidence packets; it must not see repository identity, issue/PR, patch, fixed commit, gold cause, or technical reproduction details.
- The confirmatory analyst must not see the gold cause or fix before analysis is locked.
- The external auditor must be independent of Panel A, Panel B, technical/legal reviewers, packet preparer, confirmatory analyst, and adjudicator.

**Known access constraint:** the project owner has already read the issue, PR, source review, and gold-fix explanation. The project owner may coordinate the work but must not act as a blinded Panel B reviewer, confirmatory analyst, or independent external auditor for this case.

No reviewer identities, consent records, institutional approval, or role assignments are currently recorded. Do not execute until those roles and access boundaries are documented.

## 5. Acceptance gates

This assignment draft does not accept the candidate. Acceptance still requires all of the following:

1. exact-row dataset and GitHub provenance;
2. final per-file/nested license review and reuse decision;
3. completed, reproducible base-fail/fix-pass test pair;
4. two independent Panel A reviews and adjudication;
5. three provenance-backed E1/E2/E3 packets with strict subset/hash invariants;
6. two independent Panel B reviews per packet level, blinded and calibrated;
7. exposure and project-independence clearance;
8. external-auditor attestation after Panel B ratings are locked;
9. complete hashes and a case-level acceptance decision.

A passing test alone is not case acceptance. A correct gold diagnosis alone is not evidence sufficiency. No model output may define the root cause or evidence tiers.

## 6. Current decision

**Keep row 90 as a strong static candidate. Do not run upstream tests or build yet.** The next step is to approve the role assignment and freeze the exact reproduction test/environment plan. If any prospective validation requirement cannot be met, leave the row unaccepted and select another untouched candidate under the frozen selection rules.

Accepted confirmatory cases remain **0**. Model loading, inference, fine-tuning, and training remain unauthorized.
