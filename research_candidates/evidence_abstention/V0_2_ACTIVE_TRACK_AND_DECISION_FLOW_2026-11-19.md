# Active v0.2 research track and human decision flow — 19 November 2026

## 1. Single active study definition

The active study is **SWE-rebench V2 evidence-abstention, v0.2 exploratory/feasibility**.

- Research question: whether a policy allowing evidence-conditioned abstention reduces unsupported or contradicted definitive root-cause claims when visible evidence is insufficient, compared with a diagnosis-required policy.
- Primary P0/P1 comparison: same exact frozen base-model weights, tokenizer, runtime, prompts except the predeclared policy change, and generation settings.
- Evidence support and hidden-gold correctness are separate outcomes.
- Minimum for a case-level feasibility demonstration: 1 fully accepted independent case.
- Primary target: 15 accepted cases from 15 distinct upstream projects.
- Stretch target: 20.
- Keep every case that passes unchanged criteria if fewer than 15 pass; report the smaller exploratory result without confirmatory efficacy claims.
- One case maximum per upstream project.
- Model training is a separate secondary hypothesis and authorization; primary inference acceptance does not authorize fine-tuning.

The authoritative v0.2 artifacts are:
- `SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json`
- `SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json`
- `SWE_REBENCH_V2_EXPLORATORY_CASE_ACCEPTANCE_SCHEMA_V0_1.json`
- `implementation/swe_rebench_v2_exploratory_case_acceptance.py`
- `scripts/swe_rebench_v2_exploratory_preflight.py`

## 2. Legacy files are retained, not active

The following files are historical v0.1 confirmatory artifacts and must not be mixed into the active v0.2 flow:
- `SWE_REBENCH_V2_EXPERIMENT_MANIFEST_V0_1.json`
- `SWE_REBENCH_V2_CASE_REGISTRY_V0_1.json`
- `SWE_REBENCH_V2_CASE_ACCEPTANCE_SCHEMA_V0_1.json`
- `implementation/swe_rebench_v2_case_acceptance.py`
- `scripts/swe_rebench_v2_no_inference_preflight.py`
- `HUMAN_REVIEW_ROLE_GOVERNANCE_V0_1.md`

The old validator requires a Panel A/Panel B/external-audit/confirmatory workflow and a 60-project threshold. Those are **not** v0.2 exploratory requirements. The old script already labels itself legacy; the old human role-governance draft now carries a matching legacy notice. Do not run it as the active readiness report or use its 60-case gate to reject v0.2 cases.

## 3. Case decision flow — proposal is not acceptance

The prior v0.2 case schema required `acceptance_decision="accepted"` even for a case that still needed validation and a final project-lead decision. That was circular and could make a draft look accepted too early.

The active schema and validator now distinguish:
- `proposed`: full case record can be structurally checked; final decision must be pending, with no final-decision timestamp or artifact. This status cannot enter the accepted registry.
- `accepted`: only after the project lead makes a separate explicit YES decision; the record must include a timestamped, hashed final-decision artifact. Registry validation permits only this state.
- `rejected`: the negative decision and its record may be preserved outside the accepted registry.

The validator remains structural and consistency-only. It does not verify URLs/artifacts, establish legal clearance, prove scientific truth, or authorize model execution.

## 4. Human reviewer roles are separated

Three roles must not be conflated:

1. **Project lead (Mahmut):** owns the final case and protocol decision.
2. **Technical/methodology panel reviewers:** Panel Reviewer H and Panel Reviewer T (private identity mapping is held outside the public repository) are proposed for unblinded yes/no review of case evidence and research design. The project lead reports shared agreement with the previously presented Dishka technical/gold/tier/limitations summary. Individual signed decision records are not fabricated; when formal concurrence is recorded, it must be based on the reviewers' actual submitted decisions.
3. **Blind model-output scorer `Rater_B`:** a separate role in the active v0.2 manifest. It is not automatically Hasan or Batuhan. Anyone who sees the case issue, PR, source, patch, gold mechanism or hidden evidence-tier decision cannot be called blind to those materials for the same case's model-output scoring.

If both technical panel reviewers inspect full technical case materials, they remain valid technical reviewers but are not eligible as blinded output scorers for that case. A separate unexposed scorer or a prospectively amended scoring design is needed. ChatGPT remains advisory and is never a human rater or external auditor.

## 5. Dishka #435 — first candidate, not pre-accepted

Dishka is the first candidate to complete the formal v0.2 case-review route because:
- exact buggy/fixed source pins are recorded;
- exact issue reproducer fails on the buggy base and passes on the fixed revision;
- all 8 frozen dataset selectors fail on the buggy base and the same 8 pass on the fixed revision;
- latest artifact 14536192821 has an outer SHA-256 matching GitHub, CRC passes, and 32/32 inner hashes pass;
- the project lead's gold, alternatives and E1/E2/E3 rationale approvals are recorded;
- researcher source exposure is openly acknowledged as full; exploratory-only use and single-human-adjudicator limitations are recorded.

Remaining Dishka-specific decisions:
- confirm `prior_pipeline_debug_exposure = none` as a fact. This is separate from the already acknowledged full researcher source exposure. If the answer is prior debug exposure, the current protocol excludes the case; do not weaken the rule.
- project-lead acceptance of the bounded documentary source-license screen (Apache-2.0 exact base, five changed files, minimal reproduction and pinned test/extraction environments). This is not formal legal advice or blanket redistribution approval.
- complete proposed case JSON, validate it as `proposed`, resolve all structural/provenance inconsistencies, then present one short final YES/NO project-lead decision.
- YES: create separate timestamped/hash-recorded acceptance decision, update the record to accepted, rerun case and registry validators, then insert into registry.
- NO: preserve the rejection/hold record outside registry and move to NumPyro #1916.
- No model inference or training is authorized by case acceptance alone; all global v0.2 gates and separate authorization still apply.

## 6. Candidate fallback rule

The first candidate is not privileged over the evidence. If Dishka's prior pipeline/debug classification is not `none`, its bounded license scope is unacceptable, a source/timestamp/hash mismatch emerges, or the proposed case fails the active schema/registry checks for a substantive reason, do not patch the standard to force it in. Record the reason and proceed to **NumPyro #1916**, then other Stage 2 passes in the existing order.

## 7. Current state

- Dishka technical Stage 2: PASS.
- Dishka gold/tier decision: project-lead approval recorded.
- Dishka accepted registry state: **not accepted**.
- Active case registry: 0.
- Prior pipeline/debug exposure: confirmation pending.
- Bounded documentary license-screen scope: sign-off pending.
- Project-wide model/license/runtime/protocol/hash and Rater_B gates: still open.
- No model load, inference, fine-tuning or training performed.
