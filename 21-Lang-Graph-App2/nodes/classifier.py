from state.chat_state import ChatState

def classify_question(state: ChatState) -> dict:

    question = state["question"].lower()

    payment_words = [
        "fee",
        "payment",
        "paid",
        "pending amount",
        "due",
    ]

    course_words = [
        "course",
        "topics",
        "syllabus",
        "learn",
        "duration",
        "project",
    ]

    api_words = [
        "live",
        "api",
        "external",
        "service",
        "status",
    ]

    if any(word in question for word in payment_words):
        category = "payment"
    elif any(word in question for word in course_words):
        category = "course"
    elif any(word in question for word in api_words):
        category = "live"
    else:
        category = "general"

    print(f"Classifier Selected : {category}")

    return {
        "category": category
    }
