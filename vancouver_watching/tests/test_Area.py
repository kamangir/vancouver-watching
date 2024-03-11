import pytest
from abcli.modules import objects
from abcli.plugins.testing import download_object
from vancouver_watching import env
from vancouver_watching.area import Area


@pytest.mark.parametrize(
    [
        "object_name",
        "model_id",
    ],
    [
        (
            env.VANWATCH_TEST_OBJECT,
            env.VANWATCH_DEFAULT_MODEL,
        ),
    ],
)
def test_Area(
    object_name,
    model_id,
):
    assert download_object(object_name)

    geojson_filename = objects.path_of(
        object_name=object_name,
        filename="vancouver.geojson",
    )
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
