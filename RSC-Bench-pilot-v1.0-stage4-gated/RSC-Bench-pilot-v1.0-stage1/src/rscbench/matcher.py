from __future__ import annotations
from .schemas import GroundTruth, MatchResult, ModelOutput


def deterministic_match(output: ModelOutput, truth: GroundTruth) -> MatchResult:
    """Apply the pre-specified primary matcher.

    The current protocol defines the model output schema with three primary
    diagnosis fields. Operation and required_relation are retained in
    ground truth for provenance/secondary analysis but are not silently
    treated as primary criteria because the frozen output schema does not
    request them.
    """
    component = output.diagnosed_component == truth.component
    root = output.root_cause_class == truth.root_cause
    entity = output.affected_entity == truth.entity
    return MatchResult(
        component_match=component,
        root_cause_match=root,
        entity_match=entity,
        primary_accuracy=int(component and root and entity),
    )
