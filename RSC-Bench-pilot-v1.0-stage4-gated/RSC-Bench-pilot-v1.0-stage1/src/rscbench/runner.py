from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .freeze import verify_frozen
from .hashing import sha256_text
from .io import parse_model_output
from .matcher import deterministic_match
from .model_client import ModelClient
from .prompts import PromptBuilder
from .schemas import CCDG, Case, GroundTruth, ModelOutput, RunRecord
from .validator import base_input_sha256, validate_case_links


def run_one(
    *,
    root: Path,
    case: Case,
    truth: GroundTruth,
    ccdg: CCDG,
    condition: str,
    replicate: int,
    client: ModelClient,
    experiment_id: str = "PILOT-001",
    require_frozen_prompts: bool = False,
) -> dict:
    """Run one condition/replicate and return a provenance-complete record.

    Prompt freeze is optional during pilot preparation. Main experiments must
    explicitly pass require_frozen_prompts=True.
    """
    if condition not in {"standard", "ccdg"}:
        raise ValueError(f"Unknown condition: {condition}")
    if not 1 <= replicate <= 5:
        raise ValueError("replicate must be between 1 and 5")

    validate_case_links(case, truth, ccdg)
    if require_frozen_prompts:
        verify_frozen(root)

    builder = PromptBuilder(root)
    system, user = builder.render(condition, case, ccdg if condition == "ccdg" else None)
    response = client.generate(system, user)
    parsed = parse_model_output(response.raw_text, ModelOutput)
    match = deterministic_match(parsed, truth)

    prompt_hashes = {
        "system_sha256": sha256_text(system),
        "user_sha256": sha256_text(user),
    }
    input_hashes = {
        "I_base_sha256": base_input_sha256(case),
        "rendered_user_sha256": sha256_text(user),
    }
    if condition == "ccdg":
        input_hashes["CCDG_base_input_sha256"] = ccdg.base_input_sha256
        input_hashes["CCDG_canonical_sha256"] = sha256_text(ccdg.model_dump_json(exclude_none=True, by_alias=True))

    record = RunRecord(
        run_id=f"{experiment_id}-{case.case_id}-{condition.upper()}-R{replicate}",
        experiment_date_utc=datetime.now(timezone.utc).isoformat(),
        experiment_id=experiment_id,
        case_id=case.case_id,
        condition=condition,
        replicate=replicate,
        model={
            "provider": response.provider,
            "model_id": response.model_id,
            "api_version": response.api_version,
            **response.metadata,
        },
        generation=response.generation,
        prompt_hashes=prompt_hashes,
        input_hashes=input_hashes,
        output={
            "raw_response": response.raw_text,
            "parsed": parsed.model_dump(),
        },
        match=match,
    )
    return record.model_dump()
