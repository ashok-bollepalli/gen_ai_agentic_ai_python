from fastmcp import Client

MCP_SERVER_URL = "http://localhost:8081/mcp"

#--------------------------------------------------------#

## generic function to call any tool available in mcp server
async def call_mcp_tool(tool_name, arguments):

    async with Client(MCP_SERVER_URL) as client:

        result = await client.call_tool(
            tool_name,
            arguments
        )

        if result.is_error:
            raise Exception("MCP server returned an error")

        print("MCP RESULT ::", result)

        if result.data is not None:
            return result.data

        return result.content
#--------------------------------------------------------#
async def get_weather(city: str):
    return await call_mcp_tool(
        "get_weather",
        {"city": city}
    )
#--------------------------------------------------------#

async def send_message(message: str):
    return await call_mcp_tool(
        "send_message",
        {"message": message}
    )

#--------------------------------------------------------#

async def read_slack_messages(limit: int = 10):
    return await call_mcp_tool(
        "read_messages",
        {"limit": limit}
    )
#--------------------------------------------------------#
