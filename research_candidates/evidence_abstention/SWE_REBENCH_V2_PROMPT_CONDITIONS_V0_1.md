# SWE-rebench V2 prompt conditions — v0.1 draft

**Status:** Draft only; not frozen or externally preregistered. No inference authorization.

## Shared system instruction

The exact shared system instruction is defined in `implementation/swe_rebench_v2_contract.py::SYSTEM_PROMPT`. It is identical in both conditions. The model must use only the visible packet and must not claim to have executed tests or consulted external sources.

## P0 — forced diagnosis

> Select and state the single most likely root cause. Do not decline to give a diagnosis. Even when evidence is incomplete, provide the most likely diagnosis and identify the supplied evidence that led to it.

## P1 — selective diagnosis / abstention

> Give a root-cause diagnosis only when the supplied evidence supports it and distinguishes it from plausible alternatives. When evidence is insufficient or materially contradictory, do not guess: explicitly abstain and identify the specific additional evidence needed to distinguish the alternatives.

## Controlled comparison

The same model revision, tokenizer revision, system instruction, evidence packet, response schema, decoding settings, and output budget must be used in both policies. Only the policy instruction changes. No policy name or hidden E1/E2/E3 label is included as a literal condition tag in the user prompt.

The E-level wrapper, case ID, repository name, issue/PR identifiers, patch, test patch, PR description, fixed commit, reviewer labels, and source snapshot hashes are not model-visible. The prompt builder receives the externally hash-verified packet set and serializes only the selected inner packet's item ID, kind, and visible content.

## Response rules

One JSON object only, using the common `SWE_REBENCH_V2_OUTPUT_SCHEMA_V0_1.json`. Diagnoses must include a non-empty root-cause statement and at least one evidence reference. Abstentions must set `root_cause` to the empty string. Evidence references are identifiers copied from visible items; their syntactic validity is not evidence of semantic support.

No JSON repair, Markdown-fence stripping, automatic retry, or post-hoc conversion to abstention is permitted. Preserve exact raw output bytes/string, output hash, parser result, reference-validity result, and human-adjudicated scores separately.

## Status

- Prompt text: draft.
- Human reviewer approval: pending.
- Prompt/schema hashes: not frozen.
- Model inference: not performed and not authorized.
