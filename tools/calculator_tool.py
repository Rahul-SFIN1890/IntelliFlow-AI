from langchain.tools import tool


@tool
def calculator_tool(expression: str):
    """Useful for calculations"""

    return eval(expression)