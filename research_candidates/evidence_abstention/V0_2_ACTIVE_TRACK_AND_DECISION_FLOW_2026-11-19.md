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
2. **Technical/methodology panel reviewers:** Panel Reviewer H and Panel Reviewer B (private identity mapping is held outside the public repository) are proposed for unblinded yes/no review of case evidence and research design. The project lead reports shared agreement with the previously presented Dishka technical/gold/tier/limitations summary, but this does not substitute for either reviewer's own recorded decision.
3. **Blind model-output scorer `Rater_B`:** a separate role in the active v0.2 manifest. It is not automatically either technical panel reviewer. Anyone who sees the case issue, PR, source, patch, gold mechanism or hidden evidence-tier decision cannot be called blind to those materials for the same case's model-output scoring.

If both technical panel reviewers inspect full technical case materials, they remain valid technical reviewers but are not eligible as blinded output scorers for that case. A separate unexposed scorer or a prospectively amended scoring design is needed. ChatGPT remains advisory and is never a human rater or external auditor.

## 5. Dishka #435 — excluded after factual exposure declaration

Dishka remains a technically reproduced and Stage 3 technically adjudicated engineering record:
- exact issue reproducer failed on the buggy base and passed on the fixed revision;
- all 8 frozen dataset selectors failed on the buggy base and the same 8 passed on the fixed revision;
- latest artifact 14536192821 has an outer SHA-256 matching GitHub, CRC passes, and 32/32 inner hashes pass;
- the project lead's technical gold, alternatives and E1/E2/E3 rationale approvals remain in the engineering history.

On 19 November 2026, the project lead explicitly declared `prior_pipeline_debug_exposure = some`. The active v0.2 rule requires `none`. Dishka is therefore **excluded from the model-evaluation sample**. This decision is recorded in `reproduction/dishka_issue_435/PROJECT_LEAD_EXPOSURE_DECISION_2026-11-19.md` and the candidate gate assessment.

Do not prepare a v0.2 acceptance JSON for Dishka, do not edit the eligibility validator, do not add it to the accepted registry, and do not count it toward the one-case feasibility minimum or the 15-project primary target. Preserve the source, test artifacts, hashes, Stage 2 result and Stage 3 technical record as engineering evidence. The exclusion does not mean the technical reproduction failed.

## 6. Candidate fallback rule

The first candidate is not privileged over the evidence. Dishka's prior pipeline/debug classification is now recorded as `some`, so it is excluded under the unchanged rule. The next candidate is **NumPyro #1916 / PR #1918**. If NumPyro's semantic tiers, prior-exposure eligibility, independence, documentary source/dependency license scope, timestamp provenance or acceptance record fail, do not relax the standard; preserve the evidence and proceed to the next Stage 2-passed candidate in the existing order.

## 7. Current state

- Dishka technical Stage 2: PASS.
- Dishka gold/tier decision: project-lead approval recorded.
- Dishka accepted registry state: **not accepted**.
- Active case registry: 0.
- Prior pipeline/debug exposure: confirmation pending.
- Bounded documentary license-screen scope: sign-off pending.
- Project-wide model/license/runtime/protocol/hash and Rater_B gates: still open.
- No model load, inference, fine-tuning or training performed.


## 8. NumPyro #1916 — next candidate handoff (19 November 2026)

- Upstream issue #1916 / fix PR #1918; dataset row `pyro-ppl__numpyro-1918`.
- Exact Stage 2 rerun: workflow run `44537219541`, NumPyro job `135605947673` completed successfully. Both frozen AIES and ESS selectors ran and met the exact buggy-base-fail/fixed-revision-pass contract.
- Latest 19 November artifact `14536697284` has GitHub-reported digest `88273ec9df2633d2d3a360e0f5c86188d92c5e87318e312a183bc77bf1071556`; independent local archive verification is not yet recorded for this newest artifact. The 18 November artifact remains independently archive-verified (ZIP CRC and 15/15 internal payload hashes passed).
- Real E1/E2/E3 packet-set SHA-256: `7156e7c0bebf694946495b638f8dd21fbe45b7fbafde2607e6cc11e8b4f9bdfc`.
- The exact real-packet structural test passed in the no-inference preflight at run `44537219541`, job `135605725983`. It asserts the external packet hash, strict nesting and exact tier additions; it also asserts that semantic sufficiency is not assessed and that no model inference occurred.
- The entire candidate workflow run concluded failure because Nox, Werkzeug and Moto candidate jobs failed their own selector contracts. The NumPyro job and no-inference preflight job themselves succeeded; do not report the full matrix as green.
- The main Stage 3 question remains open: do the two E1 source excerpts actually eliminate the plausible alternative that the ensemble sampler itself should support/map batched PRNG keys? Independent reviewers must be allowed to reject the proposed E1 tier if that alternative remains defensible.

### Reviewer eligibility boundary

The existing NumPyro Panel B protocol requires at least two independent, source-unexposed semantic reviewers who are disjoint from Panel A, the project lead and Panel Reviewer H. Reviewer H has already seen the design proposal and is explicitly ineligible for Panel B under the current protocol. Panel Reviewer B's eligibility is unknown until this reviewer completes the case-specific exposure/conflict declaration. Mahmut is the custodian and is not a blinded rater. If two eligible Panel B reviewers and a separate adjudicator cannot be appointed, keep the semantic tier review pending; do not substitute simple YES votes from people who have seen the design or code.

Panel A technical review is also separate: at least two source-aware reviewers must make independent mechanism/alternative assessments, with their initial records preserved. Reviewers cannot serve simultaneously as Panel A and Panel B for this case. Reviewer delivery must be restricted, randomized and access-logged; the public GitHub repository is not a controlled review channel.

**Next operational gate:** complete the reviewer exposure/role screen and confirm that the required independent human panel and restricted delivery route can actually be assembled. Only then prepare and deliver coded packet copies. No model load, inference or training is authorized.
