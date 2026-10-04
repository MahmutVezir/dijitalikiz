import json
from pathlib import Path

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.models import ResearchCase

PILOT_DIR = Path("data/pilot")

def test_three_pilot_cases_are_context_isolated():
    files = sorted(PILOT_DIR.glob("commons-math-defects4j-MATH-*.json"))
    assert {p.stem for p in files} == {
        "commons-math-defects4j-MATH-927",
        "commons-math-defects4j-MATH-950",
        "commons-math-defects4j-MATH-988",
    }
    for path in files:
        case = ResearchCase.from_dict(json.loads(path.read_text(encoding="utf-8")))
        for rendered in (render_standard_context(case), render_ccdg_context(case)):
            assert case.ground_truth.root_cause not in rendered
            assert "ground_truth" not in rendered.lower()
