import os
from typing import Generator

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "bookdb")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "books")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
books_collection: Collection = db[MONGO_COLLECTION_NAME]

books_collection.create_index("id", unique=True)


def get_db() -> Generator[Collection, None, None]:
    try:
        yield books_collection
    finally:
        pass
