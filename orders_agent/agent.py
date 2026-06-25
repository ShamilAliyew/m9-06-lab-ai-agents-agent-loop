"""
Lab: Your First Agent — ADK Web UI Version
Model: llama3.1 (via Ollama + LiteLLM)
Tools: lookup_order, calculate
"""

import json
from pathlib import Path
from datetime import date

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


# ─────────────────────────────────────────
# Tool 1: Sifarişi axtar
# ─────────────────────────────────────────
def lookup_order(order_id: str) -> dict:
    """
    Looks up an order from orders.json and returns its details.

    Args:
        order_id: The order ID to look up (e.g. 'A1001')

    Returns:
        A dict with item name, price, purchase date, warranty months,
        warranty expiry date, and whether it is still under warranty.
        Returns an error message if the order is not found.
    """
    # orders.json is one level up (project root)
    orders_path = Path(__file__).parent.parent / "orders.json"
    with open(orders_path, "r") as f:
        orders = json.load(f)

    if order_id in orders:
        order = orders[order_id]
        purchased = date.fromisoformat(order["purchased"])
        warranty_months = order["warranty_months"]
        warranty_end_year = purchased.year + (purchased.month + warranty_months - 1) // 12
        warranty_end_month = (purchased.month + warranty_months - 1) % 12 + 1
        warranty_end = date(warranty_end_year, warranty_end_month, purchased.day)
        today = date.today()

        return {
            "order_id": order_id,
            "item": order["item"],
            "price": order["price"],
            "purchased": order["purchased"],
            "warranty_months": warranty_months,
            "warranty_expires": str(warranty_end),
            "under_warranty": today <= warranty_end,
        }
    else:
        return {"error": f"Order '{order_id}' not found in the system."}


# ─────────────────────────────────────────
# Tool 2: Hesablama
# ─────────────────────────────────────────
def calculate(expression: str) -> dict:
    """
    Evaluates a simple arithmetic expression and returns the result.

    Args:
        expression: A math expression string (e.g. '1200 * 2')

    Returns:
        A dict with the expression and its numeric result,
        or an error message if evaluation fails.
    """
    try:
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return {"error": "Only basic arithmetic is allowed (+, -, *, /, parentheses)."}
        result = eval(expression)
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": f"Could not evaluate '{expression}': {str(e)}"}


# ─────────────────────────────────────────
# ADK Agent  (ADK web UI requires `root_agent`)
# ─────────────────────────────────────────
INSTRUCTIONS = """
You are a helpful orders assistant. Your job is to help customers with questions
about their orders using the tools available to you.

How to use your tools:
- Use `lookup_order(order_id)` whenever you need information about an order
  (price, item name, purchase date, warranty status). Always call this tool
  before answering any order-related question.
- Use `calculate(expression)` whenever you need to do arithmetic
  (e.g. multiplying a price by a quantity).

Important rules:
- If an order is not found, clearly and honestly tell the customer that the
  order ID does not exist in the system. Do NOT invent or guess order details.
- Always show your reasoning: explain what you looked up and how you calculated.
- Be concise but complete in your final answer.
"""

root_agent = Agent(
    name="orders_assistant",
    model=LiteLlm(model="ollama_chat/llama3.1"),
    description="A helpful orders assistant that looks up orders and does calculations.",
    instruction=INSTRUCTIONS,
    tools=[lookup_order, calculate],
)
