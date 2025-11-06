# Configuration Files

This directory contains JSON configuration files for RAWSim-O simulation.

## Files

### `default_instance.json`

Defines the warehouse layout and elements:
- Warehouse dimensions (length, width)
- Number of bots, pods, stations
- Multi-tier configuration
- Layout parameters

### `default_settings.json`

Simulation execution settings:
- Duration and time step
- Random seed for reproducibility
- Order generation parameters
- Statistics collection settings

### `default_control.json`

Controller algorithm configuration:
- Pathfinding method (A*, WHCAvStar, Simple)
- Task assignment strategy
- Pod selection strategy
- Repositioning parameters

## Usage

### CLI Mode
```bash
python cli.py --instance configs/default_instance.json \
              --setting configs/default_settings.json \
              --control configs/default_control.json
```

### Visual Mode
```bash
python visualization.py --instance configs/default_instance.json
```

## Creating Custom Configurations

1. Copy a default config file
2. Modify parameters as needed
3. Run simulation with `--instance path/to/your/config.json`

## Parameter Reference

### Pathfinding Methods
- `AStar`: Classic A* pathfinding
- `WHCAvStar`: Windowed Hierarchical Cooperative A* (recommended for multi-agent)
- `Simple`: Basic pathfinding for testing

### Task Assignment Methods
- `nearest`: Assign nearest available bot
- `balanced`: Balance workload across bots
- `priority`: Priority-based assignment

### Pod Selection Methods
- `nearest`: Select nearest pod with required items
- `random`: Random pod selection
- `fixed`: Fixed pod assignment
