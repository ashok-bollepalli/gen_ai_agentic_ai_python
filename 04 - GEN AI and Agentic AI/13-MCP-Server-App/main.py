import json
from fastmcp import FastMCP
from slack_sdk import WebClient
from weather_service import weather_data
import os
from dotenv import load_dotenv

load_dotenv()

slack_token = os.getenv('SLACK_BOT_TOKEN')
slack_channel = os.getenv("SLACK_CHANNEL_ID")

# Create MCP Server
mcp = FastMCP("MCP Server")

# create slack client obj
slack = WebClient(token=slack_token)

@mcp.tool
def get_weather(city:str):
    """ Return weather information of given city"""
    return weather_data.get(city)

@mcp.tool
def send_message(message:str):
    """ Send message to slack channel """
    slack.chat_postMessage(
        channel=slack_channel,
        text=message
    )


@mcp.tool
def read_messages(limit: int = 10):
    """Read recent Slack messages."""

    response = slack.conversations_history(
        channel=slack_channel,
        limit=limit
    )

    messages = [
        msg.get("text", "")
        for msg in response.get("messages", [])
    ]

    print("Response ::", messages)

    return json.dumps(messages)

# Run mcp server
if __name__ == "__main__":
    mcp.run(
        transport = "http",
        host = "localhost",
        port = 8081
    )