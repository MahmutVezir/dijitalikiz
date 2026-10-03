from rscbench.canonicalize import canonical_json, canonical_text

def test_canonical_json_is_stable():
    assert canonical_json({"b": 2, "a": 1}) == '{"a":1,"b":2}'

def test_canonical_text_normalizes_line_endings():
    assert canonical_text(" a\r\nb \r") == "a\nb"
