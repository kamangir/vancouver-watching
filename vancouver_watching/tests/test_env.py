from bluer_ai.tests.test_env import test_bluer_ai_env
from bluer_objects.tests.test_env import test_bluer_objects_env

from vancouver_watching import env


def test_required_env():
    test_bluer_ai_env()
    test_bluer_objects_env()


def test_vanwatch_env():
    assert env.ULTRALYTICS_API_KEY
    assert env.VANWATCH_DEFAULT_MODEL
    assert env.VANWATCH_TEST_OBJECT
    assert env.VANWATCH_QGIS_TEMPLATE
