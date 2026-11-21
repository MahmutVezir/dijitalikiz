# Project-lead reported cross-check — CTAPIpe #2732

**Date recorded:** 18 November 2026  
**Candidate:** CTAPIpe issue #2730 / PR #2732  
**Evidence class:** Project-lead narrative corroboration; not a substitute for the retained reproducible artifact.

## Reported checks

The project lead reports two additional checks consistent with the technical conclusion already established by the frozen reproduction:

1. The project lead independently reasoned through and reproduced the same technical conclusion using their own programming/coding knowledge.
2. To cross-check that assessment, the project lead consulted a separate AI tool, which reportedly returned the same conclusion.

## Scope and limitations

This record captures the project lead's statement as reported in the conversation on 18 November 2026. The exact programming language(s), source code or commands, environment versions, execution logs, second AI product/model/version, prompt, raw response and hashes were not supplied in that statement and are therefore not invented here.

Accordingly:
- the project-lead check is supplementary corroboration, not a second independently archived reproduction;
- the separate AI response is an AI-assisted cross-check, not an independent human review or ground-truth oracle;
- neither check changes the candidate's prior pipeline/debug exposure classification (`some`) or its exclusion from the model-evaluation sample;
- the authoritative technical evidence remains the pinned exact-base/fixed workflow and its independently verified artifact.

## Primary technical evidence

- Workflow run: `44324115597`
- Job: `134870646827`
- Artifact: `14436277116`
- ZIP SHA-256: `9e3e35f4f499a3a5947e0e6ad803dd7d6d9d1c240695a6558769e7f31ea501b2`
- Archive members: 137
- ZIP CRC: PASS
- Internal SHA-256 entries: 136/136 verified
- Buggy base: defect-specific frozen selector failure and direct HDF5 float/Quantity writer failure
- Fixed revision: frozen selector and direct HDF5 reproducer pass

No model loading, inference, fine-tuning or training was performed.

## Decision status

The project lead's prior pipeline/debug exposure decision remains `some`. CTAPIpe #2732 remains excluded from the model-evaluation sample and retained as an engineering/feasibility pilot only. This supplemental cross-check does not waive that exclusion or authorize inference.
