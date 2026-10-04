def test_contexts_do_not_expose_ground_truth():
    from pathlib import Path
    import json
    from dijitalikiz.models import ResearchCase
    from dijitalikiz.context import render_standard_context, render_ccdg_context
    p = Path("data/sample_cases/supabase_rls_case.json")
    case = ResearchCase.from_dict(json.loads(p.read_text(encoding="utf-8")))
    for rendered in (render_standard_context(case), render_ccdg_context(case)):
        assert "Ground truth:" not in rendered
        assert case.ground_truth.root_cause not in rendered
