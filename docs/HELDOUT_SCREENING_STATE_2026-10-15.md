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

## Workflow adjustment committed on main

The active workflow matrix now contains only the six pending candidates. The 12 previously screened candidates were removed from the active matrix; their archived red-green artifacts and source audit remain the evidence for those exact revision/test combinations and are not counted as pending work.

A first draft used `matrix.screen_pending` in a job-level `if` condition. Static review caught that GitHub Actions does not expose the `matrix` context to `jobs.<job_id>.if`; the condition was removed and the workflow now uses an explicit six-case matrix. Concurrent builds are limited to two with `max-parallel: 2`.

The `pull_request.paths` filter now watches the dedicated trigger marker, not workflow-file edits. This avoids automatically launching six long Java builds when workflow configuration changes; the workflow remains manually dispatchable. This commit is a static configuration correction only. It does not claim that any of the six candidates have red-green evidence, and it does not authorize model inference.

A candidate still requires an observed failure on its pinned pre-fix revision and a clean pass on its pinned fixed revision. Independent source review and adjudication remain separate required gates.

## Next operational gate

Before opening or running the prepared workflow change, resolve GitHub-hosted runner assignment for this private repository. Check repository Actions policy and account/organization billing usage limits. GitHub's public status page reported Actions operational during the incident review, but the available repository connector cannot inspect private billing settings. Do not make the repository public as a workaround and do not infer a specific billing cause without account evidence.
