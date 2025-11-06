"""Waypoint (navigation node) implementation."""

from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import Instance
    from .tier import Tier
    from .pod import Pod
    from .station import InputStation, OutputStation
    from .elevator import Elevator


class Waypoint:
    """Navigation node in the warehouse graph."""

    def __init__(self, instance: 'Instance'):
        self.instance = instance
        self.id: int = 0
        self.volatile_id: int = 0
        
        # Position
        self.tier: Optional['Tier'] = None
        self.x: float = 0.0
        self.y: float = 0.0
        self.radius: float = 0.3
        
        # Graph connections
        self.paths: List['Waypoint'] = []  # Adjacent waypoints
        self.path_distances: List[float] = []  # Distances to adjacent waypoints
        
        # Type flags
        self.pod_storage_location: bool = False
        self.is_queue_waypoint: bool = False
        
        # Associated elements
        self.input_station: Optional['InputStation'] = None
        self.output_station: Optional['OutputStation'] = None
        self.elevator: Optional['Elevator'] = None
        self.pod: Optional['Pod'] = None  # Pod currently at this waypoint
        
        # Reservations (for pathfinding)
        self.reserved_by = None  # Bot that reserved this waypoint
        self.reservation_time: float = 0.0

    def is_available(self) -> bool:
        """Check if waypoint is available for navigation."""
        if self.pod_storage_location and self.pod is not None:
            return False
        if self.reserved_by is not None:
            return False
        return True

    def is_station_waypoint(self) -> bool:
        """Check if this waypoint is associated with a station."""
        return self.input_station is not None or self.output_station is not None

    def add_path(self, waypoint: 'Waypoint', distance: float = None):
        """Add a bidirectional path to another waypoint."""
        if waypoint not in self.paths:
            if distance is None:
                dx = self.x - waypoint.x
                dy = self.y - waypoint.y
                distance = (dx**2 + dy**2)**0.5
            
            self.paths.append(waypoint)
            self.path_distances.append(distance)
            
            # Add reverse connection
            waypoint.paths.append(self)
            waypoint.path_distances.append(distance)

    def get_neighbors(self) -> List['Waypoint']:
        """Get all neighboring waypoints."""
        return self.paths

    def distance_to(self, other: 'Waypoint') -> float:
        """Calculate distance to another waypoint."""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2)**0.5

    def __repr__(self):
        wp_type = "storage" if self.pod_storage_location else "queue" if self.is_queue_waypoint else "normal"
        return f"Waypoint(id={self.id}, pos=({self.x:.1f}, {self.y:.1f}), type={wp_type})"
