from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass(frozen=True)
class ModelResponse:
    raw_text: str
    provider: str
    model_id: str
    api_version: str | None = None
    generation: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class ModelClient:
    def generate(self, system_prompt: str, user_prompt: str) -> ModelResponse:
        raise NotImplementedError


class MockModelClient(ModelClient):
    """Deterministic transport fixture; never used as research evidence."""

    def __init__(self, output_payload: dict | None = None):
        self.output_payload = output_payload or {
            "diagnosed_component": "RLS",
            "root_cause_class": "policy_condition_mismatch",
            "affected_entity": "profiles",
            "explanation": "mock",
        }

    def generate(self, system_prompt: str, user_prompt: str) -> ModelResponse:
        return ModelResponse(
            raw_text=json.dumps(self.output_payload, ensure_ascii=False, sort_keys=True),
            provider="mock",
            model_id="mock-v0",
            api_version="mock",
            generation={"temperature": 0.0, "top_p": 1.0, "max_output_tokens": 500, "seed": None},
        )


class OpenAIResponsesClient(ModelClient):
    """Minimal OpenAI Responses API client for the technical pilot.

    The exact model ID is supplied by configuration/environment and is recorded
    verbatim in every RunRecord. No dynamic '-latest' alias is substituted.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model_id: str | None = None,
        api_version: str | None = None,
        temperature: float = 0.0,
        top_p: float = 1.0,
        max_output_tokens: int = 500,
        seed: int | None = None,
        timeout_seconds: float = 120.0,
        base_url: str = "https://api.openai.com/v1",
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_id = model_id or os.getenv("RSCBENCH_MODEL_ID")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required for the real model client.")
        if not self.model_id:
            raise ValueError("RSCBENCH_MODEL_ID is required; use an exact fixed model ID.")
        self.api_version = api_version
        self.temperature = temperature
        self.top_p = top_p
        self.max_output_tokens = max_output_tokens
        self.seed = seed
        self.timeout_seconds = timeout_seconds
        self.base_url = base_url.rstrip("/")

    def generate(self, system_prompt: str, user_prompt: str) -> ModelResponse:
        payload: dict[str, Any] = {
            "model": self.model_id,
            "instructions": system_prompt,
            "input": user_prompt,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_output_tokens": self.max_output_tokens,
            "text": {"format": {"type": "json_object"}},
        }
        if self.seed is not None:
            payload["seed"] = self.seed

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        if self.api_version:
            headers["OpenAI-Version"] = self.api_version

        with httpx.Client(timeout=self.timeout_seconds) as client:
            response = client.post(f"{self.base_url}/responses", headers=headers, json=payload)
            response.raise_for_status()
            body = response.json()

        raw_text = _extract_response_text(body)
        return ModelResponse(
            raw_text=raw_text,
            provider="openai",
            model_id=str(body.get("model", self.model_id)),
            api_version=self.api_version,
            generation={
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_output_tokens": self.max_output_tokens,
                "seed": self.seed,
            },
            metadata={
                "response_id": body.get("id"),
                "service_tier": body.get("service_tier"),
                "usage": body.get("usage"),
            },
        )


def _extract_response_text(body: dict[str, Any]) -> str:
    """Extract Responses API message text without assuming one response shape."""
    direct = body.get("output_text")
    if isinstance(direct, str):
        return direct

    chunks: list[str] = []
    for item in body.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if not isinstance(content, dict):
                continue
            text = content.get("text")
            if isinstance(text, str):
                chunks.append(text)
    if chunks:
        return "".join(chunks)
    raise ValueError("OpenAI response did not contain extractable text output.")
