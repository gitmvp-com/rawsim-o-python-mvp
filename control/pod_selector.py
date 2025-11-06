"""Pod selection strategies for order fulfillment."""

from typing import List, Optional, TYPE_CHECKING
import random

if TYPE_CHECKING:
    from core.instance import Instance
    from core.pod import Pod
    from core.order import Order
    from core.waypoint import Waypoint


class PodSelector:
    """Selects appropriate pods for orders."""

    def __init__(self, instance: 'Instance', method: str = 'nearest'):
        self.instance = instance
        self.method = method

    def select_pod(self, order: 'Order', station_waypoint: 'Waypoint') -> Optional['Pod']:
        """Select best pod for fulfilling an order."""
        # Get pods that have required items
        suitable_pods = []
        
        for pod in self.instance.pods:
            if pod.is_carried():
                continue
            
            # Check if pod has any of the required items
            has_items = False
            for item_id, quantity in order.items.items():
                if pod.has_item(item_id, 1):  # Has at least one
                    has_items = True
                    break
            
            if has_items:
                suitable_pods.append(pod)

        if not suitable_pods:
            return None

        if self.method == 'random':
            return random.choice(suitable_pods)
        elif self.method == 'nearest':
            return self._select_nearest(suitable_pods, station_waypoint)
        elif self.method == 'fixed':
            return suitable_pods[0]  # Simple fixed assignment
        else:
            return suitable_pods[0] if suitable_pods else None

    def _select_nearest(self, pods: List['Pod'], waypoint: 'Waypoint') -> Optional['Pod']:
        """Select nearest pod to the waypoint."""
        if not pods:
            return None

        def distance(pod: 'Pod') -> float:
            dx = pod.x - waypoint.x
            dy = pod.y - waypoint.y
            return (dx * dx + dy * dy) ** 0.5

        return min(pods, key=distance)

    def __repr__(self):
        return f"PodSelector(method={self.method})"
