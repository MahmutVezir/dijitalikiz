from __future__ import annotations

"""Validate the readiness receipt produced by the single compatibility gate."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data/pilot/compatibility_report.json"
MANIFEST = ROOT / "data/pilot/pilot_manifest.json"


def main() -> int:
    try:
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"COMPATIBILITY RECEIPT MISSING/INVALID: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    valid = (
        report.get("status") == "pass"
        and report.get("pilot_authorized") is True
        and report.get("model_id") == manifest.get("model", {}).get("model_id")
        and report.get("model_revision") == manifest.get("model", {}).get("revision")
        and report.get("expected_records") == manifest.get("expected_records")
        and bool(report.get("source_commit"))
        and bool(report.get("checks"))
        and all(item.get("status") == "pass" for item in report["checks"])
    )
    if not valid:
        print("COMPATIBILITY RECEIPT REJECTED: frozen pilot must not start.", file=sys.stderr)
        return 1

    print(
        "COMPATIBILITY RECEIPT VERIFIED: model, revision, record count, and every gate check passed.",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
