from fastmcp import FastMCP
from employee_db import employees

mcp = FastMCP("Employee Server")


@mcp.tool()
def get_employee(emp_id: int):
    """
    Returns employee details.
    """

    return employees.get(emp_id, "Employee Not Found")


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000
    )
