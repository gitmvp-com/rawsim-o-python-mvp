"""Windowed Hierarchical Cooperative A* (WHCAvStar) pathfinding."""

from typing import List, Dict, Optional, Set, TYPE_CHECKING
import heapq
import math

if TYPE_CHECKING:
    from core.waypoint import Waypoint
    from core.bot import Bot

from .astar import AStar


class WHCAvStar:
    """Windowed Hierarchical Cooperative A* for multi-agent pathfinding."""

    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.astar = AStar(heuristic='euclidean')
        self.reservations: Dict['Waypoint', List[float]] = {}  # waypoint -> list of reserved times

    def reserve_waypoint(self, waypoint: 'Waypoint', time: float, duration: float = 1.0):
        """Reserve a waypoint for a specific time window."""
        if waypoint not in self.reservations:
            self.reservations[waypoint] = []
        self.reservations[waypoint].append((time, time + duration))

    def is_waypoint_available(self, waypoint: 'Waypoint', time: float) -> bool:
        """Check if waypoint is available at a specific time."""
        if waypoint not in self.reservations:
            return True

        # Check if time conflicts with any reservation
        for start_time, end_time in self.reservations[waypoint]:
            if start_time <= time <= end_time:
                return False
        return True

    def find_path_cooperative(self, bot: 'Bot', start: 'Waypoint', goal: 'Waypoint',
                             start_time: float = 0.0) -> Optional[List['Waypoint']]:
        """Find path considering other bots' reservations."""
        # Use time-extended A* with reservation table
        current_time = start_time

        def is_blocked(wp: 'Waypoint') -> bool:
            # Check if waypoint is blocked by static obstacles
            if wp.pod_storage_location and wp.pod is not None:
                return True
            # Check time-based reservations
            if not self.is_waypoint_available(wp, current_time):
                return True
            return False

        # Find basic path
        path = self.astar.find_path(start, goal, is_blocked)

        if path:
            # Reserve waypoints along the path
            time = start_time
            for wp in path:
                self.reserve_waypoint(wp, time)
                time += 1.0  # Assume 1 second per waypoint

        return path

    def clear_old_reservations(self, current_time: float):
        """Clear reservations that are in the past."""
        for waypoint in list(self.reservations.keys()):
            self.reservations[waypoint] = [
                (start, end) for start, end in self.reservations[waypoint]
                if end > current_time
            ]
            if not self.reservations[waypoint]:
                del self.reservations[waypoint]

    def __repr__(self):
        return f"WHCAvStar(window={self.window_size}, reservations={len(self.reservations)})"
