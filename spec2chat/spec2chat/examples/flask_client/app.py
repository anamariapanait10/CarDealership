from flask import Flask, request, jsonify, render_template
from spec2chat import run_chatbot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

def clean_quotes(text):
    return text.strip('"') if text.startswith('"') and text.endswith('"') else text

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

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)