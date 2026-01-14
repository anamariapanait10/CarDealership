"""
spec2chat - Example for hotel domain

This script demonstrates how to use the `run_chatbot` function from the `spec2chat` library
to simulate a hotel reservation scenario.
"""

from dotenv import load_dotenv

load_dotenv()

from spec2chat import run_chatbot


def main():
    user_input = "I want a 3-star hotel with parking and breakfast included"
    user_answers = []
    filledslots = {}

    print("\n[Step 0] Initial user message:")
    print(f"User: {user_input}")

    response = run_chatbot(user_input=user_input)
    print("\n[Step 1] Chatbot response:")
    print(response)

    tasks = response.get("tasks", {})
    domain = response.get("dom", "")
    intent = response.get("intent", "")
    reqslots = response.get("reqslots", [])
    services = response.get("services", [])

    step = 2
    while not response.get("end_of_conversation", False):
        print(f"\n[Step {step}] Sending answers to chatbot questions...")

        simulated_answers = {
            "name": "Alice",
            "phone": "987654321",
            "checkin_date": "2024-08-15",
            "checkout_date": "2024-08-18",
            "nights": "3",
            "people": "2",
            "stars": "3",
            "hotel_type": "urban",
            "parking": "yes",
            "breakfast_included": "yes",
            "location": "city center",
            "room_type": "double",
            "pricerange": "mid-range",
            "pets": "no",
            "pool": "yes"
        }

        for slot, question in response.get("questions", {}).items():
            answer = simulated_answers.get(slot, "test")
            user_answers.append({"chatbot": question, "user": answer})
            filledslots[slot] = answer

        response = run_chatbot(
            user_input=user_input,
            user_answers=user_answers,
            tasks=response.get("tasks", tasks),
            domain=response.get("dom", domain),
            intent=response.get("intent", intent),
            filledslots=filledslots,
            services=response.get("services", services),
            reqslots=response.get("reqslots", reqslots),
            service_id=response.get("service_id")
        )

        print(f"[Step {step}] Chatbot response:")
        print(response)

        if response.get("final") and not response.get("questions"):
            print("\n[DEBUG] Finished: all slots are filled and no more questions are pending.")
            break

        step += 1

    if response.get("end_of_conversation"):
        print("\nConversation successfully completed.")
    else:
        print("\nConversation incomplete or could not continue.")


if __name__ == "__main__":
    main()