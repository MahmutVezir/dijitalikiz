import json
from pathlib import Path

from dijitalikiz.context_v2 import (
    render_ccdg_context_v2,
    render_dependency_prose_context_v2,
    render_standard_context_v2,
)
from dijitalikiz.models import ResearchCase


ROOT = Path(__file__).resolve().parents[1]


def load_case(case_id: str) -> ResearchCase:
    path = ROOT / "data" / "benchmark" / "cases" / f"{case_id}.json"
    return ResearchCase.from_dict(json.loads(path.read_text(encoding="utf-8")))


def test_all_v2_conditions_preserve_source_technology_error_and_base_facts():
    case = load_case("commons-math-defects4j-MATH-305")
    contexts = [
        render_standard_context_v2(case),
        render_dependency_prose_context_v2(case),
        render_ccdg_context_v2(case),
    ]
    for rendered in contexts:
        assert case.source in rendered
        assert case.technology in rendered
        assert case.error_description in rendered
        for fact in case.i_base:
            assert fact in rendered


def test_prose_and_ccdg_arms_preserve_every_same_dependency_edge_field():
    case = load_case("commons-math-defects4j-MATH-305")
    prose = render_dependency_prose_context_v2(case)
    graph = render_ccdg_context_v2(case)
    for edge in case.ccdg:
        assert edge.source in prose and edge.source in graph
        assert edge.target in prose and edge.target in graph
        assert edge.relation.replace("_", " ") in prose
        assert edge.relation in graph
        if edge.details:
            assert edge.details in prose and edge.details in graph


def test_standard_v2_is_baseline_while_augmented_arms_explicitly_include_edges():
    case = load_case("commons-math-defects4j-MATH-305")
    standard = render_standard_context_v2(case)
    prose = render_dependency_prose_context_v2(case)
    graph = render_ccdg_context_v2(case)
    assert "Dependency facts (prose):" not in standard
    assert "Dependencies (CCDG triples):" not in standard
    assert "Dependency facts (prose):" in prose
    assert "Dependencies (CCDG triples):" in graph


def test_v2_contexts_do_not_expose_ground_truth_labels():
    case = load_case("closure-compiler-defects4j-CLOSURE-14")
    contexts = [
        render_standard_context_v2(case),
        render_dependency_prose_context_v2(case),
        render_ccdg_context_v2(case),
    ]
    for rendered in contexts:
        assert "Ground truth:" not in rendered
        assert case.ground_truth.root_cause not in rendered
