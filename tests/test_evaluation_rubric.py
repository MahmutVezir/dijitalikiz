import json
from pathlib import Path

from dijitalikiz.models import DiagnosticOutput
from scripts.evaluate_confirmatory import root_cause_alias_match, normalize_phrase


ROOT = Path(__file__).resolve().parents[1]


def test_rubric_covers_manifest_cases_in_fixed_order():
    manifest = json.loads((ROOT / "data" / "benchmark" / "benchmark_manifest.json").read_text(encoding="utf-8"))
    rubric = json.loads((ROOT / "data" / "benchmark" / "evaluation_rubric.json").read_text(encoding="utf-8"))
    assert [item["case_id"] for item in rubric["cases"]] == manifest["case_ids"]
    assert all(item["root_cause_aliases"] for item in rubric["cases"])


def test_alias_match_normalizes_punctuation_underscores_and_case():
    output = DiagnosticOutput(
        diagnosed_component="Component",
        root_cause_class="",
        affected_entity="Entity",
        explanation="The root cause is INTEGER_OVERFLOW in squared-distance accumulator.",
    )
    assert root_cause_alias_match(output, ["integer overflow in squared distance accumulator"])


def test_alias_match_is_a_contiguous_phrase_not_a_token_bag():
    output = DiagnosticOutput(
        diagnosed_component="Component",
        root_cause_class="",
        affected_entity="Entity",
        explanation="Integer accumulation is used, but it does not explain how the distance overflows.",
    )
    assert not root_cause_alias_match(output, ["integer overflow in squared distance accumulator"])


def test_normalizer_has_deterministic_ascii_tokenization():
    assert normalize_phrase("A_B/c-D") == "a b c d"
