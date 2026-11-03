import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = (
    ROOT
    / "research_candidates"
    / "evidence_abstention"
    / "02_kaggle_source_integrity_and_tests_no_inference.ipynb"
)


def load_notebook():
    return json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))


def code_source(notebook):
    return "\n\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "code"
    )


def test_no_inference_audit_notebook_is_valid_and_code_cells_compile():
    notebook = load_notebook()
    assert notebook.get("nbformat") == 4
    assert notebook.get("nbformat_minor", 0) >= 4
    code_cells = [
        cell for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    ]
    assert code_cells
    for index, cell in enumerate(code_cells):
        fragments = cell.get("source", [])
        source = "".join(fragments)
        compile(source, f"{NOTEBOOK_PATH.name}:cell-{index}", "exec")


def test_no_inference_audit_notebook_code_cells_have_executable_ast_and_line_boundaries():
    notebook = load_notebook()
    code_cells = [
        cell for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    ]
    assert code_cells

    for index, cell in enumerate(code_cells):
        fragments = cell.get("source", [])
        source = "".join(fragments)
        tree = ast.parse(source, filename=f"{NOTEBOOK_PATH.name}:cell-{index}")

        assert tree.body, (
            f"Code cell {index} is empty or comment-only"
        )
        assert all(
            fragment.endswith("\\n")
            for fragment in fragments[:-1]
        ), (
            f"Code cell {index} has missing line terminators between source fragments"
        )


def test_no_inference_notebook_does_not_load_generate_or_train_a_model():
    source = code_source(load_notebook())
    forbidden = (
        "AutoModelForCausalLM.from_pretrained",
        "AutoTokenizer.from_pretrained",
        ".generate(",
        "Trainer(",
        "optimizer.step(",
        "pip install",
        "kaggle kernels push",
        "kaggle kernels start",
    )
    for token in forbidden:
        assert token not in source


def test_notebook_pins_the_reviewed_source_snapshot_and_fails_closed():
    source = code_source(load_notebook())
    assert "99663c2874424feb9cec1d965432030f5cdb3ef8" in source
    assert "git_blob_sha1" in source
    assert "Expected 31 v2 manifest entries" in source
    assert "Expected 9 test modules" in source
    assert "source_integrity" in source
    assert "evidence_abstention_preflight.py" in source
    assert "'model_inference_performed': False" in source
    assert "'model_training_performed': False" in source
    assert "'case_registry_modified': False" in source
    assert "'experiment_manifest_modified': False" in source
