"""Event system for simulation."""

from enum import Enum
from typing import Any, Dict, Callable, List


class EventType(Enum):
    """Types of simulation events."""
    BOT_MOVED = "bot_moved"
    BOT_PICKUP = "bot_pickup"
    BOT_SETDOWN = "bot_setdown"
    ORDER_CREATED = "order_created"
    ORDER_COMPLETED = "order_completed"
    ITEM_PICKED = "item_picked"
    COLLISION = "collision"
    SIMULATION_START = "simulation_start"
    SIMULATION_END = "simulation_end"
    TIME_STEP = "time_step"


class SimulationEvent:
    """Represents a simulation event."""

    def __init__(self, event_type: EventType, time: float, data: Dict[str, Any] = None):
        self.event_type = event_type
        self.time = time
        self.data = data or {}

    def __repr__(self):
        return f"SimulationEvent({self.event_type.value}, t={self.time:.2f})"


class EventManager:
    """Manages event subscriptions and dispatching."""

    def __init__(self):
        self.subscribers: Dict[EventType, List[Callable]] = {}

    def subscribe(self, event_type: EventType, callback: Callable):
        """Subscribe to an event type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event: SimulationEvent):
        """Publish an event to all subscribers."""
        if event.event_type in self.subscribers:
            for callback in self.subscribers[event.event_type]:
                callback(event)

    def __repr__(self):
        total_subscribers = sum(len(subs) for subs in self.subscribers.values())
        return f"EventManager(subscribers={total_subscribers})"
