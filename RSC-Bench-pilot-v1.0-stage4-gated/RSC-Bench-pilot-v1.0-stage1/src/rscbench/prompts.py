from __future__ import annotations
from pathlib import Path
import json
from .canonicalize import canonical_text
from .hashing import sha256_text
from .schemas import Case, CCDG

class PromptBuilder:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.system_paths = {
            "standard": root / "prompts/standard_context/system.txt",
            "ccdg": root / "prompts/ccdg_context/system.txt",
        }
        self.user_paths = {
            "standard": root / "prompts/standard_context/user_template.txt",
            "ccdg": root / "prompts/ccdg_context/user_template.txt",
        }

    def load(self, condition: str) -> tuple[str, str]:
        if condition not in self.system_paths:
            raise ValueError(f"Unknown condition: {condition}")
        system = canonical_text(self.system_paths[condition].read_text(encoding="utf-8"))
        user = canonical_text(self.user_paths[condition].read_text(encoding="utf-8"))
        return system, user

    def render(self, condition: str, case: Case, ccdg: CCDG | None = None) -> tuple[str, str]:
        system, template = self.load(condition)
        base = json.dumps(case.I_base, ensure_ascii=False, sort_keys=True, indent=2)
        user = template.replace("{I_base}", base)
        if condition == "ccdg":
            if ccdg is None:
                raise ValueError("CCDG context requires a CCDG object.")
            user = user.replace("{CCDG}", ccdg.model_dump_json(indent=2))
        return system, canonical_text(user)

    def hashes(self, condition: str) -> tuple[str, str]:
        system, user = self.load(condition)
        return sha256_text(system), sha256_text(user)
