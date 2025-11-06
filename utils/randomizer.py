"""Random number generation for simulation."""

import random
from typing import List, TypeVar, Optional

T = TypeVar('T')


class RandomizerSimple:
    """Simple randomizer for deterministic simulation."""

    def __init__(self, seed: int = None):
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    def next_int(self, min_val: int, max_val: int) -> int:
        """Generate random integer in range [min_val, max_val]."""
        return random.randint(min_val, max_val)

    def next_float(self, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Generate random float in range [min_val, max_val]."""
        return random.uniform(min_val, max_val)

    def next_bool(self, probability: float = 0.5) -> bool:
        """Generate random boolean with given probability of True."""
        return random.random() < probability

    def choice(self, items: List[T]) -> Optional[T]:
        """Choose random item from list."""
        if not items:
            return None
        return random.choice(items)

    def shuffle(self, items: List[T]) -> List[T]:
        """Shuffle list in-place and return it."""
        random.shuffle(items)
        return items

    def sample(self, items: List[T], k: int) -> List[T]:
        """Sample k items from list without replacement."""
        if k > len(items):
            k = len(items)
        return random.sample(items, k)
