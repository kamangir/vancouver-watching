from bluer_options.env import load_config, load_env, get_env

load_env(__name__)
load_config(__name__)

ULTRALYTICS_API_KEY = get_env("ULTRALYTICS_API_KEY")

VANWATCH_DEFAULT_MODEL = get_env("VANWATCH_DEFAULT_MODEL")

VANWATCH_TEST_OBJECT = get_env("VANWATCH_TEST_OBJECT")

VANWATCH_QGIS_TEMPLATE = get_env("VANWATCH_QGIS_TEMPLATE")
