from __future__ import annotations

from .models import ResearchCase


def render_standard_context(case: ResearchCase) -> str:
    lines = [
        "=== Standard Context ===",
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
    return "\n".join(lines)
