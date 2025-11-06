"""Configuration file loader."""

import json
from typing import Dict, Any
from pathlib import Path


class ConfigLoader:
    """Loads and validates configuration files."""

    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """Load JSON configuration file."""
        with open(filepath, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_json(data: Dict[str, Any], filepath: str, indent: int = 2):
        """Save configuration to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=indent)

    @staticmethod
    def load_instance_config(filepath: str) -> Dict[str, Any]:
        """Load instance configuration."""
        config = ConfigLoader.load_json(filepath)
        # Add default values if missing
        if 'name' not in config:
            config['name'] = 'DefaultInstance'
        return config

    @staticmethod
    def load_settings_config(filepath: str) -> Dict[str, Any]:
        """Load simulation settings."""
        config = ConfigLoader.load_json(filepath)
        # Add defaults
        defaults = {
            'simulation_duration': 3600.0,
            'time_step': 0.1,
            'seed': 42,
        }
        for key, value in defaults.items():
            if key not in config:
                config[key] = value
        return config

    @staticmethod
    def load_control_config(filepath: str) -> Dict[str, Any]:
        """Load controller configuration."""
        config = ConfigLoader.load_json(filepath)
        # Add defaults
        defaults = {
            'pathfinding': {'method': 'WHCAvStar'},
            'task_assignment': {'method': 'nearest'},
            'pod_selection': {'method': 'nearest'},
        }
        for key, value in defaults.items():
            if key not in config:
                config[key] = value
        return config
