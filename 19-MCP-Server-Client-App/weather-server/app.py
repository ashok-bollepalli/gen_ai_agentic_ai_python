from fastmcp import FastMCP
from weather_service import weather_data

mcp = FastMCP("Weather Server")


@mcp.tool()
def get_weather(city: str):
    """
    Returns weather.
    """

    return weather_data.get(city, "No Data")



if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8001
    )
