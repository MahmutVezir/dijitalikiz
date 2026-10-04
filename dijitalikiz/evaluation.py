from __future__ import annotations

import re
from typing import Any

from .models import DiagnosticOutput, GroundTruth


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def _has_required_relations(output: DiagnosticOutput, ground_truth: GroundTruth) -> bool:
    required = ground_truth.required_relations
    if not required:
        return True

    haystack = " ".join(
        [
            output.explanation,
            output.diagnosed_component,
            output.root_cause_class,
            output.affected_entity,
        ]
    )
    haystack = _normalize(haystack)
    for token in required:
        if _normalize(str(token)) not in haystack:
            return False
    return True


def evaluate_output(output: DiagnosticOutput, ground_truth: GroundTruth) -> dict[str, Any]:
    explanation = _normalize(output.explanation)
    operation = _normalize(ground_truth.operation)
    checks = {
        "component": _normalize(output.diagnosed_component) == _normalize(ground_truth.component),
        "entity": _normalize(output.affected_entity) == _normalize(ground_truth.entity),
        "operation": bool(operation) and operation in explanation,
        "root_cause": _normalize(output.root_cause_class) == _normalize(ground_truth.root_cause),
        "required_relations": _has_required_relations(output, ground_truth),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
    }
