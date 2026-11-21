"""Independent tagged-recursion reproducer for ASDF issue #1821 / PR #1907."""
from __future__ import annotations

import io

from asdf import util


ASDF_HEADER = b"""#ASDF 1.0.0
#ASDF_STANDARD 1.6.0
%YAML 1.1
%TAG ! tag:stsci.edu:asdf/
--- !core/asdf-1.1.0
"""

MAPPING_RECURSION = ASDF_HEADER + b"""o: &id001 !some/tag-1.0.0
  inverse: !some/tag-1.0.0
    inverse: *id001
...
"""

SEQUENCE_RECURSION = ASDF_HEADER + b"""l: &id002 !some/tag-1.0.0
  - *id002
...
"""


def _load(contents: bytes, *, tagged: bool):
    return util.load_yaml(io.BytesIO(contents), tagged=tagged)


def test_untagged_loader_preserves_recursive_tagged_mapping():
    tree = _load(MAPPING_RECURSION, tagged=False)
    assert tree["o"] is tree["o"]["inverse"]["inverse"]


def test_untagged_loader_preserves_recursive_tagged_sequence():
    tree = _load(SEQUENCE_RECURSION, tagged=False)
    assert tree["l"] is tree["l"][0]


def test_tagged_loader_is_positive_control_for_mapping_and_sequence():
    mapping = _load(MAPPING_RECURSION, tagged=True)
    sequence = _load(SEQUENCE_RECURSION, tagged=True)
    assert mapping["o"] is mapping["o"]["inverse"]["inverse"]
    assert sequence["l"] is sequence["l"][0]
