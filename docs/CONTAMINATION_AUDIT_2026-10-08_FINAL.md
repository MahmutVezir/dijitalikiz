# Final Pilot Contamination Exposure Audit — 2026-10-08

Scope: all five Apache Commons Math candidates reviewed before pilot inference.

| Case | Public evidence checked | Risk | Interpretation |
|---|---|---|---|
| MATH-927 | Apache JIRA, Defects4J mapping, public academic reproduction | high | Exact case/fix is publicly exposed; not proof of training inclusion. |
| MATH-950 | Apache JIRA, Defects4J mapping, earlier indexed audit | medium | Original public issue is exposed; no additional indexed training-like reproduction was found in the earlier audit. |
| MATH-938 | Apache JIRA, Defects4J mapping, indexed research reproduction | high | Exact case/fix is publicly exposed; not proof of training inclusion. |
| MATH-949 | Apache JIRA, Defects4J mapping, public Apache Git history | high | Exact case/fix is publicly exposed; not proof of training inclusion. |
| MATH-988 | Apache JIRA, Defects4J mapping, indexed research reproduction | high | Exact case/fix is publicly exposed; not proof of training inclusion. |

## Policy

These are exposure-risk labels only. No model output was consulted for case selection and no label is evidence of training-set membership.

## Final selection

Included: MATH-927, MATH-950, MATH-949, MATH-988.
Excluded: MATH-938.
