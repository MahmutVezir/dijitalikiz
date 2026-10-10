import copy
import json
from pathlib import Path

from scripts.audit_followup_v2_tokenizer import build_token_audit, sha256_bytes, sha256_text


class FakeTokenizer:
    name_or_path = "fake-test-tokenizer"
    chat_template = "system{{content}}user{{content}}assistant"
    special_tokens_map = {"bos_token": "<BOS>"}

    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=True):
        assert tokenize is False
        assert add_generation_prompt is True
        return (
            "<BOS><SYSTEM>" + messages[0]["content"]
            + "</SYSTEM><USER>" + messages[1]["content"]
            + "</USER><ASSISTANT>"
        )

    def __call__(self, texts, return_tensors=None):
        assert isinstance(texts, list) and len(texts) == 1
        # Deterministic synthetic IDs for unit tests only; never used as a real tokenizer.
        return {"input_ids": [[ord(char) for char in texts[0]]]}


def prepare_root(tmp_path: Path):
    root = tmp_path
    (root / "data/pilot").mkdir(parents=True)
    (root / "data/followup_v2/cases").mkdir(parents=True)
    system = "system-test\n"
    task = "task-test\n"
    (root / "data/pilot/SYSTEM_PROMPT.txt").write_text(system, encoding="utf-8")
    (root / "data/pilot/PROMPT_TEMPLATE.txt").write_text(task, encoding="utf-8")
    source_case_path = Path(__file__).resolve().parents[1] / "data/benchmark/cases/commons-math-defects4j-MATH-305.json"
    case = json.loads(source_case_path.read_text(encoding="utf-8"))
    case["split"] = "followup_v2_confirmatory"
    case["software_twin_snapshot"] = {
        "repository_url": "https://github.com/example/project",
        "snapshot_revision": "a" * 40,
        "regression_test": "ExampleTest#failsBeforeFix",
        "observed_failure_signal": "Pinned regression failed before the fix."
    }
    # Avoid root cause text appearing literally in a synthetic-context test fixture.
    case["ground_truth"]["root_cause"] = "UNIQUE_GROUND_TRUTH_SENTINEL"
    (root / "data/followup_v2/cases/test-case.json").write_text(
        json.dumps(case), encoding="utf-8"
    )
    manifest = {
        "model": {"model_id": "test-model", "revision": "b" * 40},
        "prompts": {
            "generation_reserve_tokens": 256,
            "max_context_tokens": 32768,
            "system_prompt_path": "data/pilot/SYSTEM_PROMPT.txt",
            "system_prompt_sha256": sha256_bytes(system.encode("utf-8")),
            "task_prompt_path": "data/pilot/PROMPT_TEMPLATE.txt",
            "task_prompt_sha256": sha256_bytes(task.encode("utf-8"))
        },
        "case_pool": {
            "case_ids": ["test-case"],
            "minimum_independent_case_count": 1,
            "case_directory": "data/followup_v2/cases",
            "split_name": "followup_v2_confirmatory"
        }
    }
    return root, manifest


def test_tokenizer_audit_emits_three_hashed_cells_and_no_model_outputs(tmp_path):
    root, manifest = prepare_root(tmp_path)
    report = build_token_audit(
        manifest=manifest,
        root=root,
        tokenizer=FakeTokenizer(),
        transformers_version="test-only",
    )
    assert report["status"] == "pass"
    assert report["case_count"] == 1
    assert report["actual_prompt_cell_count"] == 3
    assert {row["condition_id"] for row in report["prompts"]} == {"A", "B", "C"}
    assert all(len(row["rendered_chat_input_sha256"]) == 64 for row in report["prompts"])
    assert all(row["fits_context_limit"] for row in report["prompts"])
    assert all("raw_output" not in row for row in report["prompts"])


def test_tokenizer_audit_blocks_when_prompt_exceeds_generation_budget(tmp_path):
    root, manifest = prepare_root(tmp_path)
    manifest["prompts"]["max_context_tokens"] = 100
    report = build_token_audit(
        manifest=manifest,
        root=root,
        tokenizer=FakeTokenizer(),
        transformers_version="test-only",
    )
    assert report["status"] == "blocked"
    assert any(item.startswith("context_overflow:") for item in report["failures"])


def test_tokenizer_audit_rejects_system_prompt_hash_mismatch(tmp_path):
    root, manifest = prepare_root(tmp_path)
    manifest["prompts"]["system_prompt_sha256"] = "0" * 64
    try:
        build_token_audit(
            manifest=manifest,
            root=root,
            tokenizer=FakeTokenizer(),
            transformers_version="test-only",
        )
    except ValueError as exc:
        assert "System-prompt SHA-256" in str(exc)
    else:
        raise AssertionError("Expected prompt hash mismatch to block the audit.")
