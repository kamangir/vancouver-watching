import pytest
from abcli.modules import objects
from vancouver_watching import env
from vancouver_watching.area import Area


@pytest.mark.parametrize(
    [
        "geojson_filename",
        "model_id",
    ],
    [
        (
            objects.path_of("vancouver.geojson", env.VANWATCH_TEST_OBJECT),
            env.VANWATCH_DEFAULT_MODEL,
        ),
    ],
)
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
