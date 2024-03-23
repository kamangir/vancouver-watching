import os
from dotenv import load_dotenv

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(parent_dir, ".env"))
load_dotenv(os.path.join(parent_dir, "config.env"))

ULTRALYTICS_API_KEY = os.getenv("ULTRALYTICS_API_KEY", "")

VANWATCH_DEFAULT_MODEL = os.getenv("VANWATCH_DEFAULT_MODEL", "")

VANWATCH_TEST_OBJECT = os.getenv("VANWATCH_TEST_OBJECT", "")
