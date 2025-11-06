"""Main simulation instance managing all warehouse elements."""

from typing import List, Dict, Optional, Any
import logging
from datetime import datetime

from .compound import Compound
from .tier import Tier
from .bot import Bot, BotNormal, BotHazard
from .pod import Pod
from .waypoint import Waypoint
from .station import InputStation, OutputStation
from .elevator import Elevator
from .item import ItemDescription, ItemBundle, SimpleItemDescription
from .order import Order, OrderList
from .semaphore import QueueSemaphore


class Instance:
    """The core element of each simulation instance."""

    def __init__(self):
        self.name: str = "DefaultInstance"
        self.setting_config: Dict[str, Any] = {}
        self.controller_config: Dict[str, Any] = {}
        
        # Core elements
        self.compound: Optional[Compound] = None
        self.bots: List[Bot] = []
        self.pods: List[Pod] = []
        self.elevators: List[Elevator] = []
        self.input_stations: List[InputStation] = []
        self.output_stations: List[OutputStation] = []
        self.waypoints: List[Waypoint] = []
        self.semaphores: List[QueueSemaphore] = []
        
        # Items and orders
        self.item_descriptions: List[ItemDescription] = []
        self.item_bundles: List[ItemBundle] = []
        self.order_list: Optional[OrderList] = None
        
        # ID generators
        self._bot_id = 0
        self._pod_id = 0
        self._waypoint_id = 0
        self._tier_id = 0
        self._item_description_id = 0
        self._item_bundle_id = 0
        self._elevator_id = 0
        self._input_station_id = 0
        self._output_station_id = 0
        self._semaphore_id = 0
        
        # Volatile ID tracking
        self._volatile_bot_ids = set()
        self._volatile_pod_ids = set()
        self._volatile_waypoint_ids = set()
        
        # Lookup dictionaries
        self._id_to_bot: Dict[int, Bot] = {}
        self._id_to_pod: Dict[int, Pod] = {}
        self._id_to_waypoint: Dict[int, Waypoint] = {}
        self._id_to_tier: Dict[int, Tier] = {}
        
        # Statistics and observers
        self.current_time: float = 0.0
        self.statistics: Dict[str, Any] = {}
        self.tag: Optional[str] = None
        
        # Randomizer
        self.randomizer = None
        
        # Waypoint graph (will be initialized by pathfinding module)
        self.waypoint_graph = None
        
        logging.info(f"Instance created: {self.name}")

    @staticmethod
    def create_instance(setting_config: Dict[str, Any] = None,
                       controller_config: Dict[str, Any] = None) -> 'Instance':
        """Create a new instance with given configurations."""
        instance = Instance()
        instance.setting_config = setting_config or {}
        instance.controller_config = controller_config or {}
        return instance

    def create_compound(self) -> Compound:
        """Create the compound that manages all tiers."""
        if self.compound is not None:
            raise ValueError("Compound already exists")
        self.compound = Compound(self)
        self.compound.id = 0
        return self.compound

    def create_tier(self, tier_id: int, length: float, width: float,
                   x: float = 0, y: float = 0, z: float = 0) -> Tier:
        """Create a new tier (warehouse floor level)."""
        if self.compound is None:
            self.create_compound()
        
        tier = Tier(self, length, width)
        tier.id = tier_id
        tier.volatile_id = self._tier_id
        tier.relative_position_x = x
        tier.relative_position_y = y
        tier.relative_position_z = z
        
        self.compound.tiers.append(tier)
        self._id_to_tier[tier.id] = tier
        self._tier_id += 1
        
        return tier

    def create_bot(self, bot_id: int, tier: Tier, x: float, y: float,
                   radius: float, orientation: float = 0.0,
                   pod_transfer_time: float = 5.0,
                   max_acceleration: float = 1.0,
                   max_deceleration: float = 1.0,
                   max_velocity: float = 2.0,
                   turn_speed: float = 1.0,
                   collision_penalty_time: float = 5.0) -> Bot:
        """Create a new bot."""
        
        # Determine bot type based on pathfinding config
        pathfinding_method = self.controller_config.get('pathfinding', {}).get('method', 'WHCAvStar')
        
        if pathfinding_method == 'Simple':
            bot = BotHazard(self, radius, pod_transfer_time, max_acceleration,
                          max_deceleration, max_velocity, turn_speed,
                          collision_penalty_time, x, y)
        else:
            bot = BotNormal(bot_id, self, radius, pod_transfer_time,
                          max_acceleration, max_deceleration, max_velocity,
                          turn_speed, collision_penalty_time, x, y)
        
        bot.id = bot_id
        bot.tier = tier
        bot.orientation = orientation
        
        self.bots.append(bot)
        tier.add_bot(bot)
        self._id_to_bot[bot.id] = bot
        
        # Assign volatile ID
        volatile_id = 0
        while volatile_id in self._volatile_bot_ids:
            volatile_id += 1
        bot.volatile_id = volatile_id
        self._volatile_bot_ids.add(volatile_id)
        
        self._bot_id = max(self._bot_id, bot_id + 1)
        
        return bot

    def create_pod(self, pod_id: int, tier: Tier, x: float, y: float,
                   radius: float, orientation: float = 0.0,
                   capacity: float = 100.0) -> Pod:
        """Create a new pod."""
        pod = Pod(self)
        pod.id = pod_id
        pod.tier = tier
        pod.x = x
        pod.y = y
        pod.radius = radius
        pod.orientation = orientation
        pod.capacity = capacity
        
        self.pods.append(pod)
        tier.add_pod(pod)
        self._id_to_pod[pod.id] = pod
        
        # Assign volatile ID
        volatile_id = 0
        while volatile_id in self._volatile_pod_ids:
            volatile_id += 1
        pod.volatile_id = volatile_id
        self._volatile_pod_ids.add(volatile_id)
        
        self._pod_id = max(self._pod_id, pod_id + 1)
        
        return pod

    def create_waypoint(self, wp_id: int, tier: Tier, x: float, y: float,
                       pod_storage_location: bool = False,
                       is_queue_waypoint: bool = False) -> Waypoint:
        """Create a new waypoint."""
        waypoint = Waypoint(self)
        waypoint.id = wp_id
        waypoint.tier = tier
        waypoint.x = x
        waypoint.y = y
        waypoint.pod_storage_location = pod_storage_location
        waypoint.is_queue_waypoint = is_queue_waypoint
        
        self.waypoints.append(waypoint)
        tier.add_waypoint(waypoint)
        self._id_to_waypoint[waypoint.id] = waypoint
        
        # Assign volatile ID
        volatile_id = 0
        while volatile_id in self._volatile_waypoint_ids:
            volatile_id += 1
        waypoint.volatile_id = volatile_id
        self._volatile_waypoint_ids.add(volatile_id)
        
        self._waypoint_id = max(self._waypoint_id, wp_id + 1)
        
        return waypoint

    def create_input_station(self, station_id: int, tier: Tier,
                            x: float, y: float, radius: float,
                            capacity: float = 100.0,
                            item_bundle_transfer_time: float = 3.0,
                            activation_order_id: int = 0) -> InputStation:
        """Create a new input station."""
        station = InputStation(self)
        station.id = station_id
        station.tier = tier
        station.x = x
        station.y = y
        station.radius = radius
        station.capacity = capacity
        station.item_bundle_transfer_time = item_bundle_transfer_time
        station.activation_order_id = activation_order_id
        
        self.input_stations.append(station)
        tier.add_input_station(station)
        
        self._input_station_id = max(self._input_station_id, station_id + 1)
        
        return station

    def create_output_station(self, station_id: int, tier: Tier,
                             x: float, y: float, radius: float,
                             capacity: int = 10,
                             item_transfer_time: float = 2.0,
                             item_pick_time: float = 1.0,
                             activation_order_id: int = 0) -> OutputStation:
        """Create a new output station."""
        station = OutputStation(self)
        station.id = station_id
        station.tier = tier
        station.x = x
        station.y = y
        station.radius = radius
        station.capacity = capacity
        station.item_transfer_time = item_transfer_time
        station.item_pick_time = item_pick_time
        station.activation_order_id = activation_order_id
        
        self.output_stations.append(station)
        tier.add_output_station(station)
        
        self._output_station_id = max(self._output_station_id, station_id + 1)
        
        return station

    def create_elevator(self, elevator_id: int) -> Elevator:
        """Create a new elevator."""
        elevator = Elevator(self)
        elevator.id = elevator_id
        self.elevators.append(elevator)
        
        self._elevator_id = max(self._elevator_id, elevator_id + 1)
        
        return elevator

    def create_item_description(self, item_id: int) -> ItemDescription:
        """Create an item description."""
        item = SimpleItemDescription(self)
        item.id = item_id
        self.item_descriptions.append(item)
        
        self._item_description_id = max(self._item_description_id, item_id + 1)
        
        return item

    def create_semaphore(self, sem_id: int, max_count: int) -> QueueSemaphore:
        """Create a queue semaphore for traffic control."""
        semaphore = QueueSemaphore(self, max_count)
        semaphore.id = sem_id
        self.semaphores.append(semaphore)
        
        self._semaphore_id = max(self._semaphore_id, sem_id + 1)
        
        return semaphore

    def get_statistics(self) -> Dict[str, Any]:
        """Get current simulation statistics."""
        return {
            'current_time': self.current_time,
            'bots_count': len(self.bots),
            'pods_count': len(self.pods),
            'input_stations': len(self.input_stations),
            'output_stations': len(self.output_stations),
            'waypoints_count': len(self.waypoints),
        }

    def __repr__(self):
        return (f"Instance(name={self.name}, bots={len(self.bots)}, "
                f"pods={len(self.pods)}, time={self.current_time:.2f})")
