import asyncio
from fastmcp import Client

employee = Client("http://localhost:8000/mcp")

weather = Client("http://localhost:8001/mcp")


async def main():

    async with employee:

        result = await employee.call_tool(
            "get_employee",
            {"emp_id":101}
        )

        print(result)


    async with weather:

        result = await weather.call_tool(
            "get_weather",
            {"city":"Hyderabad"}
        )

        print(result)


asyncio.run(main())