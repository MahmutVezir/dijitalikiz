#!/usr/bin/env python3
"""Run exact SWE-rebench FAIL_TO_PASS node IDs without shell word splitting.

Each selector is passed as one subprocess argument. A base-side result counts
only when pytest executes the selected test and reports an assertion/test
failure; collection errors and missing node IDs are not reproduction evidence.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Sequence

COLLECTION_ERROR_MARKERS = (
    "ERROR collecting",
    "ERROR: not found:",
    "no tests ran",
    "ImportError while importing test module",
    "ModuleNotFoundError:",
    "ImportError:",
    "collected 0 items",
)


def read_selectors(path: Path) -> list[str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ValueError(f"Could not read selector file {path}: {exc}") from exc

    selectors = [line.rstrip("\r") for line in lines if line.strip()]
    if not selectors:
        raise ValueError(f"No selectors found in {path}")
    if any("\n" in item or "\r" in item for item in selectors):
        raise ValueError("A selector contains an embedded line break")
    return selectors


def classify_result(expect: str, returncode: int, output: str) -> tuple[bool, str]:
    lowered = output.lower()
    for marker in COLLECTION_ERROR_MARKERS:
        if marker.lower() in lowered:
            return False, f"collection/selector/environment error: {marker}"

    failed = re.search(r"(?m)^FAILED\s+", output) is not None
    failed_count = re.search(r"(?m)^\s*(\d+) failed(?:,| in)", output)
    passed_count = re.search(r"(?m)^\s*(\d+) passed(?:,| in)", output)
    skipped_count = re.search(r"(?m)^\s*(\d+) skipped(?:,| in)", output)
    error_count = re.search(r"(?m)^\s*(\d+) error(?:s)?(?:,| in)", output)

    n_failed = int(failed_count.group(1)) if failed_count else 0
    n_passed = int(passed_count.group(1)) if passed_count else 0
    n_skipped = int(skipped_count.group(1)) if skipped_count else 0
    n_errors = int(error_count.group(1)) if error_count else 0

    if expect == "base-fail":
        if returncode == 0:
            return False, "selected test passed on the buggy base"
        if returncode != 1:
            return False, f"pytest exited with unexpected status {returncode}"
        if not failed or n_failed < 1:
            return False, "pytest did not report an executed test failure"
        if n_passed or n_skipped or n_errors:
            return False, "selected invocation was mixed, skipped, or errored"
        return True, "selected test executed and failed on the buggy base"

    if expect == "fixed-pass":
        if returncode != 0:
            return False, f"pytest exited with status {returncode} on the fixed revision"
        if n_passed < 1:
            return False, "pytest did not report a passing selected test"
        if n_failed or n_skipped or n_errors:
            return False, "selected invocation was mixed, skipped, or errored"
        return True, "selected test passed on the fixed revision"

    return False, f"unknown expectation: {expect}"


def run_one(source_dir: Path, selector: str, expect: str, no_conftest: bool = False) -> dict[str, object]:
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-c",
        "/dev/null",
        "-p",
        "no:cacheprovider",
        "-q",
        "--color=no",
    ]
    if no_conftest:
        command.append("--noconftest")
    command.append(selector)
    completed = subprocess.run(
        command,
        cwd=source_dir,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    ok, reason = classify_result(expect, completed.returncode, completed.stdout)
    return {
        "selector": selector,
        "expectation": expect,
        "command": command,
        "returncode": completed.returncode,
        "ok": ok,
        "reason": reason,
        "output": completed.stdout,
    }


def execute(source_dir: Path, selectors_file: Path, expect: str, no_conftest: bool = False) -> tuple[list[dict[str, object]], bool]:
    source_dir = source_dir.resolve()
    if not source_dir.is_dir():
        raise ValueError(f"Source directory does not exist: {source_dir}")
    selectors = read_selectors(selectors_file)
    results = [run_one(source_dir, selector, expect, no_conftest=no_conftest) for selector in selectors]
    return results, all(bool(item["ok"]) for item in results)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--selectors-file", required=True, type=Path)
    parser.add_argument("--expect", choices=("base-fail", "fixed-pass"), required=True)
    parser.add_argument("--log-file", required=True, type=Path)
    parser.add_argument("--no-conftest", action="store_true", help="run pure selectors without loading repository conftest.py files")
    args = parser.parse_args(argv)

    try:
        results, success = execute(args.source_dir, args.selectors_file, args.expect, no_conftest=args.no_conftest)
    except ValueError as exc:
        payload = {"success": False, "error": str(exc), "results": []}
        args.log_file.parent.mkdir(parents=True, exist_ok=True)
        args.log_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(payload, indent=2))
        return 2

    payload = {
        "success": success,
        "expectation": args.expect,
        "source_dir": str(args.source_dir.resolve()),
        "selector_count": len(results),
        "passed_contract_count": sum(bool(item["ok"]) for item in results),
        "failed_contract_count": sum(not bool(item["ok"]) for item in results),
        "results": results,
    }
    args.log_file.parent.mkdir(parents=True, exist_ok=True)
    args.log_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    for item in results:
        print(f"[{'OK' if item['ok'] else 'NOT-OK'}] {item['selector']}: {item['reason']}")
        print(str(item["output"]))
    print(
        f"selector_contracts={payload['passed_contract_count']}/{payload['selector_count']} "
        f"expectation={args.expect}"
    )
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
