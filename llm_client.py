import requests

from sales_tools import (
    calculate_total_sales,
    get_top_product,
    get_product_revenue
)

API_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_total_sales",
            "description": "Calculate total sales revenue."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_product",
            "description": "Find the product with the highest revenue."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_revenue",
            "description": "Find the total revenue for a named product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Name of the product"
                    }
                },
                "required": ["product_name"]
            }
        }
    }
]


AVAILABLE_TOOLS = {
    "calculate_total_sales": calculate_total_sales,
    "get_top_product": get_top_product,
    "get_product_revenue": get_product_revenue
}


def chat(messages):

    response = requests.post(
        API_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "tools": TOOLS,
            "stream": False
        },
        timeout=(10, 120)
    )

    response.raise_for_status()

    return response.json()["message"]

def execute_tool(tool_call):

    function_name = tool_call["function"]["name"]
    arguments = tool_call["function"].get("arguments", {})

    if function_name not in AVAILABLE_TOOLS:
        raise ValueError("Tool is not allowed.")

    if not isinstance(arguments, dict):
        raise ValueError("Invalid tool arguments.")

    if function_name == "get_product_revenue":
        product_name = arguments.get("product_name")

        if not isinstance(product_name, str) or not product_name.strip():
            raise ValueError("A valid product name is required.")

        return AVAILABLE_TOOLS[function_name](product_name.strip())

    if arguments:
        raise ValueError("This tool does not accept arguments.")

    return AVAILABLE_TOOLS[function_name]()