from __future__ import annotations
import json
from typing import Any

def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def canonical_text(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n").strip()
