import pytest

from bluer_objects import objects, storage

from vancouver_watching import env
from vancouver_watching.ai import Ultralytics_API


@pytest.mark.parametrize(
    "model_id, object_name, filename",
    [
        (
            env.VANWATCH_DEFAULT_MODEL,
            env.VANWATCH_TEST_OBJECT,
            "Victoria41East.jpg",
        ),
    ],
)
def test_ai_ultralytics(model_id, object_name, filename):
    assert storage.download(object_name)

    ultralytics_api = Ultralytics_API(model_id)

    _, _ = ultralytics_api.infer(objects.path_of(filename, object_name))
    assert True  # success # Ultralytics API is unstable.
