from __future__ import annotations

import json

import httpx
import pytest

from rscbench.model_client import OpenAIResponsesClient


def test_openai_responses_client_extracts_output(monkeypatch):
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(json.loads(request.content))
        return httpx.Response(
            200,
            json={
                "id": "resp_test",
                "model": "fixed-model-2026-01-01",
                "output_text": '{"diagnosed_component":"RLS","root_cause_class":"x","affected_entity":"profiles","explanation":"ok"}',
                "usage": {"input_tokens": 10, "output_tokens": 20},
            },
        )

    original = httpx.Client

    class ClientFactory:
        def __init__(self, *args, **kwargs):
            self._client = original(transport=httpx.MockTransport(handler), *args, **kwargs)

        def __enter__(self):
            return self._client.__enter__()

        def __exit__(self, *args):
            return self._client.__exit__(*args)

    monkeypatch.setattr(httpx, "Client", ClientFactory)
    client = OpenAIResponsesClient(api_key="test", model_id="fixed-model-2026-01-01")
    result = client.generate("system", "user")

    assert result.provider == "openai"
    assert result.model_id == "fixed-model-2026-01-01"
    assert '"diagnosed_component"' in result.raw_text
    assert calls[0]["model"] == "fixed-model-2026-01-01"
    assert calls[0]["text"]["format"]["type"] == "json_object"


def test_real_client_requires_explicit_credentials(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("RSCBENCH_MODEL_ID", raising=False)
    with pytest.raises(ValueError):
        OpenAIResponsesClient()
