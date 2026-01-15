"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.6
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez
"""
from bson import ObjectId
from spec2chat.db.mongo import MongoDB

db = MongoDB()

def get_service_questions(service_id: str, intent_name: str, domain: str) -> dict:
    services = db.get_collection(domain, 'services')
    document = services.find_one({"_id": ObjectId(service_id)})

    if not document:
        raise ValueError(f"Service not found with id {service_id}")

    paths = document.get("paths", {})
    intent_info = None

    for path, methods in paths.items():
        path_intent = path.lstrip('/')
        if path_intent == intent_name:
            for method, details in methods.items():
                if method == "get" and "parameters" in details:
                    slots = extract_questions_from_parameters(details.get("parameters", []))
                    intent_info = {
                        "name": path_intent,
                        "description": details.get("description", ''),
                        "questions": slots
                    }
                elif method == "post" and "requestBody" in details:
                    content = details["requestBody"].get("content", {})
                    for _, media in content.items():
                        schema = media.get("schema", {}) or {}

                        # 1) $ref schema
                        schema_ref = schema.get("$ref")
                        if schema_ref:
                            schema_name = schema_ref.split("/")[-1]
                            schema = (
                                document.get("components", {})
                                .get("schemas", {})
                                .get(schema_name, {})
                            )

                        if "allOf" in schema and isinstance(schema["allOf"], list):
                            merged_props = {}
                            for part in schema["allOf"]:
                                part_ref = part.get("$ref")
                                if part_ref:
                                    part_name = part_ref.split("/")[-1]
                                    part_schema = (
                                        document.get("components", {})
                                        .get("schemas", {})
                                        .get(part_name, {})
                                    )
                                else:
                                    part_schema = part
                                merged_props.update(part_schema.get("properties", {}) or {})
                            properties = merged_props
                        else:
                            properties = schema.get("properties", {}) or {}

                        slots = extract_questions_from_schema(properties)
                        intent_info = {
                            "name": path_intent,
                            "description": details.get("description", ''),
                            "questions": {q["name"]: q["question"] for q in slots}
                        }
            break
    else:
        raise ValueError("Intent not found in service specification")

    return intent_info

def extract_questions_from_parameters(parameters: list) -> dict:
    questions = {}
    for param in parameters:
        if 'schema' in param and 'x-value' in param['schema']:
            continue
        name = param.get("name")
        question = param.get("x-custom-question", "No question defined")
        if name:
            questions[name] = question
    return questions

def extract_questions_from_schema(properties: dict) -> list:
    return [
        {"name": name, "question": prop.get("x-custom-question", "No question defined")}
        for name, prop in properties.items()
    ]