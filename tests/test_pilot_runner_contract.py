import inspect

import pytest

from scripts import run_pilot


def test_generate_requires_frozen_system_prompt():
    parameters = inspect.signature(run_pilot.generate).parameters
    assert "system_prompt" in parameters
    assert parameters["system_prompt"].default is inspect.Parameter.empty


def test_frozen_prompt_paths_exist():
    assert run_pilot.PROMPT_TEMPLATE.is_file()
    assert run_pilot.SYSTEM_PROMPT.is_file()
    assert run_pilot.MANIFEST.is_file()


def test_runner_defaults_to_fail_closed_when_records_exist(tmp_path, monkeypatch):
    manifest = {
        "status": "model_frozen",
        "cases": ["case"],
        "conditions": ["standard", "ccdg"],
        "replications": 1,
        "generation": {"seeds": [42], "temperature": 0.2, "top_p": 1, "do_sample": True, "max_new_tokens": 16},
        "model": {"model_id": "model", "revision": "revision"},
        "prompt": {"path": "prompt.txt", "sha256": ""},
        "system_prompt": {"path": "system.txt", "sha256": ""},
    }
    monkeypatch.setattr(run_pilot, "MANIFEST", tmp_path / "manifest.json")
    monkeypatch.setattr(run_pilot, "PROMPT_TEMPLATE", tmp_path / "prompt.txt")
    monkeypatch.setattr(run_pilot, "SYSTEM_PROMPT", tmp_path / "system.txt")
    run_pilot.MANIFEST.write_text(__import__("json").dumps(manifest), encoding="utf-8")
    run_pilot.PROMPT_TEMPLATE.write_text("prompt", encoding="utf-8")
    run_pilot.SYSTEM_PROMPT.write_text("system", encoding="utf-8")
    import hashlib
    manifest["prompt"]["sha256"] = hashlib.sha256(b"prompt").hexdigest()
    manifest["system_prompt"]["sha256"] = hashlib.sha256(b"system").hexdigest()
    run_pilot.MANIFEST.write_text(__import__("json").dumps(manifest), encoding="utf-8")
    output_dir = tmp_path / "runs"
    output_dir.mkdir()
    (output_dir / "case__standard__seed42.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["run_pilot.py", "--output-dir", str(output_dir)])
    with pytest.raises(RuntimeError, match="already exist"):
        run_pilot.main()


def test_frozen_runtime_versions_are_declared_in_manifest():
    import json

    manifest = json.loads(run_pilot.MANIFEST.read_text(encoding="utf-8"))
    runtime = manifest["runtime"]
    assert runtime["python"] == "3.11"
    assert runtime["torch"] == "2.2.1"
    assert runtime["transformers"] == "4.43.2"
    assert runtime["accelerate"] == "0.33.0"
    assert runtime["optimum"] == "1.17.1"
    assert runtime["auto_gptq"] == "0.7.1"
    assert runtime["peft"] == "0.11.1"
    assert runtime["numpy"] == "1.26.4"
    assert runtime["datasets"] == "2.21.0"
    assert runtime["pyarrow"] == "15.0.2"
    assert runtime["fsspec"] == "2024.6.1"
    requirements = __import__("pathlib").Path("requirements-pilot.txt").read_text(encoding="utf-8")
    for package, version in (
        ("numpy", runtime["numpy"]),
        ("datasets", runtime["datasets"]),
        ("pyarrow", runtime["pyarrow"]),
        ("fsspec", runtime["fsspec"]),
    ):
        assert f"{package}=={version}" in requirements
