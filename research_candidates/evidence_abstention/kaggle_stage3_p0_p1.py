#!/usr/bin/env python3
"""Fail-closed Qwen runner for the preregistered Stage 3 policy experiment."""
import argparse
import csv
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import platform
import random
import secrets
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"
MODEL_REVISION = "aa8e72537993ba99e69dfaafa59ed015b17504d1"
DEFAULT_ROOT = Path(__file__).resolve().parents[2]
CASES_PATH = Path(os.getenv("EVIDENCE_CASES_PATH", "/kaggle/input/evidence-abstention/cases.json"))
RAW_OUTPUTS_PATH = Path(os.getenv("EVIDENCE_RAW_OUTPUTS_PATH", "/kaggle/working/raw_model_outputs.jsonl"))
BLIND_REVIEW_PATH = Path(os.getenv("EVIDENCE_BLIND_REVIEW_PATH", "/kaggle/working/blind_review_packet.jsonl"))
CONDITION_MAP_PATH = Path(os.getenv("EVIDENCE_CONDITION_MAP_PATH", "/kaggle/working/restricted_condition_codebook.csv"))
ANSWER_KEY_PATH = Path(os.getenv("EVIDENCE_ANSWER_KEY_PATH", "/kaggle/working/restricted_answer_key.csv"))
RUN_METADATA_PATH = Path(os.getenv("EVIDENCE_RUN_METADATA_PATH", "/kaggle/working/run_metadata.json"))
RUNTIME_REPORT_PATH = Path(os.getenv("EVIDENCE_RUNTIME_REPORT_PATH", "/kaggle/working/runtime_preflight_report.json"))
CONDITION_ORDER_SEED = 20261023
BLIND_ORDER_SEED = 20261024
LEVELS = ("E1", "E2", "E3")
LEVEL_TO_REGISTRY_KEY = {
    "E1": "E1_sufficient",
    "E2": "E2_partial",
    "E3": "E3_insufficient",
}
POLICY_INSTRUCTIONS = {
    "P0": (
        "Choose and state one single most likely root cause. Do not abstain. "
        "If the evidence is incomplete, still give the most likely diagnosis and "
        "identify which supplied evidence led you to it."
    ),
    "P1": (
        "Give a root-cause diagnosis only when the evidence packet sufficiently "
        "supports and distinguishes it from plausible alternatives. If the packet "
        "is insufficient or contradictory, abstain rather than guess, and list the "
        "specific additional evidence needed to distinguish the alternatives."
    ),
}
SYSTEM_PROMPT = (
    "You are analyzing a software defect using the evidence packet supplied in the user message. "
    "Base factual claims only on information in that packet. Do not use external tools, web search, "
    "retrieval, or code execution. Do not claim to have run tests. Distinguish a plausible hypothesis "
    "from a cause supported by the packet. Return exactly one valid JSON object matching the provided "
    "output schema, without Markdown fences or text outside the JSON."
)
REQUIRED_OUTPUT_KEYS = {
    "decision", "root_cause", "evidence_refs", "rationale",
    "alternative_hypotheses", "missing_evidence",
}


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sha256_text(value):
    return sha256_bytes(value.encode("utf-8"))


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def render_evidence_packet(pack):
    if not isinstance(pack, dict):
        raise ValueError("Evidence pack must be a JSON object.")
    code = pack.get("code")
    trace = pack.get("trace")
    context = pack.get("context", "")
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Every evidence packet requires a non-empty code field.")
    if not isinstance(trace, str) or not trace.strip():
        raise ValueError("Every evidence packet requires a non-empty trace field.")
    if not isinstance(context, str):
        raise ValueError("Evidence packet context must be a string.")
    sections = [
        "[CODE_1]\n" + code,
        "[TRACE_1]\n" + trace,
    ]
    if context.strip():
        sections.append("[CONTEXT_1]\n" + context)
    return "\n\n".join(sections)


def evidence_ids(pack):
    return {"CODE_1", "TRACE_1"} | ({"CONTEXT_1"} if pack.get("context", "").strip() else set())


def make_prompt(policy, pack, schema):
    if policy not in POLICY_INSTRUCTIONS:
        raise ValueError("Unknown policy.")
    evidence_packet = render_evidence_packet(pack)
    user_prompt = (
        "Task: Assess the likely root cause of the reported software defect.\n\n"
        "Policy instruction:\n"
        + POLICY_INSTRUCTIONS[policy]
        + "\n\nEvidence packet:\n"
        + evidence_packet
        + "\n\nUse evidence item IDs when referring to packet evidence. Do not cite information "
        "that is not present in the packet. If abstaining, leave root_cause as an empty string and "
        "list the specific evidence that would distinguish the plausible causes. Return only the JSON "
        "object defined by the schema.\n\nJSON schema:\n"
        + json.dumps(schema, ensure_ascii=False)
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def invalid_response(reason):
    return {
        "parse_ok": False,
        "parse_error": reason,
        "decision": "invalid_output",
        "root_cause": "",
        "evidence_refs": [],
        "rationale": "",
        "alternative_hypotheses": [],
        "missing_evidence": [],
    }


def parse_response(raw, allowed_evidence_ids, schema):
    try:
        parsed = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        return invalid_response("invalid_json: " + str(exc))
    if not isinstance(parsed, dict):
        return invalid_response("top_level_json_must_be_object")
    required_keys = set(schema.get("required", []))
    if required_keys != REQUIRED_OUTPUT_KEYS:
        return invalid_response("canonical_output_schema_required_keys_mismatch")
    if set(parsed) != required_keys:
        missing = sorted(required_keys - set(parsed))
        extra = sorted(set(parsed) - required_keys)
        return invalid_response("schema_keys_mismatch; missing=" + repr(missing) + "; extra=" + repr(extra))
    if parsed.get("decision") not in {"diagnose", "abstain"}:
        return invalid_response("decision_must_be_diagnose_or_abstain")
    if not isinstance(parsed.get("root_cause"), str):
        return invalid_response("root_cause_must_be_string")
    if parsed["decision"] == "diagnose" and not parsed["root_cause"].strip():
        return invalid_response("diagnosis_requires_non_empty_root_cause")
    if parsed["decision"] == "abstain" and parsed["root_cause"] != "":
        return invalid_response("abstention_requires_empty_root_cause")
    if not isinstance(parsed.get("rationale"), str):
        return invalid_response("rationale_must_be_string")
    for field in ("evidence_refs", "alternative_hypotheses", "missing_evidence"):
        values = parsed.get(field)
        if not isinstance(values, list) or len(values) > 8:
            return invalid_response(field + "_must_be_array_with_at_most_eight_items")
        if any(not isinstance(value, str) for value in values):
            return invalid_response(field + "_items_must_be_strings")
    refs = parsed["evidence_refs"]
    if len(set(refs)) != len(refs):
        return invalid_response("evidence_refs_must_be_unique")
    if any(ref not in allowed_evidence_ids for ref in refs):
        return invalid_response("evidence_refs_must_match_visible_packet_ids")
    return {
        "parse_ok": True,
        "parse_error": "",
        "decision": parsed["decision"],
        "root_cause": parsed["root_cause"],
        "evidence_refs": parsed["evidence_refs"],
        "rationale": parsed["rationale"],
        "alternative_hypotheses": parsed["alternative_hypotheses"],
        "missing_evidence": parsed["missing_evidence"],
    }


def validate_schema_contract(schema):
    properties = schema.get("properties") if isinstance(schema, dict) else None
    if (
        not isinstance(properties, dict)
        or set(schema.get("required", [])) != REQUIRED_OUTPUT_KEYS
        or set(properties) != REQUIRED_OUTPUT_KEYS
        or schema.get("additionalProperties") is not False
        or properties.get("decision", {}).get("enum") != ["diagnose", "abstain"]
        or properties.get("root_cause", {}).get("type") != "string"
        or properties.get("evidence_refs", {}).get("type") != "array"
    ):
        raise ValueError("Canonical OUTPUT_SCHEMA.json is not compatible with the frozen runner parser.")


def validate_cases(cases, manifest, registry, excluded_ids):
    if not isinstance(cases, list):
        raise ValueError("cases.json must contain a top-level list.")
    records = registry.get("records") if isinstance(registry, dict) else None
    if not isinstance(records, list):
        raise ValueError("Canonical CASE_REGISTRY must contain a records list.")
    accepted_registry = {
        row.get("case_id"): row
        for row in records
        if isinstance(row, dict) and row.get("accepted_for_confirmatory") is True
    }
    if len(accepted_registry) != sum(
        isinstance(row, dict) and row.get("accepted_for_confirmatory") is True for row in records
    ):
        raise ValueError("Canonical registry contains missing or duplicate accepted case IDs.")
    manifest_ids = manifest.get("case_ids")
    if not isinstance(manifest_ids, list) or len(manifest_ids) != len(set(manifest_ids)):
        raise ValueError("Manifest case_ids must be a unique list.")
    if set(manifest_ids) != set(accepted_registry):
        raise ValueError("Manifest case_ids must exactly match the accepted canonical registry.")
    minimum_cases = manifest.get("minimum_confirmatory_cases", 60)
    minimum_projects = manifest.get("minimum_upstream_projects", 8)
    if len(manifest_ids) < minimum_cases:
        raise ValueError("Insufficient accepted cases for confirmatory inference.")
    projects = {record.get("upstream_project") for record in accepted_registry.values()}
    if len(projects) < minimum_projects or None in projects:
        raise ValueError("Insufficient independent upstream projects for confirmatory inference.")

    accepted_cases = [
        case for case in cases
        if isinstance(case, dict) and case.get("accepted_for_confirmatory") is True
    ]
    case_map = {case.get("case_id"): case for case in accepted_cases}
    if len(case_map) != len(accepted_cases):
        raise ValueError("Duplicate or missing accepted case IDs in cases.json.")
    if set(case_map) != set(manifest_ids):
        raise ValueError("cases.json IDs must exactly match the frozen manifest case_ids.")

    ordered_cases = []
    for case_id in manifest_ids:
        case = case_map[case_id]
        record = accepted_registry[case_id]
        project = case.get("project", case.get("upstream_project"))
        if project != record.get("upstream_project"):
            raise ValueError("Project mismatch against canonical registry for " + str(case_id))
        if case_id in excluded_ids:
            raise ValueError("Permanently exposed case is not eligible: " + str(case_id))
        if not isinstance(case.get("reference_root_cause"), str) or not case["reference_root_cause"].strip():
            raise ValueError("Restricted answer key is missing a root cause for " + str(case_id))
        expected_gold_hash = record.get("reference_root_cause_sha256")
        if (
            not isinstance(expected_gold_hash, str)
            or len(expected_gold_hash) != 64
            or sha256_text(case["reference_root_cause"]) != expected_gold_hash
        ):
            raise ValueError(
                "Restricted gold root-cause SHA-256 mismatch for " + str(case_id)
            )
        packs = case.get("evidence_packs")
        if not isinstance(packs, dict) or set(packs) != set(LEVELS):
            raise ValueError("E1/E2/E3 evidence packs are missing or unexpected for " + str(case_id))
        registry_hashes = record.get("evidence_packet_sha256")
        if not isinstance(registry_hashes, dict):
            raise ValueError("Canonical packet hashes are missing for " + str(case_id))
        for level in LEVELS:
            rendered_packet = render_evidence_packet(packs[level])
            actual_hash = sha256_text(rendered_packet)
            expected_hash = registry_hashes.get(LEVEL_TO_REGISTRY_KEY[level])
            if not isinstance(expected_hash, str) or actual_hash != expected_hash:
                raise ValueError(
                    "Rendered evidence packet SHA-256 mismatch for " + str(case_id) + " " + level
                )
        ordered_cases.append(case)
    return ordered_cases


def load_model():
    if not torch.cuda.is_available():
        raise RuntimeError("A CUDA-capable GPU is required for the locked FP16 study runtime.")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        revision=MODEL_REVISION,
        trust_remote_code=False,
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=MODEL_REVISION,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=False,
    )
    model.eval()
    return tokenizer, model


def runtime_report(tokenizer, model):
    try:
        accelerate_version = importlib.metadata.version("accelerate")
    except importlib.metadata.PackageNotFoundError:
        accelerate_version = None
    device = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    template = tokenizer.chat_template or ""
    config = {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "transformers": importlib.metadata.version("transformers"),
        "accelerate": accelerate_version,
        "cuda_runtime": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "gpu_name": device,
        "gpu_count": torch.cuda.device_count(),
        "model_id": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "tokenizer_id": MODEL_ID,
        "tokenizer_revision": MODEL_REVISION,
        "tokenizer_chat_template_sha256": sha256_text(template),
        "model_type": getattr(model.config, "model_type", None),
        "model_max_position_embeddings": getattr(model.config, "max_position_embeddings", None),
        "inference_performed": False,
        "generated_tokens": 0,
    }
    canonical = json.dumps(config, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    config["runtime_fingerprint_sha256"] = sha256_text(canonical)
    return config


def generate(tokenizer, model, messages, max_new_tokens):
    input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    )
    input_device = model.get_input_embeddings().weight.device
    input_ids = input_ids.to(input_device)
    with torch.inference_mode():
        output = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    generated = output[0, input_ids.shape[-1]:]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()


def load_preflight_module(root):
    path = root / "scripts" / "evidence_abstention_preflight.py"
    spec = importlib.util.spec_from_file_location("stage3_preflight", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the canonical Stage 3 read-only preflight.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require_authorized_preflight(root):
    report = load_preflight_module(root).evaluate(root)
    if report.get("ready") is not True:
        raise RuntimeError(
            "Confirmatory inference blocked by the canonical preflight: "
            + json.dumps(report.get("blockers", []), ensure_ascii=False)
        )
    manifest = read_json(root / "research_candidates" / "evidence_abstention" / "EXPERIMENT_MANIFEST_STAGE3.json")
    if manifest.get("model", {}).get("id") != MODEL_ID:
        raise RuntimeError("Runner model ID does not match the canonical Stage 3 manifest.")
    if manifest.get("model", {}).get("revision") != MODEL_REVISION:
        raise RuntimeError("Runner model revision does not match the canonical Stage 3 manifest.")
    if manifest.get("model", {}).get("do_sample") is not False:
        raise RuntimeError("The confirmatory generation policy must remain deterministic.")
    if manifest.get("model", {}).get("max_new_tokens") != 512:
        raise RuntimeError("Runner token limit differs from the frozen Stage 3 manifest.")
    if os.getenv("EVIDENCE_ABSTENTION_INFERENCE_APPROVED") != "YES":
        raise RuntimeError("Explicit inference authorization environment variable is absent.")
    return manifest


def runtime_preflight(root):
    manifest_path = root / "research_candidates" / "evidence_abstention" / "EXPERIMENT_MANIFEST_STAGE3.json"
    manifest = read_json(manifest_path)
    model_lock = manifest.get("model", {})
    if model_lock.get("id") != MODEL_ID or model_lock.get("revision") != MODEL_REVISION:
        raise RuntimeError("Candidate model/revision differs from the canonical manifest.")
    tokenizer, model = load_model()
    report = runtime_report(tokenizer, model)
    report["mode"] = "generation_free_runtime_preflight"
    report["note"] = "No model response was generated; this report does not authorize confirmatory inference."
    RUNTIME_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if RUNTIME_REPORT_PATH.exists():
        raise FileExistsError("Runtime report exists; choose a new output path rather than overwrite evidence.")
    RUNTIME_REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def run_study(root, manifest):
    project = root / "research_candidates" / "evidence_abstention"
    registry = read_json(project / "CASE_REGISTRY.json")
    union = read_json(project / "EXPOSURE_UNION_2026-10-23.json")
    excluded = union.get("excluded_case_ids")
    if not isinstance(excluded, list) or len(excluded) != len(set(excluded)):
        raise RuntimeError("Canonical exposure exclusion union is malformed.")
    schema = read_json(project / "OUTPUT_SCHEMA.json")
    validate_schema_contract(schema)
    cases = validate_cases(read_json(CASES_PATH), manifest, registry, set(excluded))

    outputs = (RAW_OUTPUTS_PATH, BLIND_REVIEW_PATH, CONDITION_MAP_PATH, ANSWER_KEY_PATH, RUN_METADATA_PATH)
    existing = [str(path) for path in outputs if path.exists()]
    if existing:
        raise FileExistsError("Refusing to overwrite prior experiment outputs: " + ", ".join(existing))
    for path in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)

    tokenizer, model = load_model()
    runtime = runtime_report(tokenizer, model)
    runtime_hash = runtime["runtime_fingerprint_sha256"]
    generation = manifest["model"]
    order_rng = random.Random(CONDITION_ORDER_SEED)
    raw_rows = []
    blinded_rows = []
    codebook_rows = []
    answer_key_rows = []
    output_index = 0

    with RAW_OUTPUTS_PATH.open("x", encoding="utf-8") as raw_file:
        for case in cases:
            answer_key_rows.append({
                "case_id": case["case_id"],
                "reference_root_cause": case["reference_root_cause"],
            })
            for level in LEVELS:
                pack = case["evidence_packs"][level]
                packet_text = render_evidence_packet(pack)
                packet_hash = sha256_text(packet_text)
                policies = ["P0", "P1"]
                order_rng.shuffle(policies)
                for policy in policies:
                    messages = make_prompt(policy, pack, schema)
                    serialized_messages = json.dumps(messages, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                    prompt_hash = sha256_text(serialized_messages)
                    error = ""
                    raw = ""
                    try:
                        raw = generate(tokenizer, model, messages, generation["max_new_tokens"])
                        parsed = parse_response(raw, evidence_ids(pack), schema)
                    except Exception as exc:
                        parsed = invalid_response("generation_error: " + type(exc).__name__ + ": " + str(exc))
                        error = type(exc).__name__ + ": " + str(exc)
                    output_id = secrets.token_hex(10)
                    output_index += 1
                    row = {
                        "output_id": output_id,
                        "case_id": case["case_id"],
                        "upstream_project": case.get("project", case.get("upstream_project")),
                        "evidence_level": level,
                        "policy": policy,
                        "raw_output": raw,
                        **parsed,
                        "generation_error": error,
                        "model_id": MODEL_ID,
                        "model_revision": MODEL_REVISION,
                        "tokenizer_revision": MODEL_REVISION,
                        "prompt_sha256": prompt_hash,
                        "evidence_packet_sha256": packet_hash,
                        "runtime_fingerprint_sha256": runtime_hash,
                        "raw_output_sha256": sha256_text(raw),
                    }
                    raw_rows.append(row)
                    raw_file.write(json.dumps(row, ensure_ascii=False) + "\n")
                    raw_file.flush()
                    blinded_rows.append({
                        "output_id": output_id,
                        "evidence_packet": packet_text,
                        "raw_output": raw,
                    })
                    codebook_rows.append({
                        "output_id": output_id,
                        "case_id": case["case_id"],
                        "upstream_project": case.get("project", case.get("upstream_project")),
                        "evidence_level": level,
                        "policy": policy,
                        "prompt_sha256": prompt_hash,
                        "evidence_packet_sha256": packet_hash,
                        "raw_output_sha256": sha256_text(raw),
                    })

    random.Random(BLIND_ORDER_SEED).shuffle(blinded_rows)
    with BLIND_REVIEW_PATH.open("x", encoding="utf-8") as blind_file:
        for row in blinded_rows:
            blind_file.write(json.dumps(row, ensure_ascii=False) + "\n")
    with CONDITION_MAP_PATH.open("x", newline="", encoding="utf-8") as codebook_file:
        writer = csv.DictWriter(codebook_file, fieldnames=list(codebook_rows[0]))
        writer.writeheader()
        writer.writerows(codebook_rows)
    with ANSWER_KEY_PATH.open("x", newline="", encoding="utf-8") as answer_file:
        writer = csv.DictWriter(answer_file, fieldnames=["case_id", "reference_root_cause"])
        writer.writeheader()
        writer.writerows(answer_key_rows)

    metadata = {
        "status": "raw_outputs_recorded_requires_independent_blind_adjudication",
        "n_cases": len(cases),
        "n_outputs_expected": len(cases) * 6,
        "n_outputs_recorded": len(raw_rows),
        "n_invalid_or_failed_outputs": sum(row["parse_ok"] is not True for row in raw_rows),
        "model_id": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "tokenizer_revision": MODEL_REVISION,
        "runtime": runtime,
        "condition_order_seed": CONDITION_ORDER_SEED,
        "blind_order_seed": BLIND_ORDER_SEED,
        "outputs": {
            "raw_model_outputs": str(RAW_OUTPUTS_PATH),
            "blind_review_packet": str(BLIND_REVIEW_PATH),
            "restricted_condition_codebook": str(CONDITION_MAP_PATH),
            "restricted_answer_key": str(ANSWER_KEY_PATH),
        },
        "raw_output_file_sha256": sha256_bytes(RAW_OUTPUTS_PATH.read_bytes()),
        "blind_review_packet_sha256": sha256_bytes(BLIND_REVIEW_PATH.read_bytes()),
        "condition_codebook_sha256": sha256_bytes(CONDITION_MAP_PATH.read_bytes()),
    }
    RUN_METADATA_PATH.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "--runtime-preflight",
        action="store_true",
        help="Load the pinned model/tokenizer and record runtime metadata without generating a response.",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.runtime_preflight:
        runtime_preflight(root)
        return 0
    manifest = require_authorized_preflight(root)
    run_study(root, manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
