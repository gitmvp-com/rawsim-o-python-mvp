"""Input and Output station implementations."""

from typing import Optional, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import Instance
    from .tier import Tier
    from .waypoint import Waypoint
    from .item import ItemBundle
    from .order import Order


class Station:
    """Base class for warehouse stations."""

    def __init__(self, instance: 'Instance'):
        self.instance = instance
        self.id: int = 0
        self.volatile_id: int = 0
        
        # Position
        self.tier: Optional['Tier'] = None
        self.x: float = 0.0
        self.y: float = 0.0
        self.radius: float = 1.0
        
        # Configuration
        self.capacity: float = 100.0
        self.activation_order_id: int = 0
        
        # Associated waypoint
        self.waypoint: Optional['Waypoint'] = None
        
        # Queues for different waypoints
        self.queues: Dict['Waypoint', List['Waypoint']] = {}
        
        # State
        self.is_active: bool = True
        self.current_pod = None


class InputStation(Station):
    """Station for receiving inventory into the warehouse."""

    def __init__(self, instance: 'Instance'):
        super().__init__(instance)
        self.item_bundle_transfer_time: float = 3.0
        
        # Incoming items queue
        self.incoming_bundles: List['ItemBundle'] = []
        self.bundles_processed: int = 0

    def add_bundle(self, bundle: 'ItemBundle'):
        """Add an item bundle to the incoming queue."""
        self.incoming_bundles.append(bundle)

    def process_bundle(self) -> Optional['ItemBundle']:
        """Process the next bundle in queue."""
        if len(self.incoming_bundles) > 0:
            bundle = self.incoming_bundles.pop(0)
            self.bundles_processed += 1
            return bundle
        return None

    def get_bundle_count(self) -> int:
        """Get number of bundles waiting to be processed."""
        return len(self.incoming_bundles)

    def __repr__(self):
        return f"InputStation(id={self.id}, bundles={len(self.incoming_bundles)})"


class OutputStation(Station):
    """Station for fulfilling orders from the warehouse."""

    def __init__(self, instance: 'Instance'):
        super().__init__(instance)
        self.item_transfer_time: float = 2.0
        self.item_pick_time: float = 1.0
        
        # Orders
        self.assigned_orders: List['Order'] = []
        self.orders_completed: int = 0
        self.items_picked: int = 0
        
        # Current operation
        self.current_order: Optional['Order'] = None

    def assign_order(self, order: 'Order'):
        """Assign an order to this station."""
        self.assigned_orders.append(order)

    def process_order(self) -> Optional['Order']:
        """Process the next order in queue."""
        if len(self.assigned_orders) > 0 and self.current_order is None:
            self.current_order = self.assigned_orders.pop(0)
            return self.current_order
        return None

    def complete_order(self):
        """Mark current order as completed."""
        if self.current_order is not None:
            self.orders_completed += 1
            self.current_order = None

    def pick_item(self):
        """Record an item being picked."""
        self.items_picked += 1

    def get_pending_orders(self) -> int:
        """Get number of pending orders."""
        count = len(self.assigned_orders)
        if self.current_order is not None:
            count += 1
        return count

    def __repr__(self):
        return f"OutputStation(id={self.id}, orders={self.get_pending_orders()}, completed={self.orders_completed})"
