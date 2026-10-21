#!/usr/bin/env python3
"""Read-only, fail-closed readiness check. Never loads or queries a model."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HASHES = {
    "prompt_conditions": "PROMPT_CONDITIONS.md",
    "output_schema": "OUTPUT_SCHEMA.json",
    "analysis_plan": "ANALYSIS_PLAN_STAGE3.md",
    "design": "STAGE3_EXPERIMENT_DESIGN.md",
    "scoring_rubric": "RUBRIC_AND_ADJUDICATION.md",
    "runtime_lock": "RUNTIME_LOCK.json",
    "case_registry": "CASE_REGISTRY.json",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
LEVELS = ("E1_sufficient", "E2_partial", "E3_insufficient")


def read_json(path, label, blockers):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blockers.append("Missing or invalid JSON: " + label + " (" + str(exc) + ")")
        return None
    if not isinstance(value, dict):
        blockers.append(label + " must be a JSON object")
        return None
    return value


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(root):
    project = root / "research_candidates" / "evidence_abstention"
    blockers, warnings = [], []
    manifest = read_json(project / "EXPERIMENT_MANIFEST_STAGE3.json", "experiment manifest", blockers)
    registry = read_json(project / "CASE_REGISTRY.json", "case registry", blockers)
    runtime = read_json(project / "RUNTIME_LOCK.json", "runtime lock", blockers)
    schema = read_json(project / "OUTPUT_SCHEMA.json", "output schema", blockers)

    for name, relpath in HASHES.items():
        if not (project / relpath).is_file():
            blockers.append("Required hash target missing: " + relpath)

    if manifest is not None:
        checks = (
            (manifest.get("inference_allowed") is True, "Manifest does not explicitly authorize inference."),
            (manifest.get("dataset_validation_gate") == "CLOSED", "Dataset validation gate is not CLOSED."),
            (manifest.get("preregistration_status") == "registered" and bool(manifest.get("preregistration_uri")), "Protocol has no verifiable preregistration URI."),
            (manifest.get("two_rater_protocol_frozen") is True, "Two-rater rubric/adjudication protocol is not frozen."),
            (manifest.get("reviewer_calibration_complete") is True, "Independent reviewer calibration is incomplete."),
        )
        blockers.extend(message for ok, message in checks if not ok)

        model = manifest.get("model")
        if not isinstance(model, dict) or not model.get("id") or not model.get("revision"):
            blockers.append("Immutable model ID/revision is missing.")
        else:
            if model.get("runtime_verification") != "passed":
                blockers.append("Exact model/tokenizer/runtime load preflight has not passed.")
            if model.get("quantization") != "none":
                blockers.append("The candidate must be the reviewed non-quantized checkpoint.")

        frozen = manifest.get("frozen_hashes")
        if not isinstance(frozen, dict):
            frozen = {}
            blockers.append("Manifest frozen_hashes must be an object.")
        for name, relpath in HASHES.items():
            expected, path = frozen.get(name), project / relpath
            if not isinstance(expected, str) or not HEX64.fullmatch(expected):
                blockers.append("Frozen SHA-256 missing/invalid: " + name)
            elif path.is_file() and sha256(path) != expected:
                blockers.append("Frozen SHA-256 mismatch: " + name)

    accepted = []
    if registry is not None:
        records = registry.get("records", [])
        if not isinstance(records, list):
            blockers.append("Case registry records must be a list.")
            records = []
        seen = set()
        for record in records:
            if not isinstance(record, dict) or not isinstance(record.get("case_id"), str):
                blockers.append("Every case registry entry must be an object with case_id.")
                continue
            cid = record["case_id"]
            if cid in seen:
                blockers.append("Duplicate case ID: " + cid)
            seen.add(cid)
            if record.get("accepted_for_confirmatory") is True:
                accepted.append(record)
                required = ("upstream_project", "source_repository", "license_reference", "buggy_commit",
                            "fixed_commit", "test_command", "runtime_fingerprint")
                for field in required:
                    if not record.get(field):
                        blockers.append(cid + ": required field missing: " + field)
                for field in ("license_reviewed", "leakage_reviewed", "prior_exposure_clearance"):
                    if record.get(field) is not True:
                        blockers.append(cid + ": gate not passed: " + field)
                if record.get("buggy_commit") == record.get("fixed_commit"):
                    blockers.append(cid + ": buggy and fixed commits must differ.")
                if record.get("ground_truth_reviewers", 0) < 2 or record.get("evidence_reviewers", 0) < 2:
                    blockers.append(cid + ": at least two independent reviewers are required for ground truth and evidence sufficiency.")
                for field in ("buggy_test_log_sha256", "fixed_test_log_sha256"):
                    if not isinstance(record.get(field), str) or not HEX64.fullmatch(record[field]):
                        blockers.append(cid + ": missing/invalid " + field)
                packets = record.get("evidence_packet_sha256", {})
                for level in LEVELS:
                    if not isinstance(packets, dict) or not isinstance(packets.get(level), str) or not HEX64.fullmatch(packets[level]):
                        blockers.append(cid + ": missing/invalid packet hash for " + level)

        if manifest is not None:
            ids = [case["case_id"] for case in accepted]
            if manifest.get("case_ids") != ids:
                blockers.append("Manifest case_ids do not exactly match the ordered accepted registry IDs.")
            projects = {case.get("upstream_project") for case in accepted if case.get("upstream_project")}
            minimum, min_projects = manifest.get("minimum_confirmatory_cases", 60), manifest.get("minimum_upstream_projects", 8)
            target, cells = manifest.get("target_independent_cases", 80), manifest.get("cells_per_case", 6)
            if len(accepted) < minimum:
                blockers.append("Only " + str(len(accepted)) + " accepted independent cases; minimum is " + str(minimum) + " and target is " + str(target) + ".")
            if len(projects) < min_projects:
                blockers.append("Only " + str(len(projects)) + " upstream projects; minimum is " + str(min_projects) + ".")
            if manifest.get("planned_model_outputs_at_target") != target * cells:
                blockers.append("Target output count must equal target cases multiplied by cells per case.")

    if schema is not None:
        required = {"decision", "root_cause", "evidence_refs", "rationale", "alternative_hypotheses", "missing_evidence"}
        if schema.get("type") != "object" or not required.issubset(set(schema.get("required", []))):
            blockers.append("Output schema lacks required diagnosis/abstention fields.")
    if runtime is not None:
        if runtime.get("status") != "verified_for_this_study":
            blockers.append("Runtime lock is not verified for this study.")
        if runtime.get("inference_performed") is not False:
            blockers.append("Runtime lock must record inference_performed=false during preflight.")

    return {
        "project": "Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ",
        "mode": "read_only_preflight_no_model_execution",
        "ready": not blockers,
        "accepted_case_count": len(accepted),
        "accepted_project_count": len({c.get("upstream_project") for c in accepted if c.get("upstream_project")}),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "warnings": warnings,
        "model_inference_performed": False,
        "next_action": "Resolve every blocker and review separate authorization before any inference." if blockers else "Checks pass; this report itself does not authorize inference.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args(argv)
    report = evaluate(args.root.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if args.require_ready and not report["ready"] else 0


if __name__ == "__main__":
    sys.exit(main())
