import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

import db_service

# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# ==========================================
# TOOLS
# ==========================================

@tool
def get_order_status(order_id: str):
    """Get the status of the order"""
    return db_service.get_order_status(order_id)


@tool
def cancel_order(order_id: str):
    """Cancel an order"""
    return db_service.cancel_order(order_id)


# ==========================================
# CREATE LLM Client
# ==========================================

llm = ChatOpenAI(
    model="gpt-5.6",
    api_key=api_key,
    use_responses_api=True
)

# ==========================================
# GIVE TOOLS TO AI
# ==========================================

llm = llm.bind_tools([
    get_order_status,
    cancel_order
])

# ==========================================
# GET TEXT FROM RESPONSE
# ==========================================

def get_text(response):

    # normal string response
    if isinstance(response.content, str):
        return response.content

    # Structured response

    for item in response.content:
        if isinstance(item, dict):
            if item.get("type") == "text":
                return item.get("text", "")

    return str(response.content)


# ==========================================
# CUSTOMER SUPPORT Agent
# ==========================================

def customer_support(question):
    # ask AI
    response = llm.invoke(question)

    print("Response:", response)

    # --------------------------------------
    # No tool required
    # --------------------------------------
    if not response.tool_calls:
        return get_text(response)

    # --------------------------------------
    # AI selected a tool
    # --------------------------------------

    tool_call = response.tool_calls[0]
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    # --------------------------------------
    # Execute tool
    # --------------------------------------
    if tool_name == "get_order_status":
        result = get_order_status.invoke(tool_args)
    elif tool_name == "cancel_order":
        result = cancel_order.invoke(tool_args)
    else:
        return "Unknown Tool"

    # --------------------------------------
    # Give result back to AI
    # --------------------------------------

    final_response = llm.invoke(
        f"""
        Customer question:
        {question}

        Tool result:
        {result}

        Give a simple answer to the customer.

        Do not show JSON.
        Do not show tool calls.
        Do not mention internal implementation.
        """
    )

    return get_text(final_response)


