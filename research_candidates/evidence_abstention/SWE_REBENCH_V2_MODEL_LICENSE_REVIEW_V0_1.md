# Qwen model-revision license review — preliminary evidence record

**Status:** Preliminary source inspection only. Legal/mentor review remains pending. This is not a legal opinion and does not authorize model loading or inference.

## Exact model pin

- Repository: `Qwen/Qwen2.5-3B-Instruct`
- Immutable revision: `aa8e72537993ba99e69dfaafa59ed015b17504d1`
- Exact revision tree: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/tree/aa8e72537993ba99e69dfaafa59ed015b17504d1
- Exact revision LICENSE page: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/aa8e72537993ba99e69dfaafa59ed015b17504d1/LICENSE
- Hub license identifier shown at this revision: `qwen-research`
- The Hub does not identify this revision as Apache-2.0.

## Terms visible in the exact pinned LICENSE

The LICENSE page identifies a **Qwen RESEARCH LICENSE AGREEMENT**, dated 19 September 2024. The visible terms include:

1. The grant is a limited, non-exclusive, worldwide, non-transferable and royalty-free license for use, reproduction, distribution, copying, derivative works and modifications **for non-commercial purposes only**.
2. Commercial use requires requesting a separate license.
3. Redistribution of the Materials or derivatives requires providing recipients a copy of the agreement, marking modified files prominently, and retaining the specified Qwen attribution notice in a distributed Notice file.
4. The agreement includes applicable export-control compliance language.
5. It says that if Materials or outputs/results are used to create, train, fine-tune, or improve an AI model that is distributed or made available, related product documentation must prominently display “Built with Qwen” or “Improved using Qwen”.
6. The agreement specifies governing law and jurisdiction in China/Hangzhou.

This record summarizes visible clauses; it does not replace review of the complete agreement or determine how a particular competition, prize, publication, or future use is classified.

## Preliminary project relevance

- The current protocol is a non-commercial research/evaluation study and does not fine-tune, train, modify, or redistribute model weights.
- That intended scope appears more consistent with the stated research/evaluation purpose than commercial deployment, but this is not a legal conclusion.
- Public release of the paper, prompts, raw outputs, derived artifacts, or a later product must be checked separately against the full agreement and competition rules.
- Do not describe this model as Apache-2.0 or as unrestricted open source.

## Required decision before any model use

A qualified mentor/institutional reviewer must record whether the intended research-contest use and planned dissemination fall within the non-commercial grant, and whether any additional approval or attribution is required. Until then:
- `license_review_status = pending_exact_revision_review`
- model loading remains prohibited;
- inference remains prohibited;
- no weights or model-derived artifacts are redistributed.

## Source provenance

The exact revision tree and LICENSE page were inspected on 15 November 2026. The Hub tree displays the exact commit and the `LICENSE` file at that revision. The repository's immutable revision is pinned above; this record does not claim an independently computed SHA-256 of the LICENSE file bytes.
