# SkyPilot #5981 — Stage 3 screening addendum

**Date:** 21 November 2026  
**Candidate:** skypilot-org/skypilot issue #5981 / fix PR #5985  
**Dataset row:** `skypilot-org__skypilot-5985`  
**Disposition:** Stage 2 technically verified; **not recommended for the primary three-tier abstention sample** pending project-lead decision on its evidence-disclosure problem. Not accepted.

## 1. Exact Stage 2 evidence recheck

- Buggy base: `60a6c930feeb8c48511f74c25bc2d7e12b290dd6`
- Fixed PR revision: `c8154ff3a4875cbb1bac8f29bb45254f264d72ba`
- Issue #5981 / PR #5985: [issue](https://github.com/skypilot-org/skypilot/issues/5981), [merged fix](https://github.com/skypilot-org/skypilot/pull/5985)
- Frozen row SHA-256: `a846e85ec5452d8100659e5c6c8cbecc3401dae16b8830eed77543172ef9bbbe`
- Frozen selector: `tests/unit_tests/test_sky/clouds/test_ssh.py::TestSSHExistingAllowedContexts::test_complex_scenario_with_mixed_filtering`
- Exact buggy-base run: selector executed; assertion failed because the result was `['ssh-prod']` rather than `['ssh-prod', 'ssh-staging']`.
- Exact fixed revision: the same selector passed.
- Test-only patch touched only `tests/unit_tests/test_sky/clouds/test_ssh.py`; no production source was applied to the buggy base.

The downloaded Stage 2 archive was independently rehashed in this review:
- Artifact ID: `14344534041`
- Outer ZIP SHA-256: `10f5505f390426e003a833ffa60cd026a9513c33da9b5a0d288844374057f34c` (matches the recorded digest)
- ZIP CRC: pass
- Internal SHA256SUMS: 19/19 match

This is a valid exact-base/fixed-revision technical reproduction. It does not by itself establish eligibility for the three-tier abstention comparison.

## 2. Gold mechanism and evidence-tier feasibility

The defect mechanism is that Python `str.lstrip("ssh-")` removes any leading characters belonging to the set `{'s','s','h','-'}`, rather than removing the literal prefix `"ssh-"`. For example, `"ssh-staging".lstrip("ssh-")` becomes `"taging"`. PR #5985 replaces the affected calls with `common_utils.removeprefix`.

**Critical design issue:** the frozen dataset problem statement itself says that `lstrip('ssh-')` causes context names containing characters from `ssh-` to be stripped. The defect-specific semantics are therefore substantially disclosed in the E3 task evidence, before any E2/E1 enrichment. This is not an inference from the hidden source; it is text in the model-facing row.

Under the approved v0.2 protocol, E3 must leave multiple predeclared causal mechanisms genuinely possible. Here, a model can identify the central defect from the task statement alone. An honest E3 packet cannot remove or rewrite that statement to make the case artificially ambiguous.

**Advisory recommendation:** do not advance SkyPilot #5981 into the primary three-tier abstention sample unless the project lead can demonstrate a defensible, meaning-preserving E3 ambiguity that does not hide or rewrite the source task. In its current frozen form it is better treated as:
- a technical reproduction / engineering-feasibility case; or
- a possible easy-answer control outside the primary three-tier sample.

Do not force an E3 ABSTAIN label merely to make the case fit the study. E3 ANSWER is likely the evidence-supported classification for the frozen task as written, which means the intended E3 uncertainty contrast is absent.

## 3. Issue-family linkage

A later issue in the same repository, [SkyPilot #7662](https://github.com/skypilot-org/skypilot/issues/7662), also describes using `lstrip` to remove the literal `ssh-` prefix and explicitly notes the character-set behavior. A maintainer comment recommends `common_utils.removeprefix`.

This is the same root-cause family, not an independent project. #7662 is a later related report; the exact call-site overlap with #5981 was not independently mapped in this pass. Preserve it as related issue-family evidence and count at most one SkyPilot case. See the accompanying issue-family JSON.

## 4. License, provenance, and exposure gates

- Exact-base root repository license: Apache-2.0.
- Frozen dataset row license metadata: Apache-2.0.
- The dataset card's CC-BY-4.0 is a separate data-source license; it does not relicense upstream source.
- The Stage 2 lock inventory contains 86 installed distributions. Eight have a null license field despite permissive classifiers; other entries need canonical-license review, including multiple/alternative SPDX expressions and `psycopg2-binary` (reported as LGPL with exceptions). NumPy's bundled binary notices include OpenBLAS/LAPACK plus GCC runtime / libquadmath components; these require applicable notice/scope checking.
- Exact pinned dataset-card README revision/bytes provenance and canonical dependency/notice checks remain open. No bounded research-scope acknowledgement or legal clearance is recorded.
- Candidate-specific prior pipeline/debug exposure has **not yet been declared by the project lead**. Do not infer `none`.
- Researcher source exposure is `full` after review of issue, PR, exact source, selector, and Stage 2 evidence. No blinded adjudication or inter-rater claim is made.
- The pinned Qwen model's precise training-data cutoff is not established by the reviewed model metadata. Issue/PR publication dates after the public Qwen2.5 release do not prove absence from all pretraining data; do not claim a verified no-contamination result.

## 5. Status boundary

- Stage 2 technical reproduction: passed and archive integrity rechecked.
- Three-tier sample suitability: advisory no-go pending project-lead review of E3 disclosure.
- Prior pipeline/debug exposure: pending direct declaration.
- Bounded research scope: pending source/data/dependency/native-notice review and later explicit acknowledgement.
- Final case acceptance: not accepted.
- Registry inclusion: false.
- Model load, inference, fine-tuning, and training: not performed and not authorized.

The Stage 2 pass is retained as technical evidence. It must not be reported as a final accepted research case.
