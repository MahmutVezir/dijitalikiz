import json
from pathlib import Path
import tempfile

import pytest

from dijitalikiz.pilot_config import (
    expected_pilot_record_count,
    expected_pilot_run_filenames,
)
from scripts.build_pilot_records_jsonl import build


MANIFEST_PATH = Path("data/pilot/pilot_manifest.json")


def test_jsonl_export_requires_all_frozen_records(tmp_path):
    runs = tmp_path / "runs"
    runs.mkdir()
    (runs / "one.json").write_text('{"case_id":"one"}', encoding="utf-8")
    with pytest.raises(RuntimeError, match="run-file set mismatch"):
        build(runs, tmp_path / "out.jsonl")


def test_jsonl_export_is_deterministic(tmp_path):
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected_count = expected_pilot_record_count(manifest, require_declared=True)
    expected_names = sorted(
        expected_pilot_run_filenames(manifest, require_declared=True)
    )
    runs = tmp_path / "runs"
    runs.mkdir()

    for index, name in enumerate(expected_names):
        (runs / name).write_text(
            json.dumps({"index": expected_count - index - 1, "case_id": name}),
            encoding="utf-8",
        )

    output = tmp_path / "out.jsonl"
    assert build(runs, output, MANIFEST_PATH) == expected_count
    lines = output.read_text(encoding="utf-8").splitlines()
    assert len(lines) == expected_count
    assert json.loads(lines[0])["index"] == expected_count - 1
    assert json.loads(lines[-1])["index"] == 0
