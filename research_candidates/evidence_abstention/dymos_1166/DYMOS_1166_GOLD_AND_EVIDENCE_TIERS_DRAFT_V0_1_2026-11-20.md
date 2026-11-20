# OpenMDAO/dymos #1166 — proposed technical gold and E1/E2/E3 tiers

**Version:** 0.1 proposed  
**Date:** 20 November 2026  
**Disposition:** Source-aware technical proposal only; not yet the project lead's final gold/tier decision, not case acceptance, and not inference authorization.

## Candidate identity

- Upstream repository: https://github.com/OpenMDAO/dymos
- Issue: https://github.com/OpenMDAO/dymos/issues/1166
- Fix PR: https://github.com/OpenMDAO/dymos/pull/1165
- Dataset row: `openmdao__dymos-1165`
- Buggy base: `3efd1035c3bf62890034eb9e07de543f3d117867`
- Fixed PR head: `0ffc82225d6125dcb5c5b5acfb9be9fd712ef949`
- Independent reproducer: `reproduction/dymos_issue_1166/test_issue_1166.py`

## Proposed primary mechanism

On the pinned buggy base, `Phase.set_control_options` stores the caller-supplied `val` in `phase.control_options` (`phase.py:785–786`). `TranscriptionBase` passes that same `phase.control_options` mapping into `ControlInterpComp(control_options=...)` (`transcription_base.py:145–147`). In the polynomial-control branch of `ControlInterpComp._configure_controls`, the corresponding input is nevertheless initialized unconditionally as `val=np.ones(input_shape)` (`control_comp.py:120`); that active input-construction statement does not use the stored `options['val']`. The requested value is therefore recorded and propagated, but is lost at the component input's default initialization. This directly explains the observed all-ones values.

PR #1165 changes the polynomial-control input construction to normalize `options['val']` with `reshape_val` and pass that result directly into `add_input`. The exact frozen dataset selector and an independent fresh-model Brachistochrone reproducer both show the same base-fail/fixed-pass contrast.

## Competing explanations and present evidence

1. **Value-shape normalization/broadcasting defect.** This is a plausible nearby implementation concern because the fix uses `reshape_val`. However, on the buggy base the relevant `ControlInterpComp` path does not call that helper; it directly initializes with ones. The independent test uses a two-element value for a two-node polynomial control, so shape ambiguity is not required to explain the observed mismatch.
2. **A test-fixture override or stale `set_val` call.** The upstream PR rewrites the balanced-field regression into a fresh problem and removes the optimizer-only skip from the focused `run_model()` test. The independent reproducer separately constructs a fresh one-phase problem and makes no post-setup `set_val` call. Both reproduce the same mismatch.
3. **ODE target, units, or state/parameter setup.** The independent reproducer reads the promoted `phase0.controls:theta` input directly after setup/run_model, before relying on downstream ODE output interpretation. The same fixture and same runtime pass on the fixed PR head.
4. **A wider transcription-specific defect.** The candidate's frozen selector exercises the balanced-field/Gauss-Lobatto path; the additional reproducer uses a simple Gauss-Lobatto Brachistochrone phase. The evidence supports the default-initialization defect in the shared polynomial-control input component, but does not claim exhaustive coverage of every transcription/control mode.

## Proposed evidence tiers

- **E3 — issue-level only:** the frozen issue narrative.
- **E2 — observable failure:** E3 plus the independent public-API reproducer and its exact buggy-base assertion output.
- **E1 — implementation-path evidence:** E2 plus active pinned buggy-base source excerpts linking (i) API `val` storage in `Phase.control_options`, (ii) that mapping being passed to `ControlInterpComp`, and (iii) the polynomial-control input being initialized with `np.ones(input_shape)`. The commented lines from the separate `_configure_desvars` method are excluded because they are not part of this active input-construction path.

The exact inner-packet hashes and strict nesting are recorded in the proposed operational packet set. The fixed PR patch, fixed-revision output, hidden gold label, and tier names are not included in the inner packets.

## Prior related issue and counting

Dymos issue #531 (2021) concerned a broader earlier default-value problem and was explicitly resolved by PR #533. It is retained as related history in the same broad default-value issue family, not counted as an additional case. Issue #1166 is a later regression after the control-interpolation component's containment/configuration changed. Issue #1131 concerns control-rate propagation and is not the same mechanism. This candidate contributes at most one case for OpenMDAO/dymos.

## Technical evidence already verified

- Dataset selector: exact base failure / fixed revision pass; Stage 2 artifact 14341424466; outer SHA-256 `8fc5e1de9ee8c7d4be45c29b48ba9b1a0e6c82194ecb9ce2b7f5757d4fd58051`; CRC PASS; 18/18 inner hashes PASS.
- Independent public-API reproducer: workflow run 44739419824/job 136298973618; exact base failure `[[1.0],[1.0]]` vs `[[5.0],[15.0]]`; same test passes on fixed PR head; artifact 14629598269; SHA-256 `33bb899d7e4e56d177fe4c9d119eebea49519528e88d74af3efc4acf7def08d8`; CRC PASS; 15/15 inner hashes PASS.
- Exact source and dependency scope are documented separately. Documentary inventory is not legal clearance.

## Required project-lead decision

The project lead should record whether the proposed mechanism and tier thresholds are accepted, revised, or unresolved. Hasan's input may be recorded as project-lead-reported supplementary concurrence only; it is not represented as a signed independent review. Before final case acceptance, complete the bounded documentary license-scope acknowledgement, candidate-specific prior pipeline/debug exposure declaration, schema-conformant case record, registry validation, and separate final YES/NO.

No model loading, inference, fine-tuning, or training is authorized.
