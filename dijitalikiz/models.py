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
            required_relations=list(payload.get("required_relations", payload.get("required_relation", []))),
        )


@dataclass
class DiagnosticOutput:
    diagnosed_component: str
    root_cause_class: str
    affected_entity: str
    explanation: str = ""

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DiagnosticOutput":
        expected = {"diagnosed_component", "root_cause_class", "affected_entity", "explanation"}
        if set(payload) != expected:
            raise ValueError("DiagnosticOutput must contain exactly the four frozen output fields")
        if not all(isinstance(payload[key], str) for key in expected):
            raise TypeError("DiagnosticOutput fields must all be strings")
        return cls(
            diagnosed_component=payload["diagnosed_component"],
            root_cause_class=payload["root_cause_class"],
            affected_entity=payload["affected_entity"],
            explanation=payload["explanation"],
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
    software_twin_snapshot: dict[str, str] | None = None

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
        snapshot_payload = payload.get("software_twin_snapshot")
        if snapshot_payload is not None and not isinstance(snapshot_payload, dict):
            raise TypeError("software_twin_snapshot must be an object when provided")
        snapshot = None
        if isinstance(snapshot_payload, dict):
            required_snapshot_fields = (
                "repository_url",
                "snapshot_revision",
                "regression_test",
                "observed_failure_signal",
            )
            missing_snapshot_fields = [
                key for key in required_snapshot_fields
                if not isinstance(snapshot_payload.get(key), str) or not snapshot_payload[key].strip()
            ]
            if missing_snapshot_fields:
                raise ValueError(
                    "software_twin_snapshot missing non-empty fields: "
                    + ", ".join(missing_snapshot_fields)
                )
            snapshot = {key: snapshot_payload[key] for key in required_snapshot_fields}

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
            software_twin_snapshot=snapshot,
        )
