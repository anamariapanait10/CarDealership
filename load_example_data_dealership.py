import json
import os
from pathlib import Path
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

BASE_DIR = Path(__file__).resolve().parent

DOMAINS = {
    # "restaurants": {
    #     "services": BASE_DIR / "restaurants.services.json",
    #     "intents": BASE_DIR / "restaurants.intents.json",
    #     "slot_ranking": BASE_DIR / "restaurants.slot_ranking.json",
    # },
    "car_dealership": {
        "services": BASE_DIR / "car_dealership.services.json",
        "intents": BASE_DIR / "car_dealership.intents.json",
        "slot_ranking": BASE_DIR / "car_dealership.slot_ranking.json",
    },
}

def load_json_file(filepath: Path):
    with filepath.open("r", encoding="utf-8") as f:
        return json.load(f)

def strip_mongo_export_ids(obj):
    """
    Removes Mongo export-style _id fields and any {"$oid": "..."} wrappers.
    This makes exported JSON insertable via PyMongo.
    """
    if isinstance(obj, list):
        return [strip_mongo_export_ids(x) for x in obj]
    if isinstance(obj, dict):
        # Remove _id completely (let MongoDB regenerate)
        obj = {k: v for k, v in obj.items() if k != "_id"}

        # Recurse
        cleaned = {}
        for k, v in obj.items():
            # If some field itself is {"$oid": "..."} (rare outside _id), unwrap to string
            if isinstance(v, dict) and set(v.keys()) == {"$oid"}:
                cleaned[k] = v["$oid"]
            else:
                cleaned[k] = strip_mongo_export_ids(v)
        return cleaned
    return obj

def load_collection(domain: str, collection_name: str, filepath: Path):
    db = client[domain]
    collection = db[collection_name]
    collection.delete_many({})  # wipe previous

    data = load_json_file(filepath)
    data = strip_mongo_export_ids(data)

    if isinstance(data, list):
        if data:
            collection.insert_many(data)
    else:
        collection.insert_one(data)

    print(f"[OK] Loaded {collection_name} for domain '{domain}' from {filepath.name}")

def main():
    for domain, collections in DOMAINS.items():
        for collection_name, filepath in collections.items():
            load_collection(domain, collection_name, filepath)

if __name__ == "__main__":
    main()
