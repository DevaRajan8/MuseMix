from pymongo import MongoClient
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["musemix"]
collection = db["musemix"]

def find_similar_images(query_embedding, top_k=5):
    """
    Find similar images using cosine similarity
    """
    # Get all image embeddings from MongoDB
    cursor = collection.find({}, {"image_path": 1, "clip_embedding": 1, "_id": 1})
    
    similar_images = []
    query_embedding = np.array(query_embedding).reshape(1, -1)
    
    for doc in cursor:
        stored_embedding = np.array(doc["clip_embedding"]).reshape(1, -1)
        similarity = cosine_similarity(query_embedding, stored_embedding)[0][0]
        
        similar_images.append({
            "image_path": doc["image_path"],
            "similarity": float(similarity),
            "doc_id": str(doc["_id"])
        })
    
    # Sort by similarity and return top_k
    similar_images.sort(key=lambda x: x["similarity"], reverse=True)
    return similar_images[:top_k]

def get_image_context(similar_images):
    """
    Create context string from similar images for RAG
    """
    context = "Similar images found:\n"
    for i, img in enumerate(similar_images, 1):
        context += f"{i}. Image: {img['image_path']} (similarity: {img['similarity']:.3f})\n"
    return context