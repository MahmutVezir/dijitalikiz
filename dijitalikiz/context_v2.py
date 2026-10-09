from __future__ import annotations

"""Versioned context renderers for a future information-matched study.

Do not change the legacy renderers in dijitalikiz.context: frozen historical
prompt hashes and confirmatory artifacts depend on those exact functions.
"""

from .models import ResearchCase


def _shared_base_lines(case: ResearchCase) -> list[str]:
    lines = [
        "=== Software Debugging Context ===",
        f"Source: {case.source}",
        f"Technology: {case.technology}",
        "",
        "Error description:",
        case.error_description,
        "",
        "I_base:",
    ]
    lines.extend(f"- {item}" for item in case.i_base)
    return lines


def render_standard_context_v2(case: ResearchCase) -> str:
    """Baseline: source facts and error description, without explicit edge list."""
    return "\n".join(_shared_base_lines(case))


def render_dependency_prose_context_v2(case: ResearchCase) -> str:
    """Base context plus each dependency edge stated as a prose fact."""
    lines = _shared_base_lines(case)
    lines.extend(["", "Dependency relations in sentences:"])
    for edge in case.ccdg:
        relation = edge.relation.replace("_", " ")
        sentence = f"{edge.source} has the dependency relation '{relation}' to {edge.target}."
        if edge.details:
            sentence += f" Detail: {edge.details}"
        lines.append(f"- {sentence}")
    return "\n".join(lines)


def render_ccdg_context_v2(case: ResearchCase) -> str:
    """Same base facts and edge fields as the prose arm, encoded as triples."""
    lines = _shared_base_lines(case)
    lines.extend(["", "Dependency relations as directed triples:"])
    for edge in case.ccdg:
        detail_suffix = f" (details: {edge.details})" if edge.details else ""
        lines.append(f"- ({edge.source}) --[{edge.relation}]--> ({edge.target}){detail_suffix}")
    return "\n".join(lines)
