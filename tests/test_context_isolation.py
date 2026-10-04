import json
from pathlib import Path
from dijitalikiz.context import render_standard_context, render_ccdg_context
from dijitalikiz.models import ResearchCase

def test_context_does_not_include_ground_truth():
    p=Path("data/sample_cases/supabase_rls_case.json")
    case=ResearchCase.from_dict(json.loads(p.read_text(encoding="utf-8")))
    for text in (render_standard_context(case),render_ccdg_context(case)):
        assert "Ground truth:" not in text
        assert case.ground_truth.root_cause not in text
