import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

import db_service


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


# ==========================================
# TOOLS
# ==========================================

@tool
def get_order_status(order_id: str):
    """Get the current status and details of an ecommerce order."""
    return db_service.get_order_status(order_id)


@tool
def cancel_order(order_id: str):
    """Cancel an ecommerce order using the order ID."""
    return db_service.cancel_order(order_id)


# ==========================================
# TOOL REGISTRY
# ==========================================

TOOLS = {
    get_order_status.name: get_order_status,
    cancel_order.name: cancel_order
}


# ==========================================
# CREATE LLM
# ==========================================

llm = ChatOpenAI(
    model="gpt-5.6",
    api_key=api_key,
    use_responses_api=True
)

llm_with_tools = llm.bind_tools(
    list(TOOLS.values())
)


# ==========================================
# GET RESPONSE TEXT
# ==========================================

def get_text(response):

    if isinstance(response.content, str):
        return response.content

    for item in response.content:
        if isinstance(item, dict) and item.get("type") == "text":
            return item.get("text", "")

    return str(response.content)


# ==========================================
# CUSTOMER SUPPORT
# ==========================================

def customer_support(question):

    # --------------------------------------
    # STEP 1: Ask LLM
    # --------------------------------------

    response = llm_with_tools.invoke(question)

    print("AI Response:", response)

    # --------------------------------------
    # STEP 2: No Tool Required
    # --------------------------------------

    if not response.tool_calls:
        return get_text(response)

    # --------------------------------------
    # STEP 3: Execute Tool
    # --------------------------------------

    tool_results = []

    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        selected_tool = TOOLS.get(tool_name)

        if selected_tool is None:
            return f"Unknown tool: {tool_name}"

        result = selected_tool.invoke(tool_args)

        tool_results.append(
            f"Tool: {tool_name}\n"
            f"Result: {result}"
        )

    # --------------------------------------
    # STEP 4: Give Tool Result Back to LLM
    # --------------------------------------

    final_prompt = f"""
Customer Question:
{question}

Tool Results:
{chr(10).join(tool_results)}

Answer the customer clearly and simply.

Rules:
- Do not show JSON.
- Do not show tool calls.
- Do not mention internal implementation.
"""

    final_response = llm.invoke(final_prompt)

    return get_text(final_response)
