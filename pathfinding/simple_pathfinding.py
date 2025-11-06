"""Simple pathfinding for basic scenarios."""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.waypoint import Waypoint

from .astar import AStar


class SimplePathfinding:
    """Simple pathfinding using basic A* without cooperation."""

    def __init__(self):
        self.astar = AStar(heuristic='manhattan')

    def find_path(self, start: 'Waypoint', goal: 'Waypoint') -> Optional[List['Waypoint']]:
        """Find simple path from start to goal."""
        def is_blocked(wp: 'Waypoint') -> bool:
            return wp.pod_storage_location and wp.pod is not None

        return self.astar.find_path(start, goal, is_blocked)

    def __repr__(self):
        return "SimplePathfinding()"
