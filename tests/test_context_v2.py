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
        assert "=== Software Debugging Context ===" in rendered
        assert "Standard Context v2" not in rendered
        assert "CCDG Context v2" not in rendered
        assert "Dependency-Enriched Prose Context v2" not in rendered
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
    assert "Dependency relations in sentences:" not in standard
    assert "Dependency relations as directed triples:" not in standard
    assert "Dependency relations in sentences:" in prose
    assert "Dependency relations as directed triples:" in graph


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

def test_v2_conditions_share_revision_bound_software_twin_snapshot():
    case_path = ROOT / "data" / "benchmark" / "cases" / "commons-math-defects4j-MATH-305.json"
    payload = json.loads(case_path.read_text(encoding="utf-8"))
    snapshot = {
        "repository_url": "https://github.com/example/project",
        "snapshot_revision": "a" * 40,
        "regression_test": "ExampleRegressionTest#failsOnPreFixRevision",
        "observed_failure_signal": "The regression assertion failed on the pinned snapshot revision.",
    }
    payload["software_twin_snapshot"] = snapshot
    case = ResearchCase.from_dict(payload)

    contexts = [
        render_standard_context_v2(case),
        render_dependency_prose_context_v2(case),
        render_ccdg_context_v2(case),
    ]
    required_lines = [
        "Version-bound software-system twin snapshot:",
        f"Repository: {snapshot['repository_url']}",
        f"Observed code revision: {snapshot['snapshot_revision']}",
        f"Regression test: {snapshot['regression_test']}",
        f"Observed failure signal: {snapshot['observed_failure_signal']}",
    ]
    for rendered in contexts:
        for line in required_lines:
            assert line in rendered
        assert "fixed_revision" not in rendered
        assert "ground_truth" not in rendered.lower()

