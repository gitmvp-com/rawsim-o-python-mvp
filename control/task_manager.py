"""Task assignment and management for bots."""

from typing import List, Optional, TYPE_CHECKING
import math

if TYPE_CHECKING:
    from core.instance import Instance
    from core.bot import Bot
    from core.order import Order
    from core.station import OutputStation


class TaskManager:
    """Manages task assignment to bots."""

    def __init__(self, instance: 'Instance', method: str = 'nearest'):
        self.instance = instance
        self.method = method
        self.pending_tasks = []

    def assign_task(self, order: 'Order', station: 'OutputStation') -> Optional['Bot']:
        """Assign a task to the best available bot."""
        available_bots = [bot for bot in self.instance.bots 
                         if bot.is_active and not bot.has_pod() and not bot.path]

        if not available_bots:
            return None

        if self.method == 'nearest':
            return self._assign_nearest(station, available_bots)
        elif self.method == 'balanced':
            return self._assign_balanced(available_bots)
        elif self.method == 'priority':
            return self._assign_priority(order, available_bots)
        else:
            return available_bots[0] if available_bots else None

    def _assign_nearest(self, station: 'OutputStation', bots: List['Bot']) -> Optional['Bot']:
        """Assign nearest available bot."""
        if not bots:
            return None

        nearest_bot = min(bots, key=lambda b: b.distance_to(station.x, station.y))
        return nearest_bot

    def _assign_balanced(self, bots: List['Bot']) -> Optional['Bot']:
        """Assign bot with least tasks completed (load balancing)."""
        if not bots:
            return None
        # Simple: just return first available (can be enhanced with statistics)
        return bots[0]

    def _assign_priority(self, order: 'Order', bots: List['Bot']) -> Optional['Bot']:
        """Assign based on order priority."""
        # For high priority orders, prefer fastest/nearest bot
        if order.priority > 5:
            return self._assign_nearest(None, bots)
        return bots[0] if bots else None

    def __repr__(self):
        return f"TaskManager(method={self.method}, pending={len(self.pending_tasks)})"
