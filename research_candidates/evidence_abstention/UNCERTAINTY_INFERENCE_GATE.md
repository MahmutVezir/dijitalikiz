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


## Gold-label separation

The adapter field named runtime_evidence_level must come from a separately designed operational evidence-sufficiency checker. Never copy the dataset's gold E1/E2/E3 condition label into this field: doing so would leak the answerability condition to the decision policy and make E3 abstention results tautological. The operational checker has not been implemented or validated in this scaffold. If its runtime assessment is unavailable, the adapter must receive null and abstain; do not substitute the gold label to make the system appear to work.


## Manual preflight command

From the repository root, run:

    python research_candidates/evidence_abstention/implementation/uncertainty_inference_gate.py

To make an open gate fail the shell command:

    python research_candidates/evidence_abstention/implementation/uncertainty_inference_gate.py --require-ready

The report-only form prints every blocker and exits successfully without importing PyTorch or Transformers. The require-ready form exits non-zero when any blocker remains. Neither command loads the model or runs inference.
