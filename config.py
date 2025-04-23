import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load variabel dari file .env
load_dotenv()

def get_db():
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise ValueError("❌ MONGO_URI tidak ditemukan. Cek file .env kamu.")
    
    client = MongoClient(uri)
    return client["indonesiadata"]  # Ganti kalau nama DB kamu beda
