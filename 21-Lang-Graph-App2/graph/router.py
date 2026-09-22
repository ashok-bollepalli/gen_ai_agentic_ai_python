from state.chat_state import ChatState

def route_question(state: ChatState):

    category = state["category"]

    if category == "payment":
        return "database"

    elif category == "course":
        return "rag"

    elif category == "live":
        return "api"

    else:
        return "general"