# Held-out case discovery and technical screening — 2026-10-10

**Status: technical red/green screen passed; independent human review is still pending.** This log summarizes the latest corrected source-only screen. It does not admit any case to the held-out confirmatory sample and does not authorize model inference.

## Latest verified screen

- **Current screening run:** [Held-out Lead Red-Green Screening, #38054680670](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38054680670) — success.
- **Repository validation:** [Research Validation (No Inference), #38054680672](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38054680672) — success.
- **Scope:** 11 public defect leads across Apache Commons Lang, Commons Collections, Commons Net, Commons Text, Commons Compress, Jackson Databind, and Netty.
- **Test evidence:** 21 named regression targets failed on their pinned pre-fix revisions and passed on their pinned fixed revisions. All 11 screening jobs, including artifact upload, succeeded.
- **Reproducibility fix:** The first rerun, [#38054377625](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38054377625), could not run the Compress 805 test because Maven could not resolve `org.apache.commons:commons-parent:104`. That attempt was **not** counted as a regression failure. The corrected workflow installs the POM from the pinned Apache Commons Parent 104 RC1 source commit `9066f72892fba9af187520ba37889ae068a333ba`, records the POM hash, and then runs the named test. In the corrected run, Compress 805 passed both red and green checks.
- **Model execution:** none. The workflow uses Java/Maven tests only; it does not load Qwen, run Kaggle inference, or alter the historic pilot/confirmatory archives.

Machine-readable, hash-bound evidence: [discovery_screening_audit_run_38054680670.json](https://github.com/MahmutVezir/dijitalikiz/blob/research/scoring-calibration-mainline-v2/data/followup_v2/discovery_screening_audit_run_38054680670.json). The prior complete screen [#38053933548](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38053933548) is retained as a separate historical checkpoint; its archive hashes are not overwritten.

## Most promising leads for human review

1. [Commons Net #403 — check FTP parser type before instantiation](https://github.com/apache/commons-net/pull/403): an untrusted server `SYST` reply may influence parser dispatch and trigger construction/class initialization before type validation.
2. [Commons Net #404 — hostname verification on FTPS data channel](https://github.com/apache/commons-net/pull/404): the data-channel TLS handshake must honor the hostname verification applied to the control connection.
3. [Commons Text #768 — StringMatcher buffer-window forwarding](https://github.com/apache/commons-text/pull/768): the overload's buffer index must remain correct through custom matchers and `StringSubstitutor`.
4. [Commons Net #400 — reject CR/LF in protocol command arguments](https://github.com/apache/commons-net/pull/400): the same command-line injection invariant spans FTP, NNTP, POP3, and SMTP. This is **one shared defect case**, not four independent samples.
5. [Commons Compress #805 — preserve Pack200 exception propagation](https://github.com/apache/commons-compress/pull/805): malformed nested reference data should propagate the declared exception through the unpacker adapter rather than escaping as a bare `Error`.
6. [Jackson Databind #6256 — property filters for ObjectNode any-getter entries](https://github.com/FasterXML/jackson-databind/pull/6256): node-valued any-getter serialization should respect the same inclusion/ignore rules as map serialization.

Other passing leads include Commons Lang #1800 and #1807, Commons Collections #728, Jackson Databind #6096, and Netty #17759. The machine-readable audit records each case's exact revisions, test targets, artifact ID, downloaded ZIP SHA-256, and provisional limitations.

These are prioritization notes only, not final gold labels. Commons Lang #1807 may be too localized, Commons Collections #728 may represent a related implementation family rather than a deep cross-component causal path, and the Jackson/Netty leads also need reviewers to confirm that their candidate graph represents meaningful cross-component dependencies.

## What is still not complete

- Eligible held-out confirmatory cases: **0/61**.
- Independent source reviewers: not recorded.
- Separate adjudication: not recorded.
- Scoring-rubric calibration and reviewer-reliability gate: not complete.
- V2 protocol freeze and model inference permission: still blocked.

Every source and fix is public; the model's exact training-data exposure is unknown. Passing a regression test only establishes that the test distinguishes pinned revisions. It does not establish that the proposed root cause is complete, every CCDG edge is justified, or that the case is appropriate for measuring graph-structure effects.

## Next required gates

1. Have two independent Java/software reviewers inspect both exact revisions, test semantics, causal mechanism, dependency edges, license/provenance, and contamination limitations.
2. Have a separate adjudicator resolve disagreements and freeze the evidence-bound source review.
3. Exclude weak or incoherent candidates rather than padding the sample. Keep historic pilot/confirmatory cases and all scoring-calibration cases disjoint.
4. Finish human scoring calibration, runtime/tokenizer checks, power-assumption review, randomized schedule hashing, and the protocol freeze.
5. Run inference only after the fail-closed protocol validator reports readiness. The old 40-record pilot and 160-output confirmatory archive remain immutable.

Review coordination: [Issue #7](https://github.com/MahmutVezir/dijitalikiz/issues/7). More candidate submissions: [Issue #8](https://github.com/MahmutVezir/dijitalikiz/issues/8).
