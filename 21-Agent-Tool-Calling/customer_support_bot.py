import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage
)

import db_service


# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


# ==========================================
# INITIALIZE DATABASE
# ==========================================

db_service.create_database()


# ==========================================
# TOOLS
# ==========================================

@tool
def get_order_status(order_id: str):
    """Get the status of an order."""

    return db_service.get_order_status(order_id)


@tool
def cancel_order(order_id: str):
    """Cancel an order."""

    return db_service.cancel_order(order_id)


# ==========================================
# TOOLS LIST
# ==========================================

tools = [
    get_order_status,
    cancel_order
]


# ==========================================
# TOOL MAP
# ==========================================

tool_map = {
    tool.name: tool
    for tool in tools
}


# ==========================================
# CREATE LLM
# ==========================================

llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-5.6",
    use_responses_api=True
)


# ==========================================
# BIND TOOLS
# ==========================================

llm_with_tools = llm.bind_tools(tools)


# ==========================================
# SYSTEM MESSAGE
# ==========================================

SYSTEM_MESSAGE = """
You are an AI Customer Support Agent.

You can perform only two tasks:

1. Get order status
2. Cancel order

Rules:

- Use the tools when you need order information.
- Never invent order information.
- If order ID is missing, ask the customer for it.
- Give simple answers.
- Never show JSON.
- Never show tool calls.
"""


# ==========================================
# GET TEXT FROM LLM RESPONSE
# ==========================================

def get_text(response):

    if isinstance(response.content, str):

        return response.content

    for item in response.content:

        if isinstance(item, dict):

            if item.get("type") == "text":

                return item.get("text", "")

    return str(response.content)


# ==========================================
# CUSTOMER SUPPORT
# ==========================================

def customer_support(question):

    # Create messages

    messages = [
        SystemMessage(content=SYSTEM_MESSAGE),
        HumanMessage(content=question)
    ]


    # Ask LLM

    response = llm_with_tools.invoke(messages)


    # No tool required

    if not response.tool_calls:

        return get_text(response)


    # Add AI response

    messages.append(response)


    # Execute tools

    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]

        tool_args = tool_call["args"]

        selected_tool = tool_map[tool_name]

        result = selected_tool.invoke(tool_args)


        # Add tool result

        messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            )
        )


    # Ask LLM for final answer

    final_response = llm_with_tools.invoke(messages)


    # Return only text

    return get_text(final_response)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    print()
    print("===================================")
    print("🤖 AI CUSTOMER SUPPORT AGENT")
    print("===================================")

    print()
    print("You can ask:")
    print("1. Where is my order ORD1001?")
    print("2. Cancel my order ORD1003")
    print()
    print("Type 'exit' to stop.")
    print()


    while True:

        question = input("Customer: ")


        if question.lower() == "exit":

            print("Agent: Goodbye!")

            break


        try:

            answer = customer_support(question)

            print()
            print("Agent:", answer)
            print()

        except Exception as e:

            print("Error:", e)
