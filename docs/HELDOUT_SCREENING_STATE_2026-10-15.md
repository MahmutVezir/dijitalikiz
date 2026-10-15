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


## Runner assignment recheck — 2026-10-15 19:11 UTC

The latest main-branch validation is run [38791276730](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38791276730), on commit `9796cfb2db80296aa50f5705ad7e7dcf5a212ca6`. Its only job is `116616155516` and failed in approximately three seconds. The available job record reports `runner_id=0`, empty `runner_name`, and `steps=[]`. Downloading its job logs returns `BlobNotFound`; the step-list endpoint is empty. Therefore no checkout, test, or project command is evidenced as having run. This is **not a pytest failure**, and it is not evidence that the test suite passed.

A minimal no-secret runner smoke workflow was also rerun as attempt 2 of run [38779073729](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38779073729); it failed with no job steps and no retrievable logs. The pattern across the minimal smoke workflow and the project validation workflow points to a pre-step job-dispatch/allocation failure rather than a demonstrated project-code failure, but the exact cause is not identified.

GitHub's public status page showed Actions operational and no incident reported for 2026-10-15 at the time of review: https://www.githubstatus.com/ . That does not rule out an account-, repository-, billing-, or policy-specific problem. The connected repository integration can read repository/run/job data, but it cannot inspect the private account's billing usage or the repository Actions settings. Do not state that those settings were checked.

### Required account-side check

The repository owner should inspect **Repository → Settings → Actions → General** to confirm Actions are enabled and the workflow policies allow this workflow, then inspect the GitHub **Billing and plans / Usage** page for Actions minutes and payment/usage restrictions. GitHub documents that private repositories use plan-dependent included hosted-runner minutes, and when a free quota is exhausted without a valid payment method, use can be blocked. This is a plausible check, not a confirmed diagnosis: https://docs.github.com/en/billing/concepts/product-billing/github-actions . Do not make the repository public as a workaround. If usage and policy appear normal, report the two run IDs and job IDs to GitHub Support.

Until a hosted runner actually starts steps, do not mark the complete repository test suite as passed. Continue local artifact checks and independent reviewer handoff, keeping them separate from CI status.

## PR #26 disposition

PR #26 was closed as superseded on 2026-10-15, not merged. Comparing its workflow with main showed that all six active candidate IDs, pinned pre-fix/fixed revisions, test targets, and test files are already present identically on main. The PR branch was 72 commits behind main and also reintroduced the workflow-file path filter that main deliberately removed to avoid automatically starting six long Java builds on every workflow-file edit. The closure comment records this comparison. The six candidates still need new red-green evidence; closing the duplicate PR does not make them eligible.
