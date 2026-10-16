from pathlib import Path

from scripts import compatibility_gate, model_load_preflight


def test_model_load_preflight_is_present():
    assert Path(model_load_preflight.__file__).is_file()


def test_model_load_preflight_rejects_unverified_compatibility_receipts():
    source = Path(model_load_preflight.__file__).read_text(encoding="utf-8")
    required_receipt_checks = (
        'report.get("status") == "pass"',
        'report.get("pilot_authorized") is True',
        'report.get("model_id") == manifest.get("model", {}).get("model_id")',
        'report.get("model_revision") == manifest.get("model", {}).get("revision")',
        'report.get("expected_records") == manifest.get("expected_records")',
        'all(item.get("status") == "pass" for item in report["checks"])',
    )
    for fragment in required_receipt_checks:
        assert fragment in source, f"receipt check missing: {fragment}"


def test_compatibility_gate_checks_weight_integrity_and_sampled_generation():
    source = Path(compatibility_gate.__file__).read_text(encoding="utf-8")
    required_gate_checks = (
        "output_loading_info=True",
        '"checkpoint_weights_match_model"',
        '"smoke_logits_finite"',
        '"pilot_sampling_smoke"',
        'torch.isfinite(logits).all()',
        'do_sample=bool(generation["do_sample"])',
        '"temperature": float(generation["temperature"])',
        '"top_p": float(generation["top_p"])',
        "random.seed(smoke_seed)",
    )
    for fragment in required_gate_checks:
        assert fragment in source, f"compatibility check missing: {fragment}"
