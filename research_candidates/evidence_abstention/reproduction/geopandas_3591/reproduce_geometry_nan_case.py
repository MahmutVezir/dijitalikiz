#!/usr/bin/env python3
"""Reproduce the frozen GeoPandas #3591 constructor input without modifying upstream source."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import sys
from pathlib import Path

EXPECTED_ERROR = (
    "Assigning CRS to a GeoDataFrame without a geometry column is not supported."
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--expected", choices=("base-failure", "fixed-pass"), required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    source_root = args.source_root.resolve()
    sys.path.insert(0, str(source_root))

    import numpy as np
    import pandas as pd
    import geopandas as gpd
    from geopandas import GeoDataFrame

    module_path = Path(gpd.__file__).resolve()
    if not module_path.is_relative_to(source_root):
        raise SystemExit(f"Imported GeoPandas from outside the pinned checkout: {module_path}")

    observed: dict[str, object] = {
        "expected_mode": args.expected,
        "geopandas_version": gpd.__version__,
        "geopandas_module": str(module_path),
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "input": {
            "data": [["np.nan", "np.nan"]],
            "columns": ["geometry", "something"],
            "crs": "EPSG:4326",
        },
    }

    try:
        gdf = GeoDataFrame(
            data=[[np.nan, np.nan]],
            columns=["geometry", "something"],
            crs="EPSG:4326",
        )
    except Exception as exc:  # captured so the expected base failure remains a passing experiment step
        observed["observed_exception_type"] = type(exc).__name__
        observed["observed_exception_message"] = str(exc)
        if args.expected != "base-failure":
            raise
        if not isinstance(exc, ValueError) or EXPECTED_ERROR not in str(exc):
            raise SystemExit(
                "Base did not produce the exact expected CRS-without-geometry ValueError"
            ) from exc
        observed["outcome"] = "expected_bug_reproduced"
    else:
        observed["observed_exception_type"] = None
        observed["observed_exception_message"] = None
        if args.expected != "fixed-pass":
            raise SystemExit(
                "Buggy base unexpectedly constructed the all-NaN GeoDataFrame"
            )
        if gdf.shape != (1, 2):
            raise SystemExit(f"Unexpected fixed shape: {gdf.shape!r}")
        if gdf.active_geometry_name != "geometry":
            raise SystemExit(
                f"Unexpected active geometry: {gdf.active_geometry_name!r}"
            )
        if gdf.geometry.iloc[0] is not None:
            raise SystemExit("The all-NaN geometry value was not normalized to None")
        if gdf.crs != "EPSG:4326":
            raise SystemExit(f"Unexpected CRS: {gdf.crs!r}")
        observed["outcome"] = "expected_fix_behavior_observed"
        observed["shape"] = list(gdf.shape)
        observed["active_geometry_name"] = gdf.active_geometry_name
        observed["geometry_value_is_none"] = gdf.geometry.iloc[0] is None
        observed["crs"] = str(gdf.crs)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(observed, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(observed, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
