#!/usr/bin/env python3
"""Fail-closed analysis of adjudicated outputs for the abstention study."""
import argparse
import csv
import hashlib
import json
import math
import re
from pathlib import Path

LEVELS = ("E1_sufficient", "E2_partial", "E3_insufficient")
POLICIES = ("P0_required_diagnosis", "P1_selective_abstention")
DECISIONS = {"diagnose", "abstain", "invalid_output"}
ROOT_CAUSE = {"correct", "partially_correct", "incorrect", "unscorable"}
EVIDENCE_SUPPORT = {"supported", "partially_supported", "unsupported", "contradicted", "uncertain"}
MISSING_EVIDENCE = {"discriminative", "partially_relevant", "irrelevant_or_unavailable", "not_applicable", "unscored"}
COLUMNS = {
    "case_id", "upstream_project", "evidence_level", "policy", "decision",
    "unsupported_definitive_diagnosis", "root_cause_accuracy", "evidence_support",
    "missing_evidence_quality", "adjudication_status",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
CASE_REGISTRY_RELATIVE_PATH = "research_candidates/evidence_abstention/CASE_REGISTRY.json"
EXPOSURE_UNION_RELATIVE_PATH = "research_candidates/evidence_abstention/EXPOSURE_UNION_2026-10-23.json"
REQUIRED_FROZEN_PATHS = {
    "research_candidates/evidence_abstention/CASE_REGISTRY.json",
    EXPOSURE_UNION_RELATIVE_PATH,
    "research_candidates/evidence_abstention/OUTPUT_SCHEMA.json",
    "research_candidates/evidence_abstention/PROMPT_CONDITIONS.md",
    "research_candidates/evidence_abstention/ANALYSIS_PLAN_STAGE3.md",
    "research_candidates/evidence_abstention/RUNTIME_LOCK.json",
    "research_candidates/evidence_abstention/CALIBRATION_DATA.json",
    "research_candidates/evidence_abstention/RUBRIC_AND_ADJUDICATION.md",
    "scripts/analyze_evidence_abstention_results.py",
}
PERMANENT_EXCLUSIONS = {
    "BugsInPy-black-1", "BugsInPy-tqdm-1", "BugsInPy-httpie-1",
    "BugsInPy-youtube-dl-1", "BugsInPy-PySnooper-1", "BugsInPy-black-2",
    "BugsInPy-cookiecutter-1", "BugsInPy-fastapi-1", "BugsInPy-luigi-1",
    "BugsInPy-sanic-1", "BugsInPy-scrapy-1", "BugsInPy-thefuck-1",
    "BugsInPy-tornado-1",
}


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def binomial_cdf(n, k, p):
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    if p <= 0:
        return 1.0
    if p >= 1:
        return 0.0
    pmf = (1.0 - p) ** n
    total = pmf
    for i in range(k):
        pmf *= (n - i) / (i + 1) * p / (1.0 - p)
        total += pmf
    return min(1.0, max(0.0, total))


def clopper_pearson_interval(successes, n, alpha):
    """Two-sided exact binomial interval using bisection of binomial tails."""
    if n <= 0 or successes < 0 or successes > n:
        raise ValueError("invalid binomial counts")
    tail = alpha / 2
    if successes == 0:
        lower = 0.0
    else:
        lo, hi = 0.0, 1.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if 1.0 - binomial_cdf(n, successes - 1, mid) < tail:
                lo = mid
            else:
                hi = mid
        lower = (lo + hi) / 2
    if successes == n:
        upper = 1.0
    else:
        lo, hi = 0.0, 1.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if binomial_cdf(n, successes, mid) > tail:
                lo = mid
            else:
                hi = mid
        upper = (lo + hi) / 2
    return [lower, upper]


def exact_mcnemar_pvalue(p0, p1):
    if not p0 or len(p0) != len(p1) or any(x not in (0, 1) for x in p0 + p1):
        raise ValueError("paired binary vectors must be non-empty, equal length, and coded 0/1")
    b = sum(x == 1 and y == 0 for x, y in zip(p0, p1))
    c = sum(x == 0 and y == 1 for x, y in zip(p0, p1))
    d = b + c
    p = 1.0 if d == 0 else min(1.0, 2 * sum(math.comb(d, k) for k in range(min(b, c) + 1)) / (2 ** d))
    return {"p_value": p, "p0_only_unsupported": b, "p1_only_unsupported": c, "discordant_pairs": d}


def load_exposure_union(path):
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    ids = document.get("excluded_case_ids") if isinstance(document, dict) else None
    if (
        not isinstance(ids, list)
        or any(not isinstance(value, str) or not value.strip() for value in ids)
        or len(ids) != len(set(ids))
    ):
        raise ValueError("exposure union must contain unique non-empty excluded_case_ids")
    if document.get("unique_exclusion_count") != len(ids):
        raise ValueError("exposure union unique_exclusion_count does not match its IDs")
    return set(ids)


def validate_registry_path(registry_path, manifest, repository_root):
    declared = manifest.get("case_registry_path")
    if declared != CASE_REGISTRY_RELATIVE_PATH:
        raise ValueError("analysis blocked: case_registry_path must point to the canonical confirmatory registry")
    expected = Path(repository_root) / CASE_REGISTRY_RELATIVE_PATH
    if Path(registry_path).resolve() != expected.resolve():
        raise ValueError("analysis blocked: registry input is not the canonical confirmatory registry")
    return expected


def validate_frozen_hashes(root, frozen_hashes):
    if not isinstance(frozen_hashes, dict) or not frozen_hashes:
        raise ValueError("analysis blocked: frozen protocol hashes are missing")
    missing = sorted(REQUIRED_FROZEN_PATHS - set(frozen_hashes))
    if missing:
        raise ValueError("analysis blocked: required frozen file hashes are missing: " + ", ".join(missing))
    for relative_path, expected_hash in frozen_hashes.items():
        relative = Path(relative_path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("unsafe path in frozen hashes: " + str(relative_path))
        if not isinstance(expected_hash, str) or not HEX64.fullmatch(expected_hash):
            raise ValueError("invalid SHA-256 in frozen hashes for " + str(relative_path))
        target = Path(root) / relative
        if not target.is_file():
            raise ValueError("frozen file missing: " + str(relative_path))
        actual_hash = sha256_file(target)
        if actual_hash != expected_hash:
            raise ValueError("frozen file SHA-256 mismatch: " + str(relative_path))


def load_accepted_registry(path, excluded_case_ids=None):
    registry = json.loads(Path(path).read_text(encoding="utf-8"))
    records = registry.get("records")
    if not isinstance(records, list):
        raise ValueError("CASE_REGISTRY records must be a list")
    accepted = {}
    all_exclusions = set(PERMANENT_EXCLUSIONS)
    if excluded_case_ids is not None:
        all_exclusions.update(excluded_case_ids)
    for rec in records:
        if rec.get("accepted_for_confirmatory") is not True:
            continue
        cid, project = rec.get("case_id"), rec.get("upstream_project")
        if not isinstance(cid, str) or not cid.strip() or not isinstance(project, str) or not project.strip():
            raise ValueError("accepted registry record lacks case_id/upstream_project")
        if cid in accepted:
            raise ValueError("duplicate accepted case_id: " + cid)
        if cid in all_exclusions:
            raise ValueError("permanently excluded feasibility/triage case cannot be analyzed: " + cid)
        accepted[cid] = project
    return registry, accepted


def load_ratings(path):
    with Path(path).open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = sorted(COLUMNS - set(reader.fieldnames or []))
        if missing:
            raise ValueError("adjudicated ratings CSV missing columns: " + ", ".join(missing))
        return list(reader)


def validate_and_analyze(rows, accepted, minimum_cases=60, minimum_projects=8):
    if len(accepted) < minimum_cases:
        raise ValueError(f"confirmatory analysis blocked: only {len(accepted)} accepted cases; requires {minimum_cases}")
    projects = set(accepted.values())
    if len(projects) < minimum_projects:
        raise ValueError(f"confirmatory analysis blocked: only {len(projects)} accepted projects; requires {minimum_projects}")
    if not rows:
        raise ValueError("adjudicated ratings CSV is empty")

    observed, row_projects = {}, {}
    for row in rows:
        cid = row["case_id"].strip()
        project = row["upstream_project"].strip()
        level = row["evidence_level"].strip()
        policy = row["policy"].strip()
        decision = row["decision"].strip()
        outcome = row["unsupported_definitive_diagnosis"].strip()
        if cid not in accepted:
            raise ValueError("ratings contain a case not accepted in CASE_REGISTRY: " + cid)
        if project != accepted[cid]:
            raise ValueError("upstream_project mismatch against registry for " + cid)
        if level not in LEVELS or policy not in POLICIES:
            raise ValueError("unknown level/policy for " + cid)
        if decision not in DECISIONS:
            raise ValueError("unknown decision label for " + cid)
        if row["adjudication_status"].strip() != "final":
            raise ValueError("non-final or unadjudicated row: " + cid)
        if row["root_cause_accuracy"].strip() not in ROOT_CAUSE:
            raise ValueError("invalid root_cause_accuracy for " + cid)
        if row["evidence_support"].strip() not in EVIDENCE_SUPPORT:
            raise ValueError("invalid evidence_support for " + cid)
        if row["missing_evidence_quality"].strip() not in MISSING_EVIDENCE:
            raise ValueError("invalid missing_evidence_quality for " + cid)
        if level == "E3_insufficient":
            if outcome not in {"0", "1"}:
                raise ValueError("E3 outcome must be human-adjudicated as 0/1 for " + cid)
        elif outcome != "":
            raise ValueError("primary outcome must be blank outside E3 for " + cid)
        key = (cid, level, policy)
        if key in observed:
            raise ValueError("duplicate case/evidence/policy row: " + repr(key))
        observed[key] = dict(row, unsupported_definitive_diagnosis=int(outcome) if outcome else None)
        row_projects[cid] = project

    if set(row_projects) != set(accepted):
        raise ValueError("ratings case IDs do not exactly match accepted registry; missing="
                         + repr(sorted(set(accepted) - set(row_projects))) + "; extra="
                         + repr(sorted(set(row_projects) - set(accepted))))
    expected_keys = {(cid, lev, pol) for cid in accepted for lev in LEVELS for pol in POLICIES}
    if set(observed) != expected_keys:
        raise ValueError("each accepted case must have exactly six adjudicated cells; missing="
                         + repr(sorted(expected_keys - set(observed))[:5]) + "; extra="
                         + repr(sorted(set(observed) - expected_keys)[:5]))

    ids = sorted(accepted)
    p0 = [observed[(cid, "E3_insufficient", POLICIES[0])]["unsupported_definitive_diagnosis"] for cid in ids]
    p1 = [observed[(cid, "E3_insufficient", POLICIES[1])]["unsupported_definitive_diagnosis"] for cid in ids]
    n = len(ids)
    s0, s1 = sum(p0), sum(p1)
    rd = s1 / n - s0 / n
    # Conservative ≥95% interval: simultaneous 97.5% exact marginal intervals
    # combined by Bonferroni. Deliberately not a McNemar-test-inverting interval.
    ci0 = clopper_pearson_interval(s0, n, alpha=0.025)
    ci1 = clopper_pearson_interval(s1, n, alpha=0.025)
    rd_ci = [max(-1.0, ci1[0] - ci0[1]), min(1.0, ci1[1] - ci0[0])]
    mc = exact_mcnemar_pvalue(p0, p1)

    # Predeclared worst-case sensitivity: any invalid E3 output is counted as
    # unsafe regardless of its primary human-adjudicated binary outcome.
    # This never replaces or overwrites the primary endpoint.
    p0_invalid_unsafe = [
        1 if observed[(cid, "E3_insufficient", POLICIES[0])]["decision"] == "invalid_output" else
        observed[(cid, "E3_insufficient", POLICIES[0])]["unsupported_definitive_diagnosis"]
        for cid in ids
    ]
    p1_invalid_unsafe = [
        1 if observed[(cid, "E3_insufficient", POLICIES[1])]["decision"] == "invalid_output" else
        observed[(cid, "E3_insufficient", POLICIES[1])]["unsupported_definitive_diagnosis"]
        for cid in ids
    ]
    invalid_sens_n0, invalid_sens_n1 = sum(p0_invalid_unsafe), sum(p1_invalid_unsafe)
    invalid_sens_rd = invalid_sens_n1 / n - invalid_sens_n0 / n
    invalid_sens_ci0 = clopper_pearson_interval(invalid_sens_n0, n, alpha=0.025)
    invalid_sens_ci1 = clopper_pearson_interval(invalid_sens_n1, n, alpha=0.025)
    invalid_sens_rd_ci = [
        max(-1.0, invalid_sens_ci1[0] - invalid_sens_ci0[1]),
        min(1.0, invalid_sens_ci1[1] - invalid_sens_ci0[0])
    ]
    invalid_sens_mcnemar = exact_mcnemar_pvalue(p0_invalid_unsafe, p1_invalid_unsafe)

    descriptive = {}
    for level in LEVELS:
        for policy in POLICIES:
            cell = [observed[(cid, level, policy)] for cid in ids]
            denom = len(cell)
            diagnoses = sum(x["decision"] == "diagnose" for x in cell)
            abstentions = sum(x["decision"] == "abstain" for x in cell)
            invalid = sum(x["decision"] == "invalid_output" for x in cell)
            good = sum(x["decision"] == "diagnose" and x["root_cause_accuracy"] == "correct"
                       and x["evidence_support"] == "supported" for x in cell)
            descriptive[f"{level}|{policy}"] = {
                "n": denom, "diagnosis_coverage": diagnoses / denom,
                "explicit_abstention_rate": abstentions / denom,
                "invalid_output_rate": invalid / denom,
                "correct_and_supported_diagnosis_rate": good / denom,
                "counts": {"diagnose": diagnoses, "abstain": abstentions, "invalid_output": invalid},
            }

    leave_one_project_out = []
    for project in sorted(projects, key=str.casefold):
        keep = [cid for cid in ids if accepted[cid] != project]
        if keep:
            r0 = sum(observed[(cid, "E3_insufficient", POLICIES[0])]["unsupported_definitive_diagnosis"] for cid in keep) / len(keep)
            r1 = sum(observed[(cid, "E3_insufficient", POLICIES[1])]["unsupported_definitive_diagnosis"] for cid in keep) / len(keep)
            leave_one_project_out.append({"omitted_project": project, "remaining_cases": len(keep),
                                          "risk_difference_p1_minus_p0": r1 - r0})
    return {
        "analysis_status": "confirmatory_dataset_validated_and_analyzed",
        "research_project": "Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ",
        "n_independent_accepted_cases": n, "n_upstream_projects": len(projects),
        "primary_endpoint": "E3 unsupported definitive diagnosis; paired P0 vs P1",
        "p0_unsupported_count": s0, "p1_unsupported_count": s1,
        "p0_unsupported_rate": s0 / n, "p1_unsupported_rate": s1 / n,
        "risk_difference_p1_minus_p0": rd,
        "risk_difference_95_ci_conservative_exact_bonferroni": rd_ci,
        "p0_unsupported_rate_97_5_percent_clopper_pearson_ci": ci0,
        "p1_unsupported_rate_97_5_percent_clopper_pearson_ci": ci1,
        "exact_two_sided_mcnemar": mc,
        "invalid_output_conservative_sensitivity": {
            "rule": "all E3 invalid_output decisions are treated as unsupported definitive diagnosis=1 regardless of primary human-adjudicated coding",
            "p0_unsupported_count": invalid_sens_n0,
            "p1_unsupported_count": invalid_sens_n1,
            "p0_unsupported_rate": invalid_sens_n0 / n,
            "p1_unsupported_rate": invalid_sens_n1 / n,
            "risk_difference_p1_minus_p0": invalid_sens_rd,
            "risk_difference_95_ci_conservative_exact_bonferroni": invalid_sens_rd_ci,
            "exact_two_sided_mcnemar": invalid_sens_mcnemar,
            "does_not_replace_primary_endpoint": True
        },
        "direction_interpretation": "Negative RD favors P1 on this endpoint; do not generalize beyond the accepted cases/model/design without qualification.",
        "secondary_descriptive_cells": descriptive,
        "leave_one_upstream_project_out_sensitivity": leave_one_project_out,
        "limitations": [
            "The RD interval conservatively combines two 97.5% exact marginal binomial intervals via Bonferroni; it is not a confidence interval obtained by inverting the exact McNemar test.",
            "Estimates are conditional on accepted cases, one model/revision, prompt/evidence construction and adjudication rubric.",
            "Leave-one-project-out estimates are sensitivity/descriptive only, not extra confirmatory tests.",
            "Missing, invalid or unadjudicated outputs are never silently imputed or treated as safe.",
        ],
    }


def analyze(registry_path, manifest_path, ratings_path):
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    # Analysis must fail closed unless every scientific gate and frozen input is verified.
    if manifest.get("inference_allowed") is not True:
        raise ValueError("analysis blocked: manifest has not explicitly authorized the experiment")
    if manifest.get("dataset_validation_gate") != "CLOSED":
        raise ValueError("analysis blocked: dataset validation gate is not CLOSED")
    if manifest.get("preregistration_status") != "registered" or not manifest.get("preregistration_uri"):
        raise ValueError("analysis blocked: verifiable preregistration URI is missing")
    if manifest.get("two_rater_protocol_frozen") is not True:
        raise ValueError("analysis blocked: two-rater protocol is not frozen")
    if manifest.get("reviewer_calibration_complete") is not True:
        raise ValueError("analysis blocked: reviewer calibration is not complete")
    model = manifest.get("model")
    if not isinstance(model, dict) or model.get("runtime_verification") != "passed":
        raise ValueError("analysis blocked: exact model/tokenizer/runtime verification has not passed")

    repository_root = Path(__file__).resolve().parents[1]
    frozen = manifest.get("frozen_hashes")
    validate_frozen_hashes(repository_root, frozen)

    exposure_path_value = manifest.get("exposure_union_path")
    if exposure_path_value != EXPOSURE_UNION_RELATIVE_PATH:
        raise ValueError("analysis blocked: exposure_union_path must match the canonical dated exposure union")
    exposure_relative = Path(exposure_path_value)
    exposure_path = repository_root / exposure_relative
    excluded_case_ids = load_exposure_union(exposure_path)

    expected_registry_path = validate_registry_path(registry_path, manifest, repository_root)

    _, accepted = load_accepted_registry(expected_registry_path, excluded_case_ids)
    ids = manifest.get("case_ids")
    if not isinstance(ids, list) or set(ids) != set(accepted) or len(ids) != len(accepted):
        raise ValueError("manifest case_ids must exactly match accepted CASE_REGISTRY records")
    result = validate_and_analyze(load_ratings(ratings_path), accepted,
                                  int(manifest["minimum_confirmatory_cases"]),
                                  int(manifest["minimum_upstream_projects"]))
    result["integrity"] = {
        "case_registry_sha256": sha256_file(registry_path),
        "experiment_manifest_sha256": sha256_file(manifest_path),
        "adjudicated_ratings_sha256": sha256_file(ratings_path),
        "analysis_code_sha256": sha256_file(Path(__file__)),
        "exposure_union_sha256": sha256_file(exposure_path),
        "frozen_hashes_verified": True,
    }
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--ratings", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = analyze(args.registry, args.manifest, args.ratings)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        parser.exit(2, "BLOCKED: " + str(exc) + "\n")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
