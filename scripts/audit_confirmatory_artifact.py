from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from itertools import product
from math import comb
from pathlib import Path


CONDITIONS = ("standard", "ccdg")
SEEDS = (42, 43, 44, 45, 46)
MAJORITY_REQUIRED = 3


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def normalize_phrase(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def root_cause_alias_match(output: dict, aliases: list[str]) -> bool:
    haystack = " " + normalize_phrase(
        str(output.get("root_cause_class", "")) + " " + str(output.get("explanation", ""))
    ) + " "
    return any(
        (" " + normalized + " ") in haystack
        for normalized in (normalize_phrase(alias) for alias in aliases)
        if normalized
    )


def exact_mcnemar_pvalue(standard_only: int, ccdg_only: int) -> float:
    discordant = standard_only + ccdg_only
    if discordant == 0:
        return 1.0
    lower_tail = sum(
        comb(discordant, k)
        for k in range(0, min(standard_only, ccdg_only) + 1)
    )
    return min(1.0, 2.0 * lower_tail / (2**discordant))


def wilson_interval(successes: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n <= 0 or not 0 <= successes <= n:
        raise ValueError("Wilson interval requires n > 0 and 0 <= successes <= n.")
    p_hat = successes / n
    z2 = z * z
    denominator = 1.0 + z2 / n
    center = (p_hat + z2 / (2.0 * n)) / denominator
    margin = z * math.sqrt(p_hat * (1.0 - p_hat) / n + z2 / (4.0 * n * n)) / denominator
    return max(0.0, center - margin), min(1.0, center + margin)


def paired_risk_difference_ci(standard_only: int, ccdg_only: int, n: int) -> tuple[float, float]:
    ccdg_ci = wilson_interval(ccdg_only, n)
    standard_ci = wilson_interval(standard_only, n)
    return ccdg_ci[0] - standard_ci[1], ccdg_ci[1] - standard_ci[0]


def _load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def _safe_path(root: Path, relative: str) -> Path:
    candidate = Path(relative)
    if not relative or candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"Unsafe artifact path: {relative!r}")
    path = (root / candidate).resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"Artifact path escapes root: {relative!r}")
    return path


def audit_artifact(artifact_root: str | Path) -> dict:
    root = Path(artifact_root).resolve()
    manifest_path = root / "artifact_manifest.json"
    manifest = _load_json(manifest_path)
    benchmark = _load_json(root / "benchmark_manifest.json")
    pilot = _load_json(root / "pilot_manifest.json")
    rubric = _load_json(root / "evaluation_rubric.json")
    evaluation = _load_json(root / "confirmatory_evaluation.json")
    primary = _load_json(root / "primary_analysis.json")
    qa = _load_json(root / "confirmatory_qa_report.json")
    environment = _load_json(root / "environment.json")

    errors: list[str] = []
    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise ValueError("artifact manifest files must be a list")
    if manifest.get("file_count") != len(entries):
        errors.append("artifact_manifest.file_count does not match files list")

    declared: dict[str, dict] = {}
    for item in entries:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            errors.append("invalid artifact manifest entry")
            continue
        rel = item["path"]
        if rel in declared:
            errors.append(f"duplicate manifest entry: {rel}")
            continue
        declared[rel] = item
        try:
            path = _safe_path(root, rel)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not path.is_file():
            errors.append(f"missing file: {rel}")
            continue
        payload = path.read_bytes()
        if item.get("bytes") != len(payload):
            errors.append(f"size mismatch: {rel}")
        if item.get("sha256") != sha256_bytes(payload):
            errors.append(f"SHA-256 mismatch: {rel}")

    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.resolve() != manifest_path
    }
    for rel in sorted(set(declared) - actual):
        errors.append(f"manifest lists absent file: {rel}")
    for rel in sorted(actual - set(declared)):
        errors.append(f"unlisted file: {rel}")

    case_ids = benchmark.get("case_ids")
    conditions = pilot.get("conditions")
    seeds = pilot.get("generation", {}).get("seeds")
    if benchmark.get("status") != "frozen":
        errors.append("benchmark manifest is not frozen")
    if not isinstance(case_ids, list) or not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("frozen benchmark case_ids must be nonempty and unique")
    if conditions != list(CONDITIONS):
        errors.append(f"unexpected conditions: {conditions!r}")
    if seeds != list(SEEDS):
        errors.append(f"unexpected seeds: {seeds!r}")
    if set(case_ids) & set(benchmark.get("pilot_case_ids", [])):
        errors.append("pilot/confirmatory case overlap")

    rubric_hash = sha256_bytes((root / "evaluation_rubric.json").read_bytes())
    if rubric_hash != benchmark.get("scoring_rubric", {}).get("sha256"):
        errors.append("rubric SHA-256 does not match frozen benchmark manifest")
    if rubric.get("primary_endpoint") != benchmark.get("scoring_rubric", {}).get("primary_endpoint"):
        errors.append("rubric endpoint does not match frozen manifest")
    aliases_by_case = {item["case_id"]: item["root_cause_aliases"] for item in rubric.get("cases", [])}
    if list(aliases_by_case) != case_ids:
        errors.append("rubric case IDs/order do not match frozen manifest")

    expected_names = {
        f"{case}__{condition}__seed{seed}.json"
        for case, condition, seed in product(case_ids, conditions, seeds)
    }
    runs_dir = root / "runs"
    run_files = {path.name: path for path in runs_dir.glob("*.json") if path.is_file()}
    if set(run_files) != expected_names:
        errors.append(
            "run set mismatch: "
            f"missing={sorted(expected_names - set(run_files))}, "
            f"unexpected={sorted(set(run_files) - expected_names)}"
        )

    model = pilot.get("model", {})
    generation = pilot.get("generation", {})
    source_commits: set[str] = set()
    records_by_key: dict[tuple[str, str, int], dict] = {}
    alias_hits = Counter()
    parse_failures = 0
    for name in sorted(set(run_files) & expected_names):
        path = run_files[name]
        run = _load_json(path)
        try:
            case_id, condition, seed_part = name[:-5].rsplit("__", 2)
            seed = int(seed_part.removeprefix("seed"))
        except Exception:
            errors.append(f"cannot infer run identity from filename: {name}")
            continue
        key = (case_id, condition, seed)
        if key in records_by_key:
            errors.append(f"duplicate run identity: {key}")
        records_by_key[key] = run
        for field, expected in {
            "case_id": case_id,
            "condition": condition,
            "seed": seed,
            "model_id": model.get("model_id"),
            "model_revision": model.get("revision"),
            "model_dtype": "float16",
            "quantization": "none",
            "temperature": generation.get("temperature"),
            "top_p": generation.get("top_p"),
            "max_new_tokens": generation.get("max_new_tokens"),
            "system_prompt_sha256": pilot.get("system_prompt", {}).get("sha256"),
        }.items():
            if run.get(field) != expected:
                errors.append(f"{name}: {field} differs from frozen configuration")
        source_commit = run.get("source_commit")
        if not isinstance(source_commit, str) or len(source_commit) != 40:
            errors.append(f"{name}: invalid source_commit")
        else:
            source_commits.add(source_commit)
        for field in ("prompt_sha256", "context_sha256", "system_prompt_sha256", "raw_output_sha256"):
            value = run.get(field)
            if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                errors.append(f"{name}: invalid {field}")
        if isinstance(run.get("raw_output"), str) and run.get("raw_output_sha256") != sha256_text(run["raw_output"]):
            errors.append(f"{name}: raw_output SHA-256 mismatch")
        if run.get("parse_error") is not None or not isinstance(run.get("parsed_output"), dict):
            parse_failures += 1
        else:
            if root_cause_alias_match(run["parsed_output"], aliases_by_case.get(case_id, [])):
                alias_hits[condition] += 1
        if run.get("prompt_sha256") and run.get("context_sha256"):
            # A given case/condition's prompts must be identical across all five seeds.
            for other_seed in seeds:
                other_key = (case_id, condition, other_seed)
                other = records_by_key.get(other_key)
                if other and (
                    other.get("prompt_sha256") != run.get("prompt_sha256")
                    or other.get("context_sha256") != run.get("context_sha256")
                ):
                    errors.append(f"{case_id}/{condition}: prompt/context hashes vary across seeds")

    if len(source_commits) != 1:
        errors.append(f"records must use one source commit; found {sorted(source_commits)}")
    source_commit = next(iter(source_commits)) if len(source_commits) == 1 else None
    if environment.get("source_commit") != source_commit:
        errors.append("environment source_commit differs from run-record source commit")
    if manifest.get("run_record_count") != len(expected_names):
        errors.append("artifact_manifest.run_record_count disagrees with design")
    if manifest.get("finalization_gate", {}).get("expected_run_record_count") != len(expected_names):
        errors.append("artifact_manifest finalization count disagrees with design")
    if manifest.get("finalization_gate", {}).get("status") != "complete":
        errors.append("artifact finalization gate is not complete")

    expected_evaluation = {(c, cond, seed) for c, cond, seed in product(case_ids, conditions, seeds)}
    eval_records = evaluation.get("records", [])
    evaluation_keys = {
        (r.get("case_id"), r.get("condition"), r.get("seed")) for r in eval_records
    }
    if evaluation.get("status") != "complete" or evaluation.get("expected_records") != len(expected_names) or evaluation.get("found_records") != len(expected_names):
        errors.append("evaluation completion/count metadata mismatch")
    if evaluation_keys != expected_evaluation or len(eval_records) != len(expected_evaluation):
        errors.append("evaluation records are missing, duplicated, or unexpected")
    if evaluation.get("scoring_rubric_sha256") != rubric_hash:
        errors.append("evaluation rubric checksum mismatch")

    evaluation_lookup = {
        (r.get("case_id"), r.get("condition"), r.get("seed")): r for r in eval_records
    }
    case_pass = {condition: {} for condition in conditions}
    primary_counts = Counter()
    for key in sorted(expected_evaluation):
        item = evaluation_lookup.get(key)
        run = records_by_key.get(key)
        if item is None or run is None:
            continue
        should_parse = run.get("parse_error") is None and isinstance(run.get("parsed_output"), dict)
        if item.get("parse_ok") is not should_parse:
            errors.append(f"{key}: parse status differs between run and evaluation")
        actual_alias = should_parse and root_cause_alias_match(run["parsed_output"], aliases_by_case.get(key[0], []))
        if item.get("score", {}).get("passed") is not actual_alias:
            errors.append(f"{key}: frozen evaluator result disagrees with alias-matcher recomputation")
        primary_counts[key[1]]["passed"] += int(actual_alias)
        case_pass[key[1]].setdefault(key[0], 0)
        case_pass[key[1]][key[0]] += int(actual_alias)

    majority = {
        condition: {case: passes >= MAJORITY_REQUIRED for case, passes in counts.items()}
        for condition, counts in case_pass.items()
    }
    standard_only = sum(majority["standard"].get(case, False) and not majority["ccdg"].get(case, False) for case in case_ids)
    ccdg_only = sum(majority["ccdg"].get(case, False) and not majority["standard"].get(case, False) for case in case_ids)
    both_pass = sum(majority["standard"].get(case, False) and majority["ccdg"].get(case, False) for case in case_ids)
    both_fail = sum(not majority["standard"].get(case, False) and not majority["ccdg"].get(case, False) for case in case_ids)
    n = len(case_ids)
    ci = paired_risk_difference_ci(standard_only, ccdg_only, n)
    computed = {
        "n_cases": n,
        "standard_accuracy": sum(majority["standard"].get(c, False) for c in case_ids) / n,
        "ccdg_accuracy": sum(majority["ccdg"].get(c, False) for c in case_ids) / n,
        "accuracy_difference_ccdg_minus_standard": sum(majority["ccdg"].get(c, False) for c in case_ids) / n - sum(majority["standard"].get(c, False) for c in case_ids) / n,
        "exact_two_sided_mcnemar_p": exact_mcnemar_pvalue(standard_only, ccdg_only),
        "contingency_table": {
            "standard_pass_ccdg_pass": both_pass,
            "standard_pass_ccdg_fail": standard_only,
            "standard_fail_ccdg_pass": ccdg_only,
            "standard_fail_ccdg_fail": both_fail,
        },
        "paired_effect_ci_95": list(ci),
    }
    for field in ("n_cases", "standard_accuracy", "ccdg_accuracy", "accuracy_difference_ccdg_minus_standard", "exact_two_sided_mcnemar_p", "contingency_table"):
        if primary.get(field) != computed[field]:
            errors.append(f"primary_analysis.{field} disagrees with independent recomputation")
    stored_ci = primary.get("paired_effect_size", {}).get("95_ci")
    if stored_ci is None or any(abs(a-b) > 1e-10 for a,b in zip(stored_ci, computed["paired_effect_ci_95"])):
        errors.append("primary_analysis paired effect CI disagrees with independent recomputation")

    jsonl_path = root / "confirmatory_records.jsonl"
    if jsonl_path.is_file():
        try:
            jsonl_records = [json.loads(line) for line in jsonl_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            if len(jsonl_records) != len(expected_names):
                errors.append("confirmatory_records.jsonl count differs from design")
            else:
                expected_jsonl_records = [records_by_key[(c, cond, seed)] for c, cond, seed in sorted(expected_evaluation)]
                if jsonl_records != expected_jsonl_records:
                    errors.append("confirmatory_records.jsonl records differ from individual run files or deterministic order")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid confirmatory_records.jsonl: {exc}")

    if qa.get("expected_records") != len(expected_names) or qa.get("found_records") != len(expected_names):
        errors.append("QA record counts disagree with design")

    if errors:
        return {"status": "fail", "errors": errors, "error_count": len(errors)}

    discordant = standard_only + ccdg_only
    all_floor = standard_only == 0 and ccdg_only == 0 and both_pass == 0 and both_fail == n
    return {
        "status": "pass",
        "source_commit": source_commit,
        "expected_records": len(expected_names),
        "found_records": len(records_by_key),
        "parse_failures": parse_failures,
        "case_count": n,
        "condition_record_counts": {condition: len([k for k in records_by_key if k[1] == condition]) for condition in conditions},
        "primary_seed_level_alias_hits": dict(alias_hits),
        "primary_seed_level_passes": {condition: primary_counts[condition]["passed"] for condition in conditions},
        "case_level_majority_passes": {condition: sum(majority[condition].get(case, False) for case in case_ids) for condition in conditions},
        "case_level_contingency_table": computed["contingency_table"],
        "standard_accuracy": computed["standard_accuracy"],
        "ccdg_accuracy": computed["ccdg_accuracy"],
        "accuracy_difference_ccdg_minus_standard": computed["accuracy_difference_ccdg_minus_standard"],
        "paired_risk_difference_ci_95": computed["paired_effect_ci_95"],
        "exact_two_sided_mcnemar_p": computed["exact_two_sided_mcnemar_p"],
        "discordant_pairs": {"standard_only": standard_only, "ccdg_only": ccdg_only},
        "all_cases_fail_under_frozen_primary_endpoint": all_floor,
        "interpretation_warning": (
            "All cases fall in the same failing outcome category; this is a floor-effect / endpoint-sensitivity warning. "
            "The p-value does not establish equivalence and must not be interpreted as proof that CCDG has no effect."
            if all_floor
            else "Interpret the paired result under the frozen primary endpoint and its declared limitations."
        ),
        "artifact_manifest_file_count": manifest.get("file_count"),
        "artifact_manifest_verified_file_count": len(actual),
        "contamination_risk_counts": dict(Counter(qa.get("contamination_risk", {}).values())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Independently audit a completed frozen confirmatory artifact.")
    parser.add_argument("--artifact-root", required=True, help="Directory containing confirmatory-output files.")
    parser.add_argument("--output", help="Optional JSON path to save the audit result.")
    args = parser.parse_args()
    result = audit_artifact(args.artifact_root)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    print(rendered, end="")
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    return 0 if result.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
