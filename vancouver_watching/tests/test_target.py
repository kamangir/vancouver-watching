import pytest

from blue_objects import path, file, objects

from vancouver_watching import env
from vancouver_watching.target import Target


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
    assert objects.download(object_name)

    assert path.exists(objects.object_path(object_name))

    list_of_files = [
        file.name_and_extension(filename)
        for filename in objects.list_of_files(object_name=object_name)
    ]

    assert "vancouver.json" in list_of_files, objects.path_of(
        object_name=object_name,
        filename="vancouver.json",
    )

    assert file.exists(
        objects.path_of(
            object_name=object_name,
            filename="vancouver.json",
        )
    )

    # ----

    geojson_filename = objects.path_of(
        object_name=object_name,
        filename="vancouver.geojson",
    )
    target = Target(geojson_filename)
    assert target.valid

    assert target.ingest(
        count=1,
    )

    assert target.detect_objects(
        model_id=model_id,
        count=1,
    )

    assert target.summarize()
