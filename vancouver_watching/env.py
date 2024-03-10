import os
from dotenv import load_dotenv

load_dotenv()

ULTRALYTICS_API_KEY = os.getenv("ULTRALYTICS_API_KEY", "")
