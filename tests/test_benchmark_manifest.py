from scripts.validate_benchmark_manifest import validate_manifest


def test_draft_manifest_can_be_empty():
    assert validate_manifest({
        "status": "draft",
        "case_ids": [],
        "pilot_case_ids": ["pilot-a"],
    }) == []


def test_pilot_overlap_is_rejected():
    errors = validate_manifest({
        "status": "draft",
        "case_ids": ["pilot-a"],
        "pilot_case_ids": ["pilot-a"],
    })
    assert any("overlap" in error for error in errors)


def test_frozen_manifest_requires_power_assumption():
    errors = validate_manifest({
        "status": "frozen",
        "case_ids": ["main-a"],
        "pilot_case_ids": ["pilot-a"],
    })
    assert any("power_assumption" in error for error in errors)


def test_frozen_manifest_accepts_complete_power_assumption():
    errors = validate_manifest({
        "status": "frozen",
        "case_ids": ["main-a"],
        "pilot_case_ids": ["pilot-a"],
        "power_assumption": {
            "p_standard_only": 0.10,
            "p_ccdg_only": 0.30,
            "target_power": 0.80,
            "alpha": 0.05,
        },
    })
    assert errors == []
