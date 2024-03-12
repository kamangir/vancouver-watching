import os
from dotenv import load_dotenv

load_dotenv(".env")
load_dotenv("config.env")

ULTRALYTICS_API_KEY = os.getenv("ULTRALYTICS_API_KEY", "")

VANWATCH_DEFAULT_MODEL = os.getenv("VANWATCH_DEFAULT_MODEL", "")

VANWATCH_TEST_OBJECT = os.getenv("VANWATCH_TEST_OBJECT", "")
