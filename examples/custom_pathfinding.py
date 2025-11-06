#!/usr/bin/env python3
"""Example of using different pathfinding algorithms."""

import sys
sys.path.insert(0, '.')

from generator.instance_generator import InstanceGenerator
from pathfinding.astar import AStar
from pathfinding.whcav_star import WHCAvStar
from pathfinding.simple_pathfinding import SimplePathfinding
from utils.logger import setup_logger


def test_pathfinding_algorithms():
    logger = setup_logger('PathfindingExample', level=20)
    
    # Generate instance
    generator = InstanceGenerator(seed=42)
    instance = generator.generate_simple_warehouse(
        length=30.0, width=20.0, num_bots=5, num_pods=15
    )
    
    # Get some waypoints
    waypoints = instance.waypoints
    if len(waypoints) < 2:
        logger.error("Not enough waypoints for testing")
        return
    
    start = waypoints[0]
    goal = waypoints[-1]
    
    logger.info(f"Finding path from waypoint {start.id} to {goal.id}")
    logger.info(f"Distance: {start.distance_to(goal):.2f}")
    
    # Test A*
    logger.info("\n1. Testing A* (Euclidean)...")
    astar_euclidean = AStar(heuristic='euclidean')
    path1 = astar_euclidean.find_path(start, goal)
    if path1:
        logger.info(f"   Path found! Length: {len(path1)} waypoints")
    else:
        logger.info("   No path found")
    
    # Test A* Manhattan
    logger.info("\n2. Testing A* (Manhattan)...")
    astar_manhattan = AStar(heuristic='manhattan')
    path2 = astar_manhattan.find_path(start, goal)
    if path2:
        logger.info(f"   Path found! Length: {len(path2)} waypoints")
    else:
        logger.info("   No path found")
    
    # Test WHCAvStar
    logger.info("\n3. Testing WHCAvStar...")
    whcav = WHCAvStar(window_size=10)
    path3 = whcav.find_path_cooperative(instance.bots[0], start, goal, 0.0)
    if path3:
        logger.info(f"   Path found! Length: {len(path3)} waypoints")
    else:
        logger.info("   No path found")
    
    # Test Simple
    logger.info("\n4. Testing Simple Pathfinding...")
    simple = SimplePathfinding()
    path4 = simple.find_path(start, goal)
    if path4:
        logger.info(f"   Path found! Length: {len(path4)} waypoints")
    else:
        logger.info("   No path found")
    
    logger.info("\nAll pathfinding algorithms tested!")


if __name__ == '__main__':
    test_pathfinding_algorithms()
