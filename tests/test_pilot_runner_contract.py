import inspect

from scripts import run_pilot


def test_generate_requires_frozen_system_prompt():
    parameters = inspect.signature(run_pilot.generate).parameters
    assert "system_prompt" in parameters
    assert parameters["system_prompt"].default is inspect.Parameter.empty


def test_frozen_prompt_paths_exist():
    assert run_pilot.PROMPT_TEMPLATE.is_file()
    assert run_pilot.SYSTEM_PROMPT.is_file()
    assert run_pilot.MANIFEST.is_file()
