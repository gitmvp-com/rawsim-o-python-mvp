"""Queue semaphore for traffic control."""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import Instance
    from .bot import Bot


class QueueSemaphore:
    """Semaphore to limit number of bots in a specific area."""

    def __init__(self, instance: 'Instance', max_count: int):
        self.instance = instance
        self.id: int = 0
        self.max_count: int = max_count
        self.current_count: int = 0
        self.queue: List['Bot'] = []

    def request_entry(self, bot: 'Bot') -> bool:
        """Request entry to the controlled area."""
        if self.current_count < self.max_count:
            self.current_count += 1
            return True
        else:
            if bot not in self.queue:
                self.queue.append(bot)
            return False

    def release(self, bot: 'Bot'):
        """Release the semaphore when bot exits the area."""
        if self.current_count > 0:
            self.current_count -= 1
            
            # Process queue
            if len(self.queue) > 0 and self.current_count < self.max_count:
                next_bot = self.queue.pop(0)
                self.current_count += 1

    def is_available(self) -> bool:
        """Check if entry is currently available."""
        return self.current_count < self.max_count

    def __repr__(self):
        return f"QueueSemaphore(id={self.id}, count={self.current_count}/{self.max_count}, queued={len(self.queue)})"
