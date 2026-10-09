import json
from pathlib import Path

from jsonschema import Draft202012Validator
from dijitalikiz.context_v2 import (
    render_ccdg_context_v2,
    render_dependency_prose_context_v2,
    render_standard_context_v2,
)
from dijitalikiz.models import ResearchCase


ROOT = Path(__file__).resolve().parents[1]
DRAFT_PATH = ROOT / "data" / "candidate_case_drafts" / "commons-compress-github-pr-770-tar-pax-header-memory-bound.json"
SCHEMA_PATH = ROOT / "schemas" / "research_case.schema.json"
MANIFEST_PATH = ROOT / "data" / "benchmark" / "benchmark_manifest.json"


def test_candidate_case_draft_conforms_to_research_case_schema_without_entering_manifest():
    payload = json.loads(DRAFT_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert not errors, [error.message for error in errors]
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert payload["case_id"] not in manifest["case_ids"]
    assert payload["split"] == "candidates"
    assert payload["provenance"]["case_status"] == "candidate_case_draft_not_eligible_for_experiment"


def test_candidate_case_v2_contexts_keep_shared_facts_and_do_not_leak_ground_truth():
    payload = json.loads(DRAFT_PATH.read_text(encoding="utf-8"))
    case = ResearchCase.from_dict(payload)
    contexts = (
        render_standard_context_v2(case),
        render_dependency_prose_context_v2(case),
        render_ccdg_context_v2(case),
    )
    shared_base = contexts[0].strip()
    assert shared_base == contexts[1].split("Dependency relations in sentences:", 1)[0].rstrip()
    assert shared_base == contexts[2].split("Dependency relations as directed triples:", 1)[0].rstrip()
    for rendered in contexts:
        assert case.ground_truth.root_cause not in rendered
        assert payload["provenance"]["fix_commit"] not in rendered
        assert "Ground truth:" not in rendered


def test_dependency_augmented_arms_include_the_same_candidate_edges():
    payload = json.loads(DRAFT_PATH.read_text(encoding="utf-8"))
    case = ResearchCase.from_dict(payload)
    prose = render_dependency_prose_context_v2(case)
    graph = render_ccdg_context_v2(case)
    for edge in case.ccdg:
        assert edge.source in prose and edge.source in graph
        assert edge.target in prose and edge.target in graph
        assert edge.relation.replace("_", " ") in prose
        assert edge.relation in graph
        if edge.details:
            assert edge.details in prose and edge.details in graph
