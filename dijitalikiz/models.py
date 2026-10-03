from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DependencyEdge:
    source: str
    target: str
    relation: str
    details: str = ""

    def as_line(self) -> str:
        return f"{self.source} -> {self.relation} -> {self.target}"


@dataclass
class GroundTruth:
    component: str
    entity: str
    operation: str
    root_cause: str
    required_relations: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "GroundTruth":
        return cls(
            component=str(payload.get("component", "")),
            entity=str(payload.get("entity", "")),
            operation=str(payload.get("operation", "")),
            root_cause=str(payload.get("root_cause", "")),
            required_relations=list(payload.get("required_relation", [])),
        )


@dataclass
class DiagnosticOutput:
    diagnosed_component: str
    root_cause_class: str
    affected_entity: str
    explanation: str = ""

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DiagnosticOutput":
        return cls(
            diagnosed_component=str(payload.get("diagnosed_component", "")),
            root_cause_class=str(payload.get("root_cause_class", "")),
            affected_entity=str(payload.get("affected_entity", "")),
            explanation=str(payload.get("explanation", "")),
        )


@dataclass
class ResearchCase:
    case_id: str
    source: str
    source_url: str
    publication_date: str
    technology: str
    error_description: str
    i_base: list[str]
    ccdg: list[DependencyEdge]
    ground_truth: GroundTruth

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ResearchCase":
        edges = [
            DependencyEdge(
                source=str(edge.get("source", "")),
                target=str(edge.get("target", "")),
                relation=str(edge.get("relation", "")),
                details=str(edge.get("details", "")),
            )
            for edge in payload.get("ccdg", [])
        ]
        return cls(
            case_id=str(payload.get("case_id", "")),
            source=str(payload.get("source", "")),
            source_url=str(payload.get("source_url", "")),
            publication_date=str(payload.get("publication_date", "")),
            technology=str(payload.get("technology", "")),
            error_description=str(payload.get("error_description", "")),
            i_base=[str(item) for item in payload.get("i_base", [])],
            ccdg=edges,
            ground_truth=GroundTruth.from_dict(payload.get("ground_truth", {})),
        )
