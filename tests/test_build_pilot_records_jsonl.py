import json

import pytest

from scripts.build_pilot_records_jsonl import build


def test_jsonl_export_requires_all_frozen_records(tmp_path):
    runs = tmp_path / "runs"
    runs.mkdir()
    (runs / "one.json").write_text('{"case_id":"one"}', encoding="utf-8")
    with pytest.raises(RuntimeError, match="exactly 30"):
        build(runs, tmp_path / "out.jsonl")


def test_jsonl_export_is_deterministic(tmp_path):
    runs = tmp_path / "runs"
    runs.mkdir()
    for i in range(30):
        (runs / f"{30-i:02d}.json").write_text(
            json.dumps({"index": i, "case_id": f"case-{i}"}),
            encoding="utf-8",
        )

    output = tmp_path / "out.jsonl"
    assert build(runs, output) == 30
    lines = output.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 30
    assert json.loads(lines[0])["index"] == 29
    assert json.loads(lines[-1])["index"] == 0
