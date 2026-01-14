from flask import Flask, request, jsonify, render_template
from spec2chat import run_chatbot
from flask_cors import CORS
import os
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import requests
from pymongo.errors import PyMongoError

app = Flask(__name__)
CORS(app)
DB_NAME = "application_user_data"
EXTERNAL_API = "http://127.0.0.1:8000"
@app.route('/')
def home():
    return render_template('index.html')

def clean_quotes(text):
    return text.strip('"') if text.startswith('"') and text.endswith('"') else text

@app.route('/database', methods=['GET'])
def database_page():
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)

    db = client[DB_NAME]

    # Optional query params
    user_id = request.args.get("user_id")              # /database?user_id=123
    only_collection = request.args.get("collection")   # /database?collection=application_user_data
    limit = int(request.args.get("limit", 100))

    def to_jsonable(value):
        if isinstance(value, ObjectId):
            return str(value)
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, dict):
            return {k: to_jsonable(v) for k, v in value.items()}
        if isinstance(value, list):
            return [to_jsonable(v) for v in value]
        return value

    # Discover collections (skip system collections)
    collections = [
        c for c in db.list_collection_names()
        if not c.startswith("system.")
    ]

    # If user asked for just one collection
    if only_collection:
        collections = [c for c in collections if c == only_collection]

    tables = []  # each item: {name, docs, columns}

    for coll_name in collections:
        coll = db[coll_name]

        query = {}
        # Only apply user_id filter if requested.
        # (If a collection doesn't have user_id field, it'll just return 0 docs; that's fine.)
        if user_id:
            query["user_id"] = user_id

        # Sort: try updated_at desc if it exists; otherwise _id desc
        # (Mongo will still sort even if field missing; missing sorts last)
        cursor = coll.find(query).sort([("updated_at", -1), ("_id", -1)]).limit(limit)

        docs = [to_jsonable(d) for d in cursor]

        # Build columns from keys found across docs (keeps table consistent)
        columns = []
        seen = set()
        for d in docs:
            for k in d.keys():
                if k not in seen:
                    seen.add(k)
                    columns.append(k)

        # Always show _id first if present
        if "_id" in columns:
            columns.remove("_id")
            columns = ["_id"] + columns

        tables.append({
            "name": coll_name,
            "docs": docs,
            "columns": columns
        })

    client.close()

    return render_template(
        "database.html",
        tables=tables,
        user_id=user_id,
        collection=only_collection,
        limit=limit,
        all_collections=collections
    )

def handle_request(intent, body):
    r = requests.post(
        EXTERNAL_API + "/api/" + intent + '/',
        json=body
    )

    return r
    # import os
    # from datetime import datetime, timezone
    # from pymongo import MongoClient
    # from pymongo.errors import PyMongoError
    #
    # mongo_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
    # db_name = os.environ.get("MONGO_DB_NAME", DB_NAME)
    #
    # client = MongoClient(mongo_uri)
    # db = client[db_name]
    # collection = db[intent]
    #
    # user_id = (
    #         body.get("user_id")
    #         or body.get("email")
    #         or body.get("service_id")
    #         or body.get("phone")
    # )
    #
    # if not user_id:
    #     user_id = f"anonymous:{datetime.now(timezone.utc).isoformat()}"
    #
    # now = datetime.now(timezone.utc)
    #
    # update_doc = {
    #     "$set": {
    #         "user_id": user_id,
    #         f"intents.{intent}.data": body,
    #         f"intents.{intent}.updated_at": now,
    #         "updated_at": now,
    #     },
    #     "$setOnInsert": {
    #         "created_at": now,
    #     }
    # }
    #
    # try:
    #     result = collection.update_one(
    #         {"user_id": user_id},
    #         update_doc,
    #         upsert=True
    #     )
    #
    # except PyMongoError as e:
    #     print(f"[MongoDB] Failed to store data for user_id={user_id}, intent={intent}: {e}")
    # finally:
    #     client.close()


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()

    # Extraer todos los datos del cliente
    user_input = data.get("userinput", "")
    user_answers = data.get("useranswers", [])
    tasks = data.get("tasks", {})
    domain = data.get("domain", "")
    intent = data.get("intent", "")
    filledslots = data.get("filledslots", {})
    reqslots = data.get("reqslots", [])
    services = data.get("services", [])
    service_id = data.get("service_id", "")

    # Llamar a spec2chat
    response = run_chatbot(
        user_input=user_input,
        user_answers=user_answers,
        tasks=tasks,
        domain=domain,
        intent=intent,
        filledslots=filledslots,
        reqslots=reqslots,
        services=services,
        service_id=service_id
    )

    # Limpiar comillas innecesarias
    if "chatbot_answer" in response:
        response["chatbot_answer"] = clean_quotes(response["chatbot_answer"])

    if "questions" in response:
        response["questions"] = {
            slot: clean_quotes(question)
            for slot, question in response["questions"].items()
        }

    # Añadir el input original al response (opcional, si lo necesitas en frontend)
    response["userinput"] = user_input

    if "end_of_conversation" in response and response["end_of_conversation"]:
        print(f"S-a terminat conversatia. Intentul a fost {intent} iar datele au fost {response['filledslots']}")
        result = handle_request(intent, response['filledslots'])
        if result.ok:
            response["external_api_response"] = result.text

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
