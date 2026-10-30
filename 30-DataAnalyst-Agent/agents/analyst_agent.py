from langchain_openai import ChatOpenAI

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage
)

from config.settings import Settings
from agents.prompts import get_system_prompt


class AnalystAgent:

    def __init__(self, tools):

        self.tools = tools

        self.tool_map = {
            item.name: item
            for item in tools
        }

        self.llm = ChatOpenAI(
            model=Settings.OPENAI_MODEL,
            temperature=Settings.TEMPERATURE
        ).bind_tools(tools)

    def analyze(self, question, columns):

        messages = [
            SystemMessage(
                content=get_system_prompt(columns)
            ),
            HumanMessage(content=question)
        ]

        response = self.llm.invoke(messages)

        messages.append(response)

        tool_results = []

        for call in response.tool_calls:

            tool = self.tool_map[call["name"]]

            result = tool.invoke(call["args"])

            tool_results.append({
                "tool": call["name"],
                "result": result
            })

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=call["id"]
                )
            )

        if tool_results:

            final_llm = ChatOpenAI(
                model=Settings.OPENAI_MODEL,
                temperature=Settings.TEMPERATURE
            )

            final_response = final_llm.invoke(messages)

            answer = final_response.content

        else:
            answer = response.content

        return {
            "answer": answer,
            "tool_results": tool_results
        }