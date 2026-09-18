import httpx

from config.settings import EXTERNAL_API_URL
from state.chat_state import ChatState


def api_node(state: ChatState) -> dict:
    print("Executing API Node")

    try:
        response = httpx.get(
            EXTERNAL_API_URL
        )

        response.raise_for_status()

        data = response.json()

        context = f"""
        External service record ID: {data.get('id')}
        Service message: {data.get('title')}
        Completed: {data.get('completed')}
        """.strip()

    except httpx.HTTPError as error:
        context = (
            "The external API is currently unavailable. "
            f"Error type: {type(error).__name__}"
        )

    return {"context": context}
