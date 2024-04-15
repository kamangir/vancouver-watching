from abcli.tests import test_env
from vancouver_watching import env


def test_abcli_env():
    test_env.test_abcli_env()


def test_vanwatch_env():
    assert env.ULTRALYTICS_API_KEY
    assert env.VANWATCH_DEFAULT_MODEL
    assert env.VANWATCH_TEST_OBJECT
