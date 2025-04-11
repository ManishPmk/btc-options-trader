import os
from dotenv import load_dotenv

load_dotenv()  # Automatically loads .env from project root

DELTA_API_KEY = os.getenv("DELTA_API_KEY")
DELTA_API_SECRET = os.getenv("DELTA_API_SECRET")
