# Uncertainty experiment inference gate

**Current status: closed. This manifest does not authorize Qwen model loading or generation.**

The uncertainty adapter is separate from the confirmatory E1/E2/E3 × P0/P1 experiment. It uses five seeded candidate generations and entropy computed from Transformers generation-score vectors after configured decoding processors. Those scores are not mislabeled as raw base-model logits.

Before any model loading or generation, the read-only gate requires:

- Explicit manifest authorization and a CLOSED case-validation gate.
- A verifiable preregistration URI and frozen reviewer/adjudication protocol.
- At least 60 independently accepted cases across at least eight upstream projects.
- Exact model/tokenizer/runtime verification.
- Existing artifact files whose SHA-256 hashes match the frozen manifest.
- Separate explicit authorization through EVIDENCE_UNCERTAINTY_INFERENCE_APPROVED=YES.

The current manifest deliberately fails these gates: no accepted case IDs, open validation gate, draft preregistration, unverified model runtime, empty frozen hashes, empty calibration data, and no authorization. Unit tests use synthetic sample objects only; they do not load a model or generate research outputs.

The selected answer is candidate zero from a predeclared seed policy. Outputs are not cherry-picked based on self-reported confidence. Missing independent evidence-support or contradiction audits cause abstention. This prototype does not estimate pure epistemic uncertainty: generation-score entropy and response dispersion can also reflect decoding variability.


## Gold-label separation and runtime audit signals

The current `EvidenceAudit` object does **not** carry an E1/E2/E3 condition label or a `runtime_evidence_level` field. It carries a structural `packet_validation_status` plus semantic audit inputs: `supported_claim_coverage`, `self_check_conflict`, and `explicit_contradiction`.

- `packet_validation_status` may only be the output of the structural packet/hash validator. It is not an E-level label or a semantic sufficiency rating.
- A deterministic structural packet/citation auditor is implemented at `implementation/evidence_packet_audit.py`; it checks exact fields, content and packet SHA-256 hashes, duplicate IDs, forbidden hidden-label fields, and reference existence. It explicitly reports `semantic_support_status=not_assessed` and does not infer semantic entailment.
- The three semantic signals (`supported_claim_coverage`, `self_check_conflict`, and `explicit_contradiction`) still require a separately designed and independently validated operational method. They are not supplied by the structural auditor. `evidence_audit_from_structural_report()` bridges only structural status and evidence IDs and deliberately leaves all three semantic fields as `None`, which forces the decision layer to abstain.
- Never derive those runtime signals from gold E1/E2/E3 labels, the hidden root cause, the patch, or post-hoc outcome scores. Doing so would leak the answerability condition and make E3 abstention results tautological.
- If any required signal is unavailable, pass `None`; the decision policy must abstain. Do not substitute gold labels or synthetic values to make a decision look calibrated.


## Manual preflight command

From the repository root, run:

    python research_candidates/evidence_abstention/implementation/uncertainty_inference_gate.py

To make an open gate fail the shell command:

    python research_candidates/evidence_abstention/implementation/uncertainty_inference_gate.py --require-ready

The report-only form prints every blocker and exits successfully without importing PyTorch or Transformers. The require-ready form exits non-zero when any blocker remains. Neither command loads the model or runs inference.
