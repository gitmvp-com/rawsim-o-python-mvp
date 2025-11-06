"""Geometric calculations and utilities."""

import math
from typing import Tuple


class GeometryHelper:
    """Helper functions for geometric calculations."""

    @staticmethod
    def distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate Euclidean distance between two points."""
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def manhattan_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate Manhattan distance between two points."""
        return abs(x2 - x1) + abs(y2 - y1)

    @staticmethod
    def angle_between_points(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate angle from point 1 to point 2 in radians."""
        return math.atan2(y2 - y1, x2 - x1)

    @staticmethod
    def normalize_angle(angle: float) -> float:
        """Normalize angle to [-pi, pi]."""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    @staticmethod
    def circles_intersect(x1: float, y1: float, r1: float,
                         x2: float, y2: float, r2: float) -> bool:
        """Check if two circles intersect."""
        distance = GeometryHelper.distance(x1, y1, x2, y2)
        return distance < (r1 + r2)

    @staticmethod
    def point_in_rectangle(px: float, py: float,
                          rect_x: float, rect_y: float,
                          rect_width: float, rect_height: float) -> bool:
        """Check if point is inside rectangle."""
        return (rect_x <= px <= rect_x + rect_width and
                rect_y <= py <= rect_y + rect_height)

    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp value between min and max."""
        return max(min_val, min(value, max_val))
