"""Independent reproducer for repeated sibling JSON Schema references."""
from __future__ import annotations

import copy
import importlib.util
import os
from pathlib import Path
import unittest


def load_schema_module():
    source = Path(os.environ["MELTANO_SOURCE_ROOT"]) / "singer_sdk" / "singerlib" / "schema.py"
    spec = importlib.util.spec_from_file_location("meltano_schema_under_test", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load exact schema source: {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MeltanoIssue3090Regression(unittest.TestCase):
    def test_sibling_properties_can_resolve_the_same_reference(self) -> None:
        module = load_schema_module()
        schema = {
            "type": "object",
            "properties": {
                "min_compute_units": {"$ref": "components#/schemas/ComputeUnit"},
                "max_compute_units": {"$ref": "components#/schemas/ComputeUnit"},
            },
        }
        refs = {
            "components": {
                "schemas": {
                    "ComputeUnit": {"type": "number"},
                },
            },
        }

        resolved = module.resolve_schema_references(copy.deepcopy(schema), refs)
        self.assertEqual(
            resolved["properties"],
            {
                "min_compute_units": {"type": "number"},
                "max_compute_units": {"type": "number"},
            },
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
