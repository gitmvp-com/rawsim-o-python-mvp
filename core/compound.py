"""Compound container for multi-tier warehouses."""

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import Instance
    from .tier import Tier


class Compound:
    """Container managing all warehouse tiers (floors)."""

    def __init__(self, instance: 'Instance'):
        self.instance = instance
        self.id: int = 0
        self.tiers: List['Tier'] = []

    def add_tier(self, tier: 'Tier'):
        """Add a tier to the compound."""
        if tier not in self.tiers:
            self.tiers.append(tier)

    def get_tier_by_id(self, tier_id: int) -> 'Tier':
        """Get a tier by its ID."""
        for tier in self.tiers:
            if tier.id == tier_id:
                return tier
        return None

    def get_total_area(self) -> float:
        """Calculate total warehouse area across all tiers."""
        return sum(tier.length * tier.width for tier in self.tiers)

    def __repr__(self):
        return f"Compound(id={self.id}, tiers={len(self.tiers)})"
