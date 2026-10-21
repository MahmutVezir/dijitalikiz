#!/usr/bin/env python3
"""Audit one technical-triage artifact directory without accepting cases."""
import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

HEX64 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-fA-F]{7,64}$")


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def audit(root):
    root = Path(root).resolve()
    blockers = []
    warnings = []
    summary_path = root / "summary.json"
    sums_path = root / "SHA256SUMS"
    summary = {}
    if not summary_path.is_file():
        blockers.append("summary.json is missing")
    else:
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            if not isinstance(summary, dict):
                blockers.append("summary.json must contain a JSON object")
                summary = {}
        except (OSError, json.JSONDecodeError) as exc:
            blockers.append("summary.json is invalid: " + str(exc))
            summary = {}

    listed = {}
    if not sums_path.is_file():
        blockers.append("SHA256SUMS is missing")
    else:
        try:
            lines = sums_path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            lines = []
            blockers.append("SHA256SUMS cannot be read: " + str(exc))
        for number, line in enumerate(lines, 1):
            parts = line.split("  ", 1)
            if len(parts) != 2 or not HEX64.fullmatch(parts[0]):
                blockers.append("SHA256SUMS line " + str(number) + " is malformed")
                continue
            rel = parts[1]
            path = PurePosixPath(rel)
            if path.is_absolute() or ".." in path.parts or rel.startswith("./") is False:
                # The workflow uses "./filename" relative paths deliberately.
                blockers.append("SHA256SUMS path must be safe and relative ('./name'): " + rel)
                continue
            if len(path.parts) != 2 or path.parts[0] != ".":
                blockers.append("SHA256SUMS must list only top-level files: " + rel)
                continue
            name = path.name
            if name == "SHA256SUMS":
                blockers.append("SHA256SUMS must not hash itself")
                continue
            if name in listed:
                blockers.append("duplicate SHA256SUMS entry: " + name)
                continue
            listed[name] = parts[0]
            file_path = root / name
            if not file_path.is_file():
                blockers.append("listed file is missing: " + name)
            elif sha256(file_path) != parts[0]:
                blockers.append("SHA-256 mismatch: " + name)

    if root.is_dir() and sums_path.is_file():
        actual = {p.name for p in root.iterdir() if p.is_file() and p.name != "SHA256SUMS" and p.name != "artifact-audit.json"}
        unlisted = sorted(actual - set(listed))
        if unlisted:
            blockers.append("unlisted files: " + ", ".join(unlisted))

    case_id = summary.get("case_id")
    required = (
        "dataset_recorded_python", "runtime_python_observed", "runtime_matches_metadata",
        "expected_buggy_commit", "observed_buggy_base_commit", "expected_fixed_commit_reference",
        "expected_run_test_sha256", "buggy_target_test_exit_code", "fixed_target_test_exit_code",
    )
    for field in required:
        if field not in summary:
            warnings.append("triage summary field missing: " + field)

    for field in ("accepted_for_confirmatory", "confirmatory_eligible", "llm_inference_performed"):
        if summary.get(field) is not False:
            blockers.append(field + " must be explicitly false in a triage artifact")

    if isinstance(case_id, str) and case_id.strip():
        if summary.get("runtime_matches_metadata") is not True:
            warnings.append("runtime Python did not explicitly match recorded Python")
        if summary.get("runtime_python_observed") != summary.get("dataset_recorded_python"):
            warnings.append("runtime version differs from metadata or is not recorded consistently")
        expected_buggy = summary.get("expected_buggy_commit")
        observed_buggy = summary.get("observed_buggy_base_commit")
        if not isinstance(expected_buggy, str) or not COMMIT.fullmatch(expected_buggy):
            blockers.append("expected buggy commit is missing or malformed")
        if observed_buggy != expected_buggy:
            warnings.append("observed buggy base commit does not match the expected buggy commit")
        expected_fixed = summary.get("expected_fixed_commit_reference")
        if not isinstance(expected_fixed, str) or not COMMIT.fullmatch(expected_fixed):
            blockers.append("expected fixed commit reference is missing or malformed")
        if expected_fixed == expected_buggy:
            blockers.append("buggy and fixed commit references must differ")

        run_hash = summary.get("expected_run_test_sha256")
        if not isinstance(run_hash, str) or not HEX64.fullmatch(run_hash):
            blockers.append("expected run_test SHA-256 is missing or malformed")
        else:
            metadata_hashes = root / "source-metadata-hashes.txt"
            if not metadata_hashes.is_file():
                warnings.append("source-metadata-hashes.txt is missing")
            else:
                found_run_hash = False
                for line in metadata_hashes.read_text(encoding="utf-8", errors="replace").splitlines():
                    match = re.match(r"^([0-9a-f]{64})\s+(.+)$", line)
                    if match and match.group(2).endswith("/run_test.sh") and match.group(1) == run_hash:
                        found_run_hash = True
                if not found_run_hash:
                    warnings.append("expected run_test SHA-256 was not found in source-metadata-hashes.txt")

    buggy_code = summary.get("buggy_target_test_exit_code")
    fixed_code = summary.get("fixed_target_test_exit_code")
    target_signals_present = (
        isinstance(buggy_code, int) and buggy_code != 0
        and summary.get("buggy_failure_signature_present") is True
        and isinstance(fixed_code, int) and fixed_code == 0
        and summary.get("fixed_pass_marker_present") is True
    )
    if not target_signals_present:
        warnings.append("the automated target-test signals do not show a complete buggy-fail/fixed-pass pair; inspect raw logs")

    report = {
        "case_id": case_id or "unknown",
        "audit_scope": "technical-triage artifact integrity and raw target-test signals only",
        "integrity_pass": not blockers,
        "technical_buggy_fail_fixed_pass_signals_present": target_signals_present,
        "manual_review_required": True,
        "accepted_for_confirmatory": False,
        "confirmatory_eligible": False,
        "llm_inference_performed": False,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "warning_count": len(warnings),
        "warnings": warnings,
        "files_listed_in_checksum_manifest": len(listed),
    }
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)
    result = audit(args.root)
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
