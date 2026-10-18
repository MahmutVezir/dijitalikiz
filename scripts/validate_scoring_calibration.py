from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "calibration" / "manifest.json"
VALID_LABELS = {"correct", "partially_correct", "incorrect", "unscorable"}
PROTOCOL_MIN_INITIAL_REVIEW_EXACT_AGREEMENT = 0.80
PROTOCOL_MIN_INITIAL_REVIEW_COHEN_KAPPA = 0.70

def _normalize_alias_phrase(value: str) -> str:
    """Use the frozen alias matcher's lowercase ASCII-token normalization."""
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def _calibration_matcher_accepts(response_text: str, aliases: list[str]) -> bool:
    """Reproduce the frozen evaluator using root_cause_class plus explanation."""
    try:
        payload = json.loads(response_text)
    except (TypeError, json.JSONDecodeError):
        return False

    expected_fields = {"diagnosed_component", "root_cause_class", "affected_entity", "explanation"}
    if not isinstance(payload, dict) or set(payload) != expected_fields:
        return False
    if not all(isinstance(payload[field], str) for field in expected_fields):
        return False

    matcher_surface = payload["root_cause_class"] + " " + payload["explanation"]
    haystack = " " + _normalize_alias_phrase(matcher_surface) + " "
    return any(
        (" " + normalized + " ") in haystack
        for normalized in (_normalize_alias_phrase(alias) for alias in aliases)
        if normalized
    )
FORBIDDEN_REVIEW_FIELDS = {
    "condition", "seed", "model_id", "model_revision", "challenge_class",
    "legacy_matcher_accepts", "source_case_id", "ground_truth_root_cause",
    "ground_truth_rationale", "is_from_frozen_study_output",
}


def _read_json(path: Path, issues: list[str], label: str) -> dict[str, Any] | None:
    if not path.is_file():
        issues.append(f"missing_{label}: {path}")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"invalid_{label}: {exc}")
        return None
    if not isinstance(value, dict):
        issues.append(f"invalid_{label}: expected a JSON object")
        return None
    return value


def _read_jsonl(path: Path, issues: list[str], label: str) -> list[dict[str, Any]] | None:
    if not path.is_file():
        issues.append(f"missing_{label}: {path}")
        return None
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        issues.append(f"unreadable_{label}: {exc}")
        return None
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(f"invalid_{label}_json_line_{line_number}: {exc}")
            continue
        if not isinstance(row, dict):
            issues.append(f"invalid_{label}_row_{line_number}: expected a JSON object")
            continue
        rows.append(row)
    if not rows:
        issues.append(f"empty_{label}: no JSONL records found")
    return rows


def _resolve(root: Path, path_value: Any, label: str, issues: list[str]) -> Path | None:
    if not isinstance(path_value, str) or not path_value.strip():
        issues.append(f"invalid_path_{label}")
        return None
    path = Path(path_value)
    return path if path.is_absolute() else root / path


def _case_ids(path: Path, key: str, issues: list[str], label: str) -> set[str]:
    data = _read_json(path, issues, label)
    if data is None:
        return set()
    values = data.get(key)
    if not isinstance(values, list):
        issues.append(f"invalid_case_list_{label}: expected '{key}' array")
        return set()
    return {item for item in values if isinstance(item, str)}


def _index_rows(
    rows: list[dict[str, Any]] | None,
    *,
    label: str,
    issues: list[str],
    key_field: str = "review_id",
) -> dict[str, dict[str, Any]]:
    if rows is None:
        return {}
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = row.get(key_field)
        if not isinstance(key, str) or not key.strip():
            issues.append(f"{label}_row_missing_{key_field}")
            continue
        if key in indexed:
            issues.append(f"{label}_duplicate_{key_field}: {key}")
            continue
        indexed[key] = row
    return indexed


def _validate_annotation_rows(
    indexed: dict[str, dict[str, Any]],
    *,
    label: str,
    issues: list[str],
    reviewer_field: str,
    require_blinding_flags: bool,
) -> str | None:
    reviewer_ids: set[str] = set()
    allowed_fields = {
        "review_id", "label", "rationale", "evidence_urls", reviewer_field,
        "condition_blinded", "challenge_class_blinded", "matcher_result_blinded",
    }
    if label == "adjudication":
        allowed_fields.add("disagreement_resolved")
    for review_id, row in indexed.items():
        extra_fields = set(row) - allowed_fields
        missing_fields = allowed_fields - set(row)
        if extra_fields:
            issues.append(f"{label}_{review_id}_unexpected_fields: {','.join(sorted(extra_fields))}")
        if missing_fields:
            issues.append(f"{label}_{review_id}_missing_fields: {','.join(sorted(missing_fields))}")
        reviewer_id = row.get(reviewer_field)
        if not isinstance(reviewer_id, str) or not reviewer_id.strip():
            issues.append(f"{label}_{review_id}_missing_{reviewer_field}")
        else:
            reviewer_ids.add(reviewer_id)
        if row.get("label") not in VALID_LABELS:
            issues.append(f"{label}_{review_id}_invalid_label")
        if not isinstance(row.get("rationale"), str) or len(row["rationale"].strip()) < 20:
            issues.append(f"{label}_{review_id}_rationale_too_short")
        evidence = row.get("evidence_urls")
        if not isinstance(evidence, list) or not evidence or not all(
            isinstance(url, str) and url.startswith(("https://", "http://")) for url in evidence
        ):
            issues.append(f"{label}_{review_id}_missing_evidence_urls")
        for field in FORBIDDEN_REVIEW_FIELDS:
            if field in row:
                issues.append(f"{label}_{review_id}_leaks_blinding_field_{field}")
        if require_blinding_flags:
            for flag in ("condition_blinded", "challenge_class_blinded", "matcher_result_blinded"):
                if row.get(flag) is not True:
                    issues.append(f"{label}_{review_id}_blinding_not_attested_{flag}")
    if len(reviewer_ids) > 1:
        issues.append(f"{label}_reviewer_id_inconsistent_within_file")
    return next(iter(reviewer_ids)) if len(reviewer_ids) == 1 else None


def _cohen_kappa(a: list[str], b: list[str]) -> float | None:
    if not a or len(a) != len(b):
        return None
    labels = VALID_LABELS
    observed = sum(left == right for left, right in zip(a, b)) / len(a)
    counts_a = Counter(a)
    counts_b = Counter(b)
    expected = sum(
        (counts_a[label] / len(a)) * (counts_b[label] / len(b))
        for label in labels
    )
    if math.isclose(1.0 - expected, 0.0):
        return None
    return round((observed - expected) / (1.0 - expected), 6)


def _score_metrics(
    examples_by_id: dict[str, dict[str, Any]],
    adjudications_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    tp = fp = tn = fn = unscorable = 0
    per_class: dict[str, dict[str, int]] = {}
    for example_id, example in examples_by_id.items():
        label = adjudications_by_id[example_id]["label"]
        challenge = example["challenge_class"]
        bucket = per_class.setdefault(challenge, {"n": 0, "matcher_accepts": 0, "adjudicated_correct": 0})
        bucket["n"] += 1
        bucket["matcher_accepts"] += int(example["legacy_matcher_accepts"])
        bucket["adjudicated_correct"] += int(label == "correct")
        if label == "unscorable":
            unscorable += 1
            continue
        matcher = bool(example["legacy_matcher_accepts"])
        is_correct = label == "correct"
        if matcher and is_correct:
            tp += 1
        elif matcher and not is_correct:
            fp += 1
        elif not matcher and is_correct:
            fn += 1
        else:
            tn += 1
    scored = tp + fp + tn + fn
    return {
        "n_total": len(examples_by_id),
        "n_scored": scored,
        "n_unscorable_excluded": unscorable,
        "strict_binary_definition": "adjudicated 'correct' is positive; partially_correct and incorrect are negative; unscorable is excluded",
        "confusion_matrix": {"true_positive": tp, "false_positive": fp, "true_negative": tn, "false_negative": fn},
        "matcher_sensitivity": round(tp / (tp + fn), 6) if tp + fn else None,
        "matcher_specificity": round(tn / (tn + fp), 6) if tn + fp else None,
        "matcher_positive_predictive_value": round(tp / (tp + fp), 6) if tp + fp else None,
        "matcher_negative_predictive_value": round(tn / (tn + fn), 6) if tn + fn else None,
        "challenge_class_counts": per_class,
        "warning": "Calibration metrics describe this finite adjudicated set; they do not prove universal semantic validity.",
    }


def audit_calibration(
    *,
    manifest_path: Path = DEFAULT_MANIFEST,
    examples_path: Path | None = None,
    reviewer_a_path: Path | None = None,
    reviewer_b_path: Path | None = None,
    adjudication_path: Path | None = None,
    key_path: Path | None = None,
    pilot_manifest_path: Path = ROOT / "data" / "pilot" / "pilot_manifest.json",
    benchmark_manifest_path: Path = ROOT / "data" / "benchmark" / "benchmark_manifest.json",
) -> dict[str, Any]:
    issues: list[str] = []
    manifest_path = manifest_path.resolve()
    root = manifest_path.parents[2] if len(manifest_path.parents) >= 3 else ROOT
    manifest = _read_json(manifest_path, issues, "calibration_manifest")
    if manifest is None:
        return {"status": "blocked", "ready_for_new_confirmatory_inference": False, "issues": issues}

    files = manifest.get("files", {})
    examples_path = examples_path or _resolve(root, files.get("examples"), "examples", issues)
    reviewer_a_path = reviewer_a_path or _resolve(root, files.get("reviewer_a"), "reviewer_a", issues)
    reviewer_b_path = reviewer_b_path or _resolve(root, files.get("reviewer_b"), "reviewer_b", issues)
    adjudication_path = adjudication_path or _resolve(root, files.get("adjudication"), "adjudication", issues)
    if key_path is None:
        key_path = Path("/tmp/scoring-calibration/review_key_private.json")

    if any(path is None for path in (examples_path, reviewer_a_path, reviewer_b_path, adjudication_path)):
        return {"status": "blocked", "ready_for_new_confirmatory_inference": False, "issues": issues}

    examples = _read_jsonl(examples_path, issues, "examples")
    reviewer_a = _read_jsonl(reviewer_a_path, issues, "reviewer_a")
    reviewer_b = _read_jsonl(reviewer_b_path, issues, "reviewer_b")
    adjudications = _read_jsonl(adjudication_path, issues, "adjudication")
    key = _read_json(key_path, issues, "private_review_key")

    schema_path = root / "schemas" / "scoring_calibration_example.schema.json"
    schema = _read_json(schema_path, issues, "calibration_example_schema")
    if examples is not None and schema is not None:
        validator = Draft202012Validator(schema)
        for line_number, example in enumerate(examples, start=1):
            errors = sorted(validator.iter_errors(example), key=lambda error: list(error.path))
            for error in errors[:5]:
                issues.append(f"examples_line_{line_number}_schema_error: {error.message}")

    if examples is not None:
        examples_by_id: dict[str, dict[str, Any]] = {}
        valid_classes = set(manifest.get("required_challenge_classes", []))
        class_counts: Counter[str] = Counter()
        source_cases_by_class: dict[str, set[str]] = {}
        origin_counts: Counter[str] = Counter()
        model_output_cases: set[str] = set()
        for row in examples:
            example_id = row.get("example_id")
            if not isinstance(example_id, str) or not example_id.strip():
                issues.append("example_missing_example_id")
                continue
            if example_id in examples_by_id:
                issues.append(f"duplicate_example_id: {example_id}")
                continue
            examples_by_id[example_id] = row
            challenge_class = row.get("challenge_class")
            if challenge_class not in valid_classes:
                issues.append(f"{example_id}_unknown_challenge_class")
            else:
                class_counts[challenge_class] += 1
                source_case = row.get("source_case_id")
                if isinstance(source_case, str) and source_case.strip():
                    source_cases_by_class.setdefault(challenge_class, set()).add(source_case)
            origin = row.get("response_origin")
            if origin in {"independent_model_output", "human_authored_control", "synthetic_adversarial_control"}:
                origin_counts[origin] += 1
                source_case = row.get("source_case_id")
                if origin == "independent_model_output" and isinstance(source_case, str):
                    model_output_cases.add(source_case)
                if origin == "independent_model_output":
                    metadata = row.get("generation_metadata")
                    if not isinstance(metadata, dict):
                        issues.append(f"{example_id}_model_output_missing_generation_metadata")
                elif row.get("generation_metadata") is not None:
                    issues.append(f"{example_id}_control_has_unexpected_generation_metadata")
            else:
                issues.append(f"{example_id}_invalid_response_origin")
            if row.get("is_from_frozen_study_output") is not False:
                issues.append(f"{example_id}_uses_frozen_study_output")
            aliases = row.get("root_cause_aliases")
            response_text = row.get("response_text")
            if not isinstance(aliases, list) or not aliases or not all(
                isinstance(alias, str) and alias.strip() for alias in aliases
            ):
                issues.append(f"{example_id}_invalid_root_cause_aliases")
            if not isinstance(response_text, str) or not response_text.strip():
                issues.append(f"{example_id}_invalid_response_text")
            elif origin == "independent_model_output":
                metadata = row.get("generation_metadata")
                if isinstance(metadata, dict):
                    actual_raw_sha256 = hashlib.sha256(response_text.encode("utf-8")).hexdigest()
                    if metadata.get("raw_output_sha256") != actual_raw_sha256:
                        issues.append(f"{example_id}_raw_output_sha256_mismatch")
            if isinstance(response_text, str) and response_text.strip() and isinstance(aliases, list) and aliases and all(
                isinstance(alias, str) and alias.strip() for alias in aliases
            ):
                computed_match = _calibration_matcher_accepts(response_text, aliases)
                if row.get("legacy_matcher_accepts") is not computed_match:
                    issues.append(f"{example_id}_legacy_matcher_result_mismatch")
        minimum = manifest.get("minimum_examples_per_challenge_class")
        if not isinstance(minimum, int) or minimum < 1:
            issues.append("invalid_minimum_examples_per_challenge_class")
            minimum = 1
        for challenge_class in sorted(valid_classes):
            if class_counts[challenge_class] < minimum:
                issues.append(
                    f"insufficient_examples_for_{challenge_class}: {class_counts[challenge_class]} < {minimum}"
                )
        minimum_distinct = manifest.get("minimum_distinct_source_cases")
        if not isinstance(minimum_distinct, int) or minimum_distinct < 2:
            issues.append("invalid_minimum_distinct_source_cases")
            minimum_distinct = 2
        observed_sources = {
            row.get("source_case_id") for row in examples_by_id.values()
            if isinstance(row.get("source_case_id"), str) and row.get("source_case_id").strip()
        }
        if len(observed_sources) < minimum_distinct:
            issues.append(
                f"insufficient_distinct_source_cases: {len(observed_sources)} < {minimum_distinct}"
            )
        minimum_model_outputs = manifest.get("minimum_independent_model_output_examples")
        if not isinstance(minimum_model_outputs, int) or minimum_model_outputs < 1:
            issues.append("invalid_minimum_independent_model_output_examples")
            minimum_model_outputs = 1
        observed_model_outputs = origin_counts["independent_model_output"]
        if observed_model_outputs < minimum_model_outputs:
            issues.append(
                f"insufficient_independent_model_outputs: {observed_model_outputs} < {minimum_model_outputs}"
            )
        minimum_model_cases = manifest.get("minimum_independent_model_output_source_cases")
        if not isinstance(minimum_model_cases, int) or minimum_model_cases < 1:
            issues.append("invalid_minimum_independent_model_output_source_cases")
            minimum_model_cases = 1
        if len(model_output_cases) < minimum_model_cases:
            issues.append(
                f"insufficient_independent_model_output_source_cases: {len(model_output_cases)} < {minimum_model_cases}"
            )
        minimum_controls = manifest.get("minimum_human_authored_or_synthetic_control_examples")
        if not isinstance(minimum_controls, int) or minimum_controls < 1:
            issues.append("invalid_minimum_human_authored_or_synthetic_control_examples")
            minimum_controls = 1
        observed_controls = origin_counts["human_authored_control"] + origin_counts["synthetic_adversarial_control"]
        if observed_controls < minimum_controls:
            issues.append(
                f"insufficient_control_examples: {observed_controls} < {minimum_controls}"
            )
        minimum_distinct_per_class = manifest.get("minimum_distinct_cases_per_challenge_class")
        if not isinstance(minimum_distinct_per_class, int) or minimum_distinct_per_class < 1:
            issues.append("invalid_minimum_distinct_cases_per_challenge_class")
            minimum_distinct_per_class = 1
        for challenge_class in sorted(valid_classes):
            distinct_count = len(source_cases_by_class.get(challenge_class, set()))
            if distinct_count < minimum_distinct_per_class:
                issues.append(
                    f"insufficient_distinct_cases_for_{challenge_class}: "
                    f"{distinct_count} < {minimum_distinct_per_class}"
                )
        pilot_ids = _case_ids(pilot_manifest_path, "cases", issues, "pilot_manifest")
        benchmark_ids = _case_ids(benchmark_manifest_path, "case_ids", issues, "benchmark_manifest")
        for example_id, row in examples_by_id.items():
            source_case = row.get("source_case_id")
            if source_case in pilot_ids or source_case in benchmark_ids:
                issues.append(f"{example_id}_overlaps_frozen_case: {source_case}")
        example_ids = set(examples_by_id)
    else:
        examples_by_id = {}
        example_ids = set()

    reviewer_a_index = _index_rows(reviewer_a, label="reviewer_a", issues=issues)
    reviewer_b_index = _index_rows(reviewer_b, label="reviewer_b", issues=issues)
    adjudication_index = _index_rows(adjudications, label="adjudication", issues=issues)
    reviewer_a_id = _validate_annotation_rows(
        reviewer_a_index, label="reviewer_a", issues=issues, reviewer_field="reviewer_id", require_blinding_flags=True
    )
    reviewer_b_id = _validate_annotation_rows(
        reviewer_b_index, label="reviewer_b", issues=issues, reviewer_field="reviewer_id", require_blinding_flags=True
    )
    if reviewer_a_id and reviewer_b_id and reviewer_a_id == reviewer_b_id:
        issues.append("reviewers_must_be_independent_and_have_distinct_ids")
    adjudicator_id = _validate_annotation_rows(
        adjudication_index, label="adjudication", issues=issues, reviewer_field="adjudicator_id", require_blinding_flags=True
    )
    if adjudicator_id and adjudicator_id in {reviewer_a_id, reviewer_b_id}:
        issues.append("adjudicator_must_be_distinct_from_initial_reviewers")

    key_map: dict[str, dict[str, Any]] = {}
    if key is not None:
        if key.get("key_status") != "PRIVATE_DO_NOT_SHARE_BEFORE_REVIEWS_LOCKED":
            issues.append("private_key_status_invalid")
        items = key.get("items")
        if not isinstance(items, list):
            issues.append("private_key_items_missing")
        else:
            for item in items:
                if not isinstance(item, dict) or not isinstance(item.get("review_id"), str):
                    issues.append("private_key_row_invalid")
                    continue
                review_id = item["review_id"]
                if review_id in key_map:
                    issues.append(f"private_key_duplicate_review_id: {review_id}")
                    continue
                key_map[review_id] = item
            if {item.get("example_id") for item in key_map.values()} != example_ids:
                issues.append("private_key_example_coverage_mismatch")
            if {review_id for review_id in reviewer_a_index} != set(key_map):
                issues.append("reviewer_a_review_id_coverage_mismatch")
            if {review_id for review_id in reviewer_b_index} != set(key_map):
                issues.append("reviewer_b_review_id_coverage_mismatch")
            if {review_id for review_id in adjudication_index} != set(key_map):
                issues.append("adjudication_review_id_coverage_mismatch")

    if key is not None and reviewer_a_index and reviewer_b_index:
        for review_id in sorted(set(reviewer_a_index) & set(reviewer_b_index)):
            for field in ("label",):
                if field not in reviewer_a_index[review_id] or field not in reviewer_b_index[review_id]:
                    issues.append(f"{review_id}_missing_initial_review_label")
    metrics: dict[str, Any] | None = None
    if key is not None and examples is not None and adjudication_index and not any(
        issue.startswith(("private_key_", "adjudication_review_id_coverage", "examples_line_"))
        for issue in issues
    ):
        adjudications_by_example: dict[str, dict[str, Any]] = {}
        review_to_example = {
            item["review_id"]: item["example_id"]
            for item in key_map.values()
            if isinstance(item.get("example_id"), str)
        }
        reviewer_a_labels: list[str] = []
        reviewer_b_labels: list[str] = []
        comparable_ids = sorted(set(reviewer_a_index) & set(reviewer_b_index) & set(adjudication_index))
        for review_id in comparable_ids:
            reviewer_a_labels.append(reviewer_a_index[review_id].get("label", ""))
            reviewer_b_labels.append(reviewer_b_index[review_id].get("label", ""))
            example_id = review_to_example.get(review_id)
            if example_id is None or example_id not in examples_by_id:
                issues.append(f"{review_id}_missing_example_mapping")
                continue
            adjudication_row = adjudication_index[review_id]
            if adjudication_row.get("disagreement_resolved") is not True:
                issues.append(f"{review_id}_adjudication_not_locked")
            adjudications_by_example[example_id] = adjudication_row
        if len(adjudications_by_example) == len(examples_by_id):
            metrics = {
                "n_independently_reviewed": len(comparable_ids),
                "initial_review_exact_agreement": round(
                    sum(a == b for a, b in zip(reviewer_a_labels, reviewer_b_labels)) / len(comparable_ids), 6
                ) if comparable_ids else None,
                "initial_review_cohen_kappa": _cohen_kappa(reviewer_a_labels, reviewer_b_labels),
                "matcher_diagnostics": _score_metrics(examples_by_id, adjudications_by_example),
                "response_origin_counts": dict(Counter(
                    row.get("response_origin", "<missing>") for row in examples_by_id.values()
                )),
                "matcher_diagnostics_by_response_origin": {
                    origin: _score_metrics(
                        {
                            example_id: example
                            for example_id, example in examples_by_id.items()
                            if example.get("response_origin") == origin
                        },
                        {
                            example_id: adjudications_by_example[example_id]
                            for example_id, example in examples_by_id.items()
                            if example.get("response_origin") == origin and example_id in adjudications_by_example
                        },
                    )
                    for origin in sorted({
                        row.get("response_origin", "<missing>") for row in examples_by_id.values()
                    })
                },
                "labels_by_reviewer": {
                    "reviewer_a": dict(Counter(reviewer_a_labels)),
                    "reviewer_b": dict(Counter(reviewer_b_labels)),
                    "adjudicated": dict(Counter(row.get("label", "") for row in adjudications_by_example.values())),
                },
            }

    if metrics is not None:
        readiness = manifest.get("readiness_policy", {})
        minimum_agreement = readiness.get("minimum_initial_reviewer_exact_agreement")
        minimum_kappa = readiness.get("minimum_initial_reviewer_cohen_kappa")

        valid_agreement_threshold = (
            isinstance(minimum_agreement, (int, float))
            and not isinstance(minimum_agreement, bool)
            and math.isfinite(minimum_agreement)
            and 0 <= minimum_agreement <= 1
        )
        if not valid_agreement_threshold:
            issues.append("invalid_minimum_initial_reviewer_exact_agreement")
        elif minimum_agreement < PROTOCOL_MIN_INITIAL_REVIEW_EXACT_AGREEMENT:
            issues.append(
                "minimum_initial_reviewer_exact_agreement_below_protocol_floor: "
                f"{minimum_agreement} < {PROTOCOL_MIN_INITIAL_REVIEW_EXACT_AGREEMENT}"
            )
        elif (
            metrics["initial_review_exact_agreement"] is None
            or metrics["initial_review_exact_agreement"] < minimum_agreement
        ):
            issues.append(
                "initial_reviewer_exact_agreement_below_threshold: "
                f"{metrics['initial_review_exact_agreement']} < {minimum_agreement}"
            )

        valid_kappa_threshold = (
            isinstance(minimum_kappa, (int, float))
            and not isinstance(minimum_kappa, bool)
            and math.isfinite(minimum_kappa)
            and 0 <= minimum_kappa <= 1
        )
        if not valid_kappa_threshold:
            issues.append("invalid_minimum_initial_reviewer_cohen_kappa")
        elif minimum_kappa < PROTOCOL_MIN_INITIAL_REVIEW_COHEN_KAPPA:
            issues.append(
                "minimum_initial_reviewer_cohen_kappa_below_protocol_floor: "
                f"{minimum_kappa} < {PROTOCOL_MIN_INITIAL_REVIEW_COHEN_KAPPA}"
            )
        elif (
            metrics["initial_review_cohen_kappa"] is None
            or metrics["initial_review_cohen_kappa"] < minimum_kappa
        ):
            issues.append(
                "initial_reviewer_cohen_kappa_below_threshold: "
                f"{metrics['initial_review_cohen_kappa']} < {minimum_kappa}"
            )
        matcher = metrics["matcher_diagnostics"]
        sensitivity = matcher["matcher_sensitivity"]
        specificity = matcher["matcher_specificity"]
        metrics["legacy_alias_matcher_decision"] = {
            "sensitivity": sensitivity,
            "specificity": specificity,
            "meets_0_90_sensitivity_and_specificity_diagnostic_threshold": (
                sensitivity is not None and specificity is not None
                and sensitivity >= 0.90 and specificity >= 0.90
            ),
            "primary_endpoint_recommendation": "Use blinded source-grounded human adjudication for the next study; do not keep literal alias matching as the semantic primary endpoint solely because this finite calibration set scores well.",
        }

    if manifest.get("status") != "adjudicated" or manifest.get("frozen") is not True:
        issues.append("manifest_not_frozen_after_adjudication")
    freeze_metadata = manifest.get("freeze_metadata", {})
    for field in ("frozen_at_utc", "rubric_version", "adjudication_commit"):
        if not freeze_metadata.get(field):
            issues.append(f"freeze_metadata_missing_{field}")

    return {
        "status": "blocked" if issues else "pass",
        "ready_for_new_confirmatory_inference": not issues and metrics is not None,
        "protocol_version": "scoring-calibration-v1",
        "manifest_status": manifest.get("status"),
        "example_count": len(examples) if examples is not None else 0,
        "challenge_class_counts": dict(Counter(
            row.get("challenge_class", "<missing>") for row in examples or []
        )),
        "response_origin_counts": dict(Counter(
            row.get("response_origin", "<missing>") for row in examples or []
        )),
        "metrics": metrics,
        "issue_count": len(issues),
        "issues": issues,
        "interpretation": (
            "This gate can document finite-set matcher behaviour and reviewer agreement. "
            "It cannot establish universal semantic validity or alter any frozen historical score."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed gate for independent, source-grounded scoring calibration.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--examples", type=Path)
    parser.add_argument("--reviewer-a", type=Path)
    parser.add_argument("--reviewer-b", type=Path)
    parser.add_argument("--adjudication", type=Path)
    parser.add_argument("--key", type=Path, default=Path("/tmp/scoring-calibration/review_key_private.json"))
    parser.add_argument("--pilot-manifest", type=Path, default=ROOT / "data" / "pilot" / "pilot_manifest.json")
    parser.add_argument("--benchmark-manifest", type=Path, default=ROOT / "data" / "benchmark" / "benchmark_manifest.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = audit_calibration(
        manifest_path=args.manifest,
        examples_path=args.examples,
        reviewer_a_path=args.reviewer_a,
        reviewer_b_path=args.reviewer_b,
        adjudication_path=args.adjudication,
        key_path=args.key,
        pilot_manifest_path=args.pilot_manifest,
        benchmark_manifest_path=args.benchmark_manifest,
    )
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
