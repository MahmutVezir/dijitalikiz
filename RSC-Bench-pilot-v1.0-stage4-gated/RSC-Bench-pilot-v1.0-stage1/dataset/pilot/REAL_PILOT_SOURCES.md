# RSC-Bench Real Pilot Sources

These four public cases are **pilot-only**. They are permanently excluded from the main RSC-Bench dataset.

Selection rule: public technical case, reproducible/inspectable symptom, explicit or independently traceable root-cause evidence, and cross-component dependency structure.

1. RSC-PILOT-REAL-001 — Supabase issue #35459 — JWT generator/runtime signature mismatch.
2. RSC-PILOT-REAL-002 — Supabase issue #47835 — Studio proxy/runtime error-response contract mismatch.
3. RSC-PILOT-REAL-003 — Supabase discussion #40671 — Supavisor zombie client-handler connection leak.
4. RSC-PILOT-REAL-004 — Supabase Storage issue #1109 — S3 CopyObject metadata directive omission.

No secrets, tokens, passwords, project identifiers, or personal data from the sources are copied into the dataset.

Important: the `I_base` records preserve the observed problem and diagnostic constraints but do not copy the source's final root-cause sentence into the model-facing case. The confirmed root cause is stored separately in `ground_truth.jsonl` with source evidence.
