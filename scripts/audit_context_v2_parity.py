from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from dijitalikiz.context_v2 import (
    render_ccdg_context_v2,
    render_dependency_prose_context_v2,
    render_standard_context_v2,
)
from dijitalikiz.models import ResearchCase

ROOT = Path(__file__).resolve().parents[1]


def audit_case(case: ResearchCase) -> dict[str, Any]:
    standard = render_standard_context_v2(case)
    prose = render_dependency_prose_context_v2(case)
    graph = render_ccdg_context_v2(case)

    prose_marker = "Dependency relations in sentences:"
    graph_marker = "Dependency relations as directed triples:"
    if prose.count(prose_marker) != 1 or graph.count(graph_marker) != 1:
        raise ValueError(f"Expected one dependency-section marker for {case.case_id}")
    common_standard = standard.strip()
    common_prose = prose.split(prose_marker, 1)[0].rstrip()
    common_graph = graph.split(graph_marker, 1)[0].rstrip()
    if not (common_standard == common_prose == common_graph):
        raise ValueError(f"Shared base facts are not byte-identical across v2 arms for {case.case_id}")

    if not case.ccdg:
        raise ValueError(f"Case has no CCDG edge data: {case.case_id}")
    for edge in case.ccdg:
        if not all((edge.source, edge.target, edge.relation)):
            raise ValueError(f"Incomplete edge in {case.case_id}")
        relation_prose = edge.relation.replace("_", " ")
        if edge.source not in prose or edge.target not in prose or relation_prose not in prose:
            raise ValueError(f"Edge endpoint/relation missing from prose arm in {case.case_id}")
        if edge.source not in graph or edge.target not in graph or edge.relation not in graph:
            raise ValueError(f"Edge endpoint/relation missing from graph arm in {case.case_id}")
        if edge.details and (edge.details not in prose or edge.details not in graph):
            raise ValueError(f"Edge details are not matched across augmented arms in {case.case_id}")

    for rendered in (standard, prose, graph):
        if case.ground_truth.root_cause and case.ground_truth.root_cause in rendered:
            raise ValueError(f"Ground-truth label leakage in v2 context for {case.case_id}")
        if "Ground truth:" in rendered:
            raise ValueError(f"Ground-truth section leakage in v2 context for {case.case_id}")

    prose_words = len(prose.split())
    graph_words = len(graph.split())
    return {
        "case_id": case.case_id,
        "base_context_sha256": hashlib.sha256(common_standard.encode("utf-8")).hexdigest(),
        "standard_context_sha256": hashlib.sha256(standard.encode("utf-8")).hexdigest(),
        "prose_context_sha256": hashlib.sha256(prose.encode("utf-8")).hexdigest(),
        "ccdg_context_sha256": hashlib.sha256(graph.encode("utf-8")).hexdigest(),
        "edge_count": len(case.ccdg),
        "base_characters": len(common_standard),
        "prose_characters": len(prose),
        "ccdg_characters": len(graph),
        "prose_whitespace_tokens": prose_words,
        "ccdg_whitespace_tokens": graph_words,
        "whitespace_token_count_difference_ccdg_minus_prose": graph_words - prose_words,
        "whitespace_token_count_ratio_ccdg_over_prose": round(graph_words / prose_words, 4) if prose_words else None,
        "interpretation_note": "Whitespace-token counts are only a rough length diagnostic; use the frozen model tokenizer before inference.",
    }


def audit_manifest(manifest_path: Path, case_dir: Path) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    case_ids = manifest.get("case_ids", [])
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("Manifest must contain unique non-empty case_ids.")
    results = []
    for case_id in case_ids:
        path = case_dir / f"{case_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Missing case definition: {path}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("case_id") != case_id:
            raise ValueError(f"Case ID mismatch in {path}")
        results.append(audit_case(ResearchCase.from_dict(payload)))
    return {
        "status": "pass",
        "protocol_version": "context-v2",
        "case_count": len(results),
        "condition_count": 3,
        "information_parity_checks": [
            "Source, technology, error description, and I_base are byte-identical across all three arms.",
            "Every CCDG edge endpoint, relation label, and detail is represented in both dependency-enriched arms.",
            "No ground-truth root-cause label is included in rendered contexts.",
        ],
        "length_measure_caveat": "Whitespace-token counts are not model-tokenizer counts. A frozen tokenizer count and prompt hash audit is required before any inference.",
        "cases": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed content-parity audit for future context-v2 renderers.")
    parser.add_argument("--manifest", type=Path, default=ROOT / "data" / "benchmark" / "benchmark_manifest.json")
    parser.add_argument("--cases-dir", type=Path, default=ROOT / "data" / "benchmark" / "cases")
    parser.add_argument("--output", type=Path, help="Optional path to write the JSON audit report.")
    args = parser.parse_args()
    report = audit_manifest(args.manifest, args.cases_dir)
    payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "protocol_version": report["protocol_version"],
        "case_count": report["case_count"],
        "output": str(args.output) if args.output else None,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
