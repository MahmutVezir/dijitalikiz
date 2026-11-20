# Project-lead technical gold decision — NumPyro #1916

- Upstream project: `pyro-ppl/numpyro`
- Issue: https://github.com/pyro-ppl/numpyro/issues/1916
- Fix PR: https://github.com/pyro-ppl/numpyro/pull/1918
- Dataset row: `pyro-ppl__numpyro-1918`
- Decision date: 20 November 2026
- Decision maker: student project lead
- Decision source: explicit approval in the ChatGPT conversation on 20 November 2026

## Decision

**APPROVED — source-aware technical gold mechanism.**

The project lead approved this exact statement:

> MCMC.run(), warmup sonrasında saklanan sampler durumundaki skaler PRNG anahtarını vektörleştirilmiş zincirler için oluşturulan anahtar dizisiyle değiştiriyor. EnsembleSampler.sample() ise bu alanı skaler kabul ederek random.split() çağırıyor. Hata, sampler durumundaki anahtar biçiminin bu iki aşama arasında tutarsız hale gelmesinden kaynaklanıyor.

## Decision scope

This decision approves the stated NumPyro #1916 root-cause mechanism as technical gold. It does not yet approve:
- E1/E2/E3 packet membership or semantic sufficiency;
- the competing-alternative disposition as a separate adjudication;
- the bounded documentary license-scope acknowledgement;
- the case-specific prior pipeline/debug exposure declaration;
- the complete schema-conformant case-acceptance record;
- fail-closed registry validation; or
- the separate final case-acceptance YES.

The proposed packet set remains a proposed packet set until the project lead separately decides whether each evidence level is sufficient and properly nested.

## Candidate-selection decision

The project lead also accepted the five strong first-batch candidates for continued v0.2 Stage 3 case evaluation: NumPyro #1916, Dymos #1166, EODAG #1530, Meltano SDK #3090 and PyFar #721. That is approval to continue candidate-specific acceptance work; it is not five final case acceptances.

## Adjudication and exposure boundary

The v0.2 Dishka-equivalent route applies: the project lead is the sole source-aware human adjudicator for technical gold and E1/E2/E3; ChatGPT is advisory only; Hasan may be described only as project-lead-reported supplementary source-aware input. The two-human requirement applies later to blinded raw model-output evidence-support scoring, not to source-aware gold/tier construction.

Researcher source exposure is disclosed separately from prior pipeline/debug-oracle exposure. The latter remains a candidate-specific factual declaration and is not inferred from the absence of a recorded prior-debug event.

## Current status

- Candidate selection: accepted for Stage 3 case evaluation.
- Technical gold mechanism: **approved by project lead**.
- E1/E2/E3 membership and sufficiency: pending.
- Prior pipeline/debug exposure declaration: pending.
- Bounded license-scope acknowledgement: pending.
- Final case acceptance: **not accepted yet**.
- Model loading/inference/fine-tuning/training: not authorized.
