"""Pod (storage unit) implementation."""

from typing import Optional, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import Instance
    from .tier import Tier
    from .bot import Bot
    from .waypoint import Waypoint
    from .item import ItemBundle


class Pod:
    """Storage pod that can be moved by bots."""

    def __init__(self, instance: 'Instance'):
        self.instance = instance
        self.id: int = 0
        self.volatile_id: int = 0
        
        # Position
        self.tier: Optional['Tier'] = None
        self.x: float = 0.0
        self.y: float = 0.0
        self.radius: float = 0.5
        self.orientation: float = 0.0
        
        # Storage
        self.capacity: float = 100.0
        self.items: List['ItemBundle'] = []
        self.item_counts: Dict[int, int] = {}  # item_description_id -> count
        
        # State
        self.waypoint: Optional['Waypoint'] = None
        self.carried_by: Optional['Bot'] = None
        
        # Statistics
        self.times_picked: int = 0
        self.times_moved: int = 0

    def is_stored(self) -> bool:
        """Check if pod is at a storage waypoint."""
        return self.waypoint is not None and not self.is_carried()

    def is_carried(self) -> bool:
        """Check if pod is being carried by a bot."""
        return self.carried_by is not None

    def get_available_capacity(self) -> float:
        """Get remaining storage capacity."""
        used = sum(bundle.item_count for bundle in self.items)
        return self.capacity - used

    def add_item_bundle(self, bundle: 'ItemBundle') -> bool:
        """Add an item bundle to the pod."""
        if self.get_available_capacity() < bundle.item_count:
            return False
        
        self.items.append(bundle)
        item_id = bundle.item_description.id
        self.item_counts[item_id] = self.item_counts.get(item_id, 0) + bundle.item_count
        return True

    def remove_item_bundle(self, bundle: 'ItemBundle') -> bool:
        """Remove an item bundle from the pod."""
        if bundle not in self.items:
            return False
        
        self.items.remove(bundle)
        item_id = bundle.item_description.id
        self.item_counts[item_id] = max(0, self.item_counts.get(item_id, 0) - bundle.item_count)
        return True

    def has_item(self, item_description_id: int, count: int = 1) -> bool:
        """Check if pod has at least count of the specified item."""
        return self.item_counts.get(item_description_id, 0) >= count

    def __repr__(self):
        status = "carried" if self.is_carried() else "stored" if self.is_stored() else "free"
        return f"Pod(id={self.id}, pos=({self.x:.1f}, {self.y:.1f}), status={status}, items={len(self.items)})"
