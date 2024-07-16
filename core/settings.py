import os
from dotenv import load_dotenv
import redis

load_dotenv()

BTS_API_URL = os.getenv("BTS_API_URL")
BTS_TOKEN = os.getenv("BTS_TOKEN")
TRACKED_VEHICLES = os.getenv("TRACKED_VEHICLES").split(" ")

REDIS_HOST = os.getenv("REDIS_HOST")
redis = redis.Redis(host=REDIS_HOST, port=6379, db=0)

DATABASE_URL = os.getenv(
    "DB_HOST",
    default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres"
)  # connect string for the real database
