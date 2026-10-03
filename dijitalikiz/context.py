from __future__ import annotations

from .models import ResearchCase


def render_standard_context(case: ResearchCase) -> str:
    lines = [
        "=== Standard Context ===",
        f"Case ID: {case.case_id}",
        f"Source: {case.source}",
        f"Technology: {case.technology}",
        "",
        "Error description:",
        case.error_description,
        "",
        "I_base:",
    ]
    lines.extend(f"- {item}" for item in case.i_base)
    return "\n".join(lines)


def render_ccdg_context(case: ResearchCase) -> str:
    lines = [
        "=== CCDG Context ===",
        f"Case ID: {case.case_id}",
        f"Source: {case.source}",
        f"Technology: {case.technology}",
        "",
        "Dependencies:",
    ]
    for edge in case.ccdg:
        detail_suffix = f" ({edge.details})" if edge.details else ""
        lines.append(f"- {edge.source} {edge.relation} {edge.target}{detail_suffix}")

    lines.extend(["", "I_base:"])
    lines.extend(f"- {item}" for item in case.i_base)

    lines.extend(["", "Ground truth:"])
    lines.append(f"- component: {case.ground_truth.component}")
    lines.append(f"- entity: {case.ground_truth.entity}")
    lines.append(f"- operation: {case.ground_truth.operation}")
    lines.append(f"- root_cause: {case.ground_truth.root_cause}")
    if case.ground_truth.required_relations:
        lines.append(
            "- required_relations: " + ", ".join(case.ground_truth.required_relations)
        )
    return "\n".join(lines)
