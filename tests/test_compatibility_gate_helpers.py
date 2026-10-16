from contextlib import nullcontext
from types import SimpleNamespace

import pytest

from scripts.compatibility_gate import (
    inspect_checkpoint_loading_info,
    logits_are_finite,
    run_sampling_smoke,
    sampling_smoke_settings,
)


class FakeScalar:
    def __init__(self, value):
        self.value = value

    def item(self):
        return self.value


class FakeTensor:
    def __init__(self, *, finite=True, shape=(1, 1, 8)):
        self.finite = finite
        self.shape = shape

    def all(self):
        return FakeScalar(self.finite)


class FakeCuda:
    def __init__(self):
        self.seeds = []

    @staticmethod
    def is_available():
        return False

    def manual_seed_all(self, seed):
        self.seeds.append(seed)


class FakeTorch:
    def __init__(self):
        self.seeds = []
        self.cuda = FakeCuda()

    @staticmethod
    def inference_mode():
        return nullcontext()

    @staticmethod
    def isfinite(tensor):
        return tensor

    def manual_seed(self, seed):
        self.seeds.append(seed)


class FakeInputs(dict):
    def __init__(self):
        super().__init__(input_ids=[[1, 2, 3, 4]])
        self.input_ids = SimpleNamespace(shape=(1, 4))

    def to(self, _device):
        return self


class FakeModel:
    device = "cpu"
    config = SimpleNamespace(tie_word_embeddings=False)

    def __init__(self, *, finite=True, generation_error=None, output=None):
        self.finite = finite
        self.generation_error = generation_error
        self.output = output if output is not None else [[1, 2, 3, 4, 99]]
        self.generation_kwargs = None

    def __call__(self, **_kwargs):
        return SimpleNamespace(logits=FakeTensor(finite=self.finite))

    def generate(self, **kwargs):
        self.generation_kwargs = kwargs
        if self.generation_error:
            raise self.generation_error
        return self.output


class FakeTokenizer:
    def __init__(self, text='{"ok":true}'):
        self.text = text
        self.decoded_tokens = None

    def decode(self, tokens, *, skip_special_tokens):
        self.decoded_tokens = tokens
        assert skip_special_tokens is True
        return self.text


def frozen_generation():
    return {
        "do_sample": True,
        "temperature": 0.2,
        "top_p": 1.0,
        "max_new_tokens": 256,
        "seeds": [42, 43, 44, 45, 46],
    }


def recording_check():
    records = []

    def check(name, ok, detail):
        records.append({"name": name, "status": "pass" if ok else "fail", "detail": detail})

    return records, check


def test_checkpoint_loading_info_accepts_matching_weights_and_tied_lm_head():
    summary = inspect_checkpoint_loading_info(
        {"missing_keys": [], "unexpected_keys": [], "mismatched_keys": [], "error_msgs": []},
        tie_word_embeddings=False,
    )
    assert summary["matches"] is True

    tied = inspect_checkpoint_loading_info(
        {"missing_keys": ["lm_head.weight"], "unexpected_keys": [], "mismatched_keys": [], "error_msgs": []},
        tie_word_embeddings=True,
    )
    assert tied["matches"] is True
    assert tied["missing_keys"] == []


@pytest.mark.parametrize(
    "field,value",
    [
        ("missing_keys", ["model.layers.0.weight"]),
        ("unexpected_keys", ["unexpected.weight"]),
        ("mismatched_keys", [("model.layers.0.weight", (1,), (2,))]),
        ("error_msgs", ["checkpoint tensor load error"]),
    ],
)
def test_checkpoint_loading_info_rejects_each_mismatch_class(field, value):
    loading_info = {
        "missing_keys": [],
        "unexpected_keys": [],
        "mismatched_keys": [],
        "error_msgs": [],
    }
    loading_info[field] = value
    assert inspect_checkpoint_loading_info(loading_info, tie_word_embeddings=False)["matches"] is False


def test_sampling_settings_match_frozen_pilot_and_cap_only_smoke_length():
    seed, max_new_tokens, kwargs = sampling_smoke_settings(frozen_generation())
    assert seed == 42
    assert max_new_tokens == 96
    assert kwargs == {"temperature": 0.2, "top_p": 1.0}


@pytest.mark.parametrize(
    "changes",
    [
        {"do_sample": False},
        {"temperature": 0},
        {"temperature": float("nan")},
        {"top_p": 0},
        {"top_p": 1.1},
        {"max_new_tokens": 0},
        {"seeds": [True, 43]},
    ],
)
def test_invalid_sampling_settings_are_rejected(changes):
    generation = frozen_generation()
    generation.update(changes)
    with pytest.raises(ValueError):
        sampling_smoke_settings(generation)


def test_sampling_smoke_executes_the_configured_sampling_path():
    model = FakeModel()
    tokenizer = FakeTokenizer()
    torch_module = FakeTorch()
    inputs = FakeInputs()
    records, check = recording_check()

    raw = run_sampling_smoke(
        model=model,
        tokenizer=tokenizer,
        inputs=inputs,
        torch_module=torch_module,
        generation=frozen_generation(),
        device_map={"": "cpu"},
        check=check,
    )

    assert raw == '{"ok":true}'
    assert model.generation_kwargs["do_sample"] is True
    assert model.generation_kwargs["temperature"] == 0.2
    assert model.generation_kwargs["top_p"] == 1.0
    assert model.generation_kwargs["max_new_tokens"] == 96
    assert torch_module.seeds == [42]
    assert tokenizer.decoded_tokens == [99]
    assert {item["name"]: item["status"] for item in records} == {
        "smoke_logits_finite": "pass",
        "pilot_sampling_smoke": "pass",
    }


def test_nonfinite_logits_block_sampling_and_are_reported():
    model = FakeModel(finite=False)
    records, check = recording_check()
    with pytest.raises(RuntimeError, match="NaN or infinity"):
        run_sampling_smoke(
            model=model,
            tokenizer=FakeTokenizer(),
            inputs=FakeInputs(),
            torch_module=FakeTorch(),
            generation=frozen_generation(),
            device_map="cpu",
            check=check,
        )
    assert {item["name"]: item["status"] for item in records} == {
        "smoke_logits_finite": "fail",
        "pilot_sampling_smoke": "fail",
    }
    assert model.generation_kwargs is None


def test_sampling_exception_is_recorded_as_failure():
    model = FakeModel(generation_error=RuntimeError("synthetic generation failure"))
    records, check = recording_check()
    with pytest.raises(RuntimeError, match="synthetic generation failure"):
        run_sampling_smoke(
            model=model,
            tokenizer=FakeTokenizer(),
            inputs=FakeInputs(),
            torch_module=FakeTorch(),
            generation=frozen_generation(),
            device_map="cpu",
            check=check,
        )
    assert {item["name"]: item["status"] for item in records} == {
        "smoke_logits_finite": "pass",
        "pilot_sampling_smoke": "fail",
    }


def test_empty_sampling_output_is_not_reported_as_success():
    model = FakeModel()
    records, check = recording_check()
    with pytest.raises(RuntimeError, match="empty output"):
        run_sampling_smoke(
            model=model,
            tokenizer=FakeTokenizer("  "),
            inputs=FakeInputs(),
            torch_module=FakeTorch(),
            generation=frozen_generation(),
            device_map="cpu",
            check=check,
        )
    assert records[-1]["name"] == "pilot_sampling_smoke"
    assert records[-1]["status"] == "fail"
