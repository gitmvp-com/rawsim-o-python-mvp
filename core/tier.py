"""Tier (warehouse floor level) implementation."""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import Instance
    from .bot import Bot
    from .pod import Pod
    from .waypoint import Waypoint
    from .station import InputStation, OutputStation


class Tier:
    """Represents one floor/level of the warehouse."""

    def __init__(self, instance: 'Instance', length: float, width: float):
        self.instance = instance
        self.id: int = 0
        self.volatile_id: int = 0
        
        # Dimensions
        self.length: float = length
        self.width: float = width
        
        # Position in 3D space
        self.relative_position_x: float = 0.0
        self.relative_position_y: float = 0.0
        self.relative_position_z: float = 0.0
        
        # Elements on this tier
        self.bots: List['Bot'] = []
        self.pods: List['Pod'] = []
        self.waypoints: List['Waypoint'] = []
        self.input_stations: List['InputStation'] = []
        self.output_stations: List['OutputStation'] = []

    def add_bot(self, bot: 'Bot'):
        """Add a bot to this tier."""
        if bot not in self.bots:
            self.bots.append(bot)
            bot.tier = self

    def add_pod(self, pod: 'Pod'):
        """Add a pod to this tier."""
        if pod not in self.pods:
            self.pods.append(pod)
            pod.tier = self

    def add_waypoint(self, waypoint: 'Waypoint'):
        """Add a waypoint to this tier."""
        if waypoint not in self.waypoints:
            self.waypoints.append(waypoint)
            waypoint.tier = self

    def add_input_station(self, station: 'InputStation'):
        """Add an input station to this tier."""
        if station not in self.input_stations:
            self.input_stations.append(station)
            station.tier = self

    def add_output_station(self, station: 'OutputStation'):
        """Add an output station to this tier."""
        if station not in self.output_stations:
            self.output_stations.append(station)
            station.tier = self

    def get_bounds(self):
        """Get the bounds of this tier."""
        return {
            'min_x': self.relative_position_x,
            'max_x': self.relative_position_x + self.length,
            'min_y': self.relative_position_y,
            'max_y': self.relative_position_y + self.width,
        }

    def __repr__(self):
        return (f"Tier(id={self.id}, size={self.length}x{self.width}, "
                f"bots={len(self.bots)}, pods={len(self.pods)}, waypoints={len(self.waypoints)})")
