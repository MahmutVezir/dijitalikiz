from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

ALLOWED_CCDG_RELATIONS = {
    "calls",
    "depends_on",
    "reads",
    "writes",
    "authenticated_by",
    "protected_by",
    "produces_error",
}

class Source(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str
    url: str
    publication_date: str
    retrieved_at: str | None = None

class Contamination(BaseModel):
    model_config = ConfigDict(extra="forbid")
    is_pilot: bool
    excluded_from_main_dataset: bool
    reason: str

class Case(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str
    source: Source
    technology: list[str]
    error_description: str
    I_base: dict
    contamination: Contamination

class GroundTruth(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str
    component: str
    entity: str
    operation: str
    root_cause: str
    required_relation: list[str]
    evidence: list[dict] = Field(default_factory=list)

class CCDGNode(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    type: str
    name: str

class CCDGEdge(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source: str
    target: str
    relation: str

class CCDG(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str
    base_input_sha256: str
    nodes: list[CCDGNode]
    edges: list[CCDGEdge]

class ModelOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    diagnosed_component: str
    root_cause_class: str
    affected_entity: str
    explanation: str

class MatchResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    component_match: bool
    root_cause_match: bool
    entity_match: bool
    primary_accuracy: Literal[0, 1]

class RunRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_id: str
    experiment_date_utc: str
    experiment_id: str
    case_id: str
    condition: Literal["standard", "ccdg"]
    replicate: int = Field(ge=1, le=5)
    model: dict
    generation: dict
    prompt_hashes: dict
    input_hashes: dict
    output: dict
    match: MatchResult
