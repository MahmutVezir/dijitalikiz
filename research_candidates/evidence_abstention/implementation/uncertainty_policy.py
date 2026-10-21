from dataclasses import dataclass
from itertools import combinations
from math import exp, isfinite, log
import re
from typing import Iterable, Sequence


def _validate_unit_interval(value: float, name: str) -> None:
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be within [0, 1]")


def normalized_entropy_from_logits(logits: Sequence[float]) -> float:
    if len(logits) < 2:
        raise ValueError("at least two logits are required")
    if any(not isinstance(value, (int, float)) for value in logits):
        raise TypeError("logits must be numeric")
    if any(not isfinite(value) for value in logits):
        raise ValueError("logits must be finite")

    maximum = max(logits)
    weights = [exp(value - maximum) for value in logits]
    total = sum(weights)
    probabilities = [weight / total for weight in weights]
    entropy = -sum(p * log(p) for p in probabilities if p > 0.0)
    return min(1.0, max(0.0, entropy / log(len(probabilities))))


def mean_normalized_token_entropy(logits_by_step: Sequence[Sequence[float]]) -> float:
    if not logits_by_step:
        raise ValueError("at least one generated-token logit vector is required")
    return sum(normalized_entropy_from_logits(logits) for logits in logits_by_step) / len(logits_by_step)


def lexical_disagreement(answers: Sequence[str]) -> float | None:
    if len(answers) < 2:
        return None
    token_sets = [set(re.findall(r"\w+", answer.casefold())) for answer in answers]
    pair_scores = []
    for left, right in combinations(token_sets, 2):
        union = left | right
        similarity = 1.0 if not union else len(left & right) / len(union)
        pair_scores.append(1.0 - similarity)
    return sum(pair_scores) / len(pair_scores)


@dataclass(frozen=True)
class CalibrationObservation:
    uncertainty_index: float
    answer_correct_and_evidence_supported: bool

    def __post_init__(self) -> None:
        _validate_unit_interval(self.uncertainty_index, "uncertainty_index")


class EmpiricalConfidenceCalibrator:
    def __init__(self, bin_count: int = 5, min_samples_per_bin: int = 8) -> None:
        if bin_count < 2:
            raise ValueError("bin_count must be at least 2")
        if min_samples_per_bin < 1:
            raise ValueError("min_samples_per_bin must be positive")
        self.bin_count = bin_count
        self.min_samples_per_bin = min_samples_per_bin
        self._counts = [0] * bin_count
        self._correct = [0] * bin_count
        self.fitted = False

    def _bin_index(self, uncertainty_index: float) -> int:
        _validate_unit_interval(uncertainty_index, "uncertainty_index")
        return min(int(uncertainty_index * self.bin_count), self.bin_count - 1)

    def fit(self, observations: Iterable[CalibrationObservation]) -> None:
        self._counts = [0] * self.bin_count
        self._correct = [0] * self.bin_count
        count = 0
        for observation in observations:
            index = self._bin_index(observation.uncertainty_index)
            self._counts[index] += 1
            self._correct[index] += int(observation.answer_correct_and_evidence_supported)
            count += 1
        if count == 0:
            raise ValueError("calibration set must not be empty")
        self.fitted = True

    def predict(self, uncertainty_index: float) -> float | None:
        if not self.fitted:
            return None
        index = self._bin_index(uncertainty_index)
        count = self._counts[index]
        if count < self.min_samples_per_bin:
            return None
        return self._correct[index] / count

    def bin_counts(self) -> tuple[int, ...]:
        return tuple(self._counts)


def brier_score(probabilities: Sequence[float], outcomes: Sequence[bool]) -> float:
    if len(probabilities) != len(outcomes) or not probabilities:
        raise ValueError("probabilities and outcomes must have the same non-zero length")
    for value in probabilities:
        _validate_unit_interval(value, "probability")
    return sum((probability - int(outcome)) ** 2 for probability, outcome in zip(probabilities, outcomes)) / len(probabilities)


def expected_calibration_error(probabilities: Sequence[float], outcomes: Sequence[bool], bin_count: int = 10) -> float:
    if len(probabilities) != len(outcomes) or not probabilities:
        raise ValueError("probabilities and outcomes must have the same non-zero length")
    if bin_count < 1:
        raise ValueError("bin_count must be positive")
    for value in probabilities:
        _validate_unit_interval(value, "probability")

    buckets = [[] for _ in range(bin_count)]
    for probability, outcome in zip(probabilities, outcomes):
        index = min(int(probability * bin_count), bin_count - 1)
        buckets[index].append((probability, int(outcome)))

    total = len(probabilities)
    error = 0.0
    for bucket in buckets:
        if not bucket:
            continue
        mean_confidence = sum(item[0] for item in bucket) / len(bucket)
        mean_accuracy = sum(item[1] for item in bucket) / len(bucket)
        error += len(bucket) / total * abs(mean_confidence - mean_accuracy)
    return error


@dataclass(frozen=True)
class DecisionRequest:
    evidence_level: str | None
    answer: str
    available_evidence_ids: frozenset[str]
    cited_evidence_ids: tuple[str, ...]
    supported_claim_coverage: float | None
    normalized_token_entropy: float | None
    candidate_answers: tuple[str, ...]
    self_check_conflict: bool | None
    explicit_contradiction: bool | None
    calibrated_confidence: float | None
    minimum_confidence: float | None
    maximum_uncertainty: float | None
    calibration_id: str | None
    calibration_verified: bool


@dataclass(frozen=True)
class DecisionResult:
    decision: str
    confidence_probability: float | None
    uncertainty_index: float | None
    reasons: tuple[str, ...]


def decide(request: DecisionRequest) -> DecisionResult:
    reasons = []

    if request.evidence_level not in {"E1", "E2", "E3"}:
        reasons.append("evidence_level_unknown")
    elif request.evidence_level == "E3":
        reasons.append("evidence_insufficient")

    if request.explicit_contradiction is None:
        reasons.append("contradiction_status_unknown")
    elif request.explicit_contradiction:
        reasons.append("evidence_contradiction")
    if not request.answer.strip():
        reasons.append("empty_answer")
    if not request.cited_evidence_ids:
        reasons.append("no_evidence_citations")
    if any(item not in request.available_evidence_ids for item in request.cited_evidence_ids):
        reasons.append("unknown_evidence_reference")
    if request.supported_claim_coverage is None:
        reasons.append("claim_support_unavailable")
    else:
        _validate_unit_interval(request.supported_claim_coverage, "supported_claim_coverage")
        if request.supported_claim_coverage == 0.0:
            reasons.append("no_supported_claims")

    disagreement = lexical_disagreement(request.candidate_answers)
    if request.normalized_token_entropy is None or disagreement is None or request.self_check_conflict is None or request.supported_claim_coverage is None:
        reasons.append("uncertainty_signals_incomplete")

    valid_calibration_id = isinstance(request.calibration_id, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", request.calibration_id) is not None
    if request.calibrated_confidence is None or request.minimum_confidence is None or request.maximum_uncertainty is None or not valid_calibration_id or not request.calibration_verified:
        reasons.append("calibration_not_frozen")
    else:
        _validate_unit_interval(request.calibrated_confidence, "calibrated_confidence")
        _validate_unit_interval(request.minimum_confidence, "minimum_confidence")
        _validate_unit_interval(request.maximum_uncertainty, "maximum_uncertainty")

    uncertainty_values = []
    if request.normalized_token_entropy is not None:
        _validate_unit_interval(request.normalized_token_entropy, "normalized_token_entropy")
        uncertainty_values.append(request.normalized_token_entropy)
    if disagreement is not None:
        _validate_unit_interval(disagreement, "lexical_disagreement")
        uncertainty_values.append(disagreement)
    if request.supported_claim_coverage is not None:
        uncertainty_values.append(1.0 - request.supported_claim_coverage)
    if request.self_check_conflict is True:
        uncertainty_values.append(1.0)
    elif request.self_check_conflict is False:
        uncertainty_values.append(0.0)

    uncertainty_index = max(uncertainty_values) if len(uncertainty_values) == 4 else None

    if reasons:
        return DecisionResult("abstain", request.calibrated_confidence, uncertainty_index, tuple(dict.fromkeys(reasons)))

    if uncertainty_index > request.maximum_uncertainty:
        reasons.append("uncertainty_threshold_exceeded")
    if request.calibrated_confidence < request.minimum_confidence:
        reasons.append("confidence_below_threshold")

    if reasons:
        return DecisionResult("abstain", request.calibrated_confidence, uncertainty_index, tuple(reasons))
    return DecisionResult("diagnose", request.calibrated_confidence, uncertainty_index, ("all_gates_passed",))
