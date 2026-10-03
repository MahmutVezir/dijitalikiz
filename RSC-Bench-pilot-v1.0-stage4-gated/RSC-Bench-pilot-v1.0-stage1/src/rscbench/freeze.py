from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .hashing import sha256_text
from .prompts import PromptBuilder


def current_hashes(root: Path) -> dict[str, str]:
    builder = PromptBuilder(root)
    sh, su = builder.hashes("standard")
    ch, cu = builder.hashes("ccdg")
    return {
        "standard_system_sha256": sh,
        "standard_user_sha256": su,
        "ccdg_system_sha256": ch,
        "ccdg_user_sha256": cu,
    }


def freeze(root: Path) -> dict:
    manifest_path = root / "prompts/manifests/prompt_freeze.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") == "FROZEN":
        raise RuntimeError("Prompt manifest is already frozen. Do not overwrite it.")

    values = current_hashes(root)
    manifest.update(values)
    manifest["status"] = "FROZEN"
    manifest["frozen_at"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def verify_frozen(root: Path) -> None:
    manifest_path = root / "prompts/manifests/prompt_freeze.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if manifest.get("status") != "FROZEN":
        return

    expected = {
        key: manifest[key]
        for key in (
            "standard_system_sha256",
            "standard_user_sha256",
            "ccdg_system_sha256",
            "ccdg_user_sha256",
        )
    }
    actual = current_hashes(root)

    if actual != expected:
        raise RuntimeError(
            "Frozen prompt hash mismatch. A semantic prompt change occurred "
            "after freeze; experiment execution is blocked."
        )
