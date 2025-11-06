#!/usr/bin/env python3
"""Command-line interface for RAWSim-O simulation."""

import sys
import argparse
from pathlib import Path

from config.loader import ConfigLoader
from generator.instance_generator import InstanceGenerator
from simulation.executor import SimulationExecutor
from statistics.tracker import StatisticsTracker
from statistics.exporter import StatisticsExporter
from utils.logger import setup_logger
from utils.randomizer import RandomizerSimple


def main():
    parser = argparse.ArgumentParser(
        description='RAWSim-O: Robotic Mobile Fulfillment System Simulator (CLI)'
    )
    
    parser.add_argument('--instance', type=str, help='Path to instance config JSON')
    parser.add_argument('--setting', type=str, help='Path to settings config JSON')
    parser.add_argument('--control', type=str, help='Path to control config JSON')
    parser.add_argument('--output', type=str, default='results/', help='Output directory for results')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--log-file', type=str, help='Log file path')
    parser.add_argument('--generate', action='store_true', help='Generate default instance')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = 10 if args.verbose else 20  # DEBUG : INFO
    logger = setup_logger('RAWSim-O', level=log_level, log_file=args.log_file)
    
    logger.info("="*60)
    logger.info("RAWSim-O Python MVP - Command Line Interface")
    logger.info("="*60)
    
    try:
        # Load or generate instance
        if args.generate or not args.instance:
            logger.info("Generating default warehouse instance...")
            generator = InstanceGenerator(seed=args.seed)
            instance = generator.generate_simple_warehouse(
                length=50.0, width=30.0,
                num_bots=10, num_pods=50,
                num_input_stations=2, num_output_stations=3
            )
        else:
            logger.info(f"Loading instance from {args.instance}")
            loader = ConfigLoader()
            
            instance_config = loader.load_instance_config(args.instance)
            settings_config = loader.load_settings_config(args.setting) if args.setting else {}
            control_config = loader.load_control_config(args.control) if args.control else {}
            
            # For now, generate since we don't have full instance serialization
            generator = InstanceGenerator(seed=args.seed)
            instance = generator.generate_simple_warehouse()
            instance.setting_config.update(settings_config)
            instance.controller_config.update(control_config)
        
        # Set randomizer
        instance.randomizer = RandomizerSimple(args.seed)
        instance.setting_config['seed'] = args.seed
        
        logger.info(f"Instance: {instance.name}")
        logger.info(f"Bots: {len(instance.bots)}, Pods: {len(instance.pods)}")
        logger.info(f"Waypoints: {len(instance.waypoints)}")
        logger.info(f"Simulation duration: {instance.setting_config.get('simulation_duration', 3600)}s")
        
        # Create statistics tracker
        stats_tracker = StatisticsTracker(instance)
        
        # Create executor
        executor = SimulationExecutor(instance)
        
        # Subscribe to events for statistics
        executor.event_manager.subscribe(
            'time_step',
            lambda event: stats_tracker.record_snapshot(event.time) if int(event.time) % 10 == 0 else None
        )
        
        # Run simulation
        logger.info("Starting simulation...")
        executor.execute()
        
        # Export results
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Exporting statistics...")
        
        # Export time series
        if stats_tracker.time_points:
            time_series_data = {
                'throughput': stats_tracker.throughput,
                'bot_utilization': stats_tracker.bot_utilization,
            }
            StatisticsExporter.export_time_series(
                stats_tracker.time_points,
                time_series_data,
                str(output_dir / 'time_series.csv')
            )
        
        # Export summary
        summary = stats_tracker.get_summary()
        StatisticsExporter.export_summary_report(
            summary,
            str(output_dir / 'summary.json')
        )
        
        # Print summary
        logger.info("")
        logger.info("="*60)
        logger.info("Simulation Summary")
        logger.info("="*60)
        for key, value in summary.items():
            logger.info(f"{key}: {value}")
        logger.info("="*60)
        
        logger.info(f"Results saved to: {output_dir}")
        logger.info("Simulation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == '__main__':
    main()
