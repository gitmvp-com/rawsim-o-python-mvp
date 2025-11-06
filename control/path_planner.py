"""Path planning controller."""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.instance import Instance
    from core.bot import Bot
    from core.waypoint import Waypoint

from pathfinding.astar import AStar
from pathfinding.whcav_star import WHCAvStar
from pathfinding.simple_pathfinding import SimplePathfinding


class PathPlanner:
    """Plans paths for bots using various algorithms."""

    def __init__(self, instance: 'Instance', method: str = 'WHCAvStar'):
        self.instance = instance
        self.method = method

        if method == 'AStar':
            self.pathfinder = AStar()
        elif method == 'WHCAvStar':
            self.pathfinder = WHCAvStar()
        elif method == 'Simple':
            self.pathfinder = SimplePathfinding()
        else:
            self.pathfinder = AStar()  # Default

    def plan_path(self, bot: 'Bot', start: 'Waypoint', goal: 'Waypoint') -> Optional[List['Waypoint']]:
        """Plan a path from start to goal for a bot."""
        if self.method == 'WHCAvStar':
            return self.pathfinder.find_path_cooperative(
                bot, start, goal, self.instance.current_time
            )
        else:
            return self.pathfinder.find_path(start, goal)

    def update(self, delta_time: float):
        """Update path planner state."""
        if self.method == 'WHCAvStar':
            # Clear old reservations
            self.pathfinder.clear_old_reservations(self.instance.current_time)

    def __repr__(self):
        return f"PathPlanner(method={self.method})"
