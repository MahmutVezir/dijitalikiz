# QuTiP #2646 — pinned-model temporal exposure review

**Date:** 21 November 2026  
**Candidate:** qutip/qutip issue #2646 / PR #2694  
**Pinned study model:** Qwen/Qwen2.5-3B-Instruct at `aa8e72537993ba99e69dfaafa59ed015b17504d1`  
**Status:** CHRONOLOGY SCREEN PREPARED; PROJECT-LEAD ACKNOWLEDGEMENT PENDING; NOT A TRAINING-DATA ABSENCE CERTIFICATE

## 1. Exact candidate and model chronology

| Event | Date | Evidence |
|---|---|---|
| Qwen2.5 family public announcement | 19 September 2024 | Official Qwen Team announcement |
| Pinned Qwen2.5-3B-Instruct repository revision | 25 September 2024 | Pinned Hugging Face repository revision metadata |
| QuTiP issue #2646 created | 5 March 2025, 18:35:23 UTC | GitHub issue metadata |
| QuTiP PR #2694 created; matching SWE-rebench row timestamp | 15 May 2025, 15:48:33 UTC | GitHub PR metadata and authenticated dataset row |

The candidate's issue report postdates the public Qwen2.5 release by several months; the fix PR and dataset row postdate it by almost eight months.

## 2. Interpretation

The exact issue text, issue comments, PR description, and PR patch were created after the public release and pinned repository revision of the study checkpoint. This chronology lowers the likelihood that those candidate-specific materials were present in the pinned checkpoint's pre-release training data.

This does not prove the complete pretraining cutoff, the absence of all later post-training data, or the absence of the pre-existing QuTiP source code from training. QuTiP's relevant coefficient and QobjEvo source existed before the issue report and could have appeared in public code corpora. Keep the following distinctions explicit:

- Issue/PR-specific exposure: less likely based on chronology for this pinned checkpoint.
- Pre-existing QuTiP implementation exposure: unresolved.
- Exact training-data cutoff and corpus coverage: not independently verified.

No claim is made that the source implementation or every relevant public code path was absent from training.

## 3. Researcher vs model exposure

The researcher reviewed the issue body, all retrieved issue comments, PR diff/review comments, exact buggy/fixed source, Stage 2 logs and artifact. Researcher source exposure is therefore full. No blind adjudication or inter-rater reliability claim is made.

The model-visible E3 packet is the frozen dataset row's `problem_statement` only. The later issue comments and PR discussion are not part of that field and must not be added to E3. Their review still counts as researcher exposure.

Project-lead declaration about prior use of this candidate to debug or tune the shared research pipeline remains a separate pending gate.

## 4. Sources

- Qwen Team, “Qwen2.5: A Party of Foundation Models!”, 19 September 2024: https://qwenlm.github.io/blog/qwen2.5/
- Qwen2.5-3B-Instruct model card: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct
- Pinned model revision: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/tree/aa8e72537993ba99e69dfaafa59ed015b17504d1
- QuTiP issue #2646: https://github.com/qutip/qutip/issues/2646
- QuTiP PR #2694: https://github.com/qutip/qutip/pull/2694

## 5. Decision boundary

- Chronology screen supports lower likelihood of issue/PR-specific exposure, not an absence proof.
- Project-lead acknowledgement of the bounded assessment: pending.
- Project-lead prior pipeline/debug exposure declaration: pending.
- Final case acceptance, registry inclusion and inference authorization: not granted.