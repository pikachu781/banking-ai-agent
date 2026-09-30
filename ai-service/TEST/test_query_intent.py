from app.services.query_intent_service import (
    classify_query_intent
)


questions = [
    "What am I learning recently?",
    "What am I currently learning?",
    "What technologies do I know?",
    "What are all my skills?",
    "What is my career goal?",
    "What projects am I working on?",
    "What career am I preparing for?",
    "What is Python?"
]


print("\n========== QUERY INTENT TEST ==========\n")


for question in questions:

    intent = classify_query_intent(question)

    print("Question:", question)
    print("Intent:", intent)
    print("-----------------------------------")