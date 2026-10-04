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
        self.eligible_for_pilot = (
            all(x is CriterionState.PASS for x in criteria)
            and self.dependency_strength in {DependencyStrength.STRONG, DependencyStrength.MODERATE}
            and self.ccdg_suitability in {CCDGSuitability.STRONG, CCDGSuitability.MODERATE}
        )
        return self.eligible_for_pilot

    def to_dict(self) -> dict[str, Any]:
        self.recompute_eligibility()
        p = asdict(self)
        for k in ("provenance_quality","root_cause_quality","fix_quality","dependency_strength",
                  "ccdg_suitability","contamination_risk","IC1","IC2","IC3","IC4","IC5","IC6","IC7"):
            p[k] = p[k].value
        return p

    @classmethod
    def from_dict(cls, p: dict[str, Any]) -> "CandidateAssessment":
        def e(t, k):
            return t(p.get(k, "unknown"))
        obj = cls(
            case_id=str(p["case_id"]),
            provenance_quality=e(CriterionState, "provenance_quality"),
            root_cause_quality=e(CriterionState, "root_cause_quality"),
            fix_quality=e(CriterionState, "fix_quality"),
            dependency_strength=e(DependencyStrength, "dependency_strength"),
            dependency_evidence=str(p.get("dependency_evidence", "")),
            ccdg_suitability=e(CCDGSuitability, "ccdg_suitability"),
            contamination_risk=e(ContaminationRisk, "contamination_risk"),
            contamination_risk_reason=str(p.get("contamination_risk_reason", "")),
            IC1=e(CriterionState,"IC1"), IC2=e(CriterionState,"IC2"), IC3=e(CriterionState,"IC3"),
            IC4=e(CriterionState,"IC4"), IC5=e(CriterionState,"IC5"), IC6=e(CriterionState,"IC6"),
            IC7=e(CriterionState,"IC7"),
            eligible_for_pilot=bool(p.get("eligible_for_pilot", False)),
            exclusion_reason=str(p.get("exclusion_reason", "")),
            notes=list(p.get("notes", [])),
        )
        if obj.eligible_for_pilot != obj.recompute_eligibility():
            raise ValueError("eligible_for_pilot does not match deterministic eligibility")
        return obj
