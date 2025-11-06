"""Waypoint graph for pathfinding."""

from typing import List, Dict, Set, Optional, TYPE_CHECKING
import math

if TYPE_CHECKING:
    from core.waypoint import Waypoint
    from core.pod import Pod


class WaypointGraph:
    """Graph structure for waypoint-based navigation."""

    def __init__(self):
        self.waypoints: List['Waypoint'] = []
        self.adjacency: Dict['Waypoint', List['Waypoint']] = {}

    def add(self, waypoint: 'Waypoint'):
        """Add a waypoint to the graph."""
        if waypoint not in self.waypoints:
            self.waypoints.append(waypoint)
            self.adjacency[waypoint] = []

    def add_edge(self, from_wp: 'Waypoint', to_wp: 'Waypoint', bidirectional: bool = True):
        """Add an edge between two waypoints."""
        if from_wp not in self.adjacency:
            self.add(from_wp)
        if to_wp not in self.adjacency:
            self.add(to_wp)

        if to_wp not in self.adjacency[from_wp]:
            self.adjacency[from_wp].append(to_wp)

        if bidirectional and from_wp not in self.adjacency[to_wp]:
            self.adjacency[to_wp].append(from_wp)

    def get_neighbors(self, waypoint: 'Waypoint') -> List['Waypoint']:
        """Get neighboring waypoints."""
        return self.adjacency.get(waypoint, [])

    def pod_setdown(self, pod: 'Pod', waypoint: 'Waypoint'):
        """Handle pod being set down at a waypoint."""
        waypoint.pod = pod
        pod.waypoint = waypoint

    def pod_pickup(self, pod: 'Pod'):
        """Handle pod being picked up from a waypoint."""
        if pod.waypoint:
            pod.waypoint.pod = None
            pod.waypoint = None

    def is_waypoint_blocked(self, waypoint: 'Waypoint') -> bool:
        """Check if waypoint is blocked by a pod."""
        return waypoint.pod_storage_location and waypoint.pod is not None

    def get_available_storage_locations(self) -> List['Waypoint']:
        """Get all available storage waypoints."""
        return [wp for wp in self.waypoints 
                if wp.pod_storage_location and wp.pod is None]

    def get_distance(self, wp1: 'Waypoint', wp2: 'Waypoint') -> float:
        """Calculate Euclidean distance between two waypoints."""
        dx = wp1.x - wp2.x
        dy = wp1.y - wp2.y
        return math.sqrt(dx * dx + dy * dy)

    def __repr__(self):
        return f"WaypointGraph(waypoints={len(self.waypoints)})"
