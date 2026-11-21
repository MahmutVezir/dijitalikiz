"""Independent reproducers for the Meltano #3090 sibling-reference defect."""
from __future__ import annotations

import copy
import importlib.util
import os
import sys
import unittest
from pathlib import Path


def load_schema_module():
    source = Path(os.environ["MELTANO_SOURCE_ROOT"]) / "singer_sdk" / "singerlib" / "schema.py"
    spec = importlib.util.spec_from_file_location("meltano_schema_under_test", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load exact schema source: {source}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class MeltanoIssue3090Regression(unittest.TestCase):
    def test_repeated_direct_resolver_lookup_returns_target_each_time(self) -> None:
        """E2 diagnostic: the resolver itself must return the target on repeat lookups."""
        module = load_schema_module()
        components = {
            "schemas": {
                "ComputeUnit": {"type": "number"},
            },
        }
        registry = module.Registry().with_resources(
            [("components", module.DRAFT202012.create_resource(components))]
        )
        resolver = registry.resolver()

        first = resolver.lookup("components#/schemas/ComputeUnit").contents
        second = resolver.lookup("components#/schemas/ComputeUnit").contents

        self.assertEqual(first, {"type": "number"})
        self.assertEqual(second, {"type": "number"})
        self.assertEqual(first, second)

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
