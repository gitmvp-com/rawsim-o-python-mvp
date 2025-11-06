"""Bot (robot) implementation with movement and task execution."""

from typing import Optional, List, TYPE_CHECKING
import math

if TYPE_CHECKING:
    from .instance import Instance
    from .tier import Tier
    from .pod import Pod
    from .waypoint import Waypoint


class Bot:
    """Base class for warehouse robots."""

    def __init__(self, instance: 'Instance', radius: float,
                 pod_transfer_time: float, max_acceleration: float,
                 max_deceleration: float, max_velocity: float,
                 turn_speed: float, collision_penalty_time: float,
                 x: float, y: float):
        self.instance = instance
        self.id: int = 0
        self.volatile_id: int = 0
        
        # Position and movement
        self.tier: Optional['Tier'] = None
        self.x: float = x
        self.y: float = y
        self.radius: float = radius
        self.orientation: float = 0.0  # radians
        
        # Movement capabilities
        self.max_acceleration: float = max_acceleration
        self.max_deceleration: float = max_deceleration
        self.max_velocity: float = max_velocity
        self.turn_speed: float = turn_speed
        self.current_velocity: float = 0.0
        
        # Task-related
        self.pod_transfer_time: float = pod_transfer_time
        self.collision_penalty_time: float = collision_penalty_time
        self.current_pod: Optional['Pod'] = None
        
        # Path and destination
        self.current_waypoint: Optional['Waypoint'] = None
        self.destination_waypoint: Optional['Waypoint'] = None
        self.path: List['Waypoint'] = []
        
        # State
        self.is_active: bool = True
        self.is_waiting: bool = False
        self.task_start_time: float = 0.0

    def has_pod(self) -> bool:
        """Check if bot is carrying a pod."""
        return self.current_pod is not None

    def pickup_pod(self, pod: 'Pod'):
        """Pick up a pod."""
        if self.current_pod is not None:
            raise ValueError(f"Bot {self.id} already carrying a pod")
        self.current_pod = pod
        pod.carried_by = self

    def setdown_pod(self):
        """Set down the current pod."""
        if self.current_pod is None:
            raise ValueError(f"Bot {self.id} not carrying a pod")
        self.current_pod.carried_by = None
        self.current_pod = None

    def update(self, delta_time: float):
        """Update bot state for one time step."""
        # To be implemented by subclasses
        pass

    def distance_to(self, x: float, y: float) -> float:
        """Calculate distance to a point."""
        return math.sqrt((self.x - x)**2 + (self.y - y)**2)

    def __repr__(self):
        pod_status = "with pod" if self.has_pod() else "idle"
        return f"Bot(id={self.id}, pos=({self.x:.1f}, {self.y:.1f}), {pod_status})"


class BotNormal(Bot):
    """Standard bot implementation for advanced pathfinding."""

    def __init__(self, bot_id: int, instance: 'Instance', radius: float,
                 pod_transfer_time: float, max_acceleration: float,
                 max_deceleration: float, max_velocity: float,
                 turn_speed: float, collision_penalty_time: float,
                 x: float, y: float):
        super().__init__(instance, radius, pod_transfer_time,
                        max_acceleration, max_deceleration, max_velocity,
                        turn_speed, collision_penalty_time, x, y)
        self.id = bot_id

    def update(self, delta_time: float):
        """Update bot position and state."""
        if not self.is_active or self.is_waiting:
            return

        if self.path and len(self.path) > 0:
            # Move towards next waypoint in path
            target = self.path[0]
            dx = target.x - self.x
            dy = target.y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < 0.1:  # Reached waypoint
                self.x = target.x
                self.y = target.y
                self.current_waypoint = target
                self.path.pop(0)
                self.current_velocity = 0.0
            else:
                # Accelerate/move towards target
                if self.current_velocity < self.max_velocity:
                    self.current_velocity = min(
                        self.current_velocity + self.max_acceleration * delta_time,
                        self.max_velocity
                    )

                move_distance = self.current_velocity * delta_time
                if move_distance > distance:
                    move_distance = distance

                self.x += (dx / distance) * move_distance
                self.y += (dy / distance) * move_distance

                # Update orientation
                self.orientation = math.atan2(dy, dx)


class BotHazard(Bot):
    """Bot implementation for simple pathfinding with evade distance."""

    def __init__(self, instance: 'Instance', radius: float,
                 pod_transfer_time: float, max_acceleration: float,
                 max_deceleration: float, max_velocity: float,
                 turn_speed: float, collision_penalty_time: float,
                 x: float, y: float):
        super().__init__(instance, radius, pod_transfer_time,
                        max_acceleration, max_deceleration, max_velocity,
                        turn_speed, collision_penalty_time, x, y)
        self.evade_distance: float = 2.3 * radius
        self.target_orientation: float = 0.0

    def set_target_orientation(self, orientation: float):
        """Set the target orientation for the bot."""
        self.target_orientation = orientation

    def update(self, delta_time: float):
        """Update bot with hazard-based movement."""
        # Similar to BotNormal but with evade distance consideration
        super().update(delta_time)
