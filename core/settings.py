import os
from dotenv import load_dotenv

load_dotenv()

BTS_API_URL = os.getenv("BTS_API_URL")
BTS_TOKEN = os.getenv("BTS_TOKEN")