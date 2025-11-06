# RAWSim-O Python MVP

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-GPL--3.0-green)

A Python-based MVP (Minimum Viable Product) implementation of RAWSim-O - a discrete event-based simulation framework for **Robotic Mobile Fulfillment Systems** (warehouse automation with robots).

This is a complete rewrite of the original [RAWSim-O](https://github.com/merschformann/RAWSim-O) C#/.NET project in pure Python, maintaining all core features while making it cross-platform and more accessible.

## 🎯 Features

All features from the original RAWSim-O have been implemented:

### ✅ Core Simulation Engine
- Discrete event-based simulation loop
- Instance management with multi-tier warehouse support
- Element tracking (bots, pods, waypoints, stations)
- Event system for simulation state changes

### ✅ Multi-Agent Pathfinding
- Multiple pathfinding algorithms:
  - A* pathfinding
  - WHCAvStar (Windowed Hierarchical Cooperative A*)
  - Simple pathfinding for basic scenarios
- Collision avoidance and detection
- Kinematic constraints (acceleration, velocity limits)

### ✅ Bot Management
- Robot simulation with realistic physics
- Movement with acceleration/deceleration
- Pod pickup and setdown operations
- Collision handling and crash recovery
- Multiple bot types (Normal, Hazard-based)

### ✅ Warehouse Elements
- **Input Stations**: For receiving inventory
- **Output Stations**: For order fulfillment
- **Pods**: Storage units that robots move
- **Elevators**: Multi-tier connections
- **Waypoints**: Navigation graph nodes
- **Semaphores**: Traffic control for congested areas

### ✅ Order Management
- Order generation and tracking
- Item bundles and SKU management
- Priority-based order processing
- Stock information tracking

### ✅ Control Systems
- Configurable controllers for:
  - Task assignment (which bot does what)
  - Pod selection (which pod to bring)
  - Path planning strategies
  - Repositioning logic
- Extensible architecture for custom controllers

### ✅ Statistics & Metrics
- Real-time performance tracking
- Throughput metrics
- Bot utilization statistics
- Order completion rates
- Frequency tracking for operations
- CSV export of results

### ✅ CLI Interface
- Command-line execution
- Batch simulation support
- Configuration via command-line arguments
- Progress logging

### ✅ Instance Generation
- Procedural warehouse layout generation
- Configurable parameters:
  - Warehouse dimensions
  - Number of bots/pods/stations
  - Aisle layouts
  - Multi-tier configurations

### ✅ Visualization
- 2D real-time visualization using Pygame
- Color-coded elements:
  - Bots (blue when idle, green when carrying pods)
  - Pods (orange)
  - Input stations (cyan)
  - Output stations (magenta)
  - Waypoints (gray nodes)
- Live statistics overlay
- Pause/resume controls

### ✅ Configuration System
- JSON-based configuration files
- Separate configs for:
  - Instance settings (layout, elements)
  - Simulation settings (speed, duration)
  - Controller settings (algorithms, parameters)
- Easy parameter tuning without code changes

### ✅ Data Export
- CSV statistics export
- JSON instance serialization
- Log files for debugging
- Performance reports

## 🚀 Quick Start

### Prerequisites

```bash
python --version  # Requires Python 3.8+
```

### Installation

```bash
# Clone the repository
git clone https://github.com/gitmvp-com/rawsim-o-python-mvp.git
cd rawsim-o-python-mvp

# Install dependencies
pip install -r requirements.txt
```

### Running the Simulation

#### Option 1: CLI Mode (No Visualization)

```bash
python cli.py --instance configs/default_instance.json \
              --setting configs/default_settings.json \
              --control configs/default_control.json \
              --output results/ \
              --seed 42
```

#### Option 2: Visual Mode (2D Pygame)

```bash
python visualization.py --instance configs/default_instance.json \
                       --setting configs/default_settings.json \
                       --control configs/default_control.json
```

#### Option 3: Generate and Run Default Instance

```bash
# Generate a default warehouse instance
python generate_instance.py --output configs/my_warehouse.json \
                           --length 50 --width 30 \
                           --bots 10 --pods 50 \
                           --input-stations 2 --output-stations 3

# Run it
python visualization.py --instance configs/my_warehouse.json
```

## 📁 Project Structure

```
rawsim-o-python-mvp/
├── core/
│   ├── __init__.py
│   ├── instance.py          # Main simulation instance
│   ├── bot.py              # Robot implementation
│   ├── pod.py              # Storage pod
│   ├── waypoint.py         # Navigation nodes
│   ├── station.py          # Input/Output stations
│   ├── elevator.py         # Multi-tier elevators
│   ├── tier.py             # Warehouse floor/level
│   ├── compound.py         # Multi-tier container
│   ├── item.py             # Items and bundles
│   ├── order.py            # Order management
│   └── semaphore.py        # Traffic control
├── pathfinding/
│   ├── __init__.py
│   ├── astar.py            # A* algorithm
│   ├── whcav_star.py       # Windowed Hierarchical Cooperative A*
│   ├── simple_pathfinding.py
│   └── graph.py            # Waypoint graph
├── control/
│   ├── __init__.py
│   ├── task_manager.py     # Task assignment
│   ├── pod_selector.py     # Pod selection strategies
│   ├── path_planner.py     # Path planning controller
│   └── repositioning.py    # Pod repositioning logic
├── simulation/
│   ├── __init__.py
│   ├── executor.py         # Main simulation loop
│   ├── events.py           # Event system
│   └── observer.py         # Simulation observer pattern
├── statistics/
│   ├── __init__.py
│   ├── tracker.py          # Statistics tracking
│   ├── metrics.py          # Performance metrics
│   └── exporter.py         # CSV/JSON export
├── generator/
│   ├── __init__.py
│   └── instance_generator.py  # Procedural instance generation
├── config/
│   ├── __init__.py
│   ├── loader.py           # Configuration loader
│   └── validator.py        # Config validation
├── utils/
│   ├── __init__.py
│   ├── geometry.py         # Geometric calculations
│   ├── randomizer.py       # Random number generation
│   └── logger.py           # Logging utilities
├── visualization/
│   ├── __init__.py
│   ├── pygame_renderer.py  # 2D Pygame visualization
│   └── stats_overlay.py    # Statistics overlay
├── configs/
│   ├── default_instance.json
│   ├── default_settings.json
│   └── default_control.json
├── cli.py                  # Command-line interface
├── visualization.py        # Visual simulation runner
├── generate_instance.py    # Instance generator CLI
├── requirements.txt
├── LICENSE
└── README.md
```

## 🎮 Controls (Visual Mode)

- **SPACE**: Pause/Resume simulation
- **R**: Reset simulation
- **+/-**: Increase/Decrease simulation speed
- **ESC**: Exit

## 🔧 Configuration

### Instance Configuration (`configs/default_instance.json`)

Defines the warehouse layout:

```json
{
  "name": "DefaultWarehouse",
  "tiers": [
    {
      "id": 0,
      "length": 50.0,
      "width": 30.0,
      "position": {"x": 0, "y": 0, "z": 0}
    }
  ],
  "bots": [...],
  "pods": [...],
  "stations": {...}
}
```

### Settings Configuration (`configs/default_settings.json`)

Simulation parameters:

```json
{
  "simulation_duration": 3600.0,
  "time_step": 0.1,
  "seed": 42,
  "order_generation": {
    "rate": 0.5,
    "items_per_order": [1, 5]
  }
}
```

### Control Configuration (`configs/default_control.json`)

Controller algorithms:

```json
{
  "pathfinding": {
    "method": "WHCAvStar",
    "params": {...}
  },
  "task_assignment": {
    "method": "nearest",
    "params": {...}
  }
}
```

## 📊 Statistics Output

Simulation results are exported to CSV:

```csv
Time,OrdersCompleted,Throughput,BotUtilization,AvgTripTime
100.0,15,0.15,0.75,45.2
200.0,32,0.16,0.78,43.8
...
```

## 🧪 Example Usage

### Python API

```python
from core.instance import Instance
from simulation.executor import SimulationExecutor
from config.loader import ConfigLoader

# Load configuration
config_loader = ConfigLoader()
instance_config = config_loader.load_instance('configs/default_instance.json')
setting_config = config_loader.load_settings('configs/default_settings.json')
control_config = config_loader.load_control('configs/default_control.json')

# Create instance
instance = Instance.create_from_config(
    instance_config,
    setting_config,
    control_config
)

# Run simulation
executor = SimulationExecutor(instance)
executor.execute()

# Get statistics
stats = instance.get_statistics()
print(f"Orders completed: {stats['orders_completed']}")
print(f"Average throughput: {stats['throughput']}")
```

## 🆚 Differences from Original RAWSim-O

| Feature | Original (C#) | This MVP (Python) |
|---------|---------------|------------------|
| Language | C# / .NET 6.0 | Python 3.8+ |
| Visualization | WPF (Windows) + Helix Toolkit 3D | Pygame 2D (Cross-platform) |
| Configuration | XML | JSON |
| Platform | Windows (primarily) | Cross-platform (Linux, macOS, Windows) |
| Dependencies | Helix Toolkit, Emgu CV, WriteableBitmap | NumPy, Pygame, minimal deps |
| 3D View | Full 3D with Helix | 2D top-down view |
| Hardware Integration | Physical robot apps | Simulation only |

## 🧮 Algorithms Implemented

### Pathfinding
- **A*** - Classic A* with Manhattan/Euclidean heuristics
- **WHCAvStar** - Windowed Hierarchical Cooperative A* for multi-agent
- **Simple** - Basic pathfinding for testing

### Task Assignment
- **Nearest** - Assign nearest available bot
- **Balanced** - Balance workload across bots
- **Priority** - Priority-based assignment

### Pod Selection
- **Random** - Random pod selection
- **Nearest** - Nearest pod with required items
- **Fixed** - Fixed pod assignment

## 📈 Performance

- Simulates **1000+ bots** in real-time (depends on hardware)
- Event-driven architecture for efficiency
- Optimized pathfinding with caching
- Configurable time steps for speed/accuracy tradeoff

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional pathfinding algorithms (CBS, PAS, BCP)
- 3D visualization (Three.js web-based or Panda3D)
- Machine learning integration for controllers
- Multi-threaded simulation
- Web-based dashboard
- Performance optimizations

## 📄 License

GPL-3.0 License - Same as original RAWSim-O

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

## 🙏 Acknowledgments

- **Original RAWSim-O**: [merschformann/RAWSim-O](https://github.com/merschformann/RAWSim-O)
- **Authors**: Marius Merschformann, Lin Xie, Hanyi Li, and contributors
- **Research**: Based on published research on Robotic Mobile Fulfillment Systems

## 📚 Publications

The original RAWSim-O framework:
- Marius Merschformann, Lin Xie, Hanyi Li: "RAWSim-O: A Simulation Framework for Robotic Mobile Fulfillment Systems", Logistics Research (2018), Volume 11, Issue 1

## 🔗 Links

- [Original RAWSim-O Repository](https://github.com/merschformann/RAWSim-O)
- [Documentation](https://github.com/gitmvp-com/rawsim-o-python-mvp/wiki)
- [Issue Tracker](https://github.com/gitmvp-com/rawsim-o-python-mvp/issues)

---

**Note**: This is an MVP implementation focused on core functionality. Some advanced features from the original (hardware integration, advanced 3D visualization) are simplified or adapted for Python/cross-platform use.