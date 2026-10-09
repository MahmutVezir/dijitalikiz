from pathlib import Path

from scripts import model_load_preflight


def test_model_load_preflight_is_present():
    assert Path(model_load_preflight.__file__).is_file()


def test_preflight_checks_weight_integrity_and_sampled_generation():
    source = Path(model_load_preflight.__file__).read_text(encoding="utf-8")
    assert "output_loading_info=True" in source
    assert '"checkpoint_weights_match_model"' in source
    assert '"smoke_logits_finite"' in source
    assert '"pilot_sampling_smoke"' in source
    assert "do_sample=bool(generation[\"do_sample\"])" in source
