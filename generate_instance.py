#!/usr/bin/env python3
"""Generate warehouse instance configurations."""

import argparse
from pathlib import Path

from generator.instance_generator import InstanceGenerator
from config.loader import ConfigLoader
from utils.logger import setup_logger


def main():
    parser = argparse.ArgumentParser(
        description='Generate RAWSim-O warehouse instance'
    )
    
    parser.add_argument('--output', type=str, required=True, help='Output JSON file')
    parser.add_argument('--length', type=float, default=50.0, help='Warehouse length')
    parser.add_argument('--width', type=float, default=30.0, help='Warehouse width')
    parser.add_argument('--bots', type=int, default=10, help='Number of bots')
    parser.add_argument('--pods', type=int, default=50, help='Number of pods')
    parser.add_argument('--input-stations', type=int, default=2, help='Number of input stations')
    parser.add_argument('--output-stations', type=int, default=3, help='Number of output stations')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    args = parser.parse_args()
    
    logger = setup_logger('InstanceGenerator')
    
    logger.info("Generating warehouse instance...")
    logger.info(f"Dimensions: {args.length} x {args.width}")
    logger.info(f"Bots: {args.bots}, Pods: {args.pods}")
    logger.info(f"Input stations: {args.input_stations}, Output stations: {args.output_stations}")
    
    # Generate instance
    generator = InstanceGenerator(seed=args.seed)
    instance = generator.generate_simple_warehouse(
        length=args.length,
        width=args.width,
        num_bots=args.bots,
        num_pods=args.pods,
        num_input_stations=args.input_stations,
        num_output_stations=args.output_stations
    )
    
    # Generate config dictionary
    config = generator.generate_config_dict(instance)
    
    # Save to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    ConfigLoader.save_json(config, str(output_path))
    
    logger.info(f"Instance configuration saved to: {output_path}")
    logger.info(f"Generated {len(instance.waypoints)} waypoints")
    logger.info("Done!")


if __name__ == '__main__':
    main()
