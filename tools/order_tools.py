import json
import re
from pathlib import Path

from livekit.agents import function_tool

from .memory import memory

ORDERS_FILE = Path(__file__).resolve().parent.parent / "data" / "orders.json"


@function_tool
async def track_order(order_id: str) -> str:
    """Return floral order customer, status, estimated delivery, tracking ID, items, and price."""
    normalized = order_id.upper().strip()
    match = re.search(r"ORD\d+", normalized)
    normalized = match.group(0) if match else normalized
    orders = json.loads(ORDERS_FILE.read_text(encoding="utf-8"))
    order = next((item for item in orders if item["order_id"] == normalized), None)
    if not order:
        return f"I couldn't find order {normalized}. Please check the order ID and try again."
    memory["current_order"] = normalized
    return (f"Order {order['order_id']} for {order['customer']} is {order['status']}. "
            f"Estimated delivery is {order['estimated_delivery']}. Tracking ID: {order['tracking_id']}. "
            f"Items: {', '.join(order['items'])}. Total: ₹{order['price']:,}.")
