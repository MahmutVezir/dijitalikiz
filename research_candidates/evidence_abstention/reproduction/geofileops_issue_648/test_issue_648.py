"""Independent default destination-layer reproducer for geofileops issue #648."""
from __future__ import annotations

import geopandas as gpd
import geofileops as gfo
from shapely.geometry import Point


def _write_source(path):
    frame = gpd.GeoDataFrame(
        {"feature_id": [1, 2], "label": ["one", "two"]},
        geometry=[Point(4.0, 50.0), Point(4.1, 50.1)],
        crs="EPSG:31370",
    )
    frame.to_file(path, driver="GPKG", layer="source_layer", engine="pyogrio")


def test_copy_layer_default_destination_layer_uses_destination_stem(tmp_path):
    source = tmp_path / "source.gpkg"
    destination = tmp_path / "destination_result.gpkg"
    _write_source(source)

    gfo.copy_layer(source, destination)

    assert gfo.listlayers(destination) == [destination.stem]


def test_copy_layer_explicit_destination_layer_is_preserved(tmp_path):
    source = tmp_path / "source.gpkg"
    destination = tmp_path / "destination_result.gpkg"
    _write_source(source)

    gfo.copy_layer(source, destination, dst_layer="explicit_result")

    assert gfo.listlayers(destination) == ["explicit_result"]
