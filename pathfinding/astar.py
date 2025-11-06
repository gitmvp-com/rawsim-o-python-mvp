"""A* pathfinding algorithm implementation."""

from typing import List, Optional, Callable, TYPE_CHECKING
import heapq
import math

if TYPE_CHECKING:
    from core.waypoint import Waypoint


class AStar:
    """A* pathfinding algorithm for waypoint graphs."""

    def __init__(self, heuristic: str = 'euclidean'):
        self.heuristic_type = heuristic

    def heuristic(self, wp1: 'Waypoint', wp2: 'Waypoint') -> float:
        """Calculate heuristic distance between waypoints."""
        dx = wp1.x - wp2.x
        dy = wp1.y - wp2.y

        if self.heuristic_type == 'manhattan':
            return abs(dx) + abs(dy)
        elif self.heuristic_type == 'euclidean':
            return math.sqrt(dx * dx + dy * dy)
        else:
            return abs(dx) + abs(dy)  # Default to Manhattan

    def find_path(self, start: 'Waypoint', goal: 'Waypoint',
                  is_blocked: Callable[['Waypoint'], bool] = None) -> Optional[List['Waypoint']]:
        """Find shortest path from start to goal using A*."""
        if start == goal:
            return [start]

        if is_blocked is None:
            is_blocked = lambda wp: False

        # Priority queue: (f_score, counter, waypoint)
        counter = 0
        open_set = [(0, counter, start)]
        counter += 1

        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        open_set_hash = {start}

        while open_set:
            current_f, _, current = heapq.heappop(open_set)
            open_set_hash.remove(current)

            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            # Check neighbors
            for neighbor in current.get_neighbors():
                # Skip blocked waypoints (except goal)
                if neighbor != goal and is_blocked(neighbor):
                    continue

                # Calculate tentative g_score
                tentative_g = g_score[current] + current.distance_to(neighbor)

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, goal)
                    f_score[neighbor] = f

                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f, counter, neighbor))
                        counter += 1
                        open_set_hash.add(neighbor)

        # No path found
        return None

    def __repr__(self):
        return f"AStar(heuristic={self.heuristic_type})"
