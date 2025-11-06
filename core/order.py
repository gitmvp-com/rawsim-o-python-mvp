"""Order management for warehouse fulfillment."""

from typing import List, Dict, Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .instance import Instance
    from .item import ItemDescription


class Order:
    """Customer order to be fulfilled."""

    def __init__(self, order_id: int):
        self.id: int = order_id
        self.items: Dict[int, int] = {}  # item_description_id -> quantity
        self.creation_time: float = 0.0
        self.completion_time: Optional[float] = None
        self.priority: int = 0
        self.is_completed: bool = False

    def add_item(self, item_description_id: int, quantity: int):
        """Add items to the order."""
        if item_description_id in self.items:
            self.items[item_description_id] += quantity
        else:
            self.items[item_description_id] = quantity

    def get_total_items(self) -> int:
        """Get total number of items in order."""
        return sum(self.items.values())

    def complete(self, current_time: float):
        """Mark order as completed."""
        self.is_completed = True
        self.completion_time = current_time

    def get_processing_time(self) -> Optional[float]:
        """Get time taken to process the order."""
        if self.completion_time is not None:
            return self.completion_time - self.creation_time
        return None

    def __repr__(self):
        status = "completed" if self.is_completed else "pending"
        return f"Order(id={self.id}, items={self.get_total_items()}, status={status})"


class OrderList:
    """List of orders to be processed."""

    def __init__(self):
        self.orders: List[Order] = []
        self.next_order_id: int = 0

    def create_order(self, items: Dict[int, int], priority: int = 0,
                    creation_time: float = 0.0) -> Order:
        """Create a new order."""
        order = Order(self.next_order_id)
        order.priority = priority
        order.creation_time = creation_time
        
        for item_id, quantity in items.items():
            order.add_item(item_id, quantity)
        
        self.orders.append(order)
        self.next_order_id += 1
        return order

    def get_pending_orders(self) -> List[Order]:
        """Get all pending (not completed) orders."""
        return [order for order in self.orders if not order.is_completed]

    def get_completed_orders(self) -> List[Order]:
        """Get all completed orders."""
        return [order for order in self.orders if order.is_completed]

    def __repr__(self):
        pending = len(self.get_pending_orders())
        completed = len(self.get_completed_orders())
        return f"OrderList(pending={pending}, completed={completed})"
