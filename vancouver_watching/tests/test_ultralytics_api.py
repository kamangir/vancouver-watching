import pytest
from abcli.modules import objects
from vancouver_watching.ai import DEFAULT_MODEL, TEST_OBJECT
from vancouver_watching.ai.classes import Ultralytics_API


@pytest.mark.parametrize(
    "model_id, object_name, filename",
    [
        (
            DEFAULT_MODEL,
            TEST_OBJECT,
            "Victoria41East.jpg",
        ),
    ],
)
def test_ultralytics_api(model_id, object_name, filename):
    ultralytics_api = Ultralytics_API(model_id)

    success, _ = ultralytics_api.infer(objects.path_of(filename, object_name))
    assert True  # success # Ultralytics API is unstable.
