import streamlit as st
import asyncio
from mcp_client import get_weather, send_message, read_slack_messages

st.set_page_config(
    page_title="MCP Client",
    page_icon="🤖"
)

st.title("🤖 MCP Client")
st.caption("Weather and Slack tools using MCP")


weather, send, read = st.tabs(
    ["🌤️ Weather", "💬 Send Slack", "📖 Read Slack"]
)


# Weather
with weather:

    city = st.text_input("Enter City")

    if st.button("Get Weather"):

        result = asyncio.run(
            get_weather(city)
        )

        st.write(result)


# Send Slack
with send:

    message = st.text_area("Enter Message")

    if st.button("Send Message"):

        result = asyncio.run(
            send_message(message)
        )

        st.write(result)


# Read Slack
with read:

    limit = st.number_input(
        "Number of Messages",
        min_value=1,
        max_value=100,
        value=10
    )

    if st.button("Read Messages"):

        result = asyncio.run(
            read_slack_messages(int(limit))
        )

        print("Result :: ", result)
        st.write(result)