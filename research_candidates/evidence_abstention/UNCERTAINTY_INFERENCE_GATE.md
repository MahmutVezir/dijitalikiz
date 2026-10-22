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
