from state.chat_state import ChatState

def general_node(state: ChatState) -> dict:
    print("Executing general node")

    # write logic to submit ticket to customer support team.

    return {
        "context": (
            "No private database, course knowledge base, "
            "or external API information is required.",
            "Submitting Ticket to Customer Support Team."
            "We will get back to you in 24 hours."
        )
    }
