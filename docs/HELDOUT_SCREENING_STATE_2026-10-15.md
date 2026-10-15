# Held-out red-green screening state — 2026-10-15

## Current evidence boundary

The screening run `38057613670` completed successfully on 2026-10-10. It executed all 12 then-current matrix cases; each job received a GitHub-hosted runner and completed 12 workflow steps. Those results are retained as technical-screening evidence for those exact case/revision/test combinations only.

On 2026-10-14, six additional candidates were added to the screening matrix with corrected first-parent / merge-commit revision pins. Those six are the only cases requiring new red-green evidence:

- `netty-17623-negative-search-domain-cache`
- `netty-17764-tls13-signature-algorithm-key-selection`
- `collections-724-indexed-collection-iterator-index-drift`
- `collections-720-synchronized-collection-foreach-lock`
- `lang-1795-fastdateformat-mutable-timezone-cache-leak`
- `compress-797-lz77-back-reference-window-bound`

Workflow run `38595283872` attempted 18 jobs (the 12 previously screened cases plus six new cases). Both its initial attempt and rerun ended before any job steps executed; the job metadata has no assigned runner and zero steps. This is not red-green evidence for any of the six new candidates.

## Workflow adjustment prepared

The active workflow matrix now contains only the six pending candidates. The 12 previously screened candidates were removed from the active matrix; their archived red-green artifacts and source audit remain the evidence for those exact revision/test combinations and must not be counted again as pending work.

A first draft attempted to use `matrix.screen_pending` in the job-level `if` condition. On 2026-10-15, that was caught in static review: GitHub Actions does not list the `matrix` context as available for `jobs.<job_id>.if`. The draft was corrected before opening a PR. The current workflow uses an explicit six-case matrix, no matrix-based job-level condition, and `max-parallel: 2` to limit concurrent build pressure. This is a source/configuration correction only; no runner-backed test has yet verified the revised workflow.

This adjustment does not make candidates eligible by itself and does not authorize model inference. A candidate still needs observed failure on its pinned pre-fix revision and a clean pass on its pinned fixed revision. Independent source review and adjudication remain separate required gates.

## Next operational gate

Before opening or running the prepared workflow change, resolve GitHub-hosted runner assignment for this private repository. Check repository Actions policy and account/organization billing usage limits. GitHub's public status page reported Actions operational during the incident review, but the available repository connector cannot inspect private billing settings. Do not make the repository public as a workaround and do not infer a specific billing cause without account evidence.
