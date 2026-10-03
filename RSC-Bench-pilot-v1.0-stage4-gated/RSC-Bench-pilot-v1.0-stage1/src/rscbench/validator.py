from __future__ import annotations

from .canonicalize import canonical_json
from .hashing import sha256_text
from .schemas import ALLOWED_CCDG_RELATIONS, CCDG, Case, GroundTruth


def base_input_sha256(case: Case) -> str:
    return sha256_text(canonical_json(case.I_base))


def validate_case_links(case: Case, truth: GroundTruth, ccdg: CCDG) -> None:
    if case.case_id != truth.case_id or case.case_id != ccdg.case_id:
        raise ValueError("Case, ground truth and CCDG case_id values must match.")
    if not case.contamination.is_pilot:
        raise ValueError("Pilot pipeline requires is_pilot=true.")
    if not case.contamination.excluded_from_main_dataset:
        raise ValueError("Pilot case must be excluded from the main dataset.")

    expected_base_hash = base_input_sha256(case)
    if ccdg.base_input_sha256 != expected_base_hash:
        raise ValueError(
            "CCDG base_input_sha256 does not match the canonical I_base. "
            "CCDG must be derived from the same base information."
        )

    node_ids = {node.id for node in ccdg.nodes}
    if len(node_ids) != len(ccdg.nodes):
        raise ValueError("CCDG node IDs must be unique.")
    for edge in ccdg.edges:
        if edge.source not in node_ids or edge.target not in node_ids:
            raise ValueError("CCDG edge references an unknown node.")
        if edge.relation not in ALLOWED_CCDG_RELATIONS:
            raise ValueError(f"Unsupported CCDG relation: {edge.relation}")


def validate_main_dataset_exclusion(main_case_ids: set[str], pilot_case_ids: set[str]) -> None:
    overlap = main_case_ids & pilot_case_ids
    if overlap:
        raise ValueError(
            "Pilot case IDs cannot enter the main dataset: " + ", ".join(sorted(overlap))
        )
