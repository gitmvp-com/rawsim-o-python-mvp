"""Procedural warehouse instance generation."""

import math
from typing import Dict, Any

from core.instance import Instance
from utils.randomizer import RandomizerSimple


class InstanceGenerator:
    """Generates warehouse instances procedurally."""

    def __init__(self, seed: int = None):
        self.randomizer = RandomizerSimple(seed)

    def generate_simple_warehouse(self, 
                                 length: float = 50.0,
                                 width: float = 30.0,
                                 num_bots: int = 10,
                                 num_pods: int = 50,
                                 num_input_stations: int = 2,
                                 num_output_stations: int = 3,
                                 aisle_width: float = 3.0) -> Instance:
        """Generate a simple warehouse layout."""
        instance = Instance.create_instance(
            setting_config={'time_step': 0.1, 'simulation_duration': 3600.0},
            controller_config={'pathfinding': {'method': 'WHCAvStar'}}
        )
        instance.name = "GeneratedWarehouse"
        instance.randomizer = self.randomizer

        # Create single tier
        tier = instance.create_tier(0, length, width, 0, 0, 0)

        # Generate waypoints in a grid
        waypoint_spacing = 2.0
        waypoints = []
        
        cols = int(length / waypoint_spacing)
        rows = int(width / waypoint_spacing)

        for i in range(cols):
            for j in range(rows):
                x = i * waypoint_spacing + waypoint_spacing / 2
                y = j * waypoint_spacing + waypoint_spacing / 2
                
                # Determine if this is a storage location (not in aisles)
                is_storage = (i % 4 != 0)  # Every 4th column is an aisle
                
                wp = instance.create_waypoint(
                    len(waypoints), tier, x, y,
                    pod_storage_location=is_storage,
                    is_queue_waypoint=False
                )
                waypoints.append(wp)

        # Connect waypoints (4-connectivity)
        for i in range(cols):
            for j in range(rows):
                idx = i * rows + j
                wp = waypoints[idx]

                # Connect to right neighbor
                if i < cols - 1:
                    right_idx = (i + 1) * rows + j
                    wp.add_path(waypoints[right_idx])

                # Connect to top neighbor
                if j < rows - 1:
                    top_idx = i * rows + (j + 1)
                    wp.add_path(waypoints[top_idx])

        # Place input stations along left edge
        for i in range(num_input_stations):
            y_pos = (i + 1) * width / (num_input_stations + 1)
            station = instance.create_input_station(
                i, tier, 1.0, y_pos, 1.0, capacity=100.0,
                item_bundle_transfer_time=3.0, activation_order_id=i
            )
            # Create waypoint for station
            wp = instance.create_waypoint(
                len(waypoints), tier, station.x + 2.0, station.y,
                pod_storage_location=False, is_queue_waypoint=True
            )
            station.waypoint = wp
            wp.input_station = station
            waypoints.append(wp)

        # Place output stations along right edge
        for i in range(num_output_stations):
            y_pos = (i + 1) * width / (num_output_stations + 1)
            station = instance.create_output_station(
                i, tier, length - 1.0, y_pos, 1.0, capacity=10,
                item_transfer_time=2.0, item_pick_time=1.0,
                activation_order_id=i
            )
            # Create waypoint for station
            wp = instance.create_waypoint(
                len(waypoints), tier, station.x - 2.0, station.y,
                pod_storage_location=False, is_queue_waypoint=True
            )
            station.waypoint = wp
            wp.output_station = station
            waypoints.append(wp)

        # Place pods at storage locations
        storage_waypoints = [wp for wp in waypoints if wp.pod_storage_location]
        for i in range(min(num_pods, len(storage_waypoints))):
            wp = storage_waypoints[i]
            pod = instance.create_pod(
                i, tier, wp.x, wp.y, 0.5, 0.0, capacity=100.0
            )
            wp.pod = pod
            pod.waypoint = wp

        # Place bots at random non-storage waypoints
        available_waypoints = [wp for wp in waypoints if not wp.pod_storage_location]
        for i in range(num_bots):
            if i < len(available_waypoints):
                wp = self.randomizer.choice(available_waypoints)
                bot = instance.create_bot(
                    i, tier, wp.x, wp.y, 0.3, 0.0,
                    pod_transfer_time=5.0,
                    max_acceleration=1.0,
                    max_deceleration=1.0,
                    max_velocity=2.0,
                    turn_speed=1.0,
                    collision_penalty_time=5.0
                )

        return instance

    def generate_config_dict(self, instance: Instance) -> Dict[str, Any]:
        """Generate configuration dictionary for an instance."""
        return {
            'name': instance.name,
            'tiers': [
                {
                    'id': tier.id,
                    'length': tier.length,
                    'width': tier.width,
                    'position': {
                        'x': tier.relative_position_x,
                        'y': tier.relative_position_y,
                        'z': tier.relative_position_z,
                    }
                }
                for tier in instance.compound.tiers
            ],
            'bots': len(instance.bots),
            'pods': len(instance.pods),
            'waypoints': len(instance.waypoints),
            'input_stations': len(instance.input_stations),
            'output_stations': len(instance.output_stations),
        }
