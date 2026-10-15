# Validating returned blind-review JSONL files (v1.2)

This validator is used only after a real reviewer returns their completed JSONL. It checks completeness and preservation of the frozen packet, not the semantic correctness of answers, ground truth, evaluator independence, or agreement.

## Run

Attach or copy the assigned original ZIP locally, then run the matching command:

    python scripts/validate_semantic_review_submission.py --packet semantic_review_reviewer_A.zip --submission reviewer_A_completed.jsonl

For reviewer B, use B's original ZIP and returned JSONL. The validator never requires or accepts coordinator key files. It prints only structural validation status and field-level label counts; it does not print answer text or rationale notes.

A pass means 160 rows are present, IDs and row order are retained, metadata/model responses/evidence are unchanged, required labels use allowed values, and all rationale fields are nonblank. It does not mean any answer is correct.

## Tests

    python -m unittest discover -s tests -p 'test_validate_semantic_review_submission.py' -v

The tests construct synthetic records only. They do not contain genuine human ratings and do not change historical research artifacts.
