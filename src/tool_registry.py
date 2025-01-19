from langchain_core.tools import tool
from typing import Callable, Dict

class ToolRegistry:
    # Tool functions
    @tool
    def multiply(x: int, y: int) -> int:
        """Multiply 'x' to the 'y'."""
        return x * y
    @tool
    def subtract(x: int, y: int) -> int:
        """Subtract 'x' to the 'y'."""
        return x - y

    def get_tools(self) -> dict[str, Callable]:
        """
        Returns a dictionary of tool names associated with their respective functions.
        """
        tools = {
            "multiply": self.multiply,
            "subtract": self.subtract,
        }
        return tools