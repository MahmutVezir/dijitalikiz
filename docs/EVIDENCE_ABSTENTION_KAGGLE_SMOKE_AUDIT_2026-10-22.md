# Kaggle engineering smoke audit — 22 October 2026

**Classification: exploratory engineering smoke only. Not official, not confirmatory, not a calibration set.**  
**Experiment inference gate:** remains closed for the evidence-abstention study.

## Immutable run and artifact

- GitHub Actions run: [39837255019](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39837255019)
- Kaggle kernel: `mahmutvezir/qwen-e1-p0-p1-ansible4-ddc46f9e-39837255019-1`
- Kernel status: `KernelWorkerStatus.COMPLETE`
- GitHub artifact ID: `12452505143`
- GitHub artifact ZIP SHA-256: `f35f33029b0a42610e2d2ad2bfb6cedc90f2f9d7e0b14e632787872ae2a2e10d`
- Source commit for the smoke branch: `ddc46f9e35da71ebd16e220b229e882b5e4423e4`
- Model: `Qwen/Qwen2.5-3B-Instruct`, immutable revision `aa8e72537993ba99e69dfaafa59ed015b17504d1`
- Device/precision: Tesla T4 / FP16
- Observed smoke runtime: Python `3.13.15`, PyTorch `2.11.0+cu128`, Transformers `4.48.3`
- Saved output files: 10 raw JSONL responses and 955 per-token score/logit records; the five files listed in the artifact's `SHA256SUMS` all passed checksum verification.

The smoke runtime above differs from the candidate runtime lock for the dedicated uncertainty study (Python 3.11.9, torch 2.2.1, transformers 4.43.2, accelerate 0.33.0). Consequently, this smoke does **not** count as passing that study's exact-runtime preflight.

## Observed outputs

The run used the previously exposed `BugsInPy-ansible-4` defect at evidence level E1, with five seeded generations per condition.

| Descriptive metric | P0: diagnosis requested | P1: selective abstention allowed |
|---|---:|---:|
| Generations | 5 | 5 |
| JSON parsed successfully | 5/5 | 5/5 |
| Outputs labeled diagnose | 5/5 | 5/5 |
| Model-declared abstentions | 0/5 | 0/5 |
| Matches to the smoke's provisional automated rubric | 0/5 | 0/5 |
| Mean normalized token entropy | 0.044207 | 0.038143 |

The reported `0.95` confidence values are model self-reports, **not calibrated probabilities**. The smoke rubric is an automated keyword/phrase proxy, not an independent human judgment or a validated root-cause scoring metric. The fact that both conditions scored 0/5 against this provisional rubric warrants inspecting the raw responses, but it does not establish a population-level error rate or prove that P1 does not work.

Separately, the fail-closed decision engine abstained in both conditions for `claim_support_unavailable`, `uncertainty_signals_incomplete`, and `calibration_not_frozen`. Those are the software guard's decisions, not model-generated abstentions and not research outcomes.

## Protocol deviations and validity limits

1. **Previously exposed case.** Ansible-4 was already inspected while the technical workflow was being built. It is not eligible for confirmatory sampling and must remain excluded.
2. **Evidence packet differs from the frozen study design.** The smoke prompt contains the complete patch diff and successful patched-tree test output, in addition to the buggy test log and case metadata. The frozen `PROMPT_CONDITIONS.md` prohibits including the fixed patch/fix material in model prompts. This smoke therefore does not implement the frozen E1/E2/E3 packet protocol; information from the fix is directly visible to the model.
3. **Different runner environment.** The runtime does not match the dedicated study's candidate lock. The exact study runtime remains `not_run`.
4. **One defect, ten repeated responses.** The responses are not ten independent defects. Five samples per condition provide no population estimate.
5. **No independent semantic rating.** The automated rubric does not replace the two-person blinded review process and was not validated against independent ratings.
6. **Uncalibrated confidence.** No independent calibration dataset was used. Entropy and sample-to-sample variability must not be described as pure epistemic uncertainty or calibrated confidence.
7. **Attention-mask issue observed.** Kaggle logs reported that an attention mask could not be inferred because the tokenizer's padding token is the end-of-sequence token. The adapter now requests the attention mask from the chat template and passes it explicitly to generation; corresponding CPU tests were added in the code PR.

## Conclusion

This run verifies that the GitHub-to-Kaggle lane could authenticate, submit a private Tesla T4 kernel, generate outputs with the pinned Qwen checkpoint, download the output artifact and verify its checksums. It also surfaced an attention-mask handling issue.

It does **not** test the official confirmatory protocol and does not show that the proposed abstention policy reduces unsupported diagnoses. Do not copy these ten responses into the calibration dataset or accepted case registry. Preserve the artifact as an engineering-smoke record only.

## Next steps in three macro-stages

1. **Data and independent review:** establish the required accepted, unexposed cases; finish license/provenance and root-cause review with two people; prepare a separate disjoint blinded evidence-sufficiency panel.
2. **Runtime and calibration:** verify the exact locked Kaggle environment without output generation; validate the operational semantic-support/contradiction signal and a separate adjudicated calibration set; freeze thresholds and all relevant hashes.
3. **Registered experiment:** publish a verifiable preregistration, close every gate, obtain explicit authorization, then run the frozen E1/E2/E3 × P0/P1 design and analyze the prespecified endpoints.

Until all three are satisfied, no confirmatory inference should be run.

## Workflow containment

After the captured smoke artifacts were audited, both one-off GPU smoke workflow definitions were moved out of `.github/workflows/` to `research_candidates/evidence_abstention/archived_smoke_workflows/` with the suffix `.yml.disabled`. Their source is preserved for traceability but is no longer a GitHub Actions workflow. This brings the repository back to its single-canonical-Kaggle-workflow rule; it does not delete the completed historical run or its artifact.
