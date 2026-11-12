import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = (
    ROOT
    / "research_candidates"
    / "evidence_abstention"
    / "03_kaggle_current_branch_no_inference_audit.ipynb"
)
PREFLIGHT_SCRIPT = ROOT / "scripts" / "evidence_abstention_preflight.py"


def test_current_branch_kaggle_notebook_is_valid_and_compiles():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert notebook.get("nbformat") == 4
    code_cells = [
        cell for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "code"
    ]
    assert code_cells
    for index, cell in enumerate(code_cells):
        source = "".join(cell.get("source", []))
        compile(source, f"{NOTEBOOK.name}:cell-{index}", "exec")


def test_current_branch_kaggle_notebook_code_cells_have_executable_ast_and_line_boundaries():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    code_cells = [
        cell for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "code"
    ]
    assert code_cells

    for index, cell in enumerate(code_cells):
        fragments = cell.get("source", [])
        source = "".join(fragments)
        tree = ast.parse(source, filename=f"{NOTEBOOK.name}:cell-{index}")

        assert tree.body, (
            f"Code cell {index} is empty or comment-only"
        )
        assert all(
            fragment.endswith("\n")
            for fragment in fragments[:-1]
        ), (
            f"Code cell {index} has missing line terminators between source fragments"
        )


def test_current_branch_kaggle_notebook_is_strictly_no_inference():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    source = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "code"
    )
    for forbidden in (
        "AutoModelForCausalLM.from_pretrained",
        "AutoTokenizer.from_pretrained",
        ".generate(",
        "Trainer(",
        "optimizer.step(",
        "pip install",
        "kaggle kernels push",
        "kaggle kernels start",
    ):
        assert forbidden not in source
    assert "'model_inference_performed': False" in source
    assert "'model_training_performed': False" in source
    assert "EXPECTED_SOURCE_COMMIT" in source
    assert "EXPECTED_MANIFEST_GIT_BLOB_SHA1" in source


def test_current_branch_kaggle_notebook_audits_both_exposure_unions():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    source = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "code"
    )
    preflight_source = PREFLIGHT_SCRIPT.read_text(encoding="utf-8")

    # The notebook delegates the read-only exposure-union gate to the
    # canonical preflight script and runs that script's dedicated test module.
    assert "evidence_abstention_preflight.py" in source
    assert "tests/test_evidence_abstention_preflight.py" in source
    assert "BASE_EXPOSURE_UNION_PATH" in preflight_source
    assert "SCREENING_EXPOSURE_UNION_PATH" in preflight_source
    assert "EXPOSURE_UNION_2026-10-23.json" in preflight_source
    assert "EXPOSURE_UNION_2026-11-11.json" in preflight_source
    assert "pytest" in source
