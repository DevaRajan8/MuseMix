import pymongo
from pymongo import MongoClient
from models.model import get_image_embedding
import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["musemix"]
collection_name = "musemix"

if collection_name not in db.list_collection_names():
    print(f"Collection {collection_name} will be created.")

collection = db[collection_name]

def save_image_embedding(image_path):
    image_doc = {
        "image_path": str(image_path),
        "clip_embedding": get_image_embedding(image_path),
        "embedding_model": "clip-vit-base-patch32",
        "created_at": datetime.datetime.utcnow()
    }
    result = collection.insert_one(image_doc)
    return result.inserted_id