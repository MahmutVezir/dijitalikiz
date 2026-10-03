from __future__ import annotations
import json
from pathlib import Path
from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

def read_jsonl(path: Path, model: type[T]) -> list[T]:
    records: list[T] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if line.strip():
                try:
                    records.append(model.model_validate(json.loads(line)))
                except Exception as exc:
                    raise ValueError(f"Invalid JSONL record at {path}:{line_number}") from exc
    return records

def append_jsonl(path: Path, value: BaseModel) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(value.model_dump_json() + "\n")

def parse_model_output(raw_text: str, model: type[T]) -> T:
    """Parse one JSON model response and reject non-JSON/non-schema output."""
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError("Model response is not valid JSON.") from exc
    if not isinstance(payload, dict):
        raise ValueError("Model response must be a JSON object.")
    return model.model_validate(payload)
