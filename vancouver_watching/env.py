import os
from abcli.env import load_env, load_config

load_env(__name__)
load_config(__name__)

ULTRALYTICS_API_KEY = os.getenv("ULTRALYTICS_API_KEY", "")

VANWATCH_DEFAULT_MODEL = os.getenv("VANWATCH_DEFAULT_MODEL", "")

VANWATCH_TEST_OBJECT = os.getenv("VANWATCH_TEST_OBJECT", "")
