import pytest
from vancouver_watching.area import Area


def test_area(geojson_filename, count, test_object):
    object_name = "..."
    area = Area(geojson_filename)

    assert area.valid

    assert area.ingest(count=count)
