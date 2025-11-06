#!/usr/bin/env python3
"""Simple example of running a simulation programmatically."""

import sys
sys.path.insert(0, '.')

from generator.instance_generator import InstanceGenerator
from simulation.executor import SimulationExecutor
from statistics.tracker import StatisticsTracker
from utils.logger import setup_logger


def main():
    # Setup logging
    logger = setup_logger('Example', level=20)
    
    logger.info("Creating warehouse instance...")
    
    # Generate a simple warehouse
    generator = InstanceGenerator(seed=42)
    instance = generator.generate_simple_warehouse(
        length=40.0,
        width=25.0,
        num_bots=8,
        num_pods=30,
        num_input_stations=2,
        num_output_stations=2
    )
    
    logger.info(f"Instance created: {instance.name}")
    logger.info(f"- Bots: {len(instance.bots)}")
    logger.info(f"- Pods: {len(instance.pods)}")
    logger.info(f"- Waypoints: {len(instance.waypoints)}")
    
    # Set simulation duration
    instance.setting_config['simulation_duration'] = 100.0  # Short simulation
    instance.setting_config['time_step'] = 0.1
    
    # Create statistics tracker
    stats = StatisticsTracker(instance)
    
    # Create executor
    logger.info("Starting simulation...")
    executor = SimulationExecutor(instance)
    
    # Subscribe to time step events to record statistics
    def on_time_step(event):
        if int(event.time) % 10 == 0:  # Every 10 seconds
            stats.record_snapshot(event.time)
            logger.info(f"Simulation time: {event.time:.1f}s")
    
    from simulation.events import EventType
    executor.event_manager.subscribe(EventType.TIME_STEP, on_time_step)
    
    # Run simulation
    executor.execute()
    
    # Print results
    logger.info("\nSimulation complete!")
    logger.info("\nSummary:")
    summary = stats.get_summary()
    for key, value in summary.items():
        logger.info(f"  {key}: {value}")


if __name__ == '__main__':
    main()
