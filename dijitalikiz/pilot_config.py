from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any


_CASE_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\Z")


def expected_pilot_record_count(
    manifest: Mapping[str, Any],
    *,
    require_declared: bool = False,
) -> int:
    """Validate the frozen pilot design and return its planned inference count."""
    if manifest.get("status") != "model_frozen":
        raise ValueError("Pilot manifest status must be 'model_frozen'.")

    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Pilot manifest must contain a non-empty cases list.")
    if any(
        not isinstance(case_id, str) or not _CASE_ID_RE.fullmatch(case_id)
        for case_id in cases
    ):
        raise ValueError("Pilot case IDs must be safe, non-empty filename components.")
    if len(set(cases)) != len(cases):
        raise ValueError("Pilot manifest contains duplicate case IDs.")

    conditions = manifest.get("conditions")
    if conditions != ["standard", "ccdg"]:
        raise ValueError(
            "Frozen pilot conditions must be exactly ['standard', 'ccdg']."
        )

    generation = manifest.get("generation")
    if not isinstance(generation, Mapping):
        raise ValueError("Pilot manifest generation settings must be an object.")
    seeds = generation.get("seeds")
    if not isinstance(seeds, list) or not seeds:
        raise ValueError("Pilot manifest must contain a non-empty generation.seeds list.")
    if any(type(seed) is not int or seed < 0 for seed in seeds):
        raise ValueError("Pilot seeds must be non-negative integers.")
    if len(set(seeds)) != len(seeds):
        raise ValueError("Pilot manifest contains duplicate seeds.")
    if manifest.get("replications") != len(seeds):
        raise ValueError(
            "Pilot manifest replications must equal the number of generation seeds."
        )

    calculated = len(cases) * len(conditions) * len(seeds)
    declared = manifest.get("expected_records")
    if declared is None:
        if require_declared:
            raise ValueError("Frozen pilot manifest must declare expected_records.")
    elif type(declared) is not int or declared != calculated:
        raise ValueError(
            f"Pilot manifest expected_records mismatch: declared={declared!r}, "
            f"calculated={calculated}."
        )

    return calculated


def expected_pilot_run_filenames(
    manifest: Mapping[str, Any],
    *,
    require_declared: bool = False,
) -> set[str]:
    """Return the exact expected per-inference JSON filenames."""
    expected_pilot_record_count(manifest, require_declared=require_declared)
    cases = manifest["cases"]
    conditions = manifest["conditions"]
    seeds = manifest["generation"]["seeds"]
    return {
        f"{case_id}__{condition}__seed{seed}.json"
        for case_id in cases
        for condition in conditions
        for seed in seeds
    }
