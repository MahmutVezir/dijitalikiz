# Amaranth #1518 — model temporal-exposure review

**Date:** 21 November 2026  
**Candidate:** amaranth-lang/amaranth issue #1518 / PR #1519  
**Pinned study model:** Qwen/Qwen2.5-3B-Instruct at aa8e72537993ba99e69dfaafa59ed015b17504d1  
**Status:** TEMPORAL EVIDENCE SCREEN PREPARED; PROJECT-LEAD ACKNOWLEDGEMENT PENDING; NOT A PROOF OF NON-CONTAMINATION

## 1. Exact dates

| Event | Timestamp / date | Source |
|---|---|---|
| Initial model weights and index uploaded in HF commit 3ca5f5b | 17 Sep 2024, 14:27 UTC | HF model repository history and checkpoint tree |
| Public Qwen2.5 announcement | 19 Sep 2024 | Official Qwen announcement |
| Amaranth issue #1518 created | 20 Sep 2024, 13:41:02 UTC | GitHub issue metadata |
| Amaranth PR #1519 created | 20 Sep 2024, 14:00:49 UTC | GitHub PR metadata |
| Dataset row created_at | 20 Sep 2024, 14:00:49 UTC | Pinned dataset row, authenticated in Stage 2 artifact |
| Pinned model revision aa8e725 metadata commit | 25 Sep 2024 | Hugging Face model repository history |

## 2. Reported training-data cutoff

Hassan et al., in the November 2026 AACL-IJCNLP paper “Private Evaluation Protocol: Contamination-Resistant Black-Box Evaluation via Public-Slice Surrogates”, list an October 2023 knowledge cutoff for Qwen2.5-3B-Instruct in Table 5. The same paper explains that its model-pool table uses reported cutoffs where available and distinguishes “Not disclosed” from “Not verified”. This is a secondary publication's reported value, not a vendor guarantee for the exact checkpoint.

The official Qwen2.5 announcement is dated 19 September 2024. The Qwen model repository history shows the pinned checkpoint's two safetensors shards and model index in commit 3ca5f5b on 17 September 2024. Revision aa8e725 is a later metadata update, not the first public weight upload.

## 3. Interpretation and limits

The specific issue report, dataset-row timestamp and fix PR were created after the initial public upload of the pinned checkpoint's weights and after Qwen's public announcement. The AACL paper's reported October 2023 cutoff is also earlier than these candidate events. This chronology lowers the likelihood that the exact issue text, dataset row, or fix PR was present in the checkpoint's training data.

However, it does **not** prove that all relevant Amaranth source code was absent from training. The buggy source file and the behavior existed before the issue was reported and could have been present in public source repositories or other pretraining corpora. The exact training corpus, cutoff implementation, and checkpoint-specific data provenance are not disclosed in a way that permits an absence proof here.

Therefore retain two separate statements:
- Issue/PR-specific contamination: chronology makes exposure to the exact report and fix less likely, subject to the model's actual data cutoff and any post-training updates.
- Pre-existing source-code exposure: unresolved; do not claim that the buggy source itself was absent.

No blind/source-independent researcher claim is made. The researcher has reviewed the issue, PR, exact source, and reproduction artifacts. Project-lead prior pipeline/debug exposure declaration is a separate pending question.

## 4. References

- Qwen Team, Qwen2.5 announcement, 19 September 2024: https://qwenlm.github.io/blog/qwen2.5/
- Qwen2.5-3B-Instruct repository and pinned revision: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/tree/aa8e72537993ba99e69dfaafa59ed015b17504d1
- Hugging Face commit history: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/commits/main
- Initial checkpoint tree at 3ca5f5b: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/tree/3ca5f5bff0f44b2b436a9aba99b900ab157c9a27
- Hassan, Rahaman, Uddin and Karmaker (2026), AACL-IJCNLP, Table 5: https://aclanthology.org/2026.aacl-long.168/

## 5. Decision boundary

- This is a chronology-based evidence screen, not a model training-data audit or contamination certificate.
- Project-lead acknowledgement of this bounded assessment: pending.
- Legal clearance, final case acceptance, registry inclusion, and inference authorization: not granted.