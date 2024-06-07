import os
from dotenv import load_dotenv
import redis

load_dotenv()

BTS_API_URL = os.getenv("BTS_API_URL")
BTS_TOKEN = os.getenv("BTS_TOKEN")

REDIS_HOST = os.getenv("REDIS_HOST")
redis = redis.Redis(host=REDIS_HOST, port=6379, db=0)
