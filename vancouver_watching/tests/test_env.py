from abcli.tests.test_env import test_abcli_env
from blue_objects.tests.test_env import test_blue_objects_env

from vancouver_watching import env


def test_required_env():
    test_abcli_env()
    test_blue_objects_env()


def test_vanwatch_env():
    assert env.ULTRALYTICS_API_KEY
    assert env.VANWATCH_DEFAULT_MODEL
    assert env.VANWATCH_TEST_OBJECT
