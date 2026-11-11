# Canonical repository and evidence policy

## Single source of truth

`MahmutVezir/dijitalikiz` is the only canonical repository for project-authored code, notebooks, experiment protocols, review tools, test specifications, metadata, and evidence indexes. Development branches and pull requests must be created inside this repository. Do not create project forks, duplicate project repositories, or standalone gists as alternate sources of truth.

## Upstream dependencies

The experiment uses BugsInPy and upstream software projects as external research material. Workflows must fetch these repositories at the exact pinned commit IDs recorded in the cohort and case manifests. This is not a second project repository. Do not copy whole upstream codebases or fixed patches into this repository until license and redistribution terms have been checked and recorded.

## Case provenance

Each candidate case must have a stable ID, upstream repository URL, pinned BugsInPy metadata revision, buggy and fixed commit IDs, Python version, target test command, metadata hashes, technical outcome, and evidence artifact ID/digest. Case acceptance is a separate human-reviewed decision. A technical signal must never automatically add a case to the confirmatory registry.

## Durable evidence

Commit the metadata-only selection freeze and evidence index to this repository. GitHub Actions artifacts are temporary and must not be treated as long-term storage. Retention should be set to 90 days for new runs where the repository policy permits it, while the committed index remains the durable provenance ledger. Do not claim a raw file is permanently stored unless it is actually committed and retrievable from this repository.

## Research safety gates

Keep `accepted_for_confirmatory=false` and `llm_inference_performed=false` until license review, two-reviewer ground-truth review, evidence-tier review, leakage/prior-exposure review, and protocol/hash freeze are complete. Never silently replace failed or blocked candidates after observing their outcome.
