from vancouver_watching.ai import DEFAULT_MODEL, TEST_OBJECT
from vancouver_watching.area import Area


def test_Area(
    geojson_filename,
    model_id,
):
    area = Area(geojson_filename)
    assert area.valid

    assert area.ingest(
        count=1,
    )

    assert area.detect_objects(
        model_id=model_id,
        count=1,
    )

    assert area.summarize()
