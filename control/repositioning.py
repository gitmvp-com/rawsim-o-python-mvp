"""Pod repositioning logic."""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.instance import Instance
    from core.pod import Pod
    from core.waypoint import Waypoint


class RepositioningManager:
    """Manages pod repositioning for optimization."""

    def __init__(self, instance: 'Instance', enabled: bool = False):
        self.instance = instance
        self.enabled = enabled

    def should_reposition(self, pod: 'Pod') -> bool:
        """Determine if a pod should be repositioned."""
        if not self.enabled:
            return False

        # Simple heuristic: reposition if pod is frequently accessed
        if pod.times_picked > 10:
            # Move closer to output stations
            return True

        return False

    def find_reposition_location(self, pod: 'Pod') -> Optional['Waypoint']:
        """Find optimal location to reposition a pod."""
        # Get available storage locations
        available = [wp for wp in self.instance.waypoints
                    if wp.pod_storage_location and wp.pod is None]

        if not available:
            return None

        # Simple strategy: find location closest to output stations
        if self.instance.output_stations:
            avg_x = sum(s.x for s in self.instance.output_stations) / len(self.instance.output_stations)
            avg_y = sum(s.y for s in self.instance.output_stations) / len(self.instance.output_stations)

            def distance(wp: 'Waypoint') -> float:
                return ((wp.x - avg_x) ** 2 + (wp.y - avg_y) ** 2) ** 0.5

            return min(available, key=distance)

        return available[0] if available else None

    def __repr__(self):
        return f"RepositioningManager(enabled={self.enabled})"
