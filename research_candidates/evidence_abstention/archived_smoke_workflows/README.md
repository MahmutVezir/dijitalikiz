# Archived one-off Kaggle smoke workflows

The `.yml.disabled` files in this directory are historical source snapshots of one-off engineering smoke workflows. Their corresponding completed runs and generated artifacts are linked below. They are intentionally **not located in `.github/workflows/`** and cannot be triggered by GitHub Actions from this directory.

- E1 Ansible-4 smoke: [run 39837255019](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39837255019), artifact ID `12452505143`.
- Earlier four-case Qwen smoke workflow: `qwen-uncertainty-smoke-kaggle.yml.disabled`; its four candidate cases were previously exposed and are permanently excluded from confirmatory sampling.

A machine-readable outcome/hash record is available at [KAGGLE_SMOKE_AUDIT_2026-10-22.json](../KAGGLE_SMOKE_AUDIT_2026-10-22.json).

The E1 Ansible-4 workflow used a previously exposed case and placed the complete patch plus the successful fixed-test output in the model prompt. It is therefore an engineering-pipeline check, not an implementation of the frozen confirmatory evidence-packet protocol. See [the smoke audit](../../../docs/EVIDENCE_ABSTENTION_KAGGLE_SMOKE_AUDIT_2026-10-22.md).

These source files are preserved so the historical run can be inspected. They must not be copied back into `.github/workflows/` or run again without a separately reviewed change to the research plan and all applicable study gates. Keep the canonical `kaggle-pilot.yml` as the sole workflow capable of starting a Kaggle kernel.
