import os
from dotenv import load_dotenv

load_dotenv()

ULTRALYTICS_API_KEY = os.getenv("ULTRALYTICS_API_KEY", "")

VANWATCH_DEFAULT_MODEL = os.getenv("VANWATCH_DEFAULT_MODEL", "R6nMlK6kQjSsQ76MPqQM")

VANWATCH_TEST_OBJECT = os.getenv("VANWATCH_TEST_OBJECT", "vanwatch-test-object-v2")
