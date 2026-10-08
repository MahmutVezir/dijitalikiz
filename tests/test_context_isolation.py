import json
from pathlib import Path

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.models import ResearchCase


def test_context_does_not_include_ground_truth():
    path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "pilot"
        / "commons-math-defects4j-MATH-927.json"
    )
    case = ResearchCase.from_dict(json.loads(path.read_text(encoding="utf-8")))
    for rendered in (render_standard_context(case), render_ccdg_context(case)):
        assert "Ground truth:" not in rendered
        assert case.ground_truth.root_cause not in rendered
        assert "non_serializable_dependency_in_inheritance_chain" not in rendered
