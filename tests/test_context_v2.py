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

def test_v2_conditions_do_not_render_provenance_snapshot_or_answer_cues():
    case_path = ROOT / "data" / "benchmark" / "cases" / "commons-math-defects4j-MATH-305.json"
    payload = json.loads(case_path.read_text(encoding="utf-8"))
    snapshot = {
        "repository_url": "https://example.invalid/provenance-only-repository",
        "snapshot_revision": "a" * 40,
        "regression_test": "ExampleRegressionTest#revealsTheMissingPaxHeaderSizeLimit",
        "observed_failure_signal": "PROVENANCE_ONLY_FAILURE_SIGNAL_SENTINEL_6D8F",
    }
    payload["software_twin_snapshot"] = snapshot
    case = ResearchCase.from_dict(payload)

    contexts = [
        render_standard_context_v2(case),
        render_dependency_prose_context_v2(case),
        render_ccdg_context_v2(case),
    ]
    for rendered in contexts:
        assert "Version-bound software-system twin snapshot:" not in rendered
        for value in snapshot.values():
            assert value not in rendered
        assert "Regression test:" not in rendered
        assert "Observed code revision:" not in rendered
        assert "ground_truth" not in rendered.lower()




def test_v2_base_context_is_byte_identical_across_all_conditions():
    case = load_case("commons-math-defects4j-MATH-305")
    standard = render_standard_context_v2(case)
    prose = render_dependency_prose_context_v2(case)
    graph = render_ccdg_context_v2(case)

    assert prose.startswith(standard + "\n\nDependency relations in sentences:\n")
    assert graph.startswith(standard + "\n\nDependency relations as directed triples:\n")


def test_prose_and_triples_render_exactly_the_same_ordered_edge_ledger():
    case = load_case("commons-math-defects4j-MATH-305")
    prose = render_dependency_prose_context_v2(case).splitlines()
    graph = render_ccdg_context_v2(case).splitlines()

    prose_start = prose.index("Dependency relations in sentences:") + 1
    graph_start = graph.index("Dependency relations as directed triples:") + 1
    prose_edges = prose[prose_start:]
    graph_edges = graph[graph_start:]

    expected_prose = []
    expected_graph = []
    edge_signatures = []
    for edge in case.ccdg:
        relation = edge.relation.replace("_", " ")
        sentence = f"{edge.source} has the dependency relation '{relation}' to {edge.target}."
        if edge.details:
            sentence += f" Detail: {edge.details}"
        expected_prose.append(f"- {sentence}")

        detail_suffix = f" (details: {edge.details})" if edge.details else ""
        expected_graph.append(
            f"- ({edge.source}) --[{edge.relation}]--> ({edge.target}){detail_suffix}"
        )
        edge_signatures.append((edge.source, edge.relation, edge.target, edge.details))

    assert len(edge_signatures) == len(set(edge_signatures)), "Fixture contains duplicate dependency edges"
    assert prose_edges == expected_prose
    assert graph_edges == expected_graph
    assert len(prose_edges) == len(graph_edges) == len(case.ccdg)


def test_parity_contract_is_valid_and_fails_closed():
    contract_path = ROOT / "data" / "followup_v2" / "context_parity_contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    assert contract["status"] == "draft_not_frozen"
    assert contract["model_inference_permitted"] is False
    assert contract["primary_contrast"] == ["C", "B"]
    assert contract["base_fields_equal_in_all_conditions"] == [
        "source_description", "technology", "error_description", "I_base"
    ]
    assert contract["context_limit"] == 32768
    assert contract["generation_reserve"] == 256
    assert contract["historical_artifacts_immutable"] is True



def test_v2_contexts_do_not_leak_case_identity_source_url_or_gold_fields():
    payload = json.loads(
        (ROOT / "data" / "benchmark" / "cases" / "commons-math-defects4j-MATH-305.json")
        .read_text(encoding="utf-8")
    )
    payload["case_id"] = "CASE_ID_CANARY_V2_794D"
    payload["source_url"] = "https://example.invalid/SOURCE_URL_CANARY_V2_794D"
    payload["publication_date"] = "DATE_CANARY_V2_794D"
    payload["ground_truth"] = {
        "component": "GOLD_COMPONENT_CANARY_V2_794D",
        "entity": "GOLD_ENTITY_CANARY_V2_794D",
        "operation": "GOLD_OPERATION_CANARY_V2_794D",
        "root_cause": "GOLD_ROOT_CANARY_V2_794D",
        "required_relations": ["GOLD_RELATION_CANARY_V2_794D"],
    }
    case = ResearchCase.from_dict(payload)
    contexts = [
        render_standard_context_v2(case),
        render_dependency_prose_context_v2(case),
        render_ccdg_context_v2(case),
    ]
    forbidden = [
        "CASE_ID_CANARY_V2_794D",
        "SOURCE_URL_CANARY_V2_794D",
        "DATE_CANARY_V2_794D",
        "GOLD_COMPONENT_CANARY_V2_794D",
        "GOLD_ENTITY_CANARY_V2_794D",
        "GOLD_OPERATION_CANARY_V2_794D",
        "GOLD_ROOT_CANARY_V2_794D",
        "GOLD_RELATION_CANARY_V2_794D",
    ]
    for rendered in contexts:
        for marker in forbidden:
            assert marker not in rendered
