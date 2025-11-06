#!/usr/bin/env python3
"""Visual simulation runner with Pygame."""

import sys
import argparse

from config.loader import ConfigLoader
from generator.instance_generator import InstanceGenerator
from visualization.pygame_renderer import PygameRenderer
from utils.logger import setup_logger
from utils.randomizer import RandomizerSimple


def main():
    parser = argparse.ArgumentParser(
        description='RAWSim-O: Robotic Mobile Fulfillment System Simulator (Visual)'
    )
    
    parser.add_argument('--instance', type=str, help='Path to instance config JSON')
    parser.add_argument('--setting', type=str, help='Path to settings config JSON')
    parser.add_argument('--control', type=str, help='Path to control config JSON')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--width', type=int, default=1200, help='Window width')
    parser.add_argument('--height', type=int, default=800, help='Window height')
    parser.add_argument('--generate', action='store_true', help='Generate default instance')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger('RAWSim-O', level=20)
    
    logger.info("RAWSim-O Python MVP - Visual Simulation")
    
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
            # For now, generate since we don't have full serialization
            generator = InstanceGenerator(seed=args.seed)
            instance = generator.generate_simple_warehouse()
        
        # Set randomizer
        instance.randomizer = RandomizerSimple(args.seed)
        
        logger.info(f"Instance: {instance.name}")
        logger.info(f"Bots: {len(instance.bots)}, Pods: {len(instance.pods)}")
        logger.info("Starting visualization...")
        
        # Create and run renderer
        renderer = PygameRenderer(instance, width=args.width, height=args.height)
        renderer.run()
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
