"""Item descriptions and bundles."""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import Instance


class ItemDescription:
    """Abstract description of an item type (SKU)."""

    def __init__(self, instance: 'Instance'):
        self.instance = instance
        self.id: int = 0
        self.volatile_id: int = 0
        self.sku: str = ""
        self.weight: float = 1.0
        self.description: str = ""

    def __repr__(self):
        return f"ItemDescription(id={self.id}, sku={self.sku})"


class SimpleItemDescription(ItemDescription):
    """Simple item description for basic items."""

    def __init__(self, instance: 'Instance'):
        super().__init__(instance)
        self.name: str = "Item"


class ItemBundle:
    """A bundle of items of the same type."""

    def __init__(self, instance: 'Instance'):
        self.instance = instance
        self.id: int = 0
        self.item_description: Optional[ItemDescription] = None
        self.item_count: int = 0

    def __repr__(self):
        return f"ItemBundle(id={self.id}, count={self.item_count})"
