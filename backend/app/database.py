from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)

db = client["link_saver"]
users_collection = db["users"]
bookmarks_collection = db["bookmarks"]
