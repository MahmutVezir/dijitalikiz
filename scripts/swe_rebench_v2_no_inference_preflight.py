#!/usr/bin/env python3
"""Read-only, fail-closed readiness report for SWE-rebench V2; never loads a model."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "research_candidates" / "evidence_abstention" / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from swe_rebench_v2_contract import validate_manifest, validate_output_schema  # noqa: E402
from swe_rebench_v2_case_acceptance import validate_registry  # noqa: E402

TRACK = ROOT / "research_candidates" / "evidence_abstention"
MANIFEST_PATH = TRACK / "SWE_REBENCH_V2_EXPERIMENT_MANIFEST_V0_1.json"
REGISTRY_PATH = TRACK / "SWE_REBENCH_V2_CASE_REGISTRY_V0_1.json"
OUTPUT_SCHEMA_PATH = TRACK / "SWE_REBENCH_V2_OUTPUT_SCHEMA_V0_1.json"
CASE_SCHEMA_PATH = TRACK / "SWE_REBENCH_V2_CASE_ACCEPTANCE_SCHEMA_V0_1.json"
ANALYSIS_PLAN_PATH = TRACK / "SWE_REBENCH_V2_ANALYSIS_PLAN_V0_1.md"
PROTOCOL_PATH = TRACK / "SWE_REBENCH_V2_PROTOCOL_V0_1_DRAFT_2026-11-15.md"
PROMPT_PATH = TRACK / "SWE_REBENCH_V2_PROMPT_CONDITIONS_V0_1.md"
CONTRACT_PATH = IMPLEMENTATION / "swe_rebench_v2_contract.py"
ACCEPTANCE_VALIDATOR_PATH = IMPLEMENTATION / "swe_rebench_v2_case_acceptance.py"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _read_json(path: Path, label: str, blockers: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blockers.append(label + " is missing or invalid JSON: " + str(exc))
        return None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evaluate(root: Path = ROOT) -> dict[str, Any]:
    """Evaluate current V2 draft without reading source dataset or running a model."""
    track = root / "research_candidates" / "evidence_abstention"
    implementation = track / "implementation"
    paths = {
        "manifest": track / "SWE_REBENCH_V2_EXPERIMENT_MANIFEST_V0_1.json",
        "registry": track / "SWE_REBENCH_V2_CASE_REGISTRY_V0_1.json",
        "output_schema": track / "SWE_REBENCH_V2_OUTPUT_SCHEMA_V0_1.json",
        "case_acceptance_schema": track / "SWE_REBENCH_V2_CASE_ACCEPTANCE_SCHEMA_V0_1.json",
        "analysis_plan": track / "SWE_REBENCH_V2_ANALYSIS_PLAN_V0_1.md",
        "protocol": track / "SWE_REBENCH_V2_PROTOCOL_V0_1_DRAFT_2026-11-15.md",
        "prompt_conditions": track / "SWE_REBENCH_V2_PROMPT_CONDITIONS_V0_1.md",
        "response_contract": implementation / "swe_rebench_v2_contract.py",
        "case_acceptance_validator": implementation / "swe_rebench_v2_case_acceptance.py",
        "response_contract_tests": implementation / "test_swe_rebench_v2_contract.py",
        "case_acceptance_tests": implementation / "test_swe_rebench_v2_case_acceptance.py",
    }
    blockers: list[str] = []
    hashes: dict[str, str | None] = {}
    for label, path in paths.items():
        if not path.is_file():
            blockers.append("Required V2 artifact is missing: " + label + " (" + str(path.relative_to(root)) + ")")
            hashes[label] = None
        else:
            hashes[label] = _sha256(path)

    manifest = _read_json(paths["manifest"], "V2 experiment manifest", blockers)
    registry = _read_json(paths["registry"], "V2 case registry", blockers)
    output_schema = _read_json(paths["output_schema"], "V2 response schema", blockers)
    case_schema = _read_json(paths["case_acceptance_schema"], "V2 case acceptance schema", blockers)

    manifest_audit = validate_manifest(manifest) if manifest is not None else {
        "status": "invalid", "blockers": ["manifest unavailable"], "inference_authorized": False
    }
    blockers.extend("Manifest contract: " + item for item in manifest_audit["blockers"])

    registry_audit = validate_registry(registry) if registry is not None else {
        "status": "invalid", "blockers": ["registry unavailable"],
        "accepted_case_count": 0, "accepted_project_count": 0, "inference_authorized": False,
    }
    blockers.extend("Case registry: " + item for item in registry_audit["blockers"])

    if output_schema is not None:
        try:
            validate_output_schema(output_schema)
        except (TypeError, ValueError) as exc:
            blockers.append("Response output schema failed contract validation: " + str(exc))

    if case_schema is not None:
        if not isinstance(case_schema, dict):
            blockers.append("Case acceptance schema must be a JSON object.")
        else:
            required_sections = {
                "case_id", "acceptance_state", "dataset", "source", "independence",
                "exposure", "license_review", "technical_reproduction", "gold_standard",
                "evidence_tiers", "external_audit",
            }
            if case_schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                blockers.append("Case acceptance schema must identify JSON Schema 2020-12.")
            if case_schema.get("type") != "object" or case_schema.get("additionalProperties") is not False:
                blockers.append("Case acceptance schema must be a closed JSON object.")
            if not required_sections.issubset(set(case_schema.get("required", []))):
                blockers.append("Case acceptance schema is missing one or more required case sections.")
            props = case_schema.get("properties", {})
            if not isinstance(props, dict) or "prior_pipeline_debug_exposure_status" not in props.get("exposure", {}).get("required", []) or "external_audit" not in case_schema.get("required", []):
                blockers.append("Case acceptance schema does not enforce prior pipeline/debug exposure and independent external audit attestation.")

    if isinstance(manifest, dict):
        dataset = manifest.get("dataset", {})
        design = manifest.get("design", {})
        model = manifest.get("model", {})
        human = manifest.get("human_review", {})
        prereg = manifest.get("preregistration", {})
        generation = manifest.get("generation", {})
        if not isinstance(dataset, dict):
            dataset = {}
        if not isinstance(design, dict):
            design = {}
        if not isinstance(model, dict):
            model = {}
        if not isinstance(human, dict):
            human = {}
        if not isinstance(prereg, dict):
            prereg = {}
        if not isinstance(generation, dict):
            generation = {}

        if manifest.get("dataset_validation_gate") != "CLOSED":
            blockers.append("Dataset validation gate is not CLOSED.")
        if dataset.get("underlying_source_license_review") not in {"PASSED", "CLOSED"}:
            blockers.append("Exact-base and changed-file source-license review is still open.")
        if dataset.get("created_at_timezone_assumption_review") not in {"confirmed", "confirmed_utc", "passed"}:
            blockers.append("Dataset created_at timezone semantics are not confirmed.")
        if model.get("license_review_status") != "approved":
            blockers.append("Exact immutable model-revision license review is not approved.")
        if model.get("runtime_verification") != "passed":
            blockers.append("Exact model/tokenizer/runtime verification has not passed.")
        if human.get("rubric_approved") is not True:
            blockers.append("Human scoring rubric has not been approved.")
        if human.get("calibration_complete") is not True:
            blockers.append("Independent Panel A/Panel B calibration has not been completed.")
        if human.get("reviewer_consent_status") != "approved":
            blockers.append("Reviewer consent status is not approved.")
        if human.get("institutional_approval_status") != "approved":
            blockers.append("Institutional/mentor approval status is not approved or documented as not required.")
        if generation.get("status") != "frozen":
            blockers.append("Generation settings are still draft and not frozen.")
        if prereg.get("status") != "registered" or not isinstance(prereg.get("external_uri"), str) or not prereg.get("external_uri", "").startswith("https://"):
            blockers.append("External preregistration is not registered with a verifiable HTTPS URI.")
        if prereg.get("hash_freeze_complete") is not True:
            blockers.append("Protocol and analysis artifact hashes are not frozen.")
        frozen = manifest.get("frozen_artifacts")
        if not isinstance(frozen, list) or not frozen:
            blockers.append("Manifest frozen_artifacts must be a non-empty list.")
        else:
            for index, item in enumerate(frozen):
                if not isinstance(item, dict):
                    blockers.append("Frozen artifact record " + str(index) + " is malformed.")
                    continue
                digest = item.get("sha256")
                if item.get("status") not in {"frozen", "reviewed_and_frozen"} or not isinstance(digest, str) or HEX64.fullmatch(digest) is None:
                    blockers.append("Frozen artifact " + str(index) + " is not frozen with a valid SHA-256.")
        if manifest.get("case_registry_path") != "research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_REGISTRY_V0_1.json":
            blockers.append("Manifest points to a non-canonical V2 case registry.")
        if manifest.get("accepted_case_count") != registry_audit.get("accepted_case_count"):
            blockers.append("Manifest accepted_case_count differs from V2 case registry.")
        if manifest.get("accepted_project_count") != registry_audit.get("accepted_project_count"):
            blockers.append("Manifest accepted_project_count differs from V2 case registry.")
        if dataset.get("primary_cohort_csv_sha256") != (registry.get("candidate_cohort_sha256") if isinstance(registry, dict) else None):
            blockers.append("Manifest primary cohort hash differs from the V2 registry cohort pin.")

        minimum = design.get("minimum_independent_cases")
        minimum_projects = design.get("minimum_upstream_projects")
        actual_cases = registry_audit.get("accepted_case_count", 0)
        actual_projects = registry_audit.get("accepted_project_count", 0)
        if not isinstance(minimum, int) or actual_cases < minimum:
            blockers.append("Accepted independent case count " + str(actual_cases) + " is below the confirmatory minimum of " + str(minimum) + ".")
        if not isinstance(minimum_projects, int) or actual_projects < minimum_projects:
            blockers.append("Accepted independent upstream project count " + str(actual_projects) + " is below the minimum of " + str(minimum_projects) + ".")

        # No readiness report can authorize execution; these remain false in this track.
        for field in ("model_loading_performed", "model_inference_performed", "fine_tuning_performed"):
            if manifest.get(field) is not False:
                blockers.append(field + " must remain false in the no-inference draft.")
        if manifest.get("inference_allowed") is not False:
            blockers.append("inference_allowed must remain false in the no-inference draft.")

    accepted_cases = registry_audit.get("accepted_case_count", 0)
    accepted_projects = registry_audit.get("accepted_project_count", 0)
    return {
        "project": "Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ",
        "track": "SWE-rebench-V2",
        "mode": "read_only_preflight_no_model_execution",
        "ready": not blockers,
        "accepted_case_count": accepted_cases,
        "accepted_project_count": accepted_projects,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "artifact_sha256": hashes,
        "model_loading_performed": False,
        "model_inference_performed": False,
        "fine_tuning_performed": False,
        "inference_authorized": False,
        "next_action": (
            "Resolve every blocker, externally audit the records, freeze the protocol and obtain explicit authorization. "
            "This report never grants inference permission."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args(argv)
    report = evaluate(args.root.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if args.require_ready and not report["ready"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
