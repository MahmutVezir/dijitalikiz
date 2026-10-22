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


## Gold-label separation and operational packet validation

The runtime decision policy does not accept E1/E2/E3 condition labels. It only accepts a structural packet state (`valid` / `invalid` / unknown), and this structural state is not a semantic sufficiency judgement. The packet validator rejects extra fields (including case identity and gold/condition metadata), verifies content and manifest hashes, and explicitly does not claim to assess whether a root cause is supported.

An invalid or unknown packet state forces abstention. Even a structurally valid packet still lacks the independent claim-support coverage, self-check conflict and explicit-contradiction signals needed to make a diagnosis; if any signal is missing, the policy abstains. The independent semantic checker for these signals has not yet been implemented or validated. Never derive a runtime decision input from the experiment's gold E1/E2/E3 labels.


## Packet validation command

Validate a prepared, blinded packet without loading a model or interpreting the bug:

    python research_candidates/evidence_abstention/implementation/operational_packet_validator.py --packet /path/to/packet.json --output packet_validation.json

The packet schema and blinding contract are specified in `research_candidates/evidence_abstention/OPERATIONAL_PACKET_AUDIT_PROTOCOL.md`. A `valid` result certifies only structural integrity/hashes, not evidence sufficiency.

## Manual preflight command

From the repository root, run:

    python research_candidates/evidence_abstention/implementation/uncertainty_inference_gate.py

To make an open gate fail the shell command:

    python research_candidates/evidence_abstention/implementation/uncertainty_inference_gate.py --require-ready

The report-only form prints every blocker and exits successfully without importing PyTorch or Transformers. The require-ready form exits non-zero when any blocker remains. Neither command loads the model or runs inference.

A separately requested no-output checkpoint load can be run in the exactly pinned CUDA environment:

    python research_candidates/evidence_abstention/implementation/qwen_runtime_preflight.py --load-pinned-model-no-output --output runtime_preflight.json

This command downloads/loads the pinned model and tokenizer only after version/configuration checks; it never calls generation. Do not run it until the requested Python and package pins match. It does not open the inference gate or validate model answer quality.
