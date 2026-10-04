from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class CriterionState(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    UNKNOWN = "unknown"


class DependencyStrength(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    NONE = "none"
    UNKNOWN = "unknown"


class CCDGSuitability(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    UNSUITABLE = "unsuitable"
    UNKNOWN = "unknown"


class ContaminationRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


@dataclass
class CandidateAssessment:
    case_id: str
    provenance_quality: CriterionState = CriterionState.UNKNOWN
    root_cause_quality: CriterionState = CriterionState.UNKNOWN
    fix_quality: CriterionState = CriterionState.UNKNOWN
    dependency_strength: DependencyStrength = DependencyStrength.UNKNOWN
    dependency_evidence: str = ""
    ccdg_suitability: CCDGSuitability = CCDGSuitability.UNKNOWN
    contamination_risk: ContaminationRisk = ContaminationRisk.UNKNOWN
    contamination_risk_reason: str = ""
    IC1: CriterionState = CriterionState.UNKNOWN
    IC2: CriterionState = CriterionState.UNKNOWN
    IC3: CriterionState = CriterionState.UNKNOWN
    IC4: CriterionState = CriterionState.UNKNOWN
    IC5: CriterionState = CriterionState.UNKNOWN
    IC6: CriterionState = CriterionState.UNKNOWN
    IC7: CriterionState = CriterionState.UNKNOWN
    eligible_for_pilot: bool = False
    exclusion_reason: str = ""
    notes: list[str] = field(default_factory=list)

    def recompute_eligibility(self) -> bool:
        criteria = [self.IC1, self.IC2, self.IC3, self.IC4, self.IC5, self.IC6, self.IC7]
        eligible = (
            all(item is CriterionState.PASS for item in criteria)
            and self.dependency_strength in {
                DependencyStrength.STRONG,
                DependencyStrength.MODERATE,
            }
            and self.ccdg_suitability in {
                CCDGSuitability.STRONG,
                CCDGSuitability.MODERATE,
            }
        )
        self.eligible_for_pilot = eligible
        if not eligible and not self.exclusion_reason:
            failed = [f"IC{i}" for i, value in enumerate(criteria, 1) if value is not CriterionState.PASS]
            if self.dependency_strength not in {
                DependencyStrength.STRONG,
                DependencyStrength.MODERATE,
            }:
                failed.append("dependency_strength")
            if self.ccdg_suitability not in {
                CCDGSuitability.STRONG,
                CCDGSuitability.MODERATE,
            }:
                failed.append("ccdg_suitability")
            self.exclusion_reason = "Eligibility requirements not met: " + ", ".join(failed)
        return eligible

    def to_dict(self) -> dict[str, Any]:
        self.recompute_eligibility()
        payload = asdict(self)
        for key in (
            "provenance_quality",
            "root_cause_quality",
            "fix_quality",
            "dependency_strength",
            "ccdg_suitability",
            "contamination_risk",
            "IC1", "IC2", "IC3", "IC4", "IC5", "IC6", "IC7",
        ):
            payload[key] = payload[key].value
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "CandidateAssessment":
        def enum_value(enum_cls, key):
            value = payload.get(key)
            if value is None:
                return enum_cls.UNKNOWN
            try:
                return enum_cls(value)
            except ValueError:
                raise ValueError(f"Invalid {key}: {value!r}")

        obj = cls(
            case_id=str(payload["case_id"]),
            provenance_quality=enum_value(CriterionState, "provenance_quality"),
            root_cause_quality=enum_value(CriterionState, "root_cause_quality"),
            fix_quality=enum_value(CriterionState, "fix_quality"),
            dependency_strength=enum_value(DependencyStrength, "dependency_strength"),
            dependency_evidence=str(payload.get("dependency_evidence", "")),
            ccdg_suitability=enum_value(CCDGSuitability, "ccdg_suitability"),
            contamination_risk=enum_value(ContaminationRisk, "contamination_risk"),
            contamination_risk_reason=str(payload.get("contamination_risk_reason", "")),
            **{f"IC{i}": enum_value(CriterionState, f"IC{i}") for i in range(1, 8)},
            eligible_for_pilot=bool(payload.get("eligible_for_pilot", False)),
            exclusion_reason=str(payload.get("exclusion_reason", "")),
            notes=list(payload.get("notes", [])),
        )
        expected = obj.recompute_eligibility()
        if bool(payload.get("eligible_for_pilot", False)) != expected:
            raise ValueError("eligible_for_pilot does not match deterministic eligibility rules")
        return obj
