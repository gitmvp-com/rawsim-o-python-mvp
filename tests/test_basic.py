"""Basic tests for core functionality."""

import sys
sys.path.insert(0, '.')

from core.instance import Instance
from core.bot import BotNormal
from core.pod import Pod
from core.waypoint import Waypoint
from generator.instance_generator import InstanceGenerator


def test_instance_creation():
    """Test basic instance creation."""
    instance = Instance.create_instance()
    assert instance is not None
    assert instance.name == "DefaultInstance"
    print("✓ Instance creation test passed")


def test_tier_creation():
    """Test tier creation."""
    instance = Instance.create_instance()
    tier = instance.create_tier(0, 50.0, 30.0)
    assert tier is not None
    assert tier.length == 50.0
    assert tier.width == 30.0
    print("✓ Tier creation test passed")


def test_bot_creation():
    """Test bot creation."""
    instance = Instance.create_instance()
    tier = instance.create_tier(0, 50.0, 30.0)
    bot = instance.create_bot(0, tier, 10.0, 10.0, 0.5)
    assert bot is not None
    assert bot.id == 0
    assert bot.x == 10.0
    assert bot.y == 10.0
    print("✓ Bot creation test passed")


def test_pod_creation():
    """Test pod creation."""
    instance = Instance.create_instance()
    tier = instance.create_tier(0, 50.0, 30.0)
    pod = instance.create_pod(0, tier, 15.0, 15.0, 0.5)
    assert pod is not None
    assert pod.id == 0
    assert not pod.is_carried()
    print("✓ Pod creation test passed")


def test_waypoint_creation():
    """Test waypoint creation."""
    instance = Instance.create_instance()
    tier = instance.create_tier(0, 50.0, 30.0)
    wp = instance.create_waypoint(0, tier, 20.0, 20.0, pod_storage_location=True)
    assert wp is not None
    assert wp.pod_storage_location is True
    print("✓ Waypoint creation test passed")


def test_instance_generation():
    """Test instance generator."""
    generator = InstanceGenerator(seed=42)
    instance = generator.generate_simple_warehouse(
        length=30.0, width=20.0,
        num_bots=5, num_pods=20
    )
    assert instance is not None
    assert len(instance.bots) == 5
    assert len(instance.pods) <= 20  # May be limited by storage locations
    assert len(instance.waypoints) > 0
    print("✓ Instance generation test passed")


def test_bot_pod_interaction():
    """Test bot pickup and setdown."""
    instance = Instance.create_instance()
    tier = instance.create_tier(0, 50.0, 30.0)
    bot = instance.create_bot(0, tier, 10.0, 10.0, 0.5)
    pod = instance.create_pod(0, tier, 15.0, 15.0, 0.5)
    
    assert not bot.has_pod()
    bot.pickup_pod(pod)
    assert bot.has_pod()
    assert pod.is_carried()
    
    bot.setdown_pod()
    assert not bot.has_pod()
    assert not pod.is_carried()
    print("✓ Bot-Pod interaction test passed")


if __name__ == '__main__':
    print("Running basic tests...\n")
    
    test_instance_creation()
    test_tier_creation()
    test_bot_creation()
    test_pod_creation()
    test_waypoint_creation()
    test_instance_generation()
    test_bot_pod_interaction()
    
    print("\n✓ All basic tests passed!")
