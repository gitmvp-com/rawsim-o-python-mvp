"""Statistics tracking for simulation."""

from typing import Dict, List, Any, TYPE_CHECKING
from collections import defaultdict

if TYPE_CHECKING:
    from core.instance import Instance


class StatisticsTracker:
    """Tracks simulation statistics over time."""

    def __init__(self, instance: 'Instance'):
        self.instance = instance
        
        # Time series data
        self.time_points: List[float] = []
        self.orders_completed: List[int] = []
        self.throughput: List[float] = []
        self.bot_utilization: List[float] = []
        
        # Counters
        self.total_orders = 0
        self.total_items_picked = 0
        self.total_distance_traveled = 0.0
        self.total_collisions = 0
        
        # Bot statistics
        self.bot_stats = defaultdict(lambda: {
            'distance': 0.0,
            'tasks_completed': 0,
            'idle_time': 0.0,
            'active_time': 0.0,
        })

    def record_snapshot(self, current_time: float):
        """Record a snapshot of current statistics."""
        self.time_points.append(current_time)
        
        # Count completed orders
        completed = sum(1 for station in self.instance.output_stations 
                       for _ in range(station.orders_completed))
        self.orders_completed.append(completed)
        
        # Calculate throughput (orders per second)
        if current_time > 0:
            throughput = completed / current_time
            self.throughput.append(throughput)
        else:
            self.throughput.append(0.0)
        
        # Calculate bot utilization
        if self.instance.bots:
            active_bots = sum(1 for bot in self.instance.bots 
                            if bot.has_pod() or len(bot.path) > 0)
            utilization = active_bots / len(self.instance.bots)
            self.bot_utilization.append(utilization)
        else:
            self.bot_utilization.append(0.0)

    def record_order_completion(self, order_id: int, completion_time: float):
        """Record order completion."""
        self.total_orders += 1

    def record_item_pick(self):
        """Record an item being picked."""
        self.total_items_picked += 1

    def record_collision(self, bot_id: int):
        """Record a collision."""
        self.total_collisions += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        avg_throughput = sum(self.throughput) / len(self.throughput) if self.throughput else 0
        avg_utilization = sum(self.bot_utilization) / len(self.bot_utilization) if self.bot_utilization else 0
        
        return {
            'total_orders': self.total_orders,
            'total_items_picked': self.total_items_picked,
            'total_collisions': self.total_collisions,
            'average_throughput': avg_throughput,
            'average_bot_utilization': avg_utilization,
            'simulation_time': self.time_points[-1] if self.time_points else 0,
        }

    def __repr__(self):
        return f"StatisticsTracker(orders={self.total_orders}, snapshots={len(self.time_points)})"
