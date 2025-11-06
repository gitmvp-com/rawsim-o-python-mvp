"""Performance metrics calculation."""

from typing import List, Dict, Any
import statistics


class PerformanceMetrics:
    """Calculates various performance metrics."""

    @staticmethod
    def calculate_throughput(orders_completed: int, time_elapsed: float) -> float:
        """Calculate throughput (orders per hour)."""
        if time_elapsed <= 0:
            return 0.0
        return (orders_completed / time_elapsed) * 3600.0

    @staticmethod
    def calculate_bot_utilization(active_time: float, total_time: float) -> float:
        """Calculate bot utilization percentage."""
        if total_time <= 0:
            return 0.0
        return (active_time / total_time) * 100.0

    @staticmethod
    def calculate_average_order_time(order_times: List[float]) -> float:
        """Calculate average order processing time."""
        if not order_times:
            return 0.0
        return statistics.mean(order_times)

    @staticmethod
    def calculate_percentile(values: List[float], percentile: float) -> float:
        """Calculate percentile of values."""
        if not values:
            return 0.0
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100.0)
        return sorted_values[min(index, len(sorted_values) - 1)]

    @staticmethod
    def calculate_efficiency_metrics(data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate comprehensive efficiency metrics."""
        return {
            'throughput': data.get('throughput', 0.0),
            'utilization': data.get('bot_utilization', 0.0),
            'avg_order_time': data.get('avg_order_time', 0.0),
            'collision_rate': data.get('collisions', 0) / max(data.get('total_movements', 1), 1),
        }
