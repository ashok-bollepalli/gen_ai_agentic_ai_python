import asyncio
import streamlit as st
from fastmcp import Client

employee_client = Client("http://localhost:8000/mcp")
weather_client = Client("http://localhost:8001/mcp")


async def get_employee(emp_id):
    async with employee_client:
        return await employee_client.call_tool(
            "get_employee",
            {"emp_id": emp_id}
        )


async def get_weather(city):
    async with weather_client:
        return await weather_client.call_tool(
            "get_weather",
            {"city": city}
        )


st.set_page_config(
    page_title="Multi MCP Client",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Assistant using Multiple MCP Servers")

st.write("This client communicates with two MCP servers.")

col1, col2 = st.columns(2)

with col1:
    st.success("Employee MCP Server")

with col2:
    st.success("Weather MCP Server")

st.divider()

emp_id = st.number_input(
    "Employee ID",
    min_value=101,
    max_value=999,
    value=101
)

if st.button("Get Employee Details", use_container_width=True):

    employee_result = asyncio.run(get_employee(emp_id))

    if employee_result.is_error:
        st.error("Employee not found.")
        st.stop()

    employee = employee_result.data

    st.subheader("👨 Employee Details")

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Name", employee["name"])
        st.metric("Department", employee["department"])

    with c2:
        st.metric("Salary", f'₹{employee["salary"]:,}')
        st.metric("Location", employee["location"])

    weather_result = asyncio.run(
        get_weather(employee["location"])
    )

    if weather_result.is_error:
        st.error("Weather not available.")
        st.stop()

    weather = weather_result.data

    st.divider()

    st.subheader("🌤 Weather Details")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Temperature",
            weather["temperature"]
        )

    with c2:
        st.metric(
            "Condition",
            weather["condition"]
        )