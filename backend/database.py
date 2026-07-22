import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load .env
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Environment Variables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Mongo Client
client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000,
    socketTimeoutMS=5000,
    maxPoolSize=50
)

# Test Connection
client.admin.command("ping")
print("✅ MongoDB Connected Successfully")

# Database
db = client[DB_NAME]
collection = db[COLLECTION_NAME]