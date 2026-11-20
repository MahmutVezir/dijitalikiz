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


## Automated post-decision workflow event — 20 November 2026

A repository push immediately after this refusal triggered the pre-existing pull-request path filter for the NumPyro independent-reproducer workflow. The run had already started before it was identified as an automated post-decision execution; the available GitHub action controls in this session did not expose a cancellation operation.

- Workflow run: [44768193233](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44768193233), job `136398408189`, conclusion `success`.
- The workflow again executed the exact public-API reproducer: the pinned buggy base produced the expected JAX key-array shape `(100, 2)` failure; the identical test passed on the pinned fixed revision (`1 passed in 4.02s`).
- Artifact: `14645873400`, GitHub-reported ZIP digest `e595e5c8ce6e777f84fef1e3ab74d7dd1b3263ff43b7c915880711e4d189f51a`. No independent local re-download/hash verification is claimed.

This automatic CI event does **not** reverse the project-lead refusal, approve the declined scope, or create a case acceptance. Its output is retained only as an operational trace of the already-triggered workflow and is not used to advance NumPyro in the exploratory case registry. The independent-reproducer workflow has now been changed to manual-only with an explicit scope-approval input defaulting to `not-approved`; no new run should occur unless a separate future scope decision is recorded and the manual gate is explicitly satisfied.

**Decision unchanged: DECLINED. NumPyro #1916 remains not accepted.**
