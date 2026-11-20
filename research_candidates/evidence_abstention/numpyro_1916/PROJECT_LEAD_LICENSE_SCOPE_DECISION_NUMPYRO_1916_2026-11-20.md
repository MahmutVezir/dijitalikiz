# Project-lead license-scope decision — NumPyro #1916

- Upstream project: `pyro-ppl/numpyro`
- Issue: https://github.com/pyro-ppl/numpyro/issues/1916
- Fix PR: https://github.com/pyro-ppl/numpyro/pull/1918
- Dataset row: `pyro-ppl__numpyro-1918`
- Decision date: 20 November 2026
- Decision maker: student project lead
- Decision source: explicit response in the ChatGPT conversation on 20 November 2026

## Decision

**DECLINED — the proposed bounded documentary research-use scope is not approved.**

The project lead explicitly rejected the proposed scope to:
1. reproduce the two frozen AIES/ESS upstream selectors in an isolated CPU-only environment; and
2. quote minimal source-code snippets in an academic report with attribution and immutable source links,
while excluding redistribution of the installed environment, package wheels, complete upstream source, and dataset Parquet pending further review.

The rejection applies to that exact proposal. No narrower or alternative use permission is inferred from this decision.

## Effect on the candidate

- Do not treat the current documentary license inventory as project-lead approval for the proposed use.
- Do not advance NumPyro #1916 to a proposed/accepted case record or insert it into the accepted-case registry under this declined scope.
- Preserve the already-created Stage 2 reproduction outputs as historical technical audit evidence only; this decision does not convert those technical results into an approved study-use permission.
- Any future proposal must define a materially different scope, authenticate the dataset-card license at the exact pinned dataset revision, resolve applicable dependency and bundled-library notices, and receive a new explicit project-lead decision before further candidate use.
- The technical gold and E1/E2/E3 decisions remain historical source-aware technical decisions; they do not override this license-scope refusal.

## Decision boundaries

This is a project governance decision, not a legal opinion. It does not claim that the underlying upstream code or dataset is categorically unusable under all possible permissions. It records that the project lead does not approve the exact scope proposed in the current review.

**Final case acceptance: NOT ACCEPTED.** Model loading, inference, fine-tuning and training remain unauthorized.
