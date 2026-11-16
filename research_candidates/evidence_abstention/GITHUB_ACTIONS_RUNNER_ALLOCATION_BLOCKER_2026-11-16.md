# GitHub-hosted runner allocation blocker — no-inference evidence workflows

**Incident window:** 2026-11-16, approximately 15:38–16:34 UTC  
**Repository:** `MahmutVezir/dijitalikiz`  
**Affected candidate workflow:** `Evidence Abstention Preflight (No Inference)`  
**Decision:** infrastructure blocked; no candidate technical result is inferred from these runs.

## 1. Independent runner smoke test

The repository's no-secret `Runner Smoke Test (No Secrets)` workflow was deliberately triggered by a pull-request-only comment change to `.github/workflows/runner-smoke.yml`. It contains one step that prints runner OS/architecture and sentinel strings; it does not checkout code, install dependencies, read secrets, or execute candidate tests.

- Workflow run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/43908725261
- Job: `133444501890`, “Verify hosted runner assignment”
- Attempt 1: `completed / failure`, `runner_id=0`, empty `runner_name`, `steps=[]`, no `logs_url`
- Targeted rerun: attempt 2, queued at `2026-11-16T16:33:51Z`, then completed/failure at `16:33:53Z`; again `runner_id=0`, empty `runner_name`, `steps=[]`
- GitHub job API returned labels `["ubuntu-24.04"]` and no runner assignment.

This independently shows that a minimal no-secret workflow cannot obtain a GitHub-hosted runner. It is not a failure of Python, package installation, source checkout, or a candidate regression test.

## 2. Research preflight corroboration

The latest full preflight run during this incident:

- Run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/43908181500
- All 13 jobs ended with `failure` and no executable steps or logs, including:
  `no-inference-preflight`, Dishka, Nox, Earthkit-data, Moto, Robocop, Werkzeug, NumPyro, PyFar, Qutip, Meltano, Amaranth, and Python-control.
- Each job returned `steps=null` or an empty step list and no log URL.
- No reproduction artifacts were produced.

Earlier complete run `43881610067` did start hosted runners and produced candidate-specific evidence. Its results remain candidate-specific and must not be overwritten by these later runner failures.

## 3. What is and is not established

**Established:** at the time of the diagnostic, GitHub Actions created the workflow run and jobs, but the hosted-runner service assigned no runner to the jobs. The one-step runner smoke job reproduced this independently on ubuntu-24.04.

**Not established:** the underlying account-level or GitHub platform reason (for example, minute quota, policy, service incident, or another scheduler condition). The job API and logs expose no runner-side diagnostic, so do not state a specific cause without new evidence.

**Candidate consequence:** the current no-run attempts provide no base-fail/fixed-pass outcome. Mark candidates as `blocked_runner_allocation` or retain the prior candidate-specific result. Do not mark them as technical failures, passes, or exclusions on this basis.

## 4. Workflow trigger hygiene

The preflight previously triggered on every change under `research_candidates/evidence_abstention/**`. That caused documentation-only commits to fan out into all candidate jobs. The trigger has now been narrowed to implementation code, candidate reproducer tests, environment lock files, the case registry/schema, validation scripts/tests, and the workflow file itself.

This reduces unnecessary runs during evidence documentation. It does not alter any candidate acceptance rule or skip source/test changes.

## 5. Safe continuation rule

Do not repeatedly fan out the full candidate workflow while the no-secret runner smoke test cannot allocate a runner. Preserve the old successful candidate artifacts, finish static review and evidence-tier preparation where Stage 2 evidence exists, and resume actual base/fix test pairs only after a later runner smoke test shows at least one executed step and raw logs are available.

No model loading, inference, scoring, or training is performed or authorized by this diagnostic.
