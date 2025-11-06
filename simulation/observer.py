"""Observer pattern for simulation monitoring."""

from typing import List, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from core.instance import Instance


class SimulationObserver:
    """Observer for monitoring simulation state."""

    def __init__(self, instance: 'Instance'):
        self.instance = instance
        self.callbacks: List[Callable] = []

    def register_callback(self, callback: Callable):
        """Register a callback for state changes."""
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def notify(self, event_type: str, data: dict = None):
        """Notify all registered callbacks."""
        for callback in self.callbacks:
            callback(event_type, data or {})

    def __repr__(self):
        return f"SimulationObserver(callbacks={len(self.callbacks)})"
