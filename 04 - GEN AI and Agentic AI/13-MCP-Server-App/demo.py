import os

from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()

slack_token = os.getenv('SLACK_BOT_TOKEN')
slack_channel = os.getenv("SLACK_CHANNEL_ID")

slack = WebClient(token=slack_token)

slack.chat_postMessage(
    channel=slack_channel,
    text = "Hello, Good Morning...!!"
)

response = slack.conversations_history(
    channel=slack_channel,
    limit=10
)

print(response)