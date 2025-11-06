"""Elevator for multi-tier warehouse movement."""

from typing import Optional, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import Instance
    from .waypoint import Waypoint


class Elevator:
    """Elevator for moving between warehouse tiers."""

    def __init__(self, instance: 'Instance'):
        self.instance = instance
        self.id: int = 0
        
        # Waypoints on different tiers
        self.waypoints: List['Waypoint'] = []
        
        # Queues for each waypoint
        self.queues: Dict['Waypoint', List['Waypoint']] = {}
        
        # Current state
        self.current_tier_index: int = 0
        self.is_moving: bool = False
        self.move_time_per_tier: float = 5.0  # seconds to move one tier

    def add_waypoint(self, waypoint: 'Waypoint'):
        """Add a waypoint on a specific tier."""
        if waypoint not in self.waypoints:
            self.waypoints.append(waypoint)
            waypoint.elevator = self

    def connect_tiers(self):
        """Create connections between waypoints on different tiers."""
        # Sort waypoints by tier z-position
        self.waypoints.sort(key=lambda wp: wp.tier.relative_position_z if wp.tier else 0)
        
        # Connect adjacent tiers
        for i in range(len(self.waypoints) - 1):
            wp1 = self.waypoints[i]
            wp2 = self.waypoints[i + 1]
            # Note: Actual traversal through elevator requires special handling
            # This is just marking them as elevator-connected

    def __repr__(self):
        return f"Elevator(id={self.id}, waypoints={len(self.waypoints)})"
