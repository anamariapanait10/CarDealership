"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.6
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez
"""

import json
from pymongo import MongoClient
import os

# Parámetros de conexión
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

# Dominios disponibles
DOMAINS = {
    "restaurants": {
        "services": "data/restaurants.services.json",
        "intents": "data/restaurants.intents.json",
        "slot_ranking": "data/restaurant.slot_ranking.json"
    }
}

def load_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def load_collection(domain, collection_name, filepath):
    db = client[domain]
    collection = db[collection_name]
    collection.delete_many({})  # Limpiar datos anteriores
    data = load_json_file(filepath)
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)
    print(f"[OK] Cargado {collection_name} en dominio '{domain}'.")

def main():
    for domain, collections in DOMAINS.items():
        for collection_name, filepath in collections.items():
            load_collection(domain, collection_name, filepath)

if __name__ == "__main__":
    main()