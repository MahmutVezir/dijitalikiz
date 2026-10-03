from __future__ import annotations

import os
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    cfg = yaml.safe_load((ROOT / "configs/model.yaml").read_text(encoding="utf-8"))
    model_id = (cfg.get("model_id") or "").strip()
    blockers: list[str] = []

    if not model_id or model_id == "REPLACE_ME_EXACT_MODEL_ID":
        blockers.append("configs/model.yaml içinde exact fixed model_id belirlenmemiş.")
    if not os.getenv("OPENAI_API_KEY"):
        blockers.append("OPENAI_API_KEY execution environment içinde yok.")
    if not (ROOT / "outputs/real_pilot_runs.jsonl").exists():
        blockers.append("outputs/real_pilot_runs.jsonl bulunamadı; gerçek model pilotu tamamlanmamış.")

    if blockers:
        print("Prompt freeze READY değil.")
        for blocker in blockers:
            print(f"- {blocker}")
        return 1

    print("Prompt freeze için teknik ön koşullar mevcut. Son protokol kontrolünden sonra freeze uygulanabilir.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
